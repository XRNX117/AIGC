#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Neon Ruins - 赛博废土风 15秒 AIGC 视频 Pipeline
================================================
技术栈: DeepSeek (Prompt优化) + Dreamina CLI (图/视频生成)

用法:
  export DEEPSEEK_API_KEY="sk-4..."
  export DREAMINA_HOME="./.dreamina_temp"    # 可选, 日志/认证存储路径
  # 首次运行前: dreamina login (一次OAuth)
  python aigc_video_pipeline.py --step info
  python aigc_video_pipeline.py --step all

注意:
  - 不要手动创建 auth.json 文件, 会破坏CLI认证
  - 使用 --poll 参数等待生成完成, 无需手动轮询
"""

import os, sys, json, time, argparse, subprocess, logging, shutil, re, urllib.request
from pathlib import Path
from typing import Optional
from dataclasses import dataclass
import requests

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

# ── 分镜数据 ─────────────────────────────────────────────
@dataclass
class Shot:
    shot_id: int; name: str; duration: float; start_time: float; end_time: float
    camera_movement: str; visual_description: str; raw_prompt: str
    sfx_description: str; transition_to_next: str = ""; color_grading_note: str = ""

SHOTS = [
    Shot(1, "废土城市全景", 3.0, 0.0, 3.0, "广角推镜", "黄昏废墟城市天际线, 残破霓虹广告牌在风沙中闪烁, 远处半埋沙丘的巨型圆顶建筑",
         "cyberpunk wasteland city skyline at dusk, ruined skyscrapers half-buried in sand, flickering neon signs reflecting on rusted metal, volumetric god rays through dust clouds, distant dome megastructure, blade runner aesthetic, hyperdetailed",
         "低沉风声 + 金属吱嘎声", "硬切", "青橙调, 褪色胶片感"),
    Shot(2, "幸存者特写", 3.0, 3.0, 6.0, "中近景", "外骨骼手套的手从沙土中拾起发光青色数据芯片, 指尖电流火花",
         "cybernetic hand with glowing exoskeleton glove reaching into sand, picking up cyan luminous data chip, tiny electric sparks at fingertips, shallow depth of field, rusted metal background, cinematic lighting",
         "电流滋滋声 + 沙粒摩擦声", "RGB Glitch", "芯片青光主光源, 暗部偏紫"),
    Shot(3, "全息残影三联", 3.0, 6.0, 9.0, "快速剪辑", "CRT屏幕霓虹广告, 墙面全息艺伎残影, 电缆火花四溅",
         "triptych of three quick cuts: cracked CRT monitor with neon japanese ad, translucent blue holographic geisha on crumbling wall, underground cables sparking electric arcs, glitch aesthetic",
         "CRT电流声 + 数据杂音 + 火花爆裂声", "闪白+沙尘", "强故障色差, 扫描线叠加"),
    Shot(4, "埋藏巨型结构揭示", 3.0, 9.0, 12.0, "航拍上升", "城市下方埋藏的巨型机械生物混合结构体, 脉络发出橙色光芒",
         "aerial drone view rising above cyber wasteland revealing massive biomechanical structure buried beneath ruined city, glowing orange veins pulsing through metal skeleton, sand blowing away, epic cinematic scale",
         "低音轰鸣 + 机械心跳声", "渐黑 0.5s", "橙色脉络高光, 暗部深棕偏紫"),
    Shot(5, "霓虹脉冲终场", 3.0, 12.0, 15.0, "静止到冲击波", "芯片插入终端, 青色脉冲波扩散, 浮现标题",
         "close-up of glowing cyan data chip being inserted into rusty terminal port, massive energy surge, cyan shockwave expanding in slow motion, cyberpunk, symmetrical, dark background",
         "能量积聚音 + 冲击波爆发", "无", "冲击波唯一光源, 全黑背景"),
]

PROJECT_DIR = Path("./Neon_Ruins_Project")
KF_DIR = PROJECT_DIR / "01_Keyframes"
VID_DIR = PROJECT_DIR / "02_Video_Clips"
COMPOSE_FILE = PROJECT_DIR / "compose_params.json"
DEEPSEEK_URL = "https://api.deepseek.com/v1/chat/completions"

# ── 工具函数 ─────────────────────────────────────────────
def get_dreamina_bin() -> str:
    name = "dreamina.exe" if sys.platform == "win32" else "dreamina"
    if shutil.which(name): return name
    home = Path.home()
    for p in [home/"bin"/name, home/".local"/"bin"/name]:
        if p.exists(): return str(p)
    return name

def check_auth() -> bool:
    try:
        r = subprocess.run([get_dreamina_bin(), "user_credit"], capture_output=True, text=True, timeout=15)
        return r.returncode == 0 and "credit" in r.stdout.lower()
    except: return False

def deepseek_optimize(shot: Shot) -> str:
    key = os.environ.get("DEEPSEEK_API_KEY", "")
    if not key: return shot.raw_prompt
    prompt = (
        f"Optimize this for Dreamina/即梦 text-to-image (English only, no quotes):\n"
        f"Scene: {shot.visual_description}\n"
        f"Original: {shot.raw_prompt}\n"
        f"Add cyberpunk, post-apocalyptic, neon, volumetric lighting keywords."
    )
    try:
        r = requests.post(DEEPSEEK_URL, json={
            "model": "deepseek-chat", "temperature": 0.7, "max_tokens": 300,
            "messages": [
                {"role": "system", "content": "You are an AIGC prompt engineer. Output only the optimized prompt in English, no explanations."},
                {"role": "user", "content": prompt}
            ]
        }, headers={"Authorization": f"Bearer {key}"}, timeout=30)
        r.raise_for_status()
        return r.json()["choices"][0]["message"]["content"].strip().strip('"').strip("'")
    except Exception as e:
        log.warning(f"  DeepSeek failed: {e}, using original")
        return shot.raw_prompt

def run_dreamina(args, timeout=180):
    for attempt in range(3):
        try:
            r = subprocess.run([get_dreamina_bin()]+args, capture_output=True, text=True, timeout=timeout,
                env={**os.environ})
            if r.returncode == 0: return r.stdout
        except subprocess.TimeoutExpired:
            pass
        if attempt < 2: time.sleep(3)
    return None

def download_result(json_str, out_dir, shot_id, is_video=False):
    try:
        data = json.loads(json_str)
    except: return None
    if data.get("gen_status") != "success": return None
    m = data.get("media_info", {})
    url = m.get("video_url","") or (m.get("image_urls",[None])[0] if not is_video else "") or data.get("download_url","")
    if not url: return None
    ext = ".mp4" if ".mp4" in url else ".png"
    out = out_dir / f"shot_{shot_id}{ext}"
    try:
        urllib.request.urlretrieve(url, str(out))
        return out if out.stat().st_size > 100 else None
    except: return None

# ── Pipeline 步骤 ────────────────────────────────────────
def step_keyframes():
    KF_DIR.mkdir(parents=True, exist_ok=True)
    kfs = {}
    for s in SHOTS:
        if (KF_DIR/f"shot_{s.shot_id}.png").exists():
            kfs[s.shot_id] = KF_DIR/f"shot_{s.shot_id}.png"
            log.info(f"Shot {s.shot_id}: using existing keyframe"); continue
        log.info(f"Shot {s.shot_id} ({s.name})")
        p = deepseek_optimize(s)
        log.info(f"  Prompt: {p[:80]}...")
        out = run_dreamina(["text2image","--prompt",p,"--ratio","1:1","--resolution_type","2k","--generate_num","1","--poll","120"])
        if not out: log.error(f"  FAILED text2image"); continue
        f = download_result(out, KF_DIR, s.shot_id)
        if f: log.info(f"  OK ({round(f.stat().st_size/1024,1)}KB)"); kfs[s.shot_id]=f
        else: log.error(f"  FAILED download")
    log.info(f"Keyframes: {len(kfs)}/5"); return kfs

def step_videos(kfs):
    VID_DIR.mkdir(parents=True, exist_ok=True); vids = {}
    for s in SHOTS:
        img = kfs.get(s.shot_id)
        if not img: continue
        if (VID_DIR/f"shot_{s.shot_id}.mp4").exists():
            vids[s.shot_id] = VID_DIR/f"shot_{s.shot_id}.mp4"; continue
        log.info(f"Shot {s.shot_id} video")
        vp = f"cinematic motion, {s.camera_movement}, atmospheric, volumetric lighting, dust particles"
        out = run_dreamina(["image2video","--image",str(img),"--prompt",vp,"--duration","5","--poll","180"], timeout=300)
        if not out: log.error(f"  FAILED image2video"); continue
        f = download_result(out, VID_DIR, s.shot_id, is_video=True)
        if f: log.info(f"  OK ({round(f.stat().st_size/1024/1024,2)}MB)"); vids[s.shot_id]=f
        else: log.error(f"  FAILED download")
    log.info(f"Videos: {len(vids)}/{len(kfs)}"); return vids

def compose_json(kfs, vids):
    clips = []
    for s in SHOTS:
        clips.append({"shot_id":s.shot_id,"name":s.name,"start":s.start_time,"duration":s.duration,
            "keyframe":str(kfs.get(s.shot_id,"")),"video":str(vids.get(s.shot_id,"")),
            "transition":s.transition_to_next,"color":s.color_grading_note,"sfx":s.sfx_description})
    data = {"project":"Neon_Ruins","fps":24,"duration":15,"resolution":"1080x1920","clips":clips,
        "color_grading":{"lut":"Teal & Orange 70%","grain":"8%","vignette":"20%"},
        "title":{"text":"霓虹废墟","color":"#00E5FF","glow":"#B847E6","animation":"打字机0.8s","time":"13.5s-15s"},
        "export":{"codec":"H.264","bitrate":"15Mbps","container":"MP4"}}
    COMPOSE_FILE.parent.mkdir(parents=True,exist_ok=True)
    COMPOSE_FILE.write_text(json.dumps(data,indent=2,ensure_ascii=False),encoding="utf-8")
    log.info(f"compose_params.json saved: {COMPOSE_FILE}")

def step_info():
    for s in SHOTS:
        log.info(f"Shot {s.shot_id}: {s.name} ({s.duration}s {s.start_time}-{s.end_time})")
    log.info("Env: DEEPSEEK_API_KEY (required) | DREAMINA_HOME (optional)")

def run_all():
    log.info("=== Neon Ruins Pipeline ===")
    if not check_auth():
        log.error("Dreamina not logged in. Run: dreamina login")
        return
    kfs = step_keyframes()
    if kfs: vids = step_videos(kfs)
    else: vids = {}
    compose_json(kfs, vids if kfs else {})
    log.info(f"Complete. Keyframes: {len(kfs)}/5, Videos: {len(vids) if kfs else 0}/{len(kfs)}")
    fails = []
    for s in SHOTS:
        if s.shot_id not in kfs: fails.append(f"Shot{s.shot_id} keyframe")
        elif s.shot_id not in vids and kfs: fails.append(f"Shot{s.shot_id} video")
    if fails: log.warning(f"Failed: {', '.join(fails)}")

# ── CLI ──────────────────────────────────────────────────
def main():
    p = argparse.ArgumentParser(description="Neon Ruins Pipeline")
    p.add_argument("--step", choices=["all","keyframes","video","info"], default="all")
    a = p.parse_args()
    if a.step == "info": step_info(); return
    if not check_auth(): log.error("Run dreamina login first"); return
    s = os.environ.get("DREAMINA_SESSION","")
    if s: log.warning("DREAMINA_SESSION is set but not used (CLI uses OAuth). Set DREAMINA_HOME instead if needed.")
    if a.step == "keyframes": step_keyframes()
    elif a.step == "video":
        kfs = {}; [kfs.update({s.shot_id:KF_DIR/f"shot_{s.shot_id}.png"}) for s in SHOTS if (KF_DIR/f"shot_{s.shot_id}.png").exists()]
        if not kfs: log.error("No keyframes"); return
        step_videos(kfs)
    elif a.step == "all": run_all()

if __name__ == "__main__": main()

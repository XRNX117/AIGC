# AGENTS.md — 赛博废土风 15 秒 AIGC 视频制作方案

---

## 一、项目概述

| 项目 | 详情 |
|------|------|
| **片名** | 《霓虹废墟》Neon Ruins |
| **时长** | 15 秒 |
| **风格** | 赛博废土风 (Cyber Wasteland) |
| **分辨率** | 1080×1920 (9:16 竖屏，适配抖音/小红书/视频号) |
| **帧率** | 24fps |
| **目标平台** | 抖音 / 小红书 / YouTube Shorts / Instagram Reels |
| **预算参考** | 约 ¥200–400（API 调用费用） |
| **总制作周期** | 约 2–4 小时 |

---

## 二、视觉风格定义

### 2.1 赛博废土核心要素

```
赛博废土 = 赛博朋克(高科技) + 废土(低生活) + 末日美学
```

| 维度 | 具体表现 |
|------|---------|
| **色调** | 主色调：暗橙/铁锈红 (#C8553D)、暗青色 (#1A8F8F)；辅色：霓虹紫 (#B847E6)、脏金 (#A68A56)；基底：炭黑/灰烬灰 |
| **光影** | 强烈体积光（God Rays），霓虹漫反射，沙尘散射光，高对比度暗角 |
| **材质** | 锈蚀金属、破碎混凝土、裸露线缆、全息投影、沙尘覆盖表面、老旧 CRT 屏幕 |
| **氛围** | 荒凉、神秘、科技遗迹感、孤寂中的生命力 |

### 2.2 参考 Prompt 关键词库

**正向词：**
```
cyber wasteland, post-apocalyptic, neon ruins, holographic advertisements, 
rusty metal structures, sandstorm, volumetric lighting, god rays, 
dystopian cityscape, flickering neon signs, derelict megastructure, 
cybernetic implants, glitch effect, analog distortion, 
cinematic lighting, 8K, hyperdetailed, Unreal Engine 5 render, 
blade runner 2049 aesthetic, Mad Max meets Cyberpunk
```

**负向词：**
```
green vegetation, clean, modern, shiny, cartoon, anime, low quality, 
blurry, watermark, text, logo, oversaturated, happy, daylight
```

---

## 三、分镜脚本 (Shot List)

---

### Shot 1/5：废土城市全景（0–3 秒）

| 参数 | 值 |
|------|----|
| **时长** | 3.0s |
| **类型** | 广角推镜 (Wide → Push In) |
| **画面描述** | 黄昏下的废墟城市天际线，残破的霓虹广告牌在风沙中闪烁，远处有一座被沙丘半掩的巨型圆顶建筑 |
| **运镜** | 缓慢向前推镜，模拟无人机飞行 |
| **生成工具** | Midjourney 生成关键帧 → Kling/可灵 图生视频 |
| **关键帧 Prompt** | `cinematic wide shot, cyber wasteland cityscape at dusk, ruined skyscrapers half-buried in sand, flickering neon signs in cyan and magenta reflecting on rusty metal, volumetric god rays piercing through dust clouds, distant dome megastructure, blade runner 2049 aesthetic, hyperdetailed, 8K, Unreal Engine 5 render, movie still --ar 9:16 --style raw --stylize 250` |
| **视频 Prompt** | `Slow cinematic push-in drone shot flying toward ruined city, neon lights flickering, sand particles drifting in wind, atmospheric haze, 3 seconds seamless loop` |
| **Kling 参数** | `mode: std, duration: 3, cfg_scale: 0.5, movement_amplitude: medium` |
| **音效** | 低沉风声 + 远处金属结构吱嘎声 |

---

### Shot 2/5：幸存者特写（3–6 秒）

| 参数 | 值 |
|------|----|
| **时长** | 3.0s |
| **类型** | 中近景 (Medium Close-up) |
| **画面描述** | 一只戴着外骨骼手套的手从沙土中缓缓拾起一枚发出青色光芒的数据芯片，指尖有微弱的电流火花 |
| **运镜** | 焦点从沙土拉至芯片，轻微手持晃动感 |
| **生成工具** | Midjourney → Kling |
| **关键帧 Prompt** | `medium close-up shot, cybernetic hand with exoskeleton glove reaching down, picking up a glowing cyan data chip from sand, tiny electric sparks at fingertips, shallow depth of field, sand particles floating, rusty metal background, cinematic lighting, hyperdetailed texture, 8K, film grain --ar 9:16 --style raw --stylize 300` |
| **视频 Prompt** | `Hand slowly reaches into frame, fingers close around glowing data chip, electric sparks flicker, slight camera shake, dust particles illuminated by cyan glow` |
| **Kling 参数** | `mode: std, duration: 3, cfg_scale: 0.5, movement_amplitude: low` |
| **音效** | 电流滋滋声 + 沙粒摩擦声 + 低频嗡鸣 |

---

### Shot 3/5：全息残影（6–9 秒）

| 参数 | 值 |
|------|----|
| **时长** | 3.0s |
| **类型** | 快速剪辑 (Fast Cut) |
| **画面描述** | 三个快速闪过的画面：1) 破损 CRT 屏幕上跳动的霓虹日文广告 2) 墙面投射的全息艺伎残影 3) 电缆火花四溅 |
| **运镜** | 静止/微动 |
| **生成工具** | Midjourney(三张关键帧) → Runway Gen-3 图生视频 |
| **关键帧 Prompt 1** | `close-up of cracked CRT monitor screen in abandoned building, flickering neon japanese advertisement, scanlines, analog glitch distortion, dark room, volumetric dust --ar 9:16 --style raw --stylize 400` |
| **关键帧 Prompt 2** | `holographic geisha projection on crumbling concrete wall in cyber wasteland, translucent blue glow, glitch artifacts, smoke and dust, Phillip K Dick aesthetic --ar 9:16 --style raw --stylize 400` |
| **关键帧 Prompt 3** | `underground cable tunnel, exposed wires sparking electric blue arcs, rusty pipes, water dripping, emergency red beacon light, industrial cyberpunk --ar 9:16 --style raw --stylize 350` |
| **Runway 参数** | `motion_bucket: high, mode: gen3, duration: 3s total (1s each clip)` |
| **音效** | CRT 电流声 + 数据杂音 + 火花爆裂声 |

---

### Shot 4/5：埋藏巨型结构（9–12 秒）

| 参数 | 值 |
|------|----|
| **时长** | 3.0s |
| **类型** | 航拍上升镜头 (Aerial Reveal) |
| **画面描述** | 航拍镜头从地面升起到高空，揭示整个废土城市下方埋藏着一个巨大的机械/生物混合结构体，脉络发出微弱的橙色光芒 |
| **运镜** | 垂直上升 + 镜头略微俯视 |
| **生成工具** | Midjourney → Kling |
| **关键帧 Prompt** | `aerial view rising above cyber wasteland, massive buried biomechanical megastructure revealed beneath ruined city, glowing orange veins pulsing through metal skeleton, sandstorm clearing, epic scale, sense of awe, cinematic drone shot, blade runner 2049 + arrival aesthetic, hyperdetailed, 8K --ar 9:16 --style raw --stylize 300` |
| **视频 Prompt** | `Drone rapidly ascending from ground level to high altitude, revealing enormous buried structure below, sand blowing away to expose metal surface, orange light pulsing through veins, epic scale reveal` |
| **Kling 参数** | `mode: std, duration: 3, cfg_scale: 0.5, movement_amplitude: high` |
| **音效** | 低音轰鸣 + 机械心跳声 + 沙尘暴声音 |

---

### Shot 5/5：霓虹脉冲 + 标题（12–15 秒）

| 参数 | 值 |
|------|----|
| **时长** | 3.0s |
| **类型** | 特效收尾 (FX Outro) |
| **画面描述** | 幸存者将芯片插入终端，一道青色霓虹脉冲波从中心向外扩散，画面转为暗色，浮现标题文字「霓虹废墟」 |
| **运镜** | 静止，脉冲特效 |
| **生成工具** | Kling → After Effects/剪映(CapCut) 后期合成 |
| **关键帧 Prompt** | `close-up of data chip being inserted into rusty terminal port, energy surge, cyan shockwave expanding outward in slow motion, cyberpunk, symmetrical composition, dark background --ar 9:16 --style raw --stylize 300` |
| **视频 Prompt** | `Chip inserted into port, energy builds up for 1 second, then massive cyan pulse wave expands in all directions, slow motion, shockwave lighting up the dark` |
| **Kling 参数** | `mode: hd, duration: 3, cfg_scale: 0.5, movement_amplitude: high` |
| **音效** | 能量积聚声 → 冲击波爆发 → 低音余韵 + 标题出现提示音 |

---

## 四、音频设计

| 层级 | 内容 | 生成工具 | 参数建议 |
|------|------|---------|---------|
| **背景音乐** | Dark Ambient / Industrial 风格，BPM 60–80，C 小调 | Suno v4 / Udio | `genre: dark ambient industrial cyberpunk, tempo: 70bpm, key: C minor, 30s loop, no drums first 8s then heavy distorted kicks` |
| **环境音** | 风声、沙尘、金属吱嘎 | ElevenLabs SFX / 自建音效库 | — |
| **特效音** | 电流滋滋、火花、冲击波、脉冲 | ElevenLabs SFX / Artlist | — |
| **旁白**（可选） | 低沉男声一句话：「在这片废土之下，还有东西活着。」 | ElevenLabs | `voice: deep male, style: gritty whispered intensity, stability: 0.3, similarity: 0.7` |

---

## 五、后期合成流程

| 步骤 | 工具 | 操作 |
|------|------|------|
| 1. 粗剪 | 剪映(CapCut) / DaVinci Resolve | 5 段素材按时间线排列，检查节奏 |
| 2. 转场 | CapCut | Shot 2→3：RGB Glitch 转场；Shot 3→4：闪白+沙尘转场；Shot 4→5：渐黑 |
| 3. 调色 | CapCut / Resolve | LUT：青橙调(Teal & Orange) + 褪色胶片效果 15% + 颗粒 8% + 暗角 20% |
| 4. 特效叠加 | CapCut / After Effects | 全片叠加轻微扫描线、色差(Chromatic Aberration)、随机噪点 |
| 5. 标题动画 | CapCut | 最后 1.5s：霓虹文字「霓虹废墟」打字机效果出现 + 微光闪烁 |
| 6. 音频混音 | CapCut / Audacity | 背景音乐 -12dB，特效音 -6dB，整体限制器(Limiter) -1dB |

---

## 六、工具链与成本估算

| 阶段 | 工具 | 预估费用 |
|------|------|---------|
| 图像生成 (5 张关键帧) | Midjourney (Fast Mode) | ~$0.50 (已有订阅) |
| 视频生成 (5 段 × 3s) | 可灵 Kling / 即梦 Jimeng | ~¥60–150（积分/会员） |
| 视频生成备选 | Runway Gen-3 | ~$15–25 |
| 音乐生成 | Suno v4 / Udio | ~$0（免费额度） |
| 后期剪辑 | 剪映专业版 | ¥0（免费） |
| **总计** | | **约 ¥100–300** |

---

## 七、执行流程（Step-by-Step）

```
Day 1 (2–4h):
├── Phase 1: 图像生成 (30min)
│   ├── 在 Midjourney 中按分镜依次生成 5 张关键帧
│   ├── 每张生成 4 个变体，挑选最佳
│   └── 使用 Upscale 提升分辨率至 2K+
│
├── Phase 2: 视频生成 (1–2h)
│   ├── 将关键帧导入可灵 Kling 图生视频
│   ├── 按分镜参数生成 5 段视频
│   ├── 对不满意的段落重新生成（通常需要 2–3 轮）
│   └── 下载所有视频素材
│
├── Phase 3: 音频生成 (30min)
│   ├── Suno/Udio 生成背景音乐
│   ├── ElevenLabs 生成特效音（可选）
│   └── 导出所有音频素材
│
└── Phase 4: 后期合成 (1h)
    ├── 剪映中排列素材，调整节奏
    ├── 添加转场、调色、特效叠加
    ├── 混音，添加标题动画
    └── 导出：H.264, 1080×1920, 24fps, 15Mbps
```

---

## 八、质量检查清单

- [ ] 每段画面风格一致性（色调、氛围）
- [ ] 视频流畅无跳帧、无 AI 畸形帧
- [ ] 转场与 BGM 节拍对齐
- [ ] 霓虹色调统一（青/橙/紫三色体系）
- [ ] 标题文字可读性（与背景对比度足够）
- [ ] 音频无削波(Clipping)
- [ ] 导出码率 ≥ 10Mbps
- [ ] 竖屏安全区：关键元素在 1080×1420 范围内（避开上下 UI 区域）

---

## 九、备选方案 (Plan B)

若 Kling/即梦 效果不理想，可使用以下替代方案：

| 原工具 | 替代方案 | 备注 |
|--------|---------|------|
| Midjourney | Stable Diffusion + SDXL 模型 + ControlNet | 免费，但需本地 GPU (≥8GB VRAM) |
| Kling 图生视频 | Runway Gen-3 / Pika 2.0 | 价格更高，但动作幅度可控 |
| Kling 图生视频 | ComfyUI + AnimateDiff | 完全免费本地方案，配置复杂 |
| Suno | 自有音效库 + 剪辑 | 更可控但不那么便捷 |

---

## 十、最终交付物清单

```
📁 Neon_Ruins_Project/
├── 📁 01_Keyframes/          # 5 张关键帧原图 (PNG, 2K+)
├── 📁 02_Video_Clips/        # 5 段原始 AI 视频 (MP4)
├── 📁 03_Audio/              # BGM + SFX 素材 (WAV/MP3)
├── 📁 04_Project_Files/      # 剪映/DaVinci 工程文件
├── 📄 AGENTS.md              # 本方案文档
├── 📄 aigc_video_pipeline.py # Python 自动化脚本
└── 📄 Neon_Ruins_Final.mp4   # 最终成品 (1080×1920, 15s)
```

---

> **最后更新**: 2026-07-08
> **方案版本**: v1.0
> **适用工具版本**: Midjourney v6.1 / Kling 1.6 / Runway Gen-3 / Suno v4 / CapCut 6.0+

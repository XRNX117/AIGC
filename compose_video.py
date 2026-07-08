import numpy as np
import glob, os, re
from pathlib import Path
from moviepy import ImageClip, VideoClip, concatenate_videoclips, CompositeVideoClip, TextClip
from moviepy.video.fx import FadeIn, FadeOut

SRC_DIR = "F:\\aigc\\Neon_Ruins_Project"
FONT = "C:\\Windows\\Fonts\\Arial.ttf"
FPS = 24

# Find and order images by shot description keywords
all_files = glob.glob(os.path.join(SRC_DIR, "jimeng-*.png"))
if not all_files:
    all_files = glob.glob(os.path.join(SRC_DIR, "*.png"))
shot_keywords = ["city", "hand", "triptych", "aerial", "chip", "terminal", "pulse", "megastructure", "exploring", "nebula"]
SHOTS = []
for kw in shot_keywords:
    matches = [f for f in all_files if kw.lower() in os.path.basename(f).lower()]
    if matches:
        SHOTS.append(matches[0])
        all_files.remove(matches[0])
    if len(SHOTS) >= 5:
        break
if len(SHOTS) < 5:
    SHOTS += all_files[:5 - len(SHOTS)]
print(f"Found {len(SHOTS)} images in order:")
for i, f in enumerate(SHOTS):
    print(f"  Shot {i+1}: {os.path.basename(f)} ({round(os.path.getsize(f)/1024,1)} KB)")

# === 1. LOAD CLIPS ===
print("Loading clips...")
clips = []
for path in SHOTS:
    clip = ImageClip(path).resized((1080, 1920)).with_duration(3)
    clips.append(clip)

# === 2. TRANSITION OVERLAYS ===

# RGB Glitch (shot2->shot3, t=6.0s)
def make_glitch_overlay(clip_a, clip_b, duration=0.3):
    seg_a = clip_a.subclipped(clip_a.duration - duration/2, clip_a.duration)
    seg_b = clip_b.subclipped(0, duration/2)
    def make_frame(t):
        if t < duration/2:
            frame = seg_a.get_frame(t + duration/2)
        else:
            frame = seg_b.get_frame(t - duration/2)
        shift = int(10 * np.sin(t * 80))
        if abs(shift) > 2:
            f = frame.copy().astype(float)
            f[:,:,:] = 0
            r = np.roll(frame[:,:,0].copy(), shift, axis=1) if shift != 0 else frame[:,:,0].copy()
            b = np.roll(frame[:,:,2].copy(), -shift, axis=1) if shift != 0 else frame[:,:,2].copy()
            result = np.zeros_like(frame)
            result[:,:,0] = r
            result[:,:,1] = frame[:,:,1]
            result[:,:,2] = b
            return np.clip(result, 0, 255).astype(np.uint8)
        return frame
    return VideoClip(make_frame, duration=duration)

print("Creating transitions...")
glitch = make_glitch_overlay(clips[1], clips[2], 0.3)
glitch = glitch.with_start(5.9)

# Flash White (shot3->shot4)
white_frames = np.ones((1920, 1080, 3), dtype=np.uint8) * 255
white = VideoClip(lambda t: white_frames, duration=0.4)
white = white.with_effects([FadeIn(0.15), FadeOut(0.15)])
white = white.with_start(8.85)

# Fade to Black (shot4->shot5)
black_frames = np.zeros((1920, 1080, 3), dtype=np.uint8)
black = VideoClip(lambda t: black_frames, duration=1.0)
black = black.with_effects([FadeIn(0.5), FadeOut(0.5)])
black = black.with_start(11.5)

# === 3. MAIN VIDEO ===
print("Concatenating clips...")
main = concatenate_videoclips(clips, method="compose")
print(f"Main duration: {main.duration:.2f}s")

# === 4. TITLE (Typewriter + Glow) ===
print("Creating title...")
TITLE_START = 13.5
TITLE_TEXT = "Neon Ruins"

title_overlays = []

# Glow text (behind)
glow_txt = TextClip(FONT, TITLE_TEXT, font_size=76, color="#B847E6",
    stroke_color="#B847E6", stroke_width=3, size=(1080, 300), method="label")
glow_txt = (glow_txt
    .with_position(("center", 0.75), relative=True)
    .with_start(TITLE_START)
    .with_duration(15 - TITLE_START)
    .with_opacity(0.3))
title_overlays.append(glow_txt)

# Typewriter effect - letters appear one by one over 0.8s
for i in range(1, len(TITLE_TEXT) + 1):
    partial = TITLE_TEXT[:i]
    letter_time = TITLE_START + (i - 1) * 0.12
    tc = TextClip(FONT, partial, font_size=70, color="#00E5FF",
        stroke_color="#00E5FF", stroke_width=1, size=(1080, 300), method="label",
        horizontal_align="center")
    tc = (tc
        .with_position(("center", 0.75), relative=True)
        .with_start(letter_time)
        .with_duration(15 - letter_time))
    title_overlays.append(tc)

# === 5. COMPOSITE ===
print("Compositing...")
all_clips = [main, glitch, white, black] + title_overlays
final = CompositeVideoClip(all_clips, size=(1080, 1920))

# === 6. EXPORT ===
OUTPUT = os.path.join(SRC_DIR, "Neon_Ruins_Final.mp4")
print(f"Exporting to {OUTPUT}...")
final.write_videofile(OUTPUT, fps=FPS, codec="libx264", bitrate="15000k", audio=False, logger=None)
print(f"Done! {OUTPUT}")
print(f"File size: {round(os.path.getsize(OUTPUT)/1024/1024,1)} MB")
print(f"Duration: {final.duration:.1f}s")
print(f"Resolution: 1080x1920 (9:16)")
print(f"FPS: {FPS}")
print(f"Transitions: Hard cut -> RGB Glitch -> Flash White -> Fade to Black")
print(f"Title: '{TITLE_TEXT}' typewriter effect (0.8s) with purple glow")

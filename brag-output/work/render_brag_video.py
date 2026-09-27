"""
Project ORCA v7.0 — Automated High-Fidelity Launch Video Generator (/brag-slim engine)
Renders a 20-second 1080p 30fps tactical trailer with custom maritime soundtrack,
SFX mixing, kinetic typography, camera pan/zoom, and real UI assets.
"""
import os
import sys
import math
import subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from scipy.io import wavfile

# --- Paths ---
BASE_DIR = r"d:\coding\Github\SIH26"
BRAG_DIR = os.path.join(BASE_DIR, "brag-output")
WORK_DIR = os.path.join(BRAG_DIR, "work")
SFX_DIR = r"C:\Users\jadeu\.gemini\config\skills\brag\assets\sfx"
FFMPEG_BIN = r"C:\Users\jadeu\AppData\Local\Python\pythoncore-3.14-64\Lib\site-packages\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v7.1.exe"

WIDTH, HEIGHT = 1920, 1080
FPS = 30
TOTAL_FRAMES = 600  # 20.0 seconds
SAMPLE_RATE = 44100

# --- Colors (Strict Palette A) ---
COLOR_INK_SEA = (16, 42, 49)        # #102A31
COLOR_DEEP_CURRENT = (15, 99, 130)  # #0F6382
COLOR_TIDE = (169, 209, 203)        # #A9D1CB
COLOR_SHELL = (252, 250, 245)       # #FCFAF5
COLOR_SAND_PAPER = (245, 240, 230)  # #F5F0E6
COLOR_DRIFTWOOD = (217, 205, 184)   # #D9CDB8
COLOR_CHARCOAL = (23, 38, 43)       # #17262B
COLOR_HAZARD = (226, 162, 61)       # #E2A23D
COLOR_SIGNAL_LIGHT = (43, 111, 122) # #2B6F7A
COLOR_SIGNAL_DARK = (127, 196, 210) # #7FC4D2
COLOR_BG_DARK = (10, 21, 32)        # #0A1520
COLOR_BG_PANEL_DARK = (16, 30, 41)  # #101E29
COLOR_WHITE = (255, 255, 255)

# --- Fonts ---
def get_font(name="segoeuib.ttf", size=32):
    try:
        return ImageFont.truetype(name, size)
    except:
        return ImageFont.load_default()

FONT_HERO = get_font("segoeuib.ttf", 64)
FONT_SUB = get_font("segoeui.ttf", 26)
FONT_CARD_TITLE = get_font("segoeuib.ttf", 28)
FONT_CARD_DESC = get_font("segoeui.ttf", 18)
FONT_TAG = get_font("segoeuib.ttf", 16)
FONT_MONO = get_font("consola.ttf", 20)
FONT_BADGE = get_font("segoeuib.ttf", 20)

# =========================================================================
# 1. AUDIO SYNTHESIS & SFX MIXING
# =========================================================================
def generate_soundtrack():
    print("[Audio] Synthesizing cinematic maritime soundtrack...")
    duration = 20.0
    num_samples = int(duration * SAMPLE_RATE)
    t = np.linspace(0, duration, num_samples, endpoint=False)
    
    # Left and Right stereo channels
    left = np.zeros(num_samples, dtype=np.float32)
    right = np.zeros(num_samples, dtype=np.float32)

    # A. Low Ocean Sub-bass Drone (D1: 36.7 Hz, A1: 55 Hz, D2: 73.4 Hz)
    sub = (
        0.35 * np.sin(2 * np.pi * 36.7 * t) +
        0.25 * np.sin(2 * np.pi * 55.0 * t) +
        0.15 * np.sin(2 * np.pi * 73.4 * t)
    )
    # Slow swell envelope
    swell = 0.6 + 0.4 * np.sin(2 * np.pi * 0.15 * t)
    sub = sub * swell

    # B. Atmospheric Ocean Synth Pad (D minor 9: D3=146.8, F3=174.6, A3=220, C4=261.6, E4=329.6)
    pad = np.zeros(num_samples, dtype=np.float32)
    chord_freqs = [146.83, 174.61, 220.0, 261.63, 329.63]
    for i, f in enumerate(chord_freqs):
        detune = (i - 2) * 0.4
        lfo = 1.0 + 0.08 * np.sin(2 * np.pi * 0.25 * t + i)
        pad += (0.12 / len(chord_freqs)) * np.sin(2 * np.pi * (f + detune) * t) * lfo

    # C. Rhythmic Sonar / Radar Pluck Pulse (110 BPM -> 0.545s per beat)
    beat_sec = 60.0 / 110.0
    pulse = np.zeros(num_samples, dtype=np.float32)
    arp_notes = [440.0, 587.33, 659.25, 880.0]  # A4, D5, E5, A5
    for beat_idx in range(int(duration / beat_sec)):
        start_t = beat_idx * beat_sec
        start_s = int(start_t * SAMPLE_RATE)
        note_f = arp_notes[beat_idx % len(arp_notes)]
        decay_samples = int(0.25 * SAMPLE_RATE)
        if start_s + decay_samples < num_samples:
            env = np.exp(-np.linspace(0, 7, decay_samples))
            tone = 0.15 * np.sin(2 * np.pi * note_f * np.linspace(0, 0.25, decay_samples)) * env
            pulse[start_s : start_s + decay_samples] += tone

    # D. Master Master Envelope (Fade in 1s, fade out last 1.5s)
    fade_in = np.clip(t / 1.0, 0, 1)
    fade_out = np.clip((duration - t) / 1.5, 0, 1)
    master_env = fade_in * fade_out

    # Pan channels
    left = (sub + pad * 0.9 + pulse * 1.1) * master_env
    right = (sub + pad * 1.1 + pulse * 0.9) * master_env

    # E. Load and Mix Bundled SFX via FFmpeg into WAV
    sfx_cues = [
        ("interface\\switch_001.ogg", 0.6, 0.7),
        ("interface\\click_002.ogg", 4.3, 0.6),
        ("interface\\select_008.ogg", 6.8, 0.65),
        ("impact\\impactSoft_medium_001.ogg", 8.8, 0.85),
        ("interface\\click_004.ogg", 11.8, 0.6),
        ("impact\\impactPlate_light_001.ogg", 14.6, 0.9),
    ]

    for rel_path, cue_sec, vol in sfx_cues:
        sfx_path = os.path.join(SFX_DIR, rel_path)
        if os.path.exists(sfx_path):
            temp_wav = os.path.join(WORK_DIR, f"temp_sfx_{os.path.basename(rel_path)}.wav")
            subprocess.run([FFMPEG_BIN, "-y", "-i", sfx_path, temp_wav], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            if os.path.exists(temp_wav):
                try:
                    sr, sfx_data = wavfile.read(temp_wav)
                    if sfx_data.ndim == 2:
                        sfx_mono = sfx_data.mean(axis=1)
                    else:
                        sfx_mono = sfx_data.astype(np.float32)
                    # Normalize
                    if np.max(np.abs(sfx_mono)) > 0:
                        sfx_mono = sfx_mono / np.max(np.abs(sfx_mono)) * vol
                    start_s = int(cue_sec * SAMPLE_RATE)
                    end_s = min(num_samples, start_s + len(sfx_mono))
                    length = end_s - start_s
                    if length > 0:
                        left[start_s:end_s] += sfx_mono[:length]
                        right[start_s:end_s] += sfx_mono[:length]
                except Exception as ex:
                    print(f"Error mixing SFX {rel_path}: {ex}")

    # Normalize Master Mix
    max_val = max(np.max(np.abs(left)), np.max(np.abs(right)), 1e-4)
    left = np.clip(left / max_val * 0.92, -1.0, 1.0)
    right = np.clip(right / max_val * 0.92, -1.0, 1.0)

    # Convert to 16-bit PCM
    stereo_16 = np.vstack(((left * 32767).astype(np.int16), (right * 32767).astype(np.int16))).T
    wav_out = os.path.join(WORK_DIR, "soundtrack.wav")
    wavfile.write(wav_out, SAMPLE_RATE, stereo_16)
    print(f"[Audio] Soundtrack written to: {wav_out}")
    return wav_out

# =========================================================================
# 2. FRAME GENERATION PIPELINE
# =========================================================================
print("[Video] Loading raw visual assets...")
img_light_landing = Image.open(os.path.join(WORK_DIR, "light_landing.png")).convert("RGB")
img_light_workspace = Image.open(os.path.join(WORK_DIR, "light_workspace.png")).convert("RGB")
img_dark_workspace = Image.open(os.path.join(WORK_DIR, "dark_workspace.png")).convert("RGB")
logo_img_path = os.path.join(BASE_DIR, "frontend", "logo-icon.png")
logo_img = Image.open(logo_img_path).convert("RGBA") if os.path.exists(logo_img_path) else None

def fit_and_crop(img, target_w, target_h, zoom=1.0, offset_x=0.0, offset_y=0.0):
    w, h = img.size
    aspect_target = target_w / target_h
    aspect_img = w / h
    
    if aspect_img > aspect_target:
        new_h = target_h
        new_w = int(target_h * aspect_img)
    else:
        new_w = target_w
        new_h = int(target_w / aspect_img)
        
    resized = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
    
    # Zoom
    if zoom != 1.0:
        zw = int(new_w * zoom)
        zh = int(new_h * zoom)
        resized = resized.resize((zw, zh), Image.Resampling.LANCZOS)
        new_w, new_h = zw, zh
        
    # Crop center with offsets
    cx = (new_w - target_w) // 2 + int(offset_x)
    cy = (new_h - target_h) // 2 + int(offset_y)
    cx = max(0, min(new_w - target_w, cx))
    cy = max(0, min(new_h - target_h, cy))
    
    return resized.crop((cx, cy, cx + target_w, cy + target_h))

def draw_top_hud(draw, title="PROJECT ORCA v7.0", sub="TACTICAL MARINE INTELLIGENCE", is_dark=False):
    bg_bar = (16, 30, 41, 230) if is_dark else (237, 231, 216, 230)
    text_c = COLOR_WHITE if is_dark else COLOR_INK_SEA
    accent_c = COLOR_SIGNAL_DARK if is_dark else COLOR_SIGNAL_LIGHT
    
    # Top HUD Bar
    draw.rectangle([0, 0, WIDTH, 54], fill=(bg_bar[0], bg_bar[1], bg_bar[2]))
    draw.line([0, 54, WIDTH, 54], fill=accent_c, width=1)
    
    draw.text((28, 14), title, font=FONT_TAG, fill=text_c)
    draw.text((220, 15), f"// {sub}", font=FONT_TAG, fill=accent_c)
    
    telemetry_tag = "SENTINEL-3 SLSTR · MODIS AQUA · INCOIS RAG · 50+ PORTS"
    draw.text((WIDTH - 540, 16), telemetry_tag, font=get_font("consola.ttf", 14), fill=text_c)
    
    # Blinking Live Dot
    draw.ellipse([WIDTH - 565, 21, WIDTH - 555, 31], fill=(46, 204, 113) if is_dark else (30, 132, 73))

def render_frame(frame_idx):
    canvas = Image.new("RGB", (WIDTH, HEIGHT), COLOR_INK_SEA)
    draw = ImageDraw.Draw(canvas)
    t = frame_idx / FPS  # Current time in seconds
    
    # -------------------------------------------------------------------------
    # SCENE 1: The Hook — Minimalist Command Console (0.0s – 4.5s, Frames 0–134)
    # -------------------------------------------------------------------------
    if frame_idx < 135:
        progress = frame_idx / 135.0
        zoom = 1.00 + 0.05 * progress
        base = fit_and_crop(img_light_landing, WIDTH, HEIGHT, zoom=zoom, offset_x=progress * -20)
        canvas.paste(base, (0, 0))
        
        # Sonar Rings Overlay
        cx, cy = 190, 420
        sonar_radius = 50 + int(progress * 280) % 200
        draw.ellipse([cx - sonar_radius, cy - sonar_radius, cx + sonar_radius, cy + sonar_radius], outline=COLOR_SIGNAL_LIGHT, width=2)
        
        # Kinetic Lower-Third Badge
        alpha_progress = min(1.0, frame_idx / 30.0)
        box_y = int(HEIGHT - 170 - 20 * (1 - alpha_progress))
        card_w, card_h = 760, 110
        card_x = 80
        draw.rounded_rectangle([card_x, box_y, card_x + card_w, box_y + card_h], radius=8, fill=(245, 240, 230), outline=COLOR_SIGNAL_LIGHT, width=2)
        draw.text((card_x + 24, box_y + 18), "PROJECT ORCA v7.0", font=FONT_CARD_TITLE, fill=COLOR_INK_SEA)
        draw.text((card_x + 24, box_y + 58), "Ocean Remote-Sensing & Tactical Marine Intelligence Copilot", font=FONT_CARD_DESC, fill=COLOR_DEEP_CURRENT)
        
        draw_top_hud(draw, is_dark=False)

    # -------------------------------------------------------------------------
    # SCENE 2: Multi-Stakeholder Operational Roles (4.5s – 9.0s, Frames 135–269)
    # -------------------------------------------------------------------------
    elif frame_idx < 270:
        local_idx = frame_idx - 135
        progress = local_idx / 135.0
        
        # Base background with gentle pan
        base = fit_and_crop(img_light_landing, WIDTH, HEIGHT, zoom=1.03, offset_y=-30)
        canvas.paste(base, (0, 0))
        
        # Semi-transparent dark overlay for high readability
        overlay = Image.new("RGBA", (WIDTH, HEIGHT), (16, 42, 49, 140))
        canvas.paste(overlay, (0, 0), overlay)
        
        # Header banner
        draw.text((80, 80), "MULTI-STAKEHOLDER COMMAND ARCHITECTURE", font=FONT_CARD_TITLE, fill=COLOR_WHITE)
        draw.text((80, 120), "One platform. Precision workflows tailored for every marine operator.", font=FONT_SUB, fill=COLOR_TIDE)
        
        # 5 Pillar Cards
        pillars = [
            ("FISHER", "PFZ Hotspots & Fuel ROI", "Identify optimal sardine & mackerel corridors; calculate fuel return."),
            ("RESEARCHER", "SLSTR SST & Chlorophyll", "Sentinel-3 thermal front gradients, degree heating weeks & NetCDF."),
            ("AUTHORITY", "IAMSAR SAR Datum & IMBL", "Leeway drift calculations, 61-day monsoon ban & vessel biometrics."),
            ("DISASTER", "Cyclone Path & Surge", "IMD tropical cyclone forecast cones, wind gale radii & evacuation."),
            ("MARITIME", "UKC & Tidal Windows", "Dynamic vessel draft analysis & safe navigation fairways.")
        ]
        
        card_w = 330
        card_h = 360
        start_x = 80
        spacing = 345
        
        active_idx = min(4, int(progress * 5.0))
        
        for i, (title, tag, desc) in enumerate(pillars):
            cx = start_x + i * spacing
            cy = 190
            
            is_active = (i == active_idx)
            fill_c = (245, 240, 230) if is_active else (23, 38, 43)
            outline_c = COLOR_HAZARD if is_active else (50, 70, 80)
            text_title_c = COLOR_INK_SEA if is_active else COLOR_TIDE
            text_tag_c = COLOR_DEEP_CURRENT if is_active else COLOR_DRIFTWOOD
            text_desc_c = COLOR_CHARCOAL if is_active else (180, 190, 195)
            
            # Card container
            draw.rounded_rectangle([cx, cy, cx + card_w, cy + card_h], radius=8, fill=fill_c, outline=outline_c, width=3 if is_active else 1)
            
            # Active Indicator Pill
            if is_active:
                draw.rounded_rectangle([cx + 16, cy + 18, cx + 120, cy + 44], radius=4, fill=COLOR_HAZARD)
                draw.text((cx + 26, cy + 22), "ACTIVE ROLE", font=get_font("segoeuib.ttf", 12), fill=(43, 27, 4))
            
            draw.text((cx + 18, cy + 55), title, font=FONT_CARD_TITLE, fill=text_title_c)
            draw.text((cx + 18, cy + 95), tag, font=get_font("segoeuib.ttf", 15), fill=text_tag_c)
            
            # Description lines
            words = desc.split()
            line1 = " ".join(words[:5])
            line2 = " ".join(words[5:10])
            line3 = " ".join(words[10:])
            draw.text((cx + 18, cy + 145), line1, font=FONT_CARD_DESC, fill=text_desc_c)
            draw.text((cx + 18, cy + 175), line2, font=FONT_CARD_DESC, fill=text_desc_c)
            draw.text((cx + 18, cy + 205), line3, font=FONT_CARD_DESC, fill=text_desc_c)
            
        # Bottom Prompt capsule trigger
        prompt_box_y = HEIGHT - 130
        draw.rounded_rectangle([80, prompt_box_y, WIDTH - 80, prompt_box_y + 60], radius=8, fill=(16, 30, 41), outline=COLOR_SIGNAL_DARK, width=2)
        draw.text((105, prompt_box_y + 18), "QUERY >", font=FONT_MONO, fill=COLOR_HAZARD)
        draw.text((195, prompt_box_y + 18), "Arabian Sea upwelling transect profile and thermocline slope", font=FONT_MONO, fill=COLOR_WHITE)
        
        draw_top_hud(draw, is_dark=True)

    # -------------------------------------------------------------------------
    # SCENE 3: Live Workspace & Sentinel-3 Telemetry (9.0s – 14.5s, Frames 270–434)
    # -------------------------------------------------------------------------
    elif frame_idx < 435:
        local_idx = frame_idx - 270
        progress = local_idx / 165.0
        
        # Transition from light workspace to dark workspace midway
        if local_idx < 80:
            zoom = 1.00 + 0.08 * (local_idx / 80.0)
            base = fit_and_crop(img_light_workspace, WIDTH, HEIGHT, zoom=zoom, offset_x=30)
            canvas.paste(base, (0, 0))
            is_dark = False
        else:
            dark_prog = (local_idx - 80) / 85.0
            zoom = 1.08 + 0.04 * dark_prog
            base = fit_and_crop(img_dark_workspace, WIDTH, HEIGHT, zoom=zoom, offset_x=-20)
            canvas.paste(base, (0, 0))
            is_dark = True
            
        # Tactical Map Waypoint Callout Box
        callout_w, callout_h = 560, 160
        callout_x = int(WIDTH / 2 - callout_w / 2)
        callout_y = HEIGHT - 210
        
        draw.rounded_rectangle([callout_x, callout_y, callout_x + callout_w, callout_y + callout_h], radius=8, fill=(10, 21, 32) if is_dark else (245, 240, 230), outline=COLOR_SIGNAL_DARK if is_dark else COLOR_SIGNAL_LIGHT, width=2)
        
        # Waypoint Title
        draw.ellipse([callout_x + 20, callout_y + 22, callout_x + 32, callout_y + 34], fill=COLOR_TIDE)
        draw.text((callout_x + 40, callout_y + 18), "ARABIAN SEA (WEST COAST & OFFSHORE BASIN)", font=FONT_TAG, fill=COLOR_WHITE if is_dark else COLOR_INK_SEA)
        
        # Telemetry metrics grid
        telemetry_lines = [
            "SST: 28.1°C  |  Gradient: 1.35°C/km  |  Fairway Depth: -75m",
            "Wave Height: 1.1m (Swell: 6.2s)       |  Wind: 14.0 km/h NW",
            "Provenance: Sentinel-3 SLSTR Level 2  |  Confidence: 96%"
        ]
        for line_i, t_str in enumerate(telemetry_lines):
            draw.text((callout_x + 20, callout_y + 55 + line_i * 28), t_str, font=get_font("consola.ttf", 15), fill=COLOR_SIGNAL_DARK if is_dark else COLOR_DEEP_CURRENT)
            
        draw_top_hud(draw, is_dark=is_dark)

    # -------------------------------------------------------------------------
    # SCENE 4: Outro & Call to Action (14.5s – 20.0s, Frames 435–599)
    # -------------------------------------------------------------------------
    else:
        local_idx = frame_idx - 435
        progress = local_idx / 165.0
        
        # Deep ocean night canvas
        canvas.paste(Image.new("RGB", (WIDTH, HEIGHT), COLOR_BG_DARK), (0, 0))
        
        # Sonar background rings expanding
        center_x, center_y = WIDTH // 2, HEIGHT // 2 - 60
        for ring_idx in range(4):
            ring_r = int((progress * 300 + ring_idx * 120) % 500) + 40
            alpha = max(0, min(255, int(255 * (1.0 - ring_r / 500.0))))
            draw.ellipse([center_x - ring_r, center_y - ring_r, center_x + ring_r, center_y + ring_r], outline=(62, 102, 114), width=1)
            
        # Draw Brand Logo
        if logo_img:
            logo_w = 110
            logo_resized = logo_img.resize((logo_w, logo_w), Image.Resampling.LANCZOS)
            canvas.paste(logo_resized, (center_x - logo_w // 2, center_y - 150), logo_resized)
            
        # Title & Subtitles
        title_text = "PROJECT ORCA v7.0"
        title_bbox = draw.textbbox((0, 0), title_text, font=FONT_HERO)
        title_w = title_bbox[2] - title_bbox[0]
        draw.text((center_x - title_w // 2, center_y - 10), title_text, font=FONT_HERO, fill=COLOR_WHITE)
        
        tag_text = "MULTI-STAKEHOLDER OCEAN COMMAND & INTELLIGENCE"
        tag_bbox = draw.textbbox((0, 0), tag_text, font=FONT_CARD_TITLE)
        tag_w = tag_bbox[2] - tag_bbox[0]
        draw.text((center_x - tag_w // 2, center_y + 75), tag_text, font=FONT_CARD_TITLE, fill=COLOR_SIGNAL_DARK)
        
        desc_text = "50+ Global Ports · Real-Time Satellite Telemetry · Zero Emojis · Strict Palette A"
        desc_bbox = draw.textbbox((0, 0), desc_text, font=FONT_SUB)
        desc_w = desc_bbox[2] - desc_bbox[0]
        draw.text((center_x - desc_w // 2, center_y + 125), desc_text, font=FONT_SUB, fill=COLOR_TIDE)
        
        # Action URL Box
        url_box_w, url_box_h = 620, 56
        url_x = center_x - url_box_w // 2
        url_y = center_y + 185
        draw.rounded_rectangle([url_x, url_y, url_x + url_box_w, url_y + url_box_h], radius=6, fill=COLOR_BG_PANEL_DARK, outline=COLOR_SIGNAL_DARK, width=2)
        url_text = "DEPLOY: github.com/Arceus1916/SIH26"
        url_bbox = draw.textbbox((0, 0), url_text, font=FONT_MONO)
        draw.text((center_x - (url_bbox[2] - url_bbox[0]) // 2, url_y + 16), url_text, font=FONT_MONO, fill=COLOR_HAZARD)
        
        # Final fade to black across last 20 frames
        if frame_idx >= 580:
            fade_black = int(255 * (frame_idx - 580) / 20.0)
            black_overlay = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, fade_black))
            canvas.paste(black_overlay, (0, 0), black_overlay)
            
        draw_top_hud(draw, is_dark=True)
        
    return canvas

# =========================================================================
# 3. ENCODE & RENDER VIA FFMPEG
# =========================================================================
def main():
    # 1. Generate Audio
    wav_path = generate_soundtrack()
    
    # 2. Extract Settled Poster Frame (Scene 4 Hero Frame at index 480)
    poster_frame_idx = 480
    print(f"[Poster] Capturing settled poster frame at index {poster_frame_idx}...")
    poster_img = render_frame(poster_frame_idx)
    poster_path = os.path.join(BRAG_DIR, "brag.jpg")
    poster_img.save(poster_path, quality=95)
    print(f"[Poster] Saved poster frame to: {poster_path}")
    
    # 3. Stream frames to FFmpeg
    output_mp4 = os.path.join(BRAG_DIR, "brag.mp4")
    print(f"[Video] Starting 1080p 30fps encoding to: {output_mp4}")
    
    cmd = [
        FFMPEG_BIN,
        "-y",
        "-f", "rawvideo",
        "-vcodec", "rawvideo",
        "-s", f"{WIDTH}x{HEIGHT}",
        "-pix_fmt", "rgb24",
        "-r", str(FPS),
        "-i", "-",               # Video stream from stdin
        "-i", wav_path,          # Audio stream from file
        "-c:v", "libx264",
        "-preset", "medium",
        "-crf", "18",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        output_mp4
    ]
    
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    
    # Send Frame 0 as the poster frame first, then frames 1 to 599
    # (Bakes the poster frame into frame 0 as required by brag creative laws)
    poster_raw = poster_img.tobytes()
    proc.stdin.write(poster_raw)
    
    for f in range(1, TOTAL_FRAMES):
        if f % 60 == 0:
            print(f"  Rendering frame {f}/{TOTAL_FRAMES} ({(f/TOTAL_FRAMES)*100:.1f}%)...")
        frame_img = render_frame(f)
        proc.stdin.write(frame_img.tobytes())
        
    proc.stdin.close()
    stderr_output = proc.stderr.read().decode('utf-8', errors='ignore')
    proc.wait()
    
    if proc.returncode != 0:
        print(f"[Error] FFmpeg failed with code {proc.returncode}:\n{stderr_output}")
        sys.exit(1)
        
    print(f"[Success] Launch video successfully generated: {output_mp4}")
    print(f"File size: {os.path.getsize(output_mp4):,} bytes")

if __name__ == "__main__":
    main()

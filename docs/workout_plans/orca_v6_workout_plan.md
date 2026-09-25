# Project ORCA — V6.2 Finalized Tactical Workout Plan & Engineering Specification

## Document Overview
- **Version**: 6.2.0 (Finalized Version 6)
- **Codename**: *Global Ocean Intelligence, Multi-lingual SLM, Dynamic Canvas Contours & Brand Identity*
- **Scope**: Multi-lingual Maritime SLM, Seaward Water Fairway Anchors (52 Ports), Default PFZ Layer State, Dual Chat/Manual Layer Toggling, Dynamic Organic Canvas Contours, Clean Minimalist Coordinates, and Official Project Logo & Favicon Suite.

---

## 1. Executive Summary & Goals
Project ORCA v6.0 upgrades the Agentic Marine Intelligence Platform (AMIP) into a truly global ocean intelligence system capable of supporting operations across 50 international and domestic ports. 

Key milestones achieved in v6.0:
1. **Full Global Multi-Lingual SLM**: Native script and tokenization support for Japanese (Kana/Kanji), Chinese (Simplified/Traditional Hanzi), Korean (Hangul), Arabic, Spanish, French, Portuguese, Dutch, German, Norwegian, Indonesian, and Indic coastal languages (Hindi, Marathi, Tamil, Malayalam, Telugu, Bengali, Gujarati, Kannada).
2. **Strict Seaward Water Clamping**: Dedicated directional vectors and geometric bounding boxes preventing oceanographic layers (PFZ, SST isotherms, Chlorophyll plumes, depth contours) from ever landing on terrain in estuarine or island ports (Port of Singapore, Port of Shanghai, Port of New York & New Jersey, Tokyo Bay, Port of Rotterdam, San Francisco).
3. **Default Layer State & Dual Layer Control**:
   - Default state on startup: **Only PFZ Front Plumes (Multi-zone)** is enabled.
   - Secondary layers (SST Isotherms, Chlorophyll Plumes, Bathymetric Depth Grid, Thermal Wind Streamlines) are disabled by default.
   - Dual control mechanism: Toggled either manually via the Tactical Layers drawer or dynamically via natural language chat commands (e.g., *"show SST"*, *"toggle chlorophyll"*, *"only PFZ"*, *"show all layers"*).
4. **Dock Selector Bar**: Instant drop-down harbor switcher pinned beneath the map viewport allowing 1-click global spatial navigation.

---

## 2. Multi-Lingual SLM Architecture

### 2.1 Non-ASCII Tokenization & Firewall Fix
- **Problem**: Previous ASCII-only regex tokenizers (`[a-zA-Z0-9]+`) stripped non-Latin characters, causing queries in Japanese or Chinese to fail the maritime domain firewall and fall back to whatever language was stored in the active session.
- **Solution**:
  - Direct non-ASCII substring matching before tokenization across all coastal gazetteers and RAG corpora.
  - Multi-script intent classification in `slm_intent_classifier.py` and `regional_language_service.py`.
  - Dynamic session language override: current input language always takes precedence over cached historical session states.

### 2.2 Vernacular Marine Directory
Over 40 pelagic and demersal marine species indexed across English, Scientific Binomials, and local vernacular names:
- **Japanese**: Suzuki (スズキ / 鱸), Aji (アジ / 鰺), Tara (タラ / 真鱈), Buri (ブリ / 鰤), Sanma (サンマ / 秋刀魚), Tai (タイ / 真鯛).
- **Chinese**: Daiyu (带鱼), Luyu (鲈鱼), Huangyu (大黄鱼), Shiyu (鰤鱼), Sanwenyu (三文鱼).
- **Indic Coastal**: Bangda (बांगडा), Surmai (सुरमई), Pomfret/Paplet (पापलेट), Bombil (बोंबील), Ayala, Mathi, Vanjaram, Netholi.

---

## 3. Seaward Water Clamping Engine

### 3.1 Mathematical Principles
Estuarine ports located inside bays, sounds, or river deltas require custom seaward approach vectors $(\Delta x, \Delta y)$ and hard geographical bounding clamps:
```python
def clamp_to_seaward_water(lat, lon, c_lat, c_lon, dx, dy):
    # Port of Singapore: strictly South into Singapore Strait fairway
    if 1.0 <= c_lat <= 1.5 and 103.5 <= c_lon <= 104.2:
        return min(lat, 1.215), max(103.65, min(104.10, lon))
    # Port of Shanghai: strictly East into East China Sea
    if 30.8 <= c_lat <= 32.2 and 121.0 <= c_lon <= 122.5:
        return max(30.60, min(31.60, lat)), max(lon, 121.92)
    # Port of New York: strictly South into New York Bight
    if 40.2 <= c_lat <= 41.2 and -74.5 <= c_lon <= -73.6:
        return min(lat, 40.46), max(-74.15, min(-73.30, lon))
    # Tokyo Bay: strictly South into central Uraga Suido
    if 35.2 <= c_lat <= 35.8 and 139.5 <= c_lon <= 140.2:
        return min(lat, 35.53), max(139.68, min(140.05, lon))
```

---

## 4. Layer Orchestration & Chat Toggle Pipeline

### 4.1 Layer Lifecycle
1. On initialization, Leaflet creates 4 LayerGroups (`pfzLayerGroup`, `sstLayerGroup`, `chlLayerGroup`, `depthLayerGroup`).
2. Only `pfzLayerGroup.addTo(map)` is executed during map boot.
3. Checkboxes in `#tactical-drawer-overlay` reflect this state (`chk-pfz` checked; others unchecked).
4. `processChatLayerToggle(text)` intercepts messages:
   - Pure toggle directives return an immediate tactical confirmation message with suggested actions.
   - Hybrid questions (e.g. *"Check conditions in Tokyo Bay and show SST"*) toggle the layer immediately on the canvas and forward the question to the RAG backend.

---

## 5. Verification Matrix
- **Automated Tests**: 51/51 Pytest suites passing (`test_regional_language.py`, `test_chat_service.py`, `test_pfz_service.py`).
- **Design System**: 100% compliant with Palette A & v6.1 tokens, zero gradients, zero emojis, max 8px border-radius.

---

## 6. v6.1 Landing Page Redesign & Dual Palette Specification

### 6.1 Theme Tokens Specification
Version 6.1 introduces an authentic nautical cartographic theme system with two dedicated palettes:

#### Light — "chart paper"
- `--bg`: `#EDE7D8` (Page background)
- `--bg-2`: `#E3DCC8` (Panels, search capsule, chips)
- `--panel-border`: `rgba(29, 43, 38, 0.16)` (Hairline borders)
- `--ink`: `#1D2B26` (Primary text & headings)
- `--ink-secondary`: `#55645C` (Subheads, body copy)
- `--ink-muted`: `#8B7F63` (Timestamps, axis ticks, placeholders)
- `--contour`: `#8A6F45` (Background bathymetric depth chart lines)
- `--signal`: `#2B6F7A` (Teal accent, live/normal beacon, wave lines)
- `--signal-ink`: `#F4F1E6` (Text on signal fill)
- `--hazard`: `#B5651D` (Amber accent, safety-critical)
- `--hazard-bg`: `rgba(181, 101, 29, 0.12)` (Hazard tag background)
- `--hazard-ink`: `#3A2408` (Text on hazard fill/bg)

#### Dark — "night bridge"
- `--bg`: `#0A1520` (Bridge night deck floor)
- `--bg-2`: `#101E29` (Radar consoles & input panels)
- `--panel-border`: `rgba(233, 228, 214, 0.14)` (Hairline borders)
- `--ink`: `#E9E4D6` (Primary luminescent text)
- `--ink-secondary`: `#9FB0AC` (Secondary readouts)
- `--ink-muted`: `#6E8480` (Coordinate ticks & placeholders)
- `--contour`: `#3E6672` (Bathymetric depth contour lines)
- `--signal`: `#7FC4D2` (Night signal teal beacon & accents)
- `--signal-ink`: `#06232A` (Text on night signal fill)
- `--hazard`: `#E2A23D` (Safety alert amber accent)
- `--hazard-bg`: `rgba(226, 162, 61, 0.14)` (Hazard chip background)
- `--hazard-ink`: `#2B1B04` (Text on amber fill)

### 6.2 Landing Page UI Architecture
1. **Latitude Axis Ticks (Left Edge)**: Minimalist tick markers (`— 16°N` down to `— 12°N`) positioned along the left screen margin in `--ink-muted`.
2. **Bottom Axis & Sector Tag**: Longitude markers (`78°E` to `86°E`) with geographical location header `13.08°N 80.27°E — Chennai coastal sector`.
3. **Left Hero Box**:
   - Title: `Project ORCA` (sans-serif geometric, weight 800)
   - Wavy lines: 3-crest sine wave SVG in `--signal`
   - Description: Two-line marine intelligence copilot summary
   - Prompt Search Capsule: Pill input in `--bg-2` with amber `--hazard` action send button
   - 2x2 Quick Action Chips: `Bay of Bengal status` (hazard styled), `Nearby harbor safety`, `Fish hotspots near me`, `Cyclone advisory · বাংলা`.
4. **Right Bathymetric Contour Art**: Delicate, organic concentric depth contour rings centered on the right half in `--contour`.
5. **Tactical Header**: Brand title `ORCA`, subtitle `Marine data system`, real-time `Live telemetry · synced HH:MM` status indicator, and dynamic sun/moon theme switcher.

---

## 7. v6.2 Global Water Anchors & Landing UI Harmonization

### 7.1 Authoritative Harbor Water Fairway Anchors (52 Ports)
To definitively eliminate layer and zone overlap onto land across complex estuarine, riverine, and archipelago ports (e.g., Shanghai Yangtze Delta, Singapore Strait, Rotterdam Hook of Holland, Hamburg Elbe, New York Bight, Tokyo Bay, San Francisco Pacific, Mumbai Colaba):
- `HARBOR_WATER_ANCHORS` is integrated synchronously into both backend (`backend/src/services/pfz_service.py`) and frontend (`frontend/src/app.js`).
- Oceanographic layers (PFZ, SST, Chlorophyll, Depth) anchor at true seaward navigable water origins rather than dock coordinate points.
- Strict rectangular bounding boxes enforce mathematical clamping ensuring no vertex reaches the coastline.

### 7.2 Restored Previous UI Directives & Tagline
- Restored authoritative tag line: `Ocean Remote-Sensing & Tactical Marine Intelligence Copilot`.
- Restored previous UI quick directive chips:
  1. `Bangda in Mumbai` -> `Where can I catch Bangda near Mumbai Sassoon Docks?`
  2. `Bay of Bengal Status` (with hazard badge styling) -> `Bay of Bengal ocean state and wave swell advisory`
  3. `Kochi Harbor Safety` -> `Is it safe for motorized skiff to depart from Kochi harbor?`
  4. `Daryavar Jaycha Ka (Dapoli)` -> `daryavar jaycha ka vatavaran kase ahe Dapoli la`
  5. `Inniku Kadal Epdi (Chennai)` -> `inniku kadal epdi irukku meen pidikka pogalama Chennai`

### 7.3 Screen-Contained Dynamic Canvas Contour Engine
- Converted static SVG bathymetric art into a high-performance 2D `<canvas id="chart-bg">` with dynamic DPR scaling.
- Implemented mathematical multi-harmonic organic wave noise algorithm across 9 depth rings centered at `cx = w * 0.70, cy = h * 0.50`, scaling with `Math.min(w, h)`:
  - Base radius: `0.05 * min(w, h)`, ring gap: `0.052 * min(w, h)`
  - Vertical compression factor: `0.70`, ensuring all 9 concentric contour rings remain completely contained within the viewport with comfortable margins.
  - Automatically reads active CSS custom properties (`--contour` and `--ink-muted`) and redraws instantly on theme change and window resize.

### 7.4 Clean Bottom-Left Axis (Removed Chennai Coastal Sector Text)
- Completely removed the static `13.08°N 80.27°E — Chennai coastal sector` tag from the bottom left per user requirements.
- Longitude tick labels (`78°E` to `86°E`) and Latitude tick labels (`16°N` to `12°N`) are rendered directly on the chart canvas in monospace nautical typography without redundant localized text.

### 7.5 Project Logo & Favicon Integration
- Extracted and processed the authoritative Project ORCA emblem and logo assets with transparent backgrounds:
  - `favicon.png` (128x128 high-DPI square) and `favicon.ico` (multi-size 16/32/48/64) linked in `<head>`.
  - `logo-icon.png` (304x304 centered orca compass mark) integrated into the top tactical navigation bar (`.hud-icon-box`) and the landing hero header (`.landing-hero-brand-row`).
  - `logo.png` (307x382 full typographic brand mark).
  - Maintained across both `frontend/public/` and `frontend/` roots for resilient static serving in development and production.
  - Added subtle adaptive luminescence drop-shadow for dark-theme contrast.

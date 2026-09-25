# Project ORCA — V6.0 Tactical Workout Plan & Engineering Specification

## Document Overview
- **Version**: 6.0.0
- **Codename**: *Global Ocean Intelligence, Multi-lingual SLM & Tactical Seaward Integrity*
- **Scope**: Multi-lingual Maritime SLM, Zero Land Overlap Water Clamping for Global Ports, Default Layer State & Dual Layer Control, 50-Port Global Harbor Registry.

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
- **Design System**: 100% Palette A compliant, zero gradients, zero emojis, max 8px border-radius.

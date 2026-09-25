# Project ORCA v3.0 — Comprehensive Architectural Workout Plan
## Conversational-First Marine Intelligence Platform with Progressive Spatial Disclosure & Regional Language Engine

---

## 1. Executive Summary & Problem Diagnosis

### The Core Problem in v2.0
In the current interface, the user is immediately dropped into a high-density, multi-panel tactical layout (left sidebar controls, center Leaflet map, crosshair HUD, species list, bottom layers, and right-side copilot chat). While powerful for experienced maritime dispatchers, **it overwhelms first-time operators, coastal fishers, and end users with sensory overload**.

### The v3.0 Vision: "Conversational Horizon"
Transition Project ORCA into a **stage-driven progressive disclosure architecture with deep regional coastal localization**:
1. **Stage 1 (Primary Landing)**: Clean, welcoming, AI chat-first interface modeled after ChatGPT/Gemini, focused 100% on conversational marine inquiries.
2. **Stage 2 (Progressive Geospatial Reveal)**: As soon as a query involves maritime coordinates, ports, sea basins, weather, or fishing zones, the UI smoothly pulls up and docks the high-resolution tactical geospatial canvas.
3. **Stage 3 (Bidirectional Ship Risk Matrix)**: Vessel limits can be input through a dedicated UI control or typed directly into the chat; the system syncs both channels in real time and presents live risk analysis.
4. **Regional Language Engine (Chat SLM)**: Understands native scripts (Devanagari, Tamil, Malayalam, Bengali, Telugu) and transliterated romanized queries (Hinglish, Marathlish, Tanglish). Responds in the matched language/script.
5. **Vernacular Coastal Fish Nomenclature**: Replaces/augments generic English species names with regional coastal terminology (e.g. Indian Mackerel ➔ *Bangda* / *Ayala* / *Kumla*; Seer Fish ➔ *Surmai* / *Neymeen* / *Vanjaram*).
6. **Dual Theme System**: Full Light Mode & Dark Mode design tokens with automatic map tile provider switching.
7. **Hands-Free Audio & Offline Resilience**: Integrated Web Speech voice query, audio readback, and 1-click PDF mission dossier export.

```
┌────────────────────────────────────────────────────────────────────────┐
│                        PROJECT ORCA v3.0 LIFECYCLE                     │
├────────────────────────────────────────────────────────────────────────┤
│                                                                        │
│   STAGE 1: LANDING                 STAGE 2: SPATIAL REVEAL             │
│   ┌───────────────────────────┐    ┌─────────────┬───────────────────┐ │
│   │ [Header + Lang + Theme]   │    │ CHAT PANE   │ TACTICAL MAP      │ │
│   │                           │    │             │                   │ │
│   │    Conversational Copilot │ ─► │ User: Aaj   │ Dynamic Leaflet   │ │
│   │    (Gemini-style Centered)│    │ mausam      │ PFZ Plumes        │ │
│   │                           │    │ kaisa hai?  │ SST Contours      │ │
│   │ [Regional Starters (En/Hi)│    │             │ Thermal Wind Flow │ │
│   │ [Input + Mic + Vessel Set]│    │ [Risk Sync] │ [HUD Telemetry]   │ │
│   └───────────────────────────┘    └─────────────┴───────────────────┘ │
│                                                                        │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Core Architectural Pillars

### Pillar A: Progressive Disclosure (Chat-First ➔ Spatial Split)
* **Default State (Stage 1)**: Map is hidden or in standby. The user interacts with a centered, distraction-free conversational copilot with high typography standards.
* **Spatial Trigger Engine (Stage 2)**:
  * An event listener in the chat response detects geospatial payloads (`coordinates`, `harbor_name`, `bounding_box`, `pfz_features`, `weather_state`).
  * When detected, the layout transitions via fluid CSS Flexbox/Grid animations from a centered single-column chat to a 45/55 or 50/50 responsive split canvas.
* **View Mode Controls**:
  - `💬 Chat Focus` (centered chat)
  - `🗺️ Split Canvas` (chat + interactive map side-by-side)
  - `🧭 Map Focus` (fullscreen map with minimized floating chat bubble)

---

### Pillar B: Regional Language Engine & Transliteration (SLM)
* **Multi-Lingual Intent & Script Support**:
  - **Native Scripts**: Hindi (हिन्दी), Marathi (मराठी), Tamil (தமிழ்), Malayalam (മലയാളം), Bengali (বাংলা), Telugu (తెలుగు), Gujarati (ગુજરાતી), Kannada (ಕನ್ನಡ).
  - **Transliterated Romanized Input (English Alphabet)**:
    - *Hinglish*: *"aaj samundar me hawa kitna hai"*, *"kya aaj machli pakadne jaa sakte hain?"*
    - *Marathlish*: *"daryavar vatavaran kasa ahe"*, *"harnai bandarapasun kiti antar ahe"*
    - *Tanglish*: *"inniku kadal kaaththu epdi irukku"*, *"meen pidikka pogalama"*
    - *Malayalam-English*: *"innalathe pole kadal kshobhikkumo"*, *"ayala kooduthal evide kittum"*
* **Response Generation Rule**:
  - The model auto-detects the input language and notation.
  - If the user writes in Romanized regional language (Hinglish/Tanglish), the model replies in clean, conversational Romanized regional language with standard maritime safety clearances.
  - If the user writes in native script (Devanagari, Tamil, etc.), the response is generated in that native script.
  - English queries receive high-precision English with regional vernacular annotations.

---

### Pillar C: Coastal Vernacular Fish Nomenclature Glossary
Coastal fishers do not identify fish by their English academic names. Project ORCA v3.0 maps scientific and common names to established local coastal fish names across India's maritime states:

| English / Scientific Name | Marathi / Konkani (MH/Goa) | Malayalam (Kerala) | Tamil (Tamil Nadu) | Telugu (Andhra Pradesh) | Bengali (West Bengal) | Gujarati (Gujarat) |
|---|---|---|---|---|---|---|
| **Indian Mackerel** (*Rastrelliger kanagurta*) | **Bangda (बांगडा)** | **Ayala (അയല)** | **Kumla (கானாங்கெளுத்தி)** | **Kanagarthalu (కానగంతలు)** | **Bangda / Gurfa** | **Bangdi (બાંગડી)** |
| **Yellowfin Tuna** (*Thunnus albacares*) | **Gedar / Khavlya** | **Kera / Choora (ചൂര)** | **Surai (சூரை)** | **Soora (సూర)** | **Tuna** | **Gedar** |
| **Indian Oil Sardine** (*Sardinella longiceps*) | **Tarli (तारली)** | **Mathi / Chaala (മത്തി)** | **Kavalai (கவலை)** | **Kavallu (కవళ్ళు)** | **Khaira** | **Tarli** |
| **Seer Fish / King Mackerel** (*Scomberomorus commerson*) | **Surmai (सुरमई)** | **Neymeen / Ayakoora (നെയ്മീൻ)** | **Vanjaram (வஞ்சிரம்)** | **Vanjaram (వంజరం)** | **Surmai** | **Surmai** |
| **Silver Pomfret** (*Pampus argenteus*) | **Paplet (पापलेट)** | **Vellavoli (വെള്ളവോലി)** | **Vawaal (வாவல்)** | **Tella Chanduva (తెల్ల చందువ)** | **Chanda / Rupchanda** | **Vichuda** |
| **Skipjack Tuna** (*Katsuwonus pelamis*) | **Kuppa Gedar** | **Kuppa Choora (കുപ്പച്ചൂര)** | **Kandayan Surai** | **Gora Soora** | **Katsuwonus** | **Kuppa** |
| **Hilsa / Shad** (*Tenualosa ilisha*) | **Palla (पल्ला)** | **Hilsa** | **Ullam** | **Palasa (పలస)** | **Ilish (ইলিশ)** | **Palla / Chaksi** |
| **Threadfin Bream** (*Nemipterus japonicus*) | **Rani / Tamb** | **Kilimeen / Chutta (കിളിമീൻ)** | **Sankara (சங்கரா)** | **Chitti Mathi** | **Rani** | **Lal Machli** |
| **Squid / Cuttlefish** (*Loligo spp.*) | **Ghol / Makul** | **Koonthal / Kanava (കൂന്തൽ)** | **Oosi Kanawa (கணவா)** | **Kalava** | **Calmari** | **Narsinga** |

*When delivering PFZ and catch recommendations, ORCA v3.0 will automatically output:*
`• Indian Mackerel (Bangda / Ayala / Kumla) — High biological aggregation in 35-75m shelf corridor.`

---

### Pillar D: Bidirectional Vessel Seaworthiness Matrix
* **Chat ➔ Controls**: If the operator types: *"I have an artisanal catamaran, wind tolerance is 15 km/h and wave max 0.8m"*:
  1. The SLM entity extractor extracts `{vessel: "artisanal_catamaran", max_wind: 15, max_wave: 0.8}`.
  2. Updates DOM selectors & range sliders in the slide-out Vessel Drawer.
  3. Recalculates risk against current ocean state and displays instant visual clearance.
* **Controls ➔ Chat**:
  1. Adjusting sliders in the UI immediately injects parameters into the active session context.
  2. Re-evaluates risk badge (`🟢 SAFE TO SAIL`, `🟡 CAUTION ADVISED`, `🔴 DANGER — PROHIBITED`).

---

### Pillar E: Dual Theme System (Light & Dark Mode)
Built strictly around ORCA's 5-color palette:
* Deep Sea (`#0D2B45`)
* Ocean Mist (`#5A7D9A`)
* Seafoam (`#8DBFB7`)
* Sandy Shore (`#DCC7AA`)
* Salt Air (`#F4F6F6`)
* Midnight Canvas (`#0B1220`)

| Design Element | Dark Mode (Night Ops / Default) | Light Mode (High-Sunlight Decks) |
|---|---|---|
| **App Background** | `#0B1220` (Midnight Command Floor) | `#F4F6F6` (Salt Air Clean) |
| **Chat Bubbles (Agent)** | `#0D2B45` + `#5A7D9A` border | `#FFFFFF` + `#DCC7AA` subtle border |
| **Chat Bubbles (User)** | `#5A7D9A` (Ocean Mist Solid) | `#0D2B45` (Deep Sea Text-Contrast) |
| **Primary Text** | `#F4F6F6` / `#FFFFFF` | `#0B1220` / `#0D2B45` |
| **Accents & Badges** | `#8DBFB7` (Seafoam High-Glow) | `#5A7D9A` / `#8DBFB7` (Refined Seafoam) |
| **Leaflet Basemap** | ESRI Dark Gray Canvas Tiles | ESRI Light Gray / Carto Positron Tiles |

---

### Pillar F: High-Value Usability & Fisher Ergonomics
1. **Web Speech Voice Input (Hands-Free)**:
   - 1-tap microphone button supporting English (`en-IN`), Hindi (`hi-IN`), Tamil (`ta-IN`), Marathi (`mr-IN`), and Malayalam (`ml-IN`).
   - Essential for boat skippers handling nets or helm controls.
2. **Integrated 1-Click PDF Mission Dossier Export**:
   - Export official formatted dossier directly from chat action bar and floating map HUD.
   - Includes GPS coordinates, live SST/wave/wind telemetry, vessel matrix, PFZ bearings, emergency distress frequencies, and SHA-256 evidence chain.
3. **Offline Resilience & PWA Caching**:
   - Service worker caching coastal tile packs & last known advisory so fishers retain navigational data when dropping out of cellular coverage.
4. **Airtight Marine Water Land Restriction**:
   - Preserves Ray-Casting Point-in-Polygon check across all continental landmasses.

---

## 3. Phased Implementation Roadmap (GSD Lifecycle)

### Phase 1: Design Tokens & Dual-Theme Foundation
- [ ] Refactor `frontend/styles/variables.css` into `:root` (Light Theme) and `[data-theme="dark"]` with strict palette variables.
- [ ] Add smooth theme toggle in top navigation with `localStorage` persistence and OS `prefers-color-scheme` support.
- [ ] Implement dynamic basemap tile layer switcher in Leaflet (`setDarkTiles()` vs `setLightTiles()`).
- [ ] Run `node frontend/scripts/verify-palette.js` to ensure 100% compliance with strict color rules.

### Phase 2: Stage 1 — Conversational Horizon (Chat-First Landing UI)
- [ ] Redesign `frontend/index.html` into a clean, centered Gemini-style conversational feed.
- [ ] Add welcoming operational prompt: *"Where are you departing from today, Captain?"*.
- [ ] Add one-tap multi-lingual recommendation cards (English & regional starters).
- [ ] Hide dense map and layer controls on initial landing.

### Phase 3: Stage 2 — Progressive Geospatial Split Canvas
- [ ] Implement layout state engine:
  - `.layout-chat-focus`: Centered chat only.
  - `.layout-split-view`: Chat left (45%), Interactive Map right (55%).
  - `.layout-map-focus`: Fullscreen map with floating minimized chat.
- [ ] Auto-trigger transition to `.layout-split-view` when a location, coordinate, or sea basin is discussed.
- [ ] Include view-switching pills (`💬 Chat Focus`, `🗺️ Split View`, `🧭 Full Map`).

### Phase 4: Regional Language Pack & Vernacular Fish Glossary
- [ ] Create `backend/src/services/regional_language_service.py`:
  - Script & transliteration detector (Hinglish, Marathlish, Tanglish, native scripts).
  - Vernacular fish nomenclature directory (Bangda, Surmai, Ayala, Mathi, Paplet, etc.).
  - Response generator that mirrors the detected language format.
- [ ] Update `backend/src/services/marine_chat_service.py` to route through the regional language engine.
- [ ] Add comprehensive unit tests in `backend/tests/test_regional_language.py`.

### Phase 5: Stage 3 — Bidirectional Vessel Risk Matrix & Controls
- [ ] Build slide-out "Vessel Profile & Risk Matrix" drawer with:
  - Vessel type dropdown.
  - Wave tolerance slider (0.5m – 4.0m).
  - Wind tolerance slider (10 km/h – 60 km/h).
- [ ] Implement bidirectional NLP extractor in `app.js`:
  - Parse vessel limits from chat messages (in English or Romanized regional language) and update sliders.
  - Slider adjustments immediately update active chat context and live status badge.

### Phase 6: Hands-Free Voice & PDF Export Usability
- [ ] Add Web Speech Recognition mic input button to the chat input bar.
- [ ] Add optional audio speech synthesis readback for critical marine alerts.
- [ ] Wire up 1-click PDF Mission Dossier export directly into chat action pills.
- [ ] Retain Ray-Casting land restriction for custom pins.

### Phase 7: Master Verification & CI/CD Gating
- [ ] Run `py scripts/run_all_tests.py` (ensure all backend, regional language, and palette tests pass 100%).
- [ ] Validate both Light and Dark themes against WCAG AA contrast standards.
- [ ] Commit all changes with clean commit messages and push to `origin main`.

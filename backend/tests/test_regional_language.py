"""
Unit Tests for Project ORCA Regional Coastal Language Engine & Vernacular Fish Nomenclature
"""
import pytest
from backend.src.services.regional_language_service import RegionalLanguageService, VERNACULAR_FISH_DIRECTORY
from backend.src.services.marine_chat_service import marine_chat_service
from backend.src.models.chat import ChatRequest, VesselProfile, SafetyStatus

def test_detect_native_scripts():
    # Hindi Devanagari
    lang, script = RegionalLanguageService.detect_language("आज का मौसम कैसा है?")
    assert lang == "hi"
    assert script == "devanagari"

    # Marathi Devanagari
    lang, script = RegionalLanguageService.detect_language("दर्यावर आज जायचे का? लाटा कशा आहेत?")
    assert lang == "mr"
    assert script == "devanagari"

    # Tamil
    lang, script = RegionalLanguageService.detect_language("இன்று கடல் அலைகள் எப்படி உள்ளது?")
    assert lang == "ta"
    assert script == "tamil"

    # Malayalam
    lang, script = RegionalLanguageService.detect_language("ഇന്നത്തെ കടൽ അവസ്ഥ എങ്ങനെയുണ്ട്?")
    assert lang == "ml"
    assert script == "malayalam"

def test_detect_transliterated_romanized():
    # Hinglish
    lang, script = RegionalLanguageService.detect_language("aaj mausam kaisa hai samundar me")
    assert lang == "hi"
    assert script == "latin_romanized"

    # Marathlish
    lang, script = RegionalLanguageService.detect_language("daryavar jaycha ka vatavaran kase ahe")
    assert lang == "mr"
    assert script == "latin_romanized"

    # Tanglish
    lang, script = RegionalLanguageService.detect_language("inniku kadal epdi irukku meen pidikka pogalama")
    assert lang == "ta"
    assert script == "latin_romanized"

    # Malayalam-English
    lang, script = RegionalLanguageService.detect_language("innathe kadalil pokamo meen pidikkan")
    assert lang == "ml"
    assert script == "latin_romanized"

    # English default
    lang, script = RegionalLanguageService.detect_language("What is the sea condition off Mumbai port?")
    assert lang == "en"
    assert script == "latin"

def test_vernacular_fish_directory_resolution():
    # Indian Mackerel
    hi_mackerel = RegionalLanguageService.get_localized_fish_name("Indian Mackerel", "hi")
    assert "Bangda" in hi_mackerel

    ml_mackerel = RegionalLanguageService.get_localized_fish_name("Indian Mackerel", "ml")
    assert "Ayala" in ml_mackerel

    ta_mackerel = RegionalLanguageService.get_localized_fish_name("Indian Mackerel", "ta")
    assert "Kumla" in ta_mackerel

    # Seer Fish
    hi_seer = RegionalLanguageService.get_localized_fish_name("Seer Fish", "hi")
    assert "Surmai" in hi_seer

    ml_seer = RegionalLanguageService.get_localized_fish_name("Seer Fish", "ml")
    assert "Neymeen" in ml_seer

    ta_seer = RegionalLanguageService.get_localized_fish_name("Seer Fish", "ta")
    assert "Vanjaram" in ta_seer

    # Pomfret
    mr_pomfret = RegionalLanguageService.get_localized_fish_name("Silver Pomfret", "mr")
    assert "Paplet" in mr_pomfret

    # Oil Sardine
    ml_sardine = RegionalLanguageService.get_localized_fish_name("Indian Oil Sardine", "ml")
    assert "Mathi" in ml_sardine

def test_chat_hinglish_advisory():
    req = ChatRequest(
        user_id="usr-test-regional",
        message="aaj mausam kaisa hai samundar me Mumbai ke pas",
        coordinates=[18.9220, 72.8347]
    )
    resp = marine_chat_service.process_message(req)
    assert resp.reply is not None
    assert "Samundari Suraksha & Mausam Advisory" in resp.reply
    assert "Lahar ki Unchai" in resp.reply
    assert "Hawa ki Gati" in resp.reply
    assert resp.spatial_target is not None
    assert resp.spatial_target["lat"] == 18.9220

def test_chat_marathlish_advisory():
    req = ChatRequest(
        user_id="usr-test-marathi",
        message="daryavar jaycha ka vatavaran kase ahe Dapoli la",
        coordinates=[17.7554, 73.1811]
    )
    resp = marine_chat_service.process_message(req)
    assert resp.reply is not None
    assert "Daryavardi Suraksha & Vatavaran Ahwal" in resp.reply
    assert "Lataan Chi Unchi" in resp.reply
    assert "Waryacha Veg" in resp.reply
    assert resp.spatial_target is not None

def test_chat_tanglish_advisory():
    req = ChatRequest(
        user_id="usr-test-tamil",
        message="inniku kadal epdi irukku meen pidikka pogalama Chennai",
        coordinates=[13.0827, 80.2707]
    )
    resp = marine_chat_service.process_message(req)
    assert resp.reply is not None
    assert "Kadal Paathukappu & Vanilai Arikkai" in resp.reply
    assert "Alaiyin Uyarum" in resp.reply
    assert resp.spatial_target is not None

def test_chat_fish_query_vernacular_bangda():
    req = ChatRequest(
        user_id="usr-test-fish",
        message="where can I find bangda near Mumbai",
        coordinates=[18.9220, 72.8347]
    )
    resp = marine_chat_service.process_message(req)
    assert "Bangda" in resp.reply
    assert resp.spatial_target is not None

def test_chat_inline_vessel_parameter_sync():
    req = ChatRequest(
        user_id="usr-test-vessel-sync",
        message="Check safety for motorized skiff with max wave 1.2m and max wind 22 km/h near Kochi",
        coordinates=[9.9312, 76.2673]
    )
    resp = marine_chat_service.process_message(req)
    assert resp.vessel_profile is not None
    assert resp.vessel_profile.type == "motorized_skiff"
    assert resp.vessel_profile.max_safe_wave_m == 1.2
    assert resp.vessel_profile.max_safe_wind_kmh == 22.0
    assert resp.spatial_target is not None
    assert resp.spatial_target["lat"] == 9.9312

def test_chat_localized_out_of_domain_hinglish():
    req = ChatRequest(
        user_id="usr-test-ood-hinglish",
        message="kuch filam ki kahani batao ya gaana sunao",
    )
    resp = marine_chat_service.process_message(req)
    assert "Samundari Domain Notice" in resp.reply
    assert "Project ORCA marine assistant" in resp.reply

def test_chat_localized_out_of_domain_marathi():
    req = ChatRequest(
        user_id="usr-test-ood-marathi",
        message="मला एक छान गोष्ट सांगा किंवा जोक सांगा",
    )
    resp = marine_chat_service.process_message(req)
    assert "सागरी कार्यक्षेत्र सूचना" in resp.reply
    assert "प्रोजेक्ट ओर्का" in resp.reply

def test_chat_localized_out_of_domain_tamil():
    req = ChatRequest(
        user_id="usr-test-ood-tamil",
        message="oru nalla cinema sollu enna paarkalam",
    )
    resp = marine_chat_service.process_message(req)
    assert "Kadal Domain Notice" in resp.reply

def test_expanded_taxonomy_lookup():
    # Bombil (Harpadon nehereus)
    bombil = RegionalLanguageService.get_localized_fish_name("bombil", "mr")
    assert "Harpadon nehereus" in bombil or "Bombil" in bombil
    # Hilsa (Tenualosa ilisha)
    hilsa = RegionalLanguageService.get_localized_fish_name("hilsa", "bn")
    assert "Tenualosa ilisha" in hilsa or "Ilish" in hilsa

def test_chat_japanese_tokyo_bay_query():
    req = ChatRequest(
        user_id="usr-test-ja-tokyo",
        message="東京湾の魚は何ですか？",
        language="ja"
    )
    resp = marine_chat_service.process_message(req)
    # Check that spatial target resolved to Tokyo Bay
    assert resp.spatial_target is not None
    assert 35.0 <= resp.spatial_target["lat"] <= 36.0
    assert 139.0 <= resp.spatial_target["lon"] <= 140.5
    # Check Japanese response
    assert ("東京湾" in resp.reply or "海洋アドバイザリー" in resp.reply or "スズキ" in resp.reply or "アジ" in resp.reply or "Tokyo" in resp.reply)

def test_chat_language_switch_no_stale_retention():
    # Previous user request was in Marathi/Hindi, but new message is in Japanese
    req = ChatRequest(
        user_id="usr-session-switch",
        message="東京湾の魚",
        language="mr"  # Stale session language passed from previous turns
    )
    resp = marine_chat_service.process_message(req)
    # Must NOT reply in Marathi or fail
    assert "सागरी कार्यक्षेत्र सूचना" not in resp.reply
    assert resp.spatial_target is not None
    assert 35.0 <= resp.spatial_target["lat"] <= 36.0

def test_global_port_clamping_seaward():
    from backend.src.services.pfz_service import get_seaward_vector, clamp_to_seaward_water

    # Singapore: strictly south
    dx, dy = get_seaward_vector(1.29, 103.85)
    assert dy < 0
    c_lat, c_lon = clamp_to_seaward_water(1.29, 103.85, 1.29, 103.85, dx, dy)
    assert c_lat <= 1.215
    assert 103.65 <= c_lon <= 104.10

    # Shanghai: strictly east
    dx, dy = get_seaward_vector(31.23, 121.47)
    assert dx > 0
    c_lat, c_lon = clamp_to_seaward_water(31.23, 121.47, 31.23, 121.47, dx, dy)
    assert c_lon >= 121.92

    # New York: strictly south
    dx, dy = get_seaward_vector(40.69, -74.04)
    assert dy < 0
    c_lat, c_lon = clamp_to_seaward_water(40.69, -74.04, 40.69, -74.04, dx, dy)
    assert c_lat <= 40.46

    # Tokyo Bay: strictly south
    dx, dy = get_seaward_vector(35.65, 139.84)
    assert dy < 0
    c_lat, c_lon = clamp_to_seaward_water(35.65, 139.84, 35.65, 139.84, dx, dy)
    assert c_lat <= 35.53



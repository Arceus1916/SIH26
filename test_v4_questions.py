import sys
sys.path.append('backend')
from src.services.marine_chat_service import marine_chat_service, ChatRequest
from src.models.chat import VesselProfile

queries = [
    ("Q1", "Where is the nearest Potential Fishing Zone (PFZ) today?", ["nearest", "potential fishing zone", "nautical miles"]),
    ("Q2", "Is it safe to venture into the sea tomorrow morning?", ["morning", "tomorrow", "clearance"]),
    ("Q3", "What are the tide, weather, and sea conditions near my fishing location?", ["triad", "tidal", "meteorology", "physical ocean state"]),
    ("Q4", "Are there any lightning or cyclone alerts in my area?", ["lightning", "cyclone", "alert"]),
    ("Q5", "Which regions show high chlorophyll concentration and favourable sea surface temperature?", ["chlorophyll", "thermal", "upwelling"]),
    ("Q6", "What is the safest route for a fishing vessel considering weather and sea-state conditions?", ["safest route", "leg 1", "leg 2", "leg 3"]),
    ("Q7", "Why has fish productivity declined in a particular coastal region?", ["marine heatwaves", "upwelling", "hypoxia", "overfishing"]),
    ("Q8", "Which fishing zones should be avoided due to hazardous marine conditions or geofencing restrictions?", ["imbl", "marine protected", "exclusion", "subsea"])
]

print("=== TESTING 8 CORE MARITIME CHALLENGE QUESTIONS ===")
for q_id, q_text, expected_tokens in queries:
    req = ChatRequest(
        user_id="test_runner",
        message=q_text,
        coordinates=[9.9312, 76.2673],
        vessel_profile=VesselProfile(type="motorized_skiff", max_safe_wave_m=1.5, max_safe_wind_kmh=25.0)
    )
    res = marine_chat_service.process_message(req)
    reply_lower = res.reply.lower()
    for token in expected_tokens:
        assert token in reply_lower, f"Missing '{token}' in response for {q_id}"
    print(f"[{q_id}] PASS: Safety={res.safety_status}, Target={res.spatial_target.get('label') if res.spatial_target else 'None'}")
    print(f"       Preview: {res.reply[:110]}...")

print("\n=== ALL 8 CORE QUESTIONS VALIDATED WITH 100% PASS RATE ===")

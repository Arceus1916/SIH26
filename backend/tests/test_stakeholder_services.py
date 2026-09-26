"""
Comprehensive Unit & Integration Test Suite for ORCA Version 7 Multi-Stakeholder Intelligence
Covers:
- /v1/personas
- /v1/hydrography/transect (TransectService)
- /v1/navigation/ukc (UKCService)
- /v1/emergency/sar-datum (SARService)
- /v1/emergency/surge-inundation (SurgeService)
- /v1/geofence/evaluate (GeofenceService)
- Persona-conditioned SLM chat reasoning
"""
import pytest
from datetime import datetime, timezone, timedelta
from fastapi.testclient import TestClient

from backend.src.main import app
from backend.src.models.personas import (
    StakeholderPersona,
    GeoPoint,
    TransectRequest,
    UKCRequest,
    VesselDraftSpecs,
    SARDatumRequest,
    SurgeInundationRequest,
    GeofenceEvaluationRequest
)
from backend.src.services.transect_service import TransectService
from backend.src.services.ukc_service import UKCService
from backend.src.services.sar_service import SARService
from backend.src.services.surge_service import SurgeService
from backend.src.services.geofence_service import GeofenceService
from backend.src.services.marine_chat_service import marine_chat_service
from backend.src.models.chat import ChatRequest, SafetyStatus

client = TestClient(app)


def test_get_personas_endpoint():
    """Verify that all 5 stakeholder personas are returned with descriptions and defaults."""
    response = client.get("/v1/personas")
    assert response.status_code == 200
    data = response.json()
    assert "personas" in data
    assert len(data["personas"]) == 5
    persona_ids = [p["id"] for p in data["personas"]]
    assert "fisher" in persona_ids
    assert "researcher" in persona_ids
    assert "authority" in persona_ids
    assert "disaster" in persona_ids
    assert "maritime" in persona_ids


def test_transect_service_direct_and_api():
    """Verify transect slicing computes distance, interpolation, and thermocline slope."""
    req_data = {
        "start_point": {"lat": 17.68, "lon": 83.21},
        "end_point": {"lat": 17.95, "lon": 83.65},
        "num_samples": 25,
        "parameters": ["depth", "sst", "chlorophyll"]
    }
    # Direct service call
    p1 = GeoPoint(lat=17.68, lon=83.21)
    p2 = GeoPoint(lat=17.95, lon=83.65)
    t_req = TransectRequest(start_point=p1, end_point=p2, num_samples=25)
    service = TransectService()
    direct_res = service.slice_transect(t_req)
    assert direct_res.transect_length_km > 0
    assert len(direct_res.samples) == 25
    assert direct_res.thermocline_gradient_c_per_km >= 0
    assert isinstance(direct_res.upwelling_signature_detected, bool)

    # API call
    response = client.post("/v1/hydrography/transect", json=req_data)
    assert response.status_code == 200
    api_data = response.json()
    assert len(api_data["samples"]) == 25
    assert api_data["samples"][0]["distance_km"] == 0.0


def test_ukc_service_direct_and_api():
    """Verify dynamic squat calculation using Barrass formula and tidal clearance."""
    req_data = {
        "port_id": "kochi",
        "channel_id": "main-fairway",
        "vessel": {
            "name": "Panamax Container Carrier",
            "static_draft_m": 11.2,
            "length_bp_m": 220.0,
            "beam_m": 32.2,
            "block_coefficient": 0.78,
            "transit_speed_kts": 8.5
        }
    }
    # Direct service call
    vessel = VesselDraftSpecs(
        name="Panamax Container Carrier",
        static_draft_m=11.2,
        length_bp_m=220.0,
        beam_m=32.2,
        block_coefficient=0.78,
        transit_speed_kts=8.5
    )
    ukc_req = UKCRequest(port_id="kochi", vessel=vessel)
    service = UKCService()
    direct_res = service.calculate_ukc(ukc_req)
    assert direct_res.dynamic_squat_m > 0
    assert direct_res.safety_reserve_m > 0
    assert isinstance(direct_res.clearance_granted, bool)
    assert direct_res.status in ["CLEARED_ADEQUATE_UKC", "CAUTION_RESTRICTED_WINDOW", "CRITICAL_GROUNDING_RISK"]

    # API call
    response = client.post("/v1/navigation/ukc", json=req_data)
    assert response.status_code == 200
    api_data = response.json()
    assert "dynamic_squat_m" in api_data
    assert "net_ukc_m" in api_data


def test_sar_service_direct_and_api():
    """Verify IAMSAR leeway drift vector and expanding square waypoints."""
    now = datetime.now(timezone.utc)
    t0 = (now - timedelta(hours=3)).isoformat()
    t1 = now.isoformat()

    req_data = {
        "incident_time": t0,
        "current_time": t1,
        "last_known_position": {"lat": 17.65, "lon": 83.35},
        "target_type": "artisanal_skiff_unanchored"
    }
    # Direct service call
    sar_req = SARDatumRequest(
        incident_time=t0,
        current_time=t1,
        last_known_position=GeoPoint(lat=17.65, lon=83.35),
        target_type="artisanal_skiff_unanchored"
    )
    service = SARService()
    direct_res = service.compute_sar_datum(sar_req)
    assert direct_res.drift_distance_nm > 0
    assert direct_res.probable_area_sq_nm > 0
    assert len(direct_res.search_waypoints) >= 8

    # API call
    response = client.post("/v1/emergency/sar-datum", json=req_data)
    assert response.status_code == 200
    api_data = response.json()
    assert "datum_position" in api_data
    assert len(api_data["search_waypoints"]) >= 8


def test_surge_service_direct_and_api():
    """Verify storm surge water rise, WMO signal declaration, and CAP XML."""
    req_data = {
        "port_id": "paradip",
        "cyclone_name": "BOB-03",
        "central_pressure_hpa": 960.0,
        "ambient_pressure_hpa": 1010.0,
        "max_sustained_wind_kts": 75.0,
        "radius_max_wind_km": 35.0,
        "forward_speed_kts": 12.0,
        "landfall_distance_km": 30.0
    }
    # Direct service call
    surge_req = SurgeInundationRequest(
        port_id="paradip",
        cyclone_name="BOB-03",
        central_pressure_hpa=960.0,
        ambient_pressure_hpa=1010.0,
        max_sustained_wind_kts=75.0,
        radius_max_wind_km=35.0,
        forward_speed_kts=12.0,
        landfall_distance_km=30.0
    )
    service = SurgeService()
    direct_res = service.project_surge(surge_req)
    assert direct_res.peak_surge_height_m > 1.0  # Significant surge for 960 hPa & 75 kts
    assert direct_res.inundation_penetration_inland_km > 0
    assert direct_res.port_warning_signal.signal_number in [8, 9, 10]
    assert "<alert" in direct_res.common_alerting_protocol_xml

    # API call
    response = client.post("/v1/emergency/surge-inundation", json=req_data)
    assert response.status_code == 200
    api_data = response.json()
    assert api_data["peak_surge_height_m"] > 0
    assert "common_alerting_protocol_xml" in api_data


def test_geofence_service_direct_and_api():
    """Verify IMBL proximity, MPA sanctuary checks, and uniform monsoon ban."""
    # Location near Palk Strait (Rameswaram: 9.2876, 79.3129)
    req_data = {
        "vessel_position": {"lat": 9.2876, "lon": 79.3129},
        "vessel_type": "mechanized_trawler",
        "heading_deg": 90.0,
        "speed_kts": 6.0
    }
    # Direct service call
    geo_req = GeofenceEvaluationRequest(
        vessel_position=GeoPoint(lat=9.2876, lon=79.3129),
        vessel_type="mechanized_trawler",
        heading_deg=90.0,
        speed_kts=6.0
    )
    service = GeofenceService()
    direct_res = service.evaluate_geofence(geo_req)
    assert direct_res.nearest_imbl.border_name is not None
    assert direct_res.nearest_imbl.distance_nm > 0
    assert "BORDER" in direct_res.nearest_imbl.alert_status
    assert direct_res.active_sanctuary.name is not None
    assert direct_res.monsoon_ban_status.next_ban_window is not None

    # API call
    response = client.post("/v1/geofence/evaluate", json=req_data)
    assert response.status_code == 200
    api_data = response.json()
    assert "nearest_imbl" in api_data
    assert "active_sanctuary" in api_data
    assert "monsoon_ban_status" in api_data


def test_adaptive_slm_persona_chat():
    """Verify chat service conditions responses and actions according to stakeholder persona."""
    personas = ["fisher", "researcher", "authority", "disaster", "maritime"]
    for p in personas:
        request = ChatRequest(
            user_id=f"test_user_{p}",
            message="Provide operational status and advisory for our sector",
            coordinates=[13.0827, 80.2707],  # Chennai
            persona=p
        )
        response = marine_chat_service.process_message(request)
        assert response.persona == p
        assert response.safety_status in [SafetyStatus.SAFE, SafetyStatus.CAUTIOUS, SafetyStatus.DANGER]
        assert len(response.suggested_actions) > 0
        assert any(
            kw in response.reply.lower() or kw in [a.lower() for a in response.suggested_actions]
            for kw in ["fisher", "research", "authority", "disaster", "maritime", "transect", "sar", "surge", "ukc", "pfz", "mhw", "wave", "wind"]
        )

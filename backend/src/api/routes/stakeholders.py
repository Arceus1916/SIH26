"""
ORCA Stakeholder Persona API Endpoints
Provides dedicated microservices for Fisher, Researcher, Authority, Disaster, and Maritime workflows.
"""
from fastapi import APIRouter, HTTPException
from typing import Dict, Any, List

from ...models.personas import (
    TransectRequest,
    TransectResponse,
    UKCRequest,
    UKCResponse,
    SARDatumRequest,
    SARDatumResponse,
    SurgeInundationRequest,
    SurgeInundationResponse,
    GeofenceEvaluationRequest,
    GeofenceEvaluationResponse
)
from ...services.transect_service import TransectService
from ...services.ukc_service import UKCService
from ...services.sar_service import SARService
from ...services.surge_service import SurgeService
from ...services.geofence_service import GeofenceService

router = APIRouter(prefix="", tags=["stakeholders"])

transect_service = TransectService()
ukc_service = UKCService()
sar_service = SARService()
surge_service = SurgeService()
geofence_service = GeofenceService()


@router.get("/personas")
async def list_personas() -> Dict[str, Any]:
    """Returns the metadata and tooling catalog for all 5 stakeholder personas."""
    return {
        "personas": [
            {
                "id": "fisher",
                "label": "Fisher",
                "role": "Artisanal & Mechanized Fishermen",
                "default_layers": ["pfz", "isotherms"],
                "tools": ["catch_roi", "tidal_bar_window", "border_watch"],
                "dialect_priority": True
            },
            {
                "id": "researcher",
                "label": "Researcher",
                "role": "Marine Biologists & Oceanographers",
                "default_layers": ["bathymetry", "chlorophyll", "isotherms"],
                "tools": ["transect_slicer", "mhw_thermal_anomaly", "export_netcdf"],
                "scientific_mode": True
            },
            {
                "id": "authority",
                "label": "Authority",
                "role": "Coast Guard, Marine Police & Fisheries Enforcement",
                "default_layers": ["imbl_borders", "mpa_sanctuaries"],
                "tools": ["sar_datum_planner", "mpa_geofence", "monsoon_ban"],
                "enforcement_mode": True
            },
            {
                "id": "disaster",
                "label": "Disaster",
                "role": "State Disaster Management & Port Emergency Teams",
                "default_layers": ["wind_streamlines", "surge_inundation"],
                "tools": ["storm_surge_projector", "port_signal_flags", "cap_alert_dispatch"],
                "emergency_mode": True
            },
            {
                "id": "maritime",
                "label": "Maritime",
                "role": "Commercial Cargo, OSVs, Tugs & Port Pilots",
                "default_layers": ["nav_channels", "bathymetry"],
                "tools": ["dynamic_ukc_solver", "waypoint_corridor", "offshore_500m_ring"],
                "navigation_mode": True
            }
        ]
    }


@router.post("/hydrography/transect", response_model=TransectResponse)
async def extract_hydrographic_transect(req: TransectRequest):
    """Slices bathymetry, SST, and chlorophyll-a profiles along a designated maritime transect."""
    try:
        return transect_service.slice_transect(req)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Transect calculation failed: {str(e)}")


@router.post("/navigation/ukc", response_model=UKCResponse)
async def evaluate_under_keel_clearance(req: UKCRequest):
    """Calculates vessel dynamic squat, tidal water depth, and Under-Keel Clearance (UKC)."""
    try:
        return ukc_service.calculate_ukc(req)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"UKC calculation failed: {str(e)}")


@router.post("/emergency/sar-datum", response_model=SARDatumResponse)
async def compute_sar_search_datum(req: SARDatumRequest):
    """Computes IAMSAR leeway drift datum and expanding square search patterns."""
    try:
        return sar_service.compute_sar_datum(req)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"SAR datum computation failed: {str(e)}")


@router.post("/emergency/surge-inundation", response_model=SurgeInundationResponse)
async def project_surge_inundation(req: SurgeInundationRequest):
    """Projects cyclonic storm surge water rise, declares port signals 1-11, and formats CAP XML."""
    try:
        return surge_service.project_surge(req)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Surge calculation failed: {str(e)}")


@router.post("/geofence/evaluate", response_model=GeofenceEvaluationResponse)
async def evaluate_vessel_geofence(req: GeofenceEvaluationRequest):
    """Evaluates vessel distance against IMBL borders, MPAs, 500m platforms, and monsoon bans."""
    try:
        return geofence_service.evaluate_geofence(req)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Geofence evaluation failed: {str(e)}")

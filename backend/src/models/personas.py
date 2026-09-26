"""
ORCA Stakeholder Persona Data Models & Schemas
Covers Fisher, Researcher, Coastal Authority, Disaster Management, and Maritime Operator domains.
"""
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field


class StakeholderPersona(str, Enum):
    FISHER = "fisher"
    RESEARCHER = "researcher"
    AUTHORITY = "authority"
    DISASTER = "disaster"
    MARITIME = "maritime"


class GeoPoint(BaseModel):
    lat: float = Field(..., description="Latitude in decimal degrees")
    lon: float = Field(..., description="Longitude in decimal degrees")


# ==========================================
# 1. Researcher: Transect Slicing Schemas
# ==========================================

class TransectRequest(BaseModel):
    start_point: GeoPoint
    end_point: GeoPoint
    num_samples: int = Field(default=30, ge=5, le=100, description="Number of equidistant sampling points along transect")
    parameters: List[str] = Field(default=["depth", "sst", "chlorophyll"], description="Parameters to extract")


class TransectSample(BaseModel):
    distance_km: float
    lat: float
    lon: float
    depth_m: float
    sst_c: float
    chl_mg_m3: float


class TransectResponse(BaseModel):
    transect_length_km: float
    samples: List[TransectSample]
    upwelling_signature_detected: bool
    thermocline_gradient_c_per_km: float
    provenance_source: str = "ORCA-L3-Hydrographic-Mesh"


# ==========================================
# 2. Maritime Operator: UKC & Dynamic Squat
# ==========================================

class VesselDraftSpecs(BaseModel):
    name: str = Field(default="Commercial Vessel")
    static_draft_m: float = Field(..., gt=0.0, description="Static draft in meters")
    length_bp_m: float = Field(default=180.0, gt=0.0, description="Length between perpendiculars (m)")
    beam_m: float = Field(default=28.0, gt=0.0, description="Molded beam in meters")
    block_coefficient: float = Field(default=0.75, ge=0.5, le=0.9, description="Block coefficient (Cb)")
    transit_speed_kts: float = Field(default=8.0, ge=1.0, le=25.0, description="Speed through water (knots)")


class UKCRequest(BaseModel):
    port_id: str = Field(..., description="Target port ID (e.g. IN-COK)")
    channel_id: Optional[str] = Field(default="main-fairway")
    vessel: VesselDraftSpecs
    passage_timestamp: Optional[str] = None


class OptimalTransitWindow(BaseModel):
    start: str
    end: str


class UKCResponse(BaseModel):
    port_id: str
    charted_depth_m: float
    tidal_height_m: float
    total_water_depth_m: float
    static_draft_m: float
    dynamic_squat_m: float
    safety_reserve_m: float
    net_ukc_m: float
    status: str
    clearance_granted: bool
    minimum_tide_required_m: float
    optimal_transit_window: Optional[OptimalTransitWindow] = None


# ==========================================
# 3. Coastal Authority: SAR Leeway & Search Datum
# ==========================================

class VectorQuantity(BaseModel):
    speed_kts: float = Field(..., ge=0.0)
    direction_deg: float = Field(..., ge=0.0, le=360.0)


class SARDatumRequest(BaseModel):
    incident_time: str
    current_time: str
    last_known_position: GeoPoint
    target_type: str = Field(default="artisanal_skiff_unanchored", description="Target craft category for leeway coefficients")
    surface_current: Optional[VectorQuantity] = None
    surface_wind_10m: Optional[VectorQuantity] = None


class SearchWaypoint(BaseModel):
    leg: int
    lat: float
    lon: float
    heading: float
    distance_nm: float


class SARDatumResponse(BaseModel):
    datum_position: GeoPoint
    drift_distance_nm: float
    drift_course_deg: float
    probable_area_sq_nm: float
    search_pattern_type: str = "EXPANDING_SQUARE"
    recommended_track_spacing_nm: float
    search_waypoints: List[SearchWaypoint]


# ==========================================
# 4. Disaster Management: Storm Surge & Warnings
# ==========================================

class SurgeInundationRequest(BaseModel):
    port_id: str
    cyclone_name: str = "Cyclonic System"
    central_pressure_hpa: float = Field(..., ge=880.0, le=1020.0)
    ambient_pressure_hpa: float = Field(default=1010.0, ge=990.0, le=1030.0)
    max_sustained_wind_kts: float = Field(..., ge=20.0, le=170.0)
    radius_max_wind_km: float = Field(default=35.0, ge=10.0, le=150.0)
    forward_speed_kts: float = Field(default=12.0, ge=2.0, le=40.0)
    landfall_distance_km: float = Field(default=40.0, ge=0.0, le=500.0)


class PortSignalDetail(BaseModel):
    signal_number: int
    signal_name: str
    flag_description: str
    meaning: str


class SurgeInundationResponse(BaseModel):
    port_id: str
    port_warning_signal: PortSignalDetail
    peak_surge_height_m: float
    inundation_penetration_inland_km: float
    threat_level: str
    vulnerable_sectors: List[str]
    common_alerting_protocol_xml: str


# ==========================================
# 5. Geofencing: IMBL & MPA Sanctuary Check
# ==========================================

class GeofenceEvaluationRequest(BaseModel):
    vessel_position: GeoPoint
    vessel_type: str = Field(default="mechanized_trawler")
    heading_deg: float = Field(default=0.0, ge=0.0, le=360.0)
    speed_kts: float = Field(default=5.0, ge=0.0, le=35.0)


class IMBLProximity(BaseModel):
    border_name: str
    distance_nm: float
    time_to_boundary_min: Optional[float] = None
    alert_status: str


class SanctuaryProximity(BaseModel):
    name: str
    inside_boundary: bool
    distance_nm: float
    prohibited_activities: List[str]


class MonsoonBanStatus(BaseModel):
    region: str
    ban_active: bool
    next_ban_window: str


class GeofenceEvaluationResponse(BaseModel):
    nearest_imbl: IMBLProximity
    active_sanctuary: SanctuaryProximity
    monsoon_ban_status: MonsoonBanStatus
    offshore_platform_proximity_nm: Optional[float] = None

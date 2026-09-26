"""
ORCA Maritime Geofencing & Regulatory Compliance Engine
Evaluates proximity to International Maritime Boundary Lines (IMBL),
Marine Protected Areas (MPAs), 500m Offshore Energy Platforms, and Monsoon Bans.
"""
import math
from datetime import datetime, timezone
from typing import List, Tuple
from ..models.personas import (
    GeofenceEvaluationRequest,
    GeofenceEvaluationResponse,
    IMBLProximity,
    SanctuaryProximity,
    MonsoonBanStatus,
    GeoPoint
)

# Key International Maritime Boundary Line (IMBL) segments
IMBL_CATALOG = [
    {
        "name": "India - Sri Lanka IMBL (Palk Strait & Gulf of Mannar)",
        "polyline": [
            (10.08, 79.91), (9.80, 79.75), (9.50, 79.52), (9.10, 79.35), (8.75, 79.20)
        ]
    },
    {
        "name": "India - Pakistan Maritime Boundary (Sir Creek)",
        "polyline": [
            (23.65, 68.10), (23.40, 67.85), (23.10, 67.50)
        ]
    },
    {
        "name": "India - Bangladesh Maritime Boundary (Swatch of No Ground)",
        "polyline": [
            (21.40, 89.20), (20.80, 89.15), (20.20, 89.10)
        ]
    }
]

# Marine Protected Areas & Conservation Sanctuaries
MPA_CATALOG = [
    {
        "name": "Gahirmatha Olive Ridley Turtle Marine Sanctuary",
        "center": (20.72, 87.05),
        "radius_km": 25.0,
        "prohibited": ["mechanized_trawling", "gill_netting", "high_intensity_lighting"]
    },
    {
        "name": "Gulf of Mannar Marine National Park",
        "center": (9.15, 79.15),
        "radius_km": 30.0,
        "prohibited": ["bottom_trawling", "coral_mining", "dynamite_fishing", "anchoring_on_reefs"]
    },
    {
        "name": "Sundarbans Biosphere Marine Core Reserve",
        "center": (21.75, 88.85),
        "radius_km": 40.0,
        "prohibited": ["commercial_trawling", "unlicensed_artisanal_fishing", "chemical_dumping"]
    },
    {
        "name": "Gulf of Kutch Marine National Park",
        "center": (22.45, 69.60),
        "radius_km": 28.0,
        "prohibited": ["commercial_fishing", "dredging", "mangrove_felling"]
    }
]

# Offshore energy platforms (e.g. Mumbai High, KG-D6 Basin)
OFFSHORE_PLATFORMS = [
    {"name": "Mumbai High South Complex", "pos": (19.42, 71.30)},
    {"name": "KG-D6 Deepwater Gas Facility", "pos": (16.35, 82.35)}
]


class GeofenceService:
    """
    Evaluates vessel spatial distance against international boundaries and conservation zones.
    """

    @staticmethod
    def _haversine_nm(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Computes haversine distance in nautical miles (1 nm = 1.852 km)."""
        r_km = 6371.0
        phi1, phi2 = math.radians(lat1), math.radians(lat2)
        dphi = math.radians(lat2 - lat1)
        dlambda = math.radians(lon2 - lon1)
        a = math.sin(dphi / 2.0)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2.0)**2
        c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
        km = r_km * c
        return km / 1.852

    def _min_distance_to_polyline_nm(self, lat: float, lon: float, polyline: List[Tuple[float, float]]) -> float:
        """Finds minimum distance in nautical miles from point to polyline vertices."""
        min_dist = 9999.0
        for p_lat, p_lon in polyline:
            d = self._haversine_nm(lat, lon, p_lat, p_lon)
            if d < min_dist:
                min_dist = d
        return round(min_dist, 2)

    def evaluate_geofence(self, req: GeofenceEvaluationRequest) -> GeofenceEvaluationResponse:
        v_lat = req.vessel_position.lat
        v_lon = req.vessel_position.lon

        # 1. IMBL Proximity Check
        best_imbl_name = IMBL_CATALOG[0]["name"]
        min_imbl_dist = 9999.0

        for imbl in IMBL_CATALOG:
            d = self._min_distance_to_polyline_nm(v_lat, v_lon, imbl["polyline"])
            if d < min_imbl_dist:
                min_imbl_dist = d
                best_imbl_name = imbl["name"]

        # Alert status & ETA to boundary
        if min_imbl_dist <= 1.0:
            imbl_alert = "CRITICAL_IMBL_VIOLATION_IMMINENT"
        elif min_imbl_dist <= 3.0:
            imbl_alert = "WARNING_NEAR_BORDER"
        elif min_imbl_dist <= 6.0:
            imbl_alert = "ADVISORY_BORDER_MONITOR"
        else:
            imbl_alert = "NORMAL_CLEAR_BORDER"

        time_to_boundary = None
        if req.speed_kts > 0.5:
            # Approximate time to boundary in minutes
            time_to_boundary = round((min_imbl_dist / req.speed_kts) * 60.0, 1)

        imbl_proximity = IMBLProximity(
            border_name=best_imbl_name,
            distance_nm=min_imbl_dist,
            time_to_boundary_min=time_to_boundary,
            alert_status=imbl_alert
        )

        # 2. MPA Sanctuary Proximity Check
        active_sanctuary = MPA_CATALOG[0]
        min_mpa_dist_km = 9999.0
        is_inside = False

        for mpa in MPA_CATALOG:
            dist_nm = self._haversine_nm(v_lat, v_lon, mpa["center"][0], mpa["center"][1])
            dist_km = dist_nm * 1.852
            if dist_km < min_mpa_dist_km:
                min_mpa_dist_km = dist_km
                active_sanctuary = mpa
                is_inside = dist_km <= mpa["radius_km"]

        sanctuary_proximity = SanctuaryProximity(
            name=active_sanctuary["name"],
            inside_boundary=is_inside,
            distance_nm=round(min_mpa_dist_km / 1.852, 2),
            prohibited_activities=active_sanctuary["prohibited"]
        )

        # 3. Monsoon Fishing Ban Temporal Evaluation
        # West Coast: Longitude < 77.5; East Coast: Longitude >= 77.5
        is_west = v_lon < 77.5
        region_name = "West Coast (Arabian Sea)" if is_west else "East Coast (Bay of Bengal)"
        now = datetime.now(timezone.utc)
        month = now.month
        day = now.day

        if is_west:
            # June 1 to July 31
            ban_active = (month == 6) or (month == 7)
            ban_window = f"{now.year}-06-01 to {now.year}-07-31"
        else:
            # April 15 to June 14
            ban_active = (month == 5) or (month == 4 and day >= 15) or (month == 6 and day <= 14)
            ban_window = f"{now.year}-04-15 to {now.year}-06-14"

        monsoon_ban = MonsoonBanStatus(
            region=region_name,
            ban_active=ban_active,
            next_ban_window=ban_window
        )

        # 4. Offshore Platform 500m Safety Buffer
        min_platform_dist_nm = 9999.0
        for plat in OFFSHORE_PLATFORMS:
            d_plat = self._haversine_nm(v_lat, v_lon, plat["pos"][0], plat["pos"][1])
            if d_plat < min_platform_dist_nm:
                min_platform_dist_nm = d_plat

        return GeofenceEvaluationResponse(
            nearest_imbl=imbl_proximity,
            active_sanctuary=sanctuary_proximity,
            monsoon_ban_status=monsoon_ban,
            offshore_platform_proximity_nm=round(min_platform_dist_nm, 2)
        )

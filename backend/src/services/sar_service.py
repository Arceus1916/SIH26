"""
ORCA IAMSAR Search & Rescue (SAR) Leeway Drift Service
Computes probabilistic search datum and standard expanding square search patterns
based on International Aeronautical and Maritime Search and Rescue (IAMSAR) guidelines.
"""
import math
from datetime import datetime
from typing import List, Tuple
from ..models.personas import (
    SARDatumRequest,
    SARDatumResponse,
    SearchWaypoint,
    GeoPoint,
    VectorQuantity
)


class SARService:
    """
    Computes leeway drift vectors and generates Coast Guard search geometries.
    """

    # IAMSAR Leeway Coefficients: Leeway speed = slope * WindSpeed + intercept (knots)
    LEEWAY_COEFFICIENTS = {
        "artisanal_skiff_unanchored": {"slope": 0.032, "intercept": 0.15, "divergence_deg": 15.0},
        "life_raft_without_drogue": {"slope": 0.038, "intercept": 0.20, "divergence_deg": 12.0},
        "life_raft_with_drogue": {"slope": 0.022, "intercept": 0.10, "divergence_deg": 8.0},
        "person_in_water": {"slope": 0.015, "intercept": 0.05, "divergence_deg": 5.0},
        "mechanized_trawler_disabled": {"slope": 0.028, "intercept": 0.12, "divergence_deg": 20.0},
    }

    def _parse_elapsed_hours(self, t_start: str, t_current: str) -> float:
        """Computes drift time in hours between incident time and present."""
        try:
            dt1 = datetime.fromisoformat(t_start.replace("Z", "+00:00"))
            dt2 = datetime.fromisoformat(t_current.replace("Z", "+00:00"))
            diff = (dt2 - dt1).total_seconds() / 3600.0
            return max(0.5, diff)
        except Exception:
            return 4.0  # Safe fallback of 4 hours

    def _vector_components(self, speed: float, direction_deg: float) -> Tuple[float, float]:
        """Converts speed and compass direction (oceanographic/towards) to East and North components."""
        rad = math.radians(direction_deg)
        east = speed * math.sin(rad)
        north = speed * math.cos(rad)
        return east, north

    def compute_sar_datum(self, req: SARDatumRequest) -> SARDatumResponse:
        elapsed_hours = self._parse_elapsed_hours(req.incident_time, req.current_time)

        # 1. Total Water Current (TWC)
        current = req.surface_current or VectorQuantity(speed_kts=0.9, direction_deg=65.0)
        twc_e, twc_n = self._vector_components(current.speed_kts, current.direction_deg)

        # 2. Wind Leeway (Downwind vector with leeway speed)
        wind = req.surface_wind_10m or VectorQuantity(speed_kts=15.0, direction_deg=45.0)
        coef = self.LEEWAY_COEFFICIENTS.get(
            req.target_type,
            self.LEEWAY_COEFFICIENTS["artisanal_skiff_unanchored"]
        )

        leeway_speed = coef["slope"] * wind.speed_kts + coef["intercept"]
        # Downwind direction is wind direction + 180°
        downwind_dir = (wind.direction_deg + 180.0) % 360.0
        lw_e, lw_n = self._vector_components(leeway_speed, downwind_dir)

        # 3. Total Drift Vector
        total_ve = twc_e + lw_e
        total_vn = twc_n + lw_n
        total_speed_kts = math.sqrt(total_ve**2 + total_vn**2)
        total_course_deg = (math.degrees(math.atan2(total_ve, total_vn)) + 360.0) % 360.0

        drift_dist_nm = round(total_speed_kts * elapsed_hours, 2)

        # 4. Project Datum Coordinate from LKP
        # 1 degree latitude ~ 60 nautical miles
        # 1 degree longitude ~ 60 * cos(lat) nautical miles
        lkp = req.last_known_position
        cos_lat = math.cos(math.radians(lkp.lat))

        delta_lat = (total_vn * elapsed_hours) / 60.0
        delta_lon = (total_ve * elapsed_hours) / (60.0 * max(0.2, cos_lat))

        datum_lat = round(lkp.lat + delta_lat, 5)
        datum_lon = round(lkp.lon + delta_lon, 5)

        # 5. Probable Search Radius and Area
        # Navigation error (E_nav ~ 1.0 nm), Drift error (E_drift ~ 0.3 * drift_distance)
        e_nav = 1.0
        e_drift = 0.3 * drift_dist_nm
        search_radius_nm = round(1.1 * math.sqrt(e_nav**2 + e_drift**2), 1)
        search_area_sq_nm = round((2.0 * search_radius_nm) ** 2, 1)

        # 6. Generate Standard Expanding Square (SS) Search Pattern
        # S, S, 2S, 2S, 3S, 3S leg multipliers with 90° right turns
        track_spacing_nm = max(0.5, round(search_radius_nm / 3.0, 1))
        waypoints: List[SearchWaypoint] = []

        curr_w_lat = datum_lat
        curr_w_lon = datum_lon
        waypoints.append(
            SearchWaypoint(
                leg=0,
                lat=curr_w_lat,
                lon=curr_w_lon,
                heading=0.0,
                distance_nm=0.0
            )
        )

        headings = [0.0, 90.0, 180.0, 270.0]
        leg_lengths = [1, 1, 2, 2, 3, 3, 4, 4]

        for idx, mult in enumerate(leg_lengths):
            leg_num = idx + 1
            heading = headings[idx % 4]
            leg_dist = mult * track_spacing_nm

            rad_h = math.radians(heading)
            d_north_nm = leg_dist * math.cos(rad_h)
            d_east_nm = leg_dist * math.sin(rad_h)

            curr_w_lat += d_north_nm / 60.0
            curr_w_lon += d_east_nm / (60.0 * max(0.2, math.cos(math.radians(curr_w_lat))))

            waypoints.append(
                SearchWaypoint(
                    leg=leg_num,
                    lat=round(curr_w_lat, 5),
                    lon=round(curr_w_lon, 5),
                    heading=heading,
                    distance_nm=round(leg_dist, 2)
                )
            )

        return SARDatumResponse(
            datum_position=GeoPoint(lat=datum_lat, lon=datum_lon),
            drift_distance_nm=drift_dist_nm,
            drift_course_deg=round(total_course_deg, 1),
            probable_area_sq_nm=search_area_sq_nm,
            search_pattern_type="EXPANDING_SQUARE",
            recommended_track_spacing_nm=track_spacing_nm,
            search_waypoints=waypoints
        )

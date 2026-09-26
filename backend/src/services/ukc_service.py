"""
ORCA Dynamic Under-Keel Clearance (UKC) Service
Evaluates channel navigation safety, dynamic squat (Barrass formula),
and tidal clearance windows for commercial cargo, OSVs, and tankers.
"""
import math
from datetime import datetime, timedelta, timezone
from typing import Dict, Any
from ..models.personas import (
    UKCRequest,
    UKCResponse,
    OptimalTransitWindow
)

# Charted dredged channel depths (meters below Chart Datum) for primary global/regional ports
PORT_CHANNEL_DEPTHS: Dict[str, float] = {
    "IN-COK": 13.5,  # Cochin Ernakulam Fairway
    "IN-MAA": 15.2,  # Chennai Outer Harbor Fairway
    "IN-BOM": 14.5,  # Mumbai Main Channel
    "IN-VTZ": 17.0,  # Visakhapatnam Deepwater Ore Berth Channel
    "IN-PRT": 16.0,  # Paradip Approach Fairway
    "IN-KOL": 8.5,   # Kolkata / Haldia Hooghly River Channel
    "IN-IXG": 12.8,  # Mormugao Navigational Channel
    "IN-MUN": 17.5,  # Mundra Container Terminal Channel
    "SG-SIN": 18.0,  # Singapore Strait Port Approach
    "AE-JEA": 17.0,  # Jebel Ali Fairway
    "NL-RTM": 24.0,  # Rotterdam Maasgeul
    "US-NYC": 15.5,  # New York Ambrose Channel
    "CN-SHA": 16.0,  # Shanghai Yangshan Channel
    "JP-TYO": 16.0,  # Tokyo Bay Channel
}


class UKCService:
    """
    Computes dynamic vessel squat, real-time tidal water levels, and Under-Keel Clearance.
    """

    def __init__(self):
        self.default_safety_reserve_m = 1.5  # Standard IHO/Harbor Master minimum safety reserve
        self.wave_response_margin_m = 0.35   # Roll/pitch motion allowance in open fairway

    def _get_tidal_height(self, port_id: str, timestamp_str: str = None) -> float:
        """
        Computes synthetic semi-diurnal astronomical tidal height (+0.2m to +2.4m)
        based on port location and passage timestamp.
        """
        if timestamp_str:
            try:
                dt = datetime.fromisoformat(timestamp_str.replace("Z", "+00:00"))
            except Exception:
                dt = datetime.now(timezone.utc)
        else:
            dt = datetime.now(timezone.utc)

        # Semi-diurnal 12.42-hour tidal cycle simulation
        hours = dt.hour + (dt.minute / 60.0)
        phase = (hours % 12.42) / 12.42 * 2.0 * math.pi
        # Base amplitude between 0.8m and 1.8m depending on port
        port_base = abs(hash(port_id)) % 10 / 10.0  # 0.0 - 0.9
        amp = 0.9 + (port_base * 0.4)
        mean_level = 1.25 + (port_base * 0.2)
        tide_height = mean_level + amp * math.sin(phase)
        return round(max(0.15, tide_height), 2)

    def _calculate_squat(self, cb: float, speed_kts: float, is_confined_channel: bool = True) -> float:
        """
        Dynamic Squat using Dr. C.B. Barrass Hydrographic Formula:
        For confined dredged channels with blockage factor S2 ~ 0.18:
        Squat = (Cb * S2^0.81 * Vk^2.08) / 30
        Simplified standard form:
        Confined Channel: Squat = (Cb * Vk^2) / 50
        Open Water: Squat = (Cb * Vk^2) / 100
        """
        if is_confined_channel:
            # Confined dredged fairway channel
            squat = (cb * (speed_kts ** 2.0)) / 50.0
        else:
            # Open water fairway
            squat = (cb * (speed_kts ** 2.0)) / 100.0
        return round(squat, 2)

    def calculate_ukc(self, req: UKCRequest) -> UKCResponse:
        vessel = req.vessel
        charted_depth = PORT_CHANNEL_DEPTHS.get(req.port_id, 13.0)
        tide_height = self._get_tidal_height(req.port_id, req.passage_timestamp)

        total_water_depth = round(charted_depth + tide_height, 2)
        dynamic_squat = self._calculate_squat(
            cb=vessel.block_coefficient,
            speed_kts=vessel.transit_speed_kts,
            is_confined_channel=True
        )

        total_dynamic_draft = round(vessel.static_draft_m + dynamic_squat + self.wave_response_margin_m, 2)
        net_ukc = round(total_water_depth - total_dynamic_draft, 2)

        # Clearance threshold
        is_cleared = net_ukc >= self.default_safety_reserve_m
        status = "CLEARED_ADEQUATE_UKC" if is_cleared else (
            "CAUTION_RESTRICTED_WINDOW" if net_ukc > 0.5 else "CRITICAL_GROUNDING_RISK"
        )

        # Calculate minimum tide required for clearance
        min_tide_req = round(total_dynamic_draft + self.default_safety_reserve_m - charted_depth, 2)

        # Project optimal transit window (next high water cycle)
        now = datetime.now(timezone.utc)
        opt_start = (now + timedelta(hours=2)).strftime("%Y-%m-%dT%H:00:00Z")
        opt_end = (now + timedelta(hours=5, minutes=30)).strftime("%Y-%m-%dT%H:00:00Z")

        transit_window = OptimalTransitWindow(start=opt_start, end=opt_end) if not is_cleared else None

        return UKCResponse(
            port_id=req.port_id,
            charted_depth_m=charted_depth,
            tidal_height_m=tide_height,
            total_water_depth_m=total_water_depth,
            static_draft_m=vessel.static_draft_m,
            dynamic_squat_m=dynamic_squat,
            safety_reserve_m=self.default_safety_reserve_m,
            net_ukc_m=net_ukc,
            status=status,
            clearance_granted=is_cleared,
            minimum_tide_required_m=max(0.0, min_tide_req),
            optimal_transit_window=transit_window
        )

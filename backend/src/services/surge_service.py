"""
ORCA Coastal Inundation & Storm Surge Engine
Projects cyclonic water rise, determines official WMO / IMD Port Warning Signals (1 to 11),
and produces Common Alerting Protocol (CAP v1.2) emergency payloads.
"""
import math
from datetime import datetime, timezone
from typing import List, Dict, Any
from ..models.personas import (
    SurgeInundationRequest,
    SurgeInundationResponse,
    PortSignalDetail
)

PORT_SIGNALS_CATALOG = {
    1: PortSignalDetail(
        signal_number=1,
        signal_name="CAUTIONARY_DISTANT",
        flag_description="White flag with black ball",
        meaning="There is a region of squally weather in which a storm may be forming."
    ),
    2: PortSignalDetail(
        signal_number=2,
        signal_name="WARNING_DISTANT",
        flag_description="White flag with red ball",
        meaning="A storm of cyclonic intensity has formed; vessels leaving port may encounter heavy seas."
    ),
    3: PortSignalDetail(
        signal_number=3,
        signal_name="LOCAL_CAUTIONARY",
        flag_description="Red flag with black cross",
        meaning="Port threatened by squally weather; sea state deteriorating rapidly."
    ),
    4: PortSignalDetail(
        signal_number=4,
        signal_name="LOCAL_WARNING",
        flag_description="Square red flag",
        meaning="Port threatened by storm; small craft and fishing vessels must seek sheltered creek moorings immediately."
    ),
    5: PortSignalDetail(
        signal_number=5,
        signal_name="DANGER_LANDFALL_SOUTH",
        flag_description="Red pendant with black ball",
        meaning="Cyclonic storm expected to make landfall south of the port; gale force onshore winds imminent."
    ),
    6: PortSignalDetail(
        signal_number=6,
        signal_name="DANGER_LANDFALL_NORTH",
        flag_description="Red pendant with white cross",
        meaning="Cyclonic storm expected to make landfall north of the port; offshore/squally gales expected."
    ),
    7: PortSignalDetail(
        signal_number=7,
        signal_name="DANGER_CROSSING_OVER_PORT",
        flag_description="Red pendant with black square",
        meaning="Cyclonic storm expected to cross the coast over or very near the port."
    ),
    8: PortSignalDetail(
        signal_number=8,
        signal_name="GREAT_DANGER_LANDFALL_NORTH",
        flag_description="Red flag with black square center above white pennant",
        meaning="Severe / Very Severe Cyclonic Storm crossing coast to the north of port with hurricane-force winds."
    ),
    9: PortSignalDetail(
        signal_number=9,
        signal_name="GREAT_DANGER_LANDFALL_SOUTH",
        flag_description="Red flag with black square center above red pennant",
        meaning="Severe / Very Severe Cyclonic Storm crossing coast to the south of port; catastrophic storm surge expected."
    ),
    10: PortSignalDetail(
        signal_number=10,
        signal_name="GREAT_DANGER_DIRECT_HIT",
        flag_description="Two red flags each with black square center",
        meaning="Super Cyclonic Storm expected to make direct landfall over port; total suspension of port operations."
    ),
    11: PortSignalDetail(
        signal_number=11,
        signal_name="FAILURE_OF_COMMUNICATIONS",
        flag_description="Single red flag with white ball",
        meaning="Communications with meteorological warning center broken down; local harbor master emergency authority enacted."
    ),
}


class SurgeService:
    """
    Computes barometric rise, wind setup, coastal inundation penetration, and warning signals.
    """

    def _determine_port_signal(self, max_wind_kts: float, landfall_dist_km: float) -> PortSignalDetail:
        """Determines official port signal flag based on cyclone intensity and distance."""
        if max_wind_kts >= 90.0 and landfall_dist_km <= 60.0:
            return PORT_SIGNALS_CATALOG[10]
        elif max_wind_kts >= 64.0 and landfall_dist_km <= 80.0:
            return PORT_SIGNALS_CATALOG[8]
        elif max_wind_kts >= 48.0 and landfall_dist_km <= 120.0:
            return PORT_SIGNALS_CATALOG[7]
        elif max_wind_kts >= 34.0 and landfall_dist_km <= 180.0:
            return PORT_SIGNALS_CATALOG[4]
        elif max_wind_kts >= 28.0:
            return PORT_SIGNALS_CATALOG[3]
        else:
            return PORT_SIGNALS_CATALOG[1]

    def project_surge(self, req: SurgeInundationRequest) -> SurgeInundationResponse:
        # 1. Inverted Barometer Effect: ~1 cm rise per 1 hPa drop
        # delta_p in hPa: delta_eta_ib = 0.01 * (ambient - central)
        delta_p = max(0.0, req.ambient_pressure_hpa - req.central_pressure_hpa)
        ib_surge_m = delta_p * 0.01

        # 2. Wind Setup over shallow coastal shelf
        # U in m/s: 1 knot = 0.51444 m/s
        wind_ms = req.max_sustained_wind_kts * 0.51444
        # Empirical shallow water wind setup: eta_w = (k * U^2 * L) / (g * H_avg)
        # Scaled parameter for coastal shelf L=50km, H_avg=20m:
        wind_setup_m = 0.0028 * (wind_ms ** 1.85)

        # 3. Distance decay factor if system is still offshore
        dist_factor = max(0.3, 1.0 - (req.landfall_distance_km / 300.0))

        total_peak_surge = round((ib_surge_m + wind_setup_m) * dist_factor, 2)
        # Astronomical tide allowance (~1.2m mean spring tide)
        total_surge_with_tide = round(total_peak_surge + 1.20, 2)

        # 4. Inundation penetration inland (km) based on flat coastal slope (1:1000 to 1:2000)
        inland_penetration_km = round(total_surge_with_tide * 0.55, 1)

        # 5. Threat Level
        if total_surge_with_tide >= 4.0:
            threat = "RED_CRITICAL_CATASTROPHIC"
        elif total_surge_with_tide >= 2.5:
            threat = "ORANGE_SEVERE"
        elif total_surge_with_tide >= 1.5:
            threat = "YELLOW_MODERATE"
        else:
            threat = "GREEN_MONITORING"

        # 6. Signal Flag
        signal = self._determine_port_signal(req.max_sustained_wind_kts, req.landfall_distance_km)

        # 7. Vulnerable sectors
        vulnerable = [
            f"{req.port_id} Artisanal Fishing Jetty & Beach Landings",
            "Low-Lying Estuary Mangrove Settlements",
            "Coastal Perimeter Highway & Salt Pan Flats",
            "Shallow Creek Mooring Basins"
        ]

        # 8. Standard CAP XML v1.2 Payload
        now_dt = datetime.now(timezone.utc)
        now_iso = now_dt.strftime("%Y-%m-%dT%H:%M:%S+00:00")
        cap_xml = (
            f"<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"
            f"<alert xmlns=\"urn:oasis:names:tc:emergency:cap:1.2\">\n"
            f"  <identifier>ORCA-SURGE-{req.port_id}-{int(now_dt.timestamp())}</identifier>\n"
            f"  <sender>ORCA-Emergency-Engine@amip.marine</sender>\n"
            f"  <sent>{now_iso}</sent>\n"
            f"  <status>Actual</status>\n"
            f"  <msgType>Alert</msgType>\n"
            f"  <scope>Public</scope>\n"
            f"  <info>\n"
            f"    <category>Met</category>\n"
            f"    <event>Coastal Storm Surge & Gale Hazard</event>\n"
            f"    <urgency>Immediate</urgency>\n"
            f"    <severity>{threat}</severity>\n"
            f"    <certainty>Observed</certainty>\n"
            f"    <headline>Port Signal {signal.signal_number} Raised at {req.port_id} for {req.cyclone_name}</headline>\n"
            f"    <description>Projected peak surge {total_surge_with_tide}m with {inland_penetration_km}km inland inundation envelope.</description>\n"
            f"    <instruction>Evacuate all small craft; halt cargo operations; retreat beyond inundation contour.</instruction>\n"
            f"  </info>\n"
            f"</alert>"
        )

        return SurgeInundationResponse(
            port_id=req.port_id,
            port_warning_signal=signal,
            peak_surge_height_m=total_surge_with_tide,
            inundation_penetration_inland_km=inland_penetration_km,
            threat_level=threat,
            vulnerable_sectors=vulnerable,
            common_alerting_protocol_xml=cap_xml
        )

"""AEGIS Physical Climate & Environmental Asset Exposure Engine
Quantifies physical flood, wildfire, hurricane, and heat stress damage probabilities for enterprise assets.
"""
from typing import Dict, Any, List
import numpy as np

class PhysicalClimateRiskEngine:
    HAZARD_BASE_PROBABILITIES = {
        "coastal_flood": 0.035,
        "wildfire": 0.020,
        "severe_convective_storm": 0.080,
        "extreme_heat_downtime": 0.120,
    }

    @classmethod
    def evaluate_facility_exposure(
        cls,
        facility_name: str,
        replacement_asset_value_usd: float,
        is_coastal_hub: bool,
        elevation_meters: float,
        regional_heat_index_days: int,
    ) -> Dict[str, Any]:
        """Calculates Expected Annual Loss (EAL) and Climate Value-at-Risk."""
        flood_prob = cls.HAZARD_BASE_PROBABILITIES["coastal_flood"] * (2.5 if is_coastal_hub and elevation_meters < 5.0 else 0.5)
        storm_prob = cls.HAZARD_BASE_PROBABILITIES["severe_convective_storm"] * (1.5 if is_coastal_hub else 1.0)
        heat_prob = min(0.40, (regional_heat_index_days / 100.0) * cls.HAZARD_BASE_PROBABILITIES["extreme_heat_downtime"])

        # Damage ratios given hazard occurrence
        flood_loss = replacement_asset_value_usd * 0.28 * flood_prob
        storm_loss = replacement_asset_value_usd * 0.12 * storm_prob
        heat_downtime_loss = (replacement_asset_value_usd * 0.02) * heat_prob

        total_eal = flood_loss + storm_loss + heat_downtime_loss
        climate_var_99 = total_eal * 6.5

        return {
            "facility_name": facility_name,
            "asset_value_usd": replacement_asset_value_usd,
            "expected_annual_climate_loss_usd": round(total_eal, 2),
            "climate_value_at_risk_99_usd": round(climate_var_99, 2),
            "eal_intensity_pct": round((total_eal / replacement_asset_value_usd) * 100.0, 3) if replacement_asset_value_usd > 0 else 0.0,
            "climate_vulnerability_tier": "Critical Exposure" if (total_eal / replacement_asset_value_usd) > 0.02 else "Managed Environmental Risk",
        }

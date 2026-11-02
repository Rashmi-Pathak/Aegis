"""AEGIS Multi-Echelon Inventory Optimization (MEIO)
Computes base-stock policies, safety stock pooling across regional distribution centers (DCs).
"""
from typing import List, Dict, Any
import numpy as np
import scipy.stats as stats

class MEIOEngine:
    @staticmethod
    def calculate_pooled_safety_stock(
        independent_dc_demands_std: List[float],
        lead_time_days: float,
        service_level_pct: float = 95.0,
    ) -> Dict[str, Any]:
        """Calculates safety stock savings from centralized inventory risk pooling."""
        z = stats.norm.ppf(service_level_pct / 100.0)

        # Decentralized sum of safety stocks
        decentralized_ss = sum(z * std * np.sqrt(lead_time_days) for std in independent_dc_demands_std)

        # Centralized pooled safety stock (assuming zero correlation)
        pooled_std = np.sqrt(sum(std ** 2 for std in independent_dc_demands_std))
        centralized_ss = z * pooled_std * np.sqrt(lead_time_days)

        savings_units = decentralized_ss - centralized_ss
        savings_pct = (savings_units / decentralized_ss) * 100.0 if decentralized_ss > 0 else 0.0

        return {
            "decentralized_safety_stock_units": round(float(decentralized_ss), 1),
            "centralized_safety_stock_units": round(float(centralized_ss), 1),
            "capital_freed_savings_units": round(float(savings_units), 1),
            "working_capital_reduction_pct": round(float(savings_pct), 1),
            "risk_pooling_benefit": "Significant Capital Efficiency" if savings_pct > 25.0 else "Modest Benefit",
        }

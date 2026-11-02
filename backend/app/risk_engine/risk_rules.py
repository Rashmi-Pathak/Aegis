"""AEGIS Risk Classification & Category Tagging Rules
Maps observed telemetry anomalies into ISO 31000 standard corporate risk buckets.
"""
from typing import Dict, Any, List

class RiskClassificationRules:
    CATEGORY_MAPPING = {
        "fuel_price": "financial",
        "diesel": "financial",
        "freight_rate": "financial",
        "port_dwell": "operational",
        "transit_delay": "operational",
        "driver_turnover": "operational",
        "customer_churn": "strategic",
        "covenant_breach": "regulatory",
        "temperature_drift": "supply_chain",
    }

    @classmethod
    def classify_metric_risk(cls, metric_name: str) -> str:
        """Determines category for anomalous metric."""
        metric_lower = metric_name.lower()
        for k, cat in cls.CATEGORY_MAPPING.items():
            if k in metric_lower:
                return cat
        return "operational"

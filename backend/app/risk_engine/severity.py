"""AEGIS Risk Severity Tier Determination
Categorizes continuous composite scores into standardized critical, high, medium, low tiers.
"""
from typing import Dict, Any

class SeverityClassifier:
    @staticmethod
    def get_tier(risk_score: float) -> str:
        """Assigns categorical severity based on quantitative score."""
        if risk_score >= 75.0:
            return "critical"
        elif risk_score >= 50.0:
            return "high"
        elif risk_score >= 25.0:
            return "medium"
        else:
            return "low"

    @staticmethod
    def get_color_token(severity: str) -> str:
        """Hex color code for dashboard indicators."""
        tokens = {
            "critical": "#FF3B30",
            "high": "#FF6A00",
            "medium": "#FFB15A",
            "low": "#34C759",
        }
        return tokens.get(severity, "#A89D92")

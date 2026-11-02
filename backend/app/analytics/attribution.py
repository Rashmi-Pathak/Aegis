"""AEGIS Markov Chain Multi-Touch Marketing Attribution
Calculates customer conversion attribution weights using Markov graph removal effects.
"""
from typing import List, Dict, Any
import numpy as np

class MarkovAttributionEngine:
    @staticmethod
    def calculate_removal_effects(
        channels: List[str],
        touchpoint_paths: List[List[str]],
        conversions: List[int],
    ) -> Dict[str, Any]:
        """Measures conversion drop when each channel is removed from customer journey."""
        if not channels or not touchpoint_paths:
            return {"channel_weights_pct": {}, "total_conversions": 0}

        total_conversions = sum(conversions)
        removal_effects = {}

        for ch in channels:
            # Baseline without channel ch
            retained_conv = 0
            for path, conv in zip(touchpoint_paths, conversions):
                if ch not in path:
                    retained_conv += conv
            # Removal effect = 1 - (retained / total)
            eff = (total_conversions - retained_conv) / total_conversions if total_conversions > 0 else 0.0
            removal_effects[ch] = max(0.01, eff)

        total_eff = sum(removal_effects.values()) or 1.0
        normalized = {ch: round((val / total_eff) * 100.0, 1) for ch, val in removal_effects.items()}

        return {
            "channel_attribution_weights_pct": normalized,
            "total_observed_conversions": total_conversions,
            "highest_converting_channel": max(normalized, key=normalized.get) if normalized else "None",
        }

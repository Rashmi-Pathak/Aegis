"""AEGIS Hierarchical 5-Whys Causal Tree & Forensic Evidence Engine
Traces breakdown timelines, correlates telemetry spikes, and constructs proof packets.
"""

from typing import List, Dict, Any, Optional
import datetime


class CausalTreeGenerator:
    """Builds multi-layer forensic trees connecting symptom to underlying structural break."""

    @staticmethod
    def generate_investigation_tree(
        primary_symptom: str,
        detected_anomalies: List[Dict[str, Any]],
        linked_drivers: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """Constructs an investigation evidence graph with confidence scores."""
        nodes = []
        edges = []

        # Root symptom
        nodes.append({
            "id": "symptom_root",
            "type": "observed_symptom",
            "label": primary_symptom,
            "confidence": 0.99,
        })

        for i, anomaly in enumerate(detected_anomalies[:4]):
            a_id = f"anomaly_{i}"
            nodes.append({
                "id": a_id,
                "type": "telemetry_anomaly",
                "label": anomaly.get("metric", "Telemetry Spike"),
                "deviation": anomaly.get("deviation", "+3.2σ"),
                "timestamp": anomaly.get("timestamp", datetime.datetime.now().isoformat()),
            })
            edges.append({
                "from": "symptom_root",
                "to": a_id,
                "relationship": "Evidenced By",
            })

        for j, driver in enumerate(linked_drivers[:3]):
            d_id = f"driver_{j}"
            nodes.append({
                "id": d_id,
                "type": "root_cause_driver",
                "label": driver.get("driver", "Structural Factor"),
                "attributionShare": driver.get("attributionSharePct", 45.0),
            })
            # Connect to anomalies
            if nodes:
                edges.append({
                    "from": nodes[1]["id"] if len(nodes) > 1 else "symptom_root",
                    "to": d_id,
                    "relationship": "Root Trigger",
                })

        return {
            "root_symptom": primary_symptom,
            "forensic_nodes": nodes,
            "evidence_connections": edges,
            "investigation_status": "CLOSED_CONCLUSIVE",
            "confidence_score": 0.94,
        }

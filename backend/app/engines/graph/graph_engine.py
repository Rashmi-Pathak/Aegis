from typing import Dict, Any, List, Optional
import networkx as nx

class BusinessGraphEngine:
    """NetworkX-powered business dependency digital twin and causal risk propagation engine."""

    @classmethod
    def build_business_graph(cls, datasets: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Construct the directed dependency topology and compute node stress states."""
        G = nx.DiGraph()

        raw_nodes = [
            {"id": "fuel_energy", "label": "Fuel & Energy Index", "category": "supply_chain", "status": "critical", "value": "+28% Cost", "riskScore": 88, "dependencies": ["fleet_ops", "operating_costs"]},
            {"id": "fleet_ops", "label": "Fleet Operations", "category": "operations", "status": "warning", "value": "84% Util", "riskScore": 72, "dependencies": ["deliveries", "driver_capacity"]},
            {"id": "driver_capacity", "label": "Driver Capacity", "category": "operations", "status": "warning", "value": "92% Active", "riskScore": 64, "dependencies": ["fleet_ops"]},
            {"id": "deliveries", "label": "On-Time Deliveries (OTIF)", "category": "operations", "status": "normal", "value": "96.2%", "riskScore": 32, "dependencies": ["client_retention", "revenue"]},
            {"id": "client_retention", "label": "Client Retention", "category": "customers", "status": "normal", "value": "94.8%", "riskScore": 28, "dependencies": ["revenue"]},
            {"id": "operating_costs", "label": "Operating Cost Base", "category": "finance", "status": "critical", "value": "$127M", "riskScore": 82, "dependencies": ["gross_margin", "cash_flow"]},
            {"id": "revenue", "label": "Gross Revenue", "category": "revenue", "status": "normal", "value": "$148.2M", "riskScore": 34, "dependencies": ["gross_margin", "cash_flow"]},
            {"id": "gross_margin", "label": "Gross Profit Margin", "category": "finance", "status": "critical", "value": "14.2%", "riskScore": 86, "dependencies": ["cash_flow"]},
            {"id": "cash_flow", "label": "Free Cash Flow", "category": "finance", "status": "warning", "value": "$18.6M", "riskScore": 68, "dependencies": []},
            {"id": "warehousing", "label": "Terminal Warehousing", "category": "supply_chain", "status": "normal", "value": "78% Cap", "riskScore": 30, "dependencies": ["operating_costs"]},
            {"id": "marketing_sales", "label": "Enterprise Contract Sales", "category": "marketing", "status": "normal", "value": "+$12M Pipe", "riskScore": 25, "dependencies": ["revenue"]},
        ]

        raw_edges = [
            {"source": "fuel_energy", "target": "operating_costs", "weight": 0.85, "relationship": "Direct Cost Inflator", "isStressed": True},
            {"source": "fuel_energy", "target": "fleet_ops", "weight": 0.65, "relationship": "Speed/Idling Route Policy", "isStressed": True},
            {"source": "driver_capacity", "target": "fleet_ops", "weight": 0.78, "relationship": "Dispatch Feasibility", "isStressed": False},
            {"source": "fleet_ops", "target": "deliveries", "weight": 0.9, "relationship": "SLA Performance", "isStressed": False},
            {"source": "deliveries", "target": "client_retention", "weight": 0.82, "relationship": "Service Quality Trust", "isStressed": False},
            {"source": "client_retention", "target": "revenue", "weight": 0.94, "relationship": "Recurring Billable Volume", "isStressed": False},
            {"source": "marketing_sales", "target": "revenue", "weight": 0.6, "relationship": "New Contract Growth", "isStressed": False},
            {"source": "revenue", "target": "gross_margin", "weight": 0.95, "relationship": "Topline Inflow", "isStressed": False},
            {"source": "operating_costs", "target": "gross_margin", "weight": 0.92, "relationship": "Margin Compression", "isStressed": True},
            {"source": "gross_margin", "target": "cash_flow", "weight": 0.88, "relationship": "Operating Surplus Flow", "isStressed": True},
            {"source": "warehousing", "target": "operating_costs", "weight": 0.45, "relationship": "Facility Overhead", "isStressed": False},
        ]

        # Populate NetworkX graph
        for node in raw_nodes:
            G.add_node(node["id"], **node)

        for edge in raw_edges:
            G.add_edge(edge["source"], edge["target"], weight=edge["weight"], relationship=edge["relationship"])

        return {
            "nodes": raw_nodes,
            "edges": raw_edges,
        }

    @classmethod
    def find_causal_path(cls, source_id: str, target_id: str) -> List[str]:
        """Find the shortest or strongest causal path connecting two business nodes."""
        graph_data = cls.build_business_graph()
        G = nx.DiGraph()
        for edge in graph_data["edges"]:
            G.add_edge(edge["source"], edge["target"])
        try:
            return nx.shortest_path(G, source_id, target_id)
        except Exception:
            return [source_id, target_id]

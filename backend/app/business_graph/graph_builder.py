"""AEGIS Enterprise Business Dependency Digital Twin Graph Builder
Constructs directed dependency graphs in NetworkX linking operations, logistics,
cost centers, customer segments, and financial liquidity.
"""

from typing import Dict, Any, List, Optional
import networkx as nx


class BusinessGraphBuilder:
    """Builds and queries the enterprise structural dependency NetworkX graph."""

    def __init__(self):
        self.graph = nx.DiGraph()

    def add_business_node(
        self,
        node_id: str,
        label: str,
        category: str,
        status: str,
        value: str,
        risk_score: float,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        """Adds an enterprise entity vertex with telemetry attributes."""
        self.graph.add_node(
            node_id,
            id=node_id,
            label=label,
            category=category,
            status=status,
            value=value,
            riskScore=risk_score,
            metadata=metadata or {},
        )

    def add_dependency_edge(
        self,
        source: str,
        target: str,
        relationship: str,
        weight: float = 0.5,
        is_stressed: bool = False,
    ):
        """Adds a directed causal/operational dependency edge."""
        self.graph.add_edge(
            source,
            target,
            relationship=relationship,
            weight=weight,
            isStressed=is_stressed,
        )

    def to_json_dict(self) -> Dict[str, Any]:
        """Serializes NetworkX graph to API-compatible nodes and edges format."""
        nodes = []
        for node_id, data in self.graph.nodes(data=True):
            deps = list(self.graph.successors(node_id))
            nodes.append({
                "id": node_id,
                "label": data.get("label", node_id),
                "category": data.get("category", "general"),
                "status": data.get("status", "normal"),
                "value": data.get("value", ""),
                "riskScore": data.get("riskScore", 0),
                "dependencies": deps,
            })

        edges = []
        for u, v, data in self.graph.edges(data=True):
            edges.append({
                "source": u,
                "target": v,
                "relationship": data.get("relationship", "Impacts"),
                "weight": data.get("weight", 0.5),
                "isStressed": data.get("isStressed", False),
            })

        return {"nodes": nodes, "edges": edges}

    @classmethod
    def create_default_primelogix_digital_twin(cls) -> "BusinessGraphBuilder":
        """Instantiates default canonical logistics enterprise topology."""
        builder = cls()

        nodes = [
            ("fuel_energy", "Diesel Benchmark & Energy Index", "supply_chain", "critical", "+28% Spot Squeeze", 88),
            ("fleet_ops", "Linehaul & Regional Dispatch", "operations", "warning", "84% Utilization", 72),
            ("driver_capacity", "Class-A Driver Retention", "operations", "warning", "91% Active", 64),
            ("port_terminals", "Rotterdam / Long Beach Dwell", "supply_chain", "critical", "6.4d Average Dwell", 85),
            ("deliveries", "On-Time Deliveries (OTIF)", "operations", "normal", "94.8% SLA", 32),
            ("client_retention", "Key Enterprise Retention", "customers", "normal", "95.2%", 28),
            ("operating_costs", "Operating Cost Base (OpEx)", "finance", "critical", "$127.2M Ann.", 82),
            ("revenue", "Gross Operating Revenue", "revenue", "normal", "$148.2M", 34),
            ("gross_margin", "Gross Profit Margin", "finance", "critical", "14.2% (-280 bps)", 86),
            ("cash_flow", "Free Cash Flow (FCF)", "finance", "warning", "$18.5M Reserve", 68),
            ("contract_sales", "Strategic B2B Pipeline", "marketing", "normal", "+$14.5M Pipeline", 25),
        ]

        for n_id, label, cat, stat, val, rsk in nodes:
            builder.add_business_node(n_id, label, cat, stat, val, rsk)

        edges = [
            ("fuel_energy", "operating_costs", "Direct Fuel Expense Inflator", 0.92, True),
            ("fuel_energy", "fleet_ops", "Speed / Idle Route Cost Caps", 0.65, True),
            ("driver_capacity", "fleet_ops", "Dispatch Scheduling Feasibility", 0.78, False),
            ("port_terminals", "fleet_ops", "Drayage Chassis Bottleneck", 0.84, True),
            ("fleet_ops", "deliveries", "Transit Reliability Execution", 0.90, False),
            ("deliveries", "client_retention", "SLA Satisfaction Guarantee", 0.85, False),
            ("client_retention", "revenue", "Recurring Billable Freight Volume", 0.95, False),
            ("contract_sales", "revenue", "New Enterprise Long-Term Contracts", 0.60, False),
            ("revenue", "gross_margin", "Topline Revenue Inflow", 0.95, False),
            ("operating_costs", "gross_margin", "Gross Margin Squeeze", 0.92, True),
            ("gross_margin", "cash_flow", "Operating Surplus Conversion", 0.88, True),
        ]

        for u, v, rel, w, st in edges:
            builder.add_dependency_edge(u, v, rel, w, st)

        return builder

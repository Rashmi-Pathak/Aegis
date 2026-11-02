"""AEGIS Automated Field Semantic Mapper
Uses synonym dictionaries and string distance to map raw heterogeneous CSV columns into canonical fields.
"""
from typing import Dict, List, Optional
import difflib

class SemanticFieldMapper:
    SYNONYM_MAP = {
        "revenue": ["rev", "gross_revenue", "sales", "turnover", "inflow", "amount", "total_sales"],
        "cogs": ["cost_of_goods", "direct_costs", "cost_of_sales", "product_cost"],
        "date": ["timestamp", "txn_date", "order_date", "created_at", "ship_date"],
        "customer_id": ["client_id", "account_id", "cust_id", "buyer_id"],
        "operating_expenses": ["opex", "overhead", "operating_costs", "expenses"],
    }

    @classmethod
    def map_column(cls, raw_col_name: str) -> Optional[str]:
        """Matches a raw column to canonical field name."""
        clean = raw_col_name.lower().strip().replace(" ", "_")
        for canonical, synonyms in cls.SYNONYM_MAP.items():
            if clean == canonical or clean in synonyms:
                return canonical
            matches = difflib.get_close_matches(clean, [canonical] + synonyms, n=1, cutoff=0.82)
            if matches:
                return canonical
        return None

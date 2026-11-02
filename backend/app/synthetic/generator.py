"""AEGIS Synthetic Enterprise Data Generator
Synthesizes high-fidelity multi-domain enterprise datasets for sandbox simulation,
load testing, and risk benchmarking.
"""

from typing import Dict, Any, List, Optional
import datetime
import random
import numpy as np
import pandas as pd


class SyntheticEnterpriseGenerator:
    """Generates synthetic relational enterprise records with controllable failure injections."""

    @staticmethod
    def generate_customers(n_customers: int = 250, seed: int = 42) -> pd.DataFrame:
        """Generates B2B client portfolio with ARR, credit limits, and industry tiers."""
        np.random.seed(seed)
        random.seed(seed)

        tiers = ["Enterprise Tier 1", "Strategic Mid-Market", "Regional Core", "Growth Tier"]
        industries = ["Automotive", "Retail / FMCG", "Pharmaceuticals", "Heavy Industrial", "Aerospace"]

        records = []
        for i in range(1, n_customers + 1):
            tier = random.choices(tiers, weights=[0.1, 0.25, 0.45, 0.2])[0]
            ind = random.choice(industries)
            arr = np.random.lognormal(mean=11.5, sigma=1.0) if tier == "Enterprise Tier 1" else np.random.lognormal(mean=9.5, sigma=0.8)
            payment_terms = random.choice([30, 45, 60, 90])

            records.append({
                "customer_id": f"CUST-{i:05d}",
                "company_name": f"{ind} Corp {i}",
                "industry": ind,
                "tier": tier,
                "annual_contract_value": round(float(arr), 2),
                "credit_limit": round(float(arr * 0.25), 2),
                "payment_terms_days": payment_terms,
                "is_active": True,
            })

        return pd.DataFrame(records)

    @staticmethod
    def generate_freight_shipments(
        n_shipments: int = 1500,
        start_date: str = "2025-01-01",
        days: int = 180,
        inject_port_congestion: bool = True,
        seed: int = 42,
    ) -> pd.DataFrame:
        """Generates logistics freight shipments with dwell times, routes, and delay telemetry."""
        np.random.seed(seed)
        random.seed(seed)

        start = pd.to_datetime(start_date)
        lanes = [
            ("Rotterdam", "Frankfurt", 420),
            ("Long Beach", "Chicago", 2050),
            ("Shanghai", "Los Angeles", 5800),
            ("Antwerp", "Munich", 580),
            ("Savannah", "Atlanta", 250),
        ]

        records = []
        for i in range(1, n_shipments + 1):
            offset_days = random.randint(0, days)
            ship_date = start + pd.Timedelta(days=offset_days)
            origin, dest, dist_miles = random.choice(lanes)

            base_transit_days = dist_miles / 500.0
            actual_transit_days = np.random.normal(loc=base_transit_days, scale=0.5)

            # Injected Port Congestion shock after day 100
            dwell_hours = np.random.exponential(scale=18.0)
            if inject_port_congestion and offset_days > 90 and origin in ["Rotterdam", "Long Beach"]:
                dwell_hours += np.random.gamma(shape=4.0, scale=12.0)
                actual_transit_days += np.random.uniform(2.0, 5.0)

            is_delayed = bool(actual_transit_days > (base_transit_days * 1.25))

            records.append({
                "shipment_id": f"SHP-{i:06d}",
                "dispatch_date": ship_date.strftime("%Y-%m-%d"),
                "origin_hub": origin,
                "destination_hub": dest,
                "distance_miles": dist_miles,
                "scheduled_days": round(base_transit_days, 1),
                "actual_days": round(float(max(1.0, actual_transit_days)), 1),
                "terminal_dwell_hours": round(float(dwell_hours), 1),
                "freight_rate_usd": round(dist_miles * np.random.uniform(2.1, 3.8), 2),
                "is_delayed": is_delayed,
                "status": "Delivered",
            })

        return pd.DataFrame(records)

"""AEGIS Multi-Industry Enterprise Dataset Synthesizer
Synthesizes comprehensive multi-table schema datasets (Transactions, Operations,
Sensors, Customers, Ledger, Inventory) for 15 heterogeneous corporate verticals.
"""

from typing import Dict, Any, List, Tuple
import datetime
import random
import numpy as np
import pandas as pd


class EnterpriseScenarioSynthesizer:
    """Generates synthetic relational enterprise tables for each canonical business vertical."""

    INDUSTRIES = [
        ("primelogix", "Freight & Global Logistics", "shipments", "fuel", "customers"),
        ("cloudscale_saas", "B2B Enterprise Software", "subscriptions", "usage", "accounts"),
        ("apex_retail", "Omni-Channel Retail", "transactions", "inventory", "stores"),
        ("vanguard_health", "Hospital & MedTech Systems", "admissions", "equipment", "patients"),
        ("aerodyne_manufacturing", "Aerospace & Precision Manufacturing", "work_orders", "sensors", "suppliers"),
        ("solaris_energy", "Renewable Energy & Power Grid", "generation", "turbines", "distribution"),
        ("apex_fintech", "Commercial Lending & FinTech", "loans", "repayments", "borrowers"),
        ("biovita_pharma", "Cold-Chain Pharmaceuticals", "batches", "temperature_telemetry", "distributors"),
        ("titan_heavy", "Heavy Industrial & Machinery", "deployments", "maintenance", "clients"),
        ("horizon_telecom", "Cellular & Fiber Infrastructure", "towers", "traffic", "subscribers"),
        ("veritas_automotive", "Tier-1 Automotive OEM", "assembly", "defect_telemetry", "parts"),
        ("agripure_foods", "Cold-Chain Agriculture & Food", "harvests", "processing", "logistics"),
        ("pinnacle_epc", "Infrastructure Construction & EPC", "projects", "materials", "contractors"),
        ("nexus_media", "Streaming & Digital Media Network", "content", "bandwidth", "subscribers"),
        ("summit_hospitality", "Fleet Fleet Leasing & Rentals", "leases", "vehicle_telemetry", "corporate_clients"),
    ]

    @classmethod
    def generate_industry_tables(
        cls,
        industry_slug: str,
        n_records: int = 500,
        seed: int = 42,
    ) -> Dict[str, pd.DataFrame]:
        """Generates primary operational, financial, and master tables for the given industry."""
        np.random.seed(seed)
        random.seed(seed)

        start_date = pd.to_datetime("2025-01-01")
        dates = [start_date + pd.Timedelta(days=int(i)) for i in np.random.uniform(0, 365, n_records)]

        # 1. Master Customers / Accounts table
        customers_df = pd.DataFrame({
            "account_id": [f"ACC-{i:05d}" for i in range(1, 101)],
            "company_name": [f"Enterprise Client {i}" for i in range(1, 101)],
            "contract_tier": random.choices(["Platinum", "Gold", "Silver"], weights=[0.2, 0.4, 0.4], k=100),
            "annual_contract_value": [round(float(x), 2) for x in np.random.lognormal(11.0, 0.8, 100)],
            "credit_score": np.random.randint(620, 850, 100),
            "region": random.choices(["North America", "EMEA", "APAC", "LATAM"], k=100),
        })

        # 2. Primary Transactional / Operational Ledger table
        assigned_accounts = random.choices(customers_df["account_id"].tolist(), k=n_records)
        base_amounts = np.random.lognormal(9.0, 1.2, n_records)
        operating_costs = base_amounts * np.random.uniform(0.65, 0.92, n_records)

        ledger_df = pd.DataFrame({
            "transaction_id": [f"TXN-{i:07d}" for i in range(1, n_records + 1)],
            "date": [d.strftime("%Y-%m-%d") for d in dates],
            "account_id": assigned_accounts,
            "gross_revenue": [round(float(a), 2) for a in base_amounts],
            "operating_cost": [round(float(c), 2) for c in operating_costs],
            "gross_profit": [round(float(a - c), 2) for a, c in zip(base_amounts, operating_costs)],
            "status": random.choices(["Settled", "Pending", "Audited"], weights=[0.85, 0.12, 0.03], k=n_records),
        })

        # 3. Operations / Sensor / Telemetry table
        operational_df = pd.DataFrame({
            "event_id": [f"EVT-{i:07d}" for i in range(1, n_records + 1)],
            "timestamp": [(d + pd.Timedelta(hours=random.randint(0, 23))).isoformat() for d in dates],
            "asset_id": [f"AST-{random.randint(100, 150)}" for _ in range(n_records)],
            "temperature_celsius": np.random.normal(loc=22.0, scale=3.5, size=n_records).round(1),
            "pressure_psi": np.random.normal(loc=120.0, scale=8.0, size=n_records).round(1),
            "utilization_pct": np.random.uniform(40.0, 98.0, n_records).round(1),
            "anomaly_flag": random.choices([False, True], weights=[0.96, 0.04], k=n_records),
        })

        return {
            "customers": customers_df,
            "ledger": ledger_df,
            "telemetry": operational_df,
        }

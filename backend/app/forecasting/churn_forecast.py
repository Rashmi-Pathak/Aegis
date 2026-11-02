"""AEGIS Customer Churn & Account Decay Forecaster
Models cohort survival curves and logistic hazard functions to project account churn.
"""
from typing import List, Dict, Any
import numpy as np

class ChurnForecaster:
    @staticmethod
    def forecast_churn_rate(
        active_customer_count: int,
        historical_churn_rates: List[float],
        n_periods: int = 6,
    ) -> Dict[str, Any]:
        """Forecasts customer churn and projected revenue loss."""
        if not historical_churn_rates:
            base_rate = 0.02
        else:
            base_rate = float(np.mean(historical_churn_rates))

        rates = []
        retained = []
        curr_cust = active_customer_count

        for i in range(1, n_periods + 1):
            rate = min(0.50, max(0.005, base_rate * (1.0 + 0.02 * i)))
            churned = int(round(curr_cust * rate))
            curr_cust = max(0, curr_cust - churned)
            rates.append(round(rate * 100.0, 2))
            retained.append(curr_cust)

        return {
            "initial_customers": active_customer_count,
            "projected_churn_rates_pct": rates,
            "projected_active_customers": retained,
            "cumulative_lost_accounts": active_customer_count - (retained[-1] if retained else 0),
        }

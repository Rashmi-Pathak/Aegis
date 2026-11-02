"""AEGIS Advanced Intelligence Tier:
Earned Value Management (EVM), Credit Transition Matrices, Theta Method,
Wavelet Multi-Resolution, Multi-Armed Bandits, Real Options Valuation (Binomial Lattice),
Basel IV RWA Capital, and Generalized Extreme Value (GEV) Tail Risk.
"""

import os

FILES = {
    "backend/app/analytics/earned_value_management.py": '''"""AEGIS Earned Value Management (EVM) Project Health Engine
Computes PV, EV, AC, Cost Variance (CV), Schedule Variance (SV), CPI, SPI, and Estimate at Completion (EAC).
"""
from typing import Dict, Any, List

class EVMAnalysisEngine:
    @staticmethod
    def compute_evm_metrics(
        planned_value_pv: float,
        earned_value_ev: float,
        actual_cost_ac: float,
        budget_at_completion_bac: float,
    ) -> Dict[str, Any]:
        """Calculates standard ANSI/EIA-748 Earned Value Management indices."""
        cost_variance = earned_value_ev - actual_cost_ac
        schedule_variance = earned_value_ev - planned_value_pv

        cpi = round(earned_value_ev / actual_cost_ac, 3) if actual_cost_ac > 0 else 1.0
        spi = round(earned_value_ev / planned_value_pv, 3) if planned_value_pv > 0 else 1.0

        # Estimate At Completion (EAC) assuming current cost efficiency continues
        eac = round(budget_at_completion_bac / cpi, 2) if cpi > 0 else budget_at_completion_bac
        variance_at_completion = round(budget_at_completion_bac - eac, 2)

        # To Complete Performance Index (TCPI) to stay within budget
        remaining_work = budget_at_completion_bac - earned_value_ev
        remaining_funds = budget_at_completion_bac - actual_cost_ac
        tcpi = round(remaining_work / remaining_funds, 3) if remaining_funds > 0 else 999.0

        health = "On Track"
        if cpi < 0.85 or spi < 0.85:
            health = "Critical Project Distress (Severe Overrun/Delay)"
        elif cpi < 0.95 or spi < 0.95:
            health = "Warning: Sub-Optimal Efficiency"

        return {
            "planned_value_pv": planned_value_pv,
            "earned_value_ev": earned_value_ev,
            "actual_cost_ac": actual_cost_ac,
            "budget_at_completion_bac": budget_at_completion_bac,
            "cost_variance_cv": round(cost_variance, 2),
            "schedule_variance_sv": round(schedule_variance, 2),
            "cost_performance_index_cpi": cpi,
            "schedule_performance_index_spi": spi,
            "estimate_at_completion_eac": eac,
            "variance_at_completion_vac": variance_at_completion,
            "to_complete_performance_index_tcpi": tcpi,
            "project_health_status": health,
        }
''',
    "backend/app/analytics/credit_transition_matrix.py": '''"""AEGIS Credit Rating Migration & Absorbing Markov Default Chain
Models corporate rating migration probabilities across AAA through Default (D).
"""
from typing import List, Dict, Any
import numpy as np

class CreditTransitionMatrixEngine:
    RATINGS = ["AAA", "AA", "A", "BBB", "BB", "B", "CCC", "Default"]

    DEFAULT_1Y_TRANSITION = np.array([
        [0.908, 0.083, 0.007, 0.001, 0.001, 0.000, 0.000, 0.000],  # AAA
        [0.006, 0.914, 0.073, 0.005, 0.001, 0.001, 0.000, 0.000],  # AA
        [0.001, 0.021, 0.912, 0.058, 0.005, 0.002, 0.001, 0.000],  # A
        [0.000, 0.002, 0.041, 0.893, 0.048, 0.010, 0.004, 0.002],  # BBB
        [0.000, 0.001, 0.004, 0.063, 0.832, 0.076, 0.014, 0.010],  # BB
        [0.000, 0.001, 0.001, 0.004, 0.068, 0.824, 0.058, 0.044],  # B
        [0.000, 0.000, 0.001, 0.003, 0.015, 0.118, 0.638, 0.225],  # CCC
        [0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 1.000],  # Default (Absorbing)
    ])

    @classmethod
    def project_n_year_default_probability(
        cls,
        initial_rating: str,
        n_years: int = 3,
    ) -> Dict[str, Any]:
        """Calculates multi-year rating distribution by powering Markov matrix P^n."""
        if initial_rating not in cls.RATINGS:
            initial_rating = "BBB"

        r_idx = cls.RATINGS.index(initial_rating)

        # Matrix power
        p_n = np.linalg.matrix_power(cls.DEFAULT_1Y_TRANSITION, n_years)
        distribution = p_n[r_idx, :]

        return {
            "initial_rating": initial_rating,
            "projection_horizon_years": n_years,
            "cumulative_default_probability_pct": round(float(distribution[-1]) * 100.0, 3),
            "projected_rating_probabilities": {
                cls.RATINGS[i]: round(float(distribution[i]) * 100.0, 2)
                for i in range(len(cls.RATINGS))
            },
        }
''',
    "backend/app/forecasting/theta_method_forecaster.py": '''"""AEGIS Theta Forecasting Method (Assimakopoulos & Nikolopoulos)
Decomposes time series into Theta lines: linear long-term trend (Theta=0) and short-term curvature (Theta=2).
"""
from typing import List, Dict, Any
import numpy as np

class ThetaForecaster:
    @staticmethod
    def forecast_theta(
        series: List[float],
        horizon: int = 4,
    ) -> Dict[str, Any]:
        """Forecasts via linear regression trend line and seasonal mean reversion."""
        arr = np.array(series, dtype=float)
        n = len(arr)

        if n < 4:
            last = arr[-1] if n > 0 else 100.0
            return {"forecast": [last] * horizon}

        # Linear trend: Theta=0
        t = np.arange(n)
        slope, intercept = np.polyfit(t, arr, 1)

        # Project trend
        future_t = np.arange(n, n + horizon)
        trend_forecast = intercept + (slope * future_t)

        # Simple exponential smoothing on residuals: Theta=2
        residuals = arr - (intercept + slope * t)
        last_residual = float(residuals[-1])

        # Combine with 0.5 weights (standard Theta formulation)
        forecast = [round(float(trend_forecast[i] + 0.5 * last_residual * (0.8 ** (i + 1))), 2) for i in range(horizon)]

        return {
            "forecast": forecast,
            "linear_slope": round(float(slope), 3),
            "last_residual": round(last_residual, 2),
        }
''',
    "backend/app/decision_engine/multi_armed_bandit.py": '''"""AEGIS Contextual & Multi-Armed Bandit Dynamic Mitigation Engine
Balances Exploration and Exploitation across competing mitigation policies using Upper Confidence Bound (UCB1).
"""
from typing import List, Dict, Any
import numpy as np

class MultiArmedBanditEngine:
    @staticmethod
    def select_action_ucb1(
        action_names: List[str],
        action_pulls: List[int],
        action_rewards: List[float],
        exploration_constant_c: float = 1.414,
    ) -> Dict[str, Any]:
        """Selects optimal mitigation action via UCB1 index: Q(a) + c * sqrt(ln(N) / N_a)."""
        total_pulls = sum(action_pulls)

        # If any arm has 0 pulls, explore it immediately
        for i, pulls in enumerate(action_pulls):
            if pulls == 0:
                return {
                    "selected_action": action_names[i],
                    "reason": "Pure Exploration (Untested Mitigation Lever)",
                    "ucb_scores": {action_names[k]: float("inf") if action_pulls[k] == 0 else 0.0 for k in range(len(action_names))},
                }

        ucb_values = []
        for i in range(len(action_names)):
            avg_reward = action_rewards[i] / action_pulls[i]
            exploration_bonus = exploration_constant_c * np.sqrt(np.log(total_pulls) / action_pulls[i])
            ucb_values.append(avg_reward + exploration_bonus)

        best_idx = int(np.argmax(ucb_values))

        return {
            "selected_action": action_names[best_idx],
            "highest_ucb_index": round(float(ucb_values[best_idx]), 3),
            "ucb_scores": {action_names[i]: round(float(ucb_values[i]), 3) for i in range(len(action_names))},
            "reason": "Exploitation / Uncertainty Bound Maximization",
        }
''',
    "backend/app/decision_engine/real_options_valuation.py": '''"""AEGIS Real Options Valuation & Binomial Lattice Engine
Values strategic flexibility: Option to Expand, Option to Defer, Option to Abandon capital projects.
"""
from typing import Dict, Any, List
import numpy as np

class RealOptionsBinomialLattice:
    @staticmethod
    def price_expansion_option(
        underlying_asset_value_S: float,
        expansion_capital_cost_K: float,
        volatility_sigma: float = 0.25,
        risk_free_rate_r: float = 0.05,
        time_to_expiry_years_T: float = 2.0,
        lattice_steps_N: int = 4,
    ) -> Dict[str, Any]:
        """Cox, Ross, Rubinstein (CRR) binomial lattice option pricing."""
        dt = time_to_expiry_years_T / lattice_steps_N
        u = np.exp(volatility_sigma * np.sqrt(dt))
        d = 1.0 / u
        p = (np.exp(risk_free_rate_r * dt) - d) / (u - d)

        # Asset tree at maturity
        asset_values = np.zeros(lattice_steps_N + 1)
        option_values = np.zeros(lattice_steps_N + 1)

        for j in range(lattice_steps_N + 1):
            s_t = underlying_asset_value_S * (u ** (lattice_steps_N - j)) * (d ** j)
            asset_values[j] = s_t
            option_values[j] = max(0.0, s_t - expansion_capital_cost_K)

        # Backward rollback
        disc = np.exp(-risk_free_rate_r * dt)
        for step in range(lattice_steps_N - 1, -1, -1):
            for j in range(step + 1):
                option_values[j] = disc * (p * option_values[j] + (1.0 - p) * option_values[j + 1])

        real_option_val = float(option_values[0])
        expanded_npv = (underlying_asset_value_S - expansion_capital_cost_K) + real_option_val

        return {
            "underlying_project_value": underlying_asset_value_S,
            "strike_capital_cost": expansion_capital_cost_K,
            "real_option_value": round(real_option_val, 2),
            "expanded_strategic_npv": round(expanded_npv, 2),
            "up_factor": round(float(u), 3),
            "down_factor": round(float(d), 3),
            "recommendation": "Maintain Strategic Growth Option" if real_option_val > 0 else "Abandon Expansion",
        }
''',
    "backend/app/risk_engine/regulatory_basel_iv_rwa.py": '''"""AEGIS Basel IV Regulatory Capital & Risk-Weighted Assets (RWA) Engine
Calculates Standardized Approach Risk-Weighted Assets (RWA) and Tier 1 Minimum Capital.
"""
from typing import Dict, Any, List

class BaselIVCapitalEngine:
    RISK_WEIGHTS_BY_RATING = {
        "AAA": 0.20,
        "AA": 0.20,
        "A": 0.50,
        "BBB": 0.75,
        "BB": 1.00,
        "B": 1.50,
        "Unrated": 1.00,
    }

    @classmethod
    def calculate_capital_requirement(
        cls,
        credit_exposures: List[Dict[str, Any]],  # exposure_amount, rating
        operational_loss_historical_mean: float = 2000000.0,
        tier1_capital_target_pct: float = 10.5,
    ) -> Dict[str, Any]:
        """Calculates Credit RWA, Operational RWA, and Required Regulatory Equity Cushion."""
        credit_rwa = 0.0
        for exp in credit_exposures:
            amt = exp.get("exposure_amount", 0.0)
            rating = exp.get("rating", "BBB")
            weight = cls.RISK_WEIGHTS_BY_RATING.get(rating, 1.00)
            credit_rwa += amt * weight

        # Basel SMA Operational Risk RWA approximation (12.5 * Business Indicator Component)
        operational_rwa = operational_loss_historical_mean * 12.5
        total_rwa = credit_rwa + operational_rwa

        required_capital = total_rwa * (tier1_capital_target_pct / 100.0)

        return {
            "credit_rwa_usd": round(credit_rwa, 2),
            "operational_rwa_usd": round(operational_rwa, 2),
            "total_risk_weighted_assets_usd": round(total_rwa, 2),
            "minimum_tier1_capital_required_usd": round(required_capital, 2),
            "target_capital_ratio_pct": tier1_capital_target_pct,
        }
''',
    "backend/app/risk_engine/black_swan_extreme_value.py": '''"""AEGIS Extreme Value Theory (EVT) & Tail Risk Engine
Fits Generalized Pareto Distribution (GPD) over high thresholds to model extreme fat-tailed Black Swan losses.
"""
from typing import Dict, Any, List
import numpy as np

class ExtremeValueTheoryEngine:
    @staticmethod
    def peaks_over_threshold_gpd(
        losses: List[float],
        threshold_quantile: float = 0.90,
    ) -> Dict[str, Any]:
        """Calculates GPD tail parameters (shape xi, scale beta) for losses exceeding threshold u."""
        arr = np.array(losses, dtype=float)
        u = float(np.percentile(arr, threshold_quantile * 100.0))
        exceedances = arr[arr > u] - u

        if len(exceedances) < 5:
            return {"threshold_u": u, "tail_shape_xi": 0.0, "status": "Insufficient Tail Sample"}

        # Method of Moments GPD estimator
        mean_excess = float(np.mean(exceedances))
        var_excess = float(np.var(exceedances))

        if var_excess > 0:
            xi = 0.5 * (1.0 - ((mean_excess ** 2) / var_excess))
            sigma = 0.5 * mean_excess * (((mean_excess ** 2) / var_excess) + 1.0)
        else:
            xi, sigma = 0.0, mean_excess

        # 99.9% 1-in-1000 year catastrophic Black Swan loss
        n_total = len(arr)
        n_exceed = len(exceedances)
        p_target = 0.999

        if xi != 0:
            black_swan_val = u + (sigma / xi) * ((((n_total / n_exceed) * (1.0 - p_target)) ** (-xi)) - 1.0)
        else:
            black_swan_val = u - sigma * np.log((n_total / n_exceed) * (1.0 - p_target))

        return {
            "threshold_u": round(u, 2),
            "tail_shape_parameter_xi": round(float(xi), 3),
            "tail_scale_parameter_sigma": round(float(sigma), 2),
            "black_swan_loss_p999_usd": round(float(black_swan_val), 2),
            "tail_classification": "Heavy Fat-Tailed (Fréchet Domain)" if xi > 0 else "Thin-Tailed (Gumbel)",
        }
''',
    "backend/tests/test_advanced_intelligence_tier.py": '''"""AEGIS Advanced Intelligence Tier Test Suite."""
import pytest
from app.analytics.earned_value_management import EVMAnalysisEngine
from app.analytics.credit_transition_matrix import CreditTransitionMatrixEngine
from app.forecasting.theta_method_forecaster import ThetaForecaster
from app.decision_engine.multi_armed_bandit import MultiArmedBanditEngine
from app.decision_engine.real_options_valuation import RealOptionsBinomialLattice
from app.risk_engine.regulatory_basel_iv_rwa import BaselIVCapitalEngine
from app.risk_engine.black_swan_extreme_value import ExtremeValueTheoryEngine

def test_evm_metrics():
    res = EVMAnalysisEngine.compute_evm_metrics(
        planned_value_pv=1000000.0,
        earned_value_ev=900000.0,
        actual_cost_ac=950000.0,
        budget_at_completion_bac=5000000.0,
    )
    assert res["cost_performance_index_cpi"] < 1.0
    assert res["schedule_performance_index_spi"] < 1.0
    assert res["estimate_at_completion_eac"] > 5000000.0

def test_credit_transition():
    res = CreditTransitionMatrixEngine.project_n_year_default_probability("BBB", n_years=3)
    assert res["cumulative_default_probability_pct"] > 0
    assert "Default" in res["projected_rating_probabilities"]

def test_theta_forecaster():
    series = [100.0, 102.0, 105.0, 108.0, 112.0]
    res = ThetaForecaster.forecast_theta(series, horizon=3)
    assert len(res["forecast"]) == 3
    assert res["linear_slope"] > 0

def test_bandit_ucb1():
    names = ["Action A", "Action B"]
    pulls = [10, 10]
    rewards = [25.0, 80.0]  # Action B has much higher reward
    res = MultiArmedBanditEngine.select_action_ucb1(names, pulls, rewards)
    assert res["selected_action"] == "Action B"

def test_real_options_crr():
    res = RealOptionsBinomialLattice.price_expansion_option(
        underlying_asset_value_S=10000000.0,
        expansion_capital_cost_K=8000000.0,
    )
    assert res["real_option_value"] > 0
    assert res["expanded_strategic_npv"] > 2000000.0

def test_basel_iv_rwa():
    exposures = [
        {"exposure_amount": 10000000.0, "rating": "AAA"},
        {"exposure_amount": 20000000.0, "rating": "BBB"},
    ]
    res = BaselIVCapitalEngine.calculate_capital_requirement(exposures)
    assert res["total_risk_weighted_assets_usd"] > 0
    assert res["minimum_tier1_capital_required_usd"] > 0

def test_extreme_value_theory():
    losses = list(range(10, 100)) + [250.0, 480.0, 950.0]
    res = ExtremeValueTheoryEngine.peaks_over_threshold_gpd(losses)
    assert res["black_swan_loss_p999_usd"] > 100.0
'''
}

for path, code in FILES.items():
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(code)
    print(f"Wrote {path}")

print("Advanced intelligence tier generated successfully.")

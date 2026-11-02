"""AEGIS Vector Autoregression (VAR) Multivariate Forecaster
Fits simultaneous interdependent econometric equations linking Macro, Fuel, and Volume.
y_t = c + A_1 * y_{t-1} + ... + A_p * y_{t-p} + e_t
"""
from typing import Dict, Any, List
import numpy as np

class VectorAutoregressionForecaster:
    @staticmethod
    def forecast_multivariate_system(
        variables: List[str],
        data_matrix: List[List[float]],  # T x K matrix
        horizon_steps: int = 4,
    ) -> Dict[str, Any]:
        """Fits VAR(1) system and projects multi-variate trajectory."""
        Y = np.array(data_matrix, dtype=float)
        T, K = Y.shape

        if T < 6 or K < 2:
            return {"variables": variables, "forecasts": {v: [] for v in variables}}

        # Standard VAR(1) Ordinary Least Squares
        Y_target = Y[1:, :]
        X_lag = np.column_stack([np.ones(T - 1), Y[:-1, :]])

        # Solve (X'X)^-1 X'Y
        beta = np.linalg.pinv(X_lag.T @ X_lag) @ (X_lag.T @ Y_target)
        c = beta[0, :]
        A1 = beta[1:, :].T

        curr = Y[-1, :]
        trajectory = []

        for _ in range(horizon_steps):
            next_step = c + (A1 @ curr)
            trajectory.append([round(float(x), 2) for x in next_step])
            curr = next_step

        res_dict = {}
        for k_idx, var_name in enumerate(variables):
            res_dict[var_name] = [step[k_idx] for step in trajectory]

        return {
            "variables": variables,
            "forecast_horizon_steps": horizon_steps,
            "forecasts_by_variable": res_dict,
            "var_coefficients_matrix": [[round(float(val), 3) for val in row] for row in A1],
        }

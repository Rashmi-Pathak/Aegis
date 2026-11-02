"""AEGIS State-Space Local Linear Trend & Kalman Filtering
Separates true underlying business trajectory from high-frequency observation noise.
x_{t} = F * x_{t-1} + w_t
y_{t} = H * x_{t} + v_t
"""
from typing import List, Dict, Any, Tuple
import numpy as np

class KalmanFilterForecaster:
    @staticmethod
    def filter_and_forecast(
        observations: List[float],
        process_variance_q: float = 0.5,
        observation_variance_r: float = 2.0,
        horizon_steps: int = 5,
    ) -> Dict[str, Any]:
        """Executes 1D Kalman filter and projects forward trajectory."""
        if not observations:
            return {"filtered_states": [], "forecast": []}

        # Initial state estimates: [level, trend]
        x = np.array([observations[0], 0.0])
        P = np.eye(2) * 5.0

        F = np.array([[1.0, 1.0], [0.0, 1.0]])  # State transition matrix
        H = np.array([[1.0, 0.0]])             # Measurement matrix
        Q = np.eye(2) * process_variance_q
        R = np.array([[observation_variance_r]])

        filtered_levels = []

        for z in observations:
            # 1. Predict step
            x_pred = F @ x
            P_pred = F @ P @ F.T + Q

            # 2. Update step
            y_innov = z - (H @ x_pred)
            S = H @ P_pred @ H.T + R
            K = P_pred @ H.T @ np.linalg.inv(S)

            x = x_pred + K @ y_innov
            P = (np.eye(2) - K @ H) @ P_pred

            filtered_levels.append(round(float(x[0]), 2))

        # 3. Forecast future steps
        forecast = []
        curr_x = x.copy()
        for _ in range(horizon_steps):
            curr_x = F @ curr_x
            forecast.append(round(float(curr_x[0]), 2))

        return {
            "filtered_historical_levels": filtered_levels,
            "final_estimated_level": round(float(x[0]), 2),
            "final_estimated_trend": round(float(x[1]), 3),
            "forecast": forecast,
        }

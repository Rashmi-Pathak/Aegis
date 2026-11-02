"""AEGIS Machine Learning Autoregressive Forecaster
Engineers lag features, rolling statistics, and fits gradient boosted models
for multi-horizon demand and revenue predictions.
"""

from typing import List, Dict, Any, Optional
import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor


class MLForecaster:
    """Feature engineering & tree-based regression for tabular time series."""

    @classmethod
    def create_lag_features(
        cls,
        series: List[float],
        lags: List[int] = [1, 2, 3, 6],
        windows: List[int] = [3, 6],
    ) -> pd.DataFrame:
        """Transforms a univariate sequence into supervised feature matrix."""
        df = pd.DataFrame({"target": series})
        for lag in lags:
            df[f"lag_{lag}"] = df["target"].shift(lag)

        for w in windows:
            df[f"rolling_mean_{w}"] = df["target"].shift(1).rolling(w).mean()
            df[f"rolling_std_{w}"] = df["target"].shift(1).rolling(w).std()

        return df.dropna()

    @classmethod
    def forecast(
        cls,
        historical_series: List[float],
        horizon: int = 6,
    ) -> Dict[str, Any]:
        """Trains regressor on autoregressive features and forecasts step-by-step."""
        if len(historical_series) < 12:
            # Fallback for short series
            last = historical_series[-1] if historical_series else 100.0
            return {
                "forecast": [round(last * (1 + 0.01 * (i + 1)), 2) for i in range(horizon)],
                "p10": [round(last * 0.92, 2)] * horizon,
                "p90": [round(last * 1.08, 2)] * horizon,
            }

        df_features = cls.create_lag_features(historical_series)
        X = df_features.drop(columns=["target"])
        y = df_features["target"]

        model = GradientBoostingRegressor(n_estimators=50, random_state=42)
        model.fit(X, y)

        # Multi-step autoregressive rollout
        curr_series = list(historical_series)
        forecast_vals = []

        for _ in range(horizon):
            df_curr = cls.create_lag_features(curr_series)
            if df_curr.empty:
                next_val = curr_series[-1]
            else:
                last_row = df_curr.drop(columns=["target"]).iloc[[-1]]
                next_val = float(model.predict(last_row)[0])
            forecast_vals.append(round(next_val, 2))
            curr_series.append(next_val)

        sigma = float(np.std(historical_series)) * 0.15
        p10 = [round(f - (1.645 * sigma * np.sqrt(i + 1)), 2) for i, f in enumerate(forecast_vals)]
        p90 = [round(f + (1.645 * sigma * np.sqrt(i + 1)), 2) for i, f in enumerate(forecast_vals)]

        return {
            "forecast": forecast_vals,
            "p10": p10,
            "p90": p90,
            "feature_importance": dict(zip(X.columns, [round(float(imp), 3) for imp in model.feature_importances_])),
        }

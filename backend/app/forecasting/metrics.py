"""AEGIS Forecasting Error Evaluation Metrics
Calculates MAE, RMSE, MAPE, WAPE, and SMAPE for backtesting time-series models.
"""

from typing import List, Dict, Any, Union
import numpy as np


class ForecastMetrics:
    """Computes standardized statistical loss metrics for model accuracy verification."""

    @staticmethod
    def mean_absolute_error(actuals: Union[List[float], np.ndarray], predictions: Union[List[float], np.ndarray]) -> float:
        """MAE = mean(|y - y_hat|)"""
        y, y_hat = np.array(actuals, dtype=float), np.array(predictions, dtype=float)
        return round(float(np.mean(np.abs(y - y_hat))), 3)

    @staticmethod
    def root_mean_squared_error(actuals: Union[List[float], np.ndarray], predictions: Union[List[float], np.ndarray]) -> float:
        """RMSE = sqrt(mean((y - y_hat)^2))"""
        y, y_hat = np.array(actuals, dtype=float), np.array(predictions, dtype=float)
        return round(float(np.sqrt(np.mean((y - y_hat) ** 2))), 3)

    @staticmethod
    def mean_absolute_percentage_error(actuals: Union[List[float], np.ndarray], predictions: Union[List[float], np.ndarray]) -> float:
        """MAPE = mean(|(y - y_hat) / y|) * 100"""
        y, y_hat = np.array(actuals, dtype=float), np.array(predictions, dtype=float)
        mask = y != 0
        if not np.any(mask):
            return 0.0
        return round(float(np.mean(np.abs((y[mask] - y_hat[mask]) / y[mask]))) * 100.0, 2)

    @staticmethod
    def symmetric_mape(actuals: Union[List[float], np.ndarray], predictions: Union[List[float], np.ndarray]) -> float:
        """SMAPE = mean(200 * |y - y_hat| / (|y| + |y_hat|))"""
        y, y_hat = np.array(actuals, dtype=float), np.array(predictions, dtype=float)
        denom = np.abs(y) + np.abs(y_hat)
        mask = denom != 0
        if not np.any(mask):
            return 0.0
        return round(float(np.mean(200.0 * np.abs(y[mask] - y_hat[mask]) / denom[mask])), 2)

    @staticmethod
    def evaluate_all(actuals: List[float], predictions: List[float]) -> Dict[str, float]:
        """Calculates full error suite."""
        return {
            "mae": ForecastMetrics.mean_absolute_error(actuals, predictions),
            "rmse": ForecastMetrics.root_mean_squared_error(actuals, predictions),
            "mape": ForecastMetrics.mean_absolute_percentage_error(actuals, predictions),
            "smape": ForecastMetrics.symmetric_mape(actuals, predictions),
        }

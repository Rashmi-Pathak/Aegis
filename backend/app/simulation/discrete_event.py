"""AEGIS Discrete-Event Queue & Logistics Bottleneck Simulator
Simulates stochastic terminal dwell queues, dock turnaround times, and chassis starvation.
"""

from typing import List, Dict, Any
import numpy as np


class DiscreteEventSimulator:
    """M/M/c queueing simulation for terminal logistics and freight unloading bottlenecks."""

    @staticmethod
    def simulate_terminal_dock_queue(
        arrival_rate_per_hour: float,  # lambda
        service_rate_per_dock: float,  # mu
        num_docks: int,                # c
        simulation_hours: int = 24,
        seed: int = 42,
    ) -> Dict[str, Any]:
        """Simulates freight arrivals, queue wait times, and dock utilization."""
        np.random.seed(seed)

        # Expected arrivals
        total_arrivals = np.random.poisson(arrival_rate_per_hour * simulation_hours)

        arrival_times = np.sort(np.random.uniform(0, simulation_hours, total_arrivals))
        service_times = np.random.exponential(1.0 / service_rate_per_dock, total_arrivals)

        dock_free_at = [0.0] * num_docks
        wait_times = []
        total_service_time = 0.0

        for arr_t, s_t in zip(arrival_times, service_times):
            # Assign to dock with earliest availability
            earliest_dock = int(np.argmin(dock_free_at))
            dock_avail = dock_free_at[earliest_dock]

            start_time = max(arr_t, dock_avail)
            wait = start_time - arr_t
            wait_times.append(wait)

            dock_free_at[earliest_dock] = start_time + s_t
            total_service_time += s_t

        avg_wait_hours = float(np.mean(wait_times)) if wait_times else 0.0
        p95_wait_hours = float(np.percentile(wait_times, 95)) if wait_times else 0.0

        # Utilization = Total Service Hours / (Num Docks * Total Hours)
        utilization_pct = min(100.0, (total_service_time / (num_docks * simulation_hours)) * 100.0)

        congestion_status = "Optimal Flow"
        if avg_wait_hours > 3.0 or utilization_pct > 88.0:
            congestion_status = "Severe Terminal Congestion & Bottleneck"
        elif avg_wait_hours > 1.0 or utilization_pct > 75.0:
            congestion_status = "Elevated Queue Delay"

        return {
            "simulation_hours": simulation_hours,
            "total_shipments_simulated": total_arrivals,
            "number_of_active_docks": num_docks,
            "dock_utilization_pct": round(utilization_pct, 1),
            "average_queue_wait_hours": round(avg_wait_hours, 2),
            "p95_queue_wait_hours": round(p95_wait_hours, 2),
            "terminal_congestion_status": congestion_status,
        }

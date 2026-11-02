"""AEGIS Linear Resource Allocation & Simplex Optimization Engine
Solves bounded multi-facility production and freight dispatch subject to capacity constraints.
"""

from typing import List, Dict, Any, Tuple
import numpy as np
from scipy.optimize import linprog


class ResourceOptimizer:
    """Bounded linear programming for fleet dispatch, warehouse storage, and capital budgeting."""

    @staticmethod
    def solve_fleet_route_allocation(
        costs_per_route: List[float],  # c vector
        min_demand_deliveries: List[float],  # lower bound requirements
        max_driver_capacities: List[float],  # upper capacity constraints
        max_total_budget: float,
    ) -> Dict[str, Any]:
        """Minimizes total logistics delivery cost subject to demand constraints."""
        n_routes = len(costs_per_route)
        if n_routes == 0:
            return {"status": "No Routes Configured", "optimal_cost": 0.0}

        c = np.array(costs_per_route)

        # Inequality constraints: A_ub * x <= b_ub
        # 1. Budget constraint: c.T * x <= max_total_budget
        A_ub = [costs_per_route]
        b_ub = [max_total_budget]

        # Bounds per route: min_demand <= x_i <= max_capacity
        bounds = [
            (min_demand_deliveries[i], max_driver_capacities[i])
            for i in range(n_routes)
        ]

        res = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method="highs")

        if res.success:
            return {
                "success": True,
                "optimal_cost": round(float(res.fun), 2),
                "allocated_deliveries": [round(float(x), 1) for x in res.x],
                "budget_utilized": round(float(np.dot(c, res.x)), 2),
                "optimization_status": "Optimal Solution Landed",
            }
        else:
            return {
                "success": False,
                "optimal_cost": 0.0,
                "allocated_deliveries": min_demand_deliveries,
                "optimization_status": f"Constraint conflict: {res.message}",
            }

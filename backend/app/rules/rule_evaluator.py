"""AEGIS Business Rules Engine & Condition Evaluator
Executes deterministic corporate policies, covenant bounds, and automated compliance triggers.
"""

from typing import List, Dict, Any, Optional
import operator


class BusinessRuleEvaluator:
    """Evaluates predicate rules against business state dictionaries."""

    OPERATORS = {
        ">": operator.gt,
        ">=": operator.ge,
        "<": operator.lt,
        "<=": operator.le,
        "==": operator.eq,
        "!=": operator.ne,
        "in": lambda a, b: a in b,
        "not in": lambda a, b: a not in b,
    }

    @classmethod
    def evaluate_predicate(
        cls,
        field_value: Any,
        op_str: str,
        threshold: Any,
    ) -> bool:
        """Evaluates single binary predicate."""
        op_func = cls.OPERATORS.get(op_str)
        if not op_func:
            return False
        try:
            return bool(op_func(field_value, threshold))
        except Exception:
            return False

    @classmethod
    def evaluate_rule_set(
        cls,
        telemetry: Dict[str, Any],
        rules: List[Dict[str, Any]],  # id, name, field, op, threshold, severity, action
    ) -> List[Dict[str, Any]]:
        """Applies a collection of rules and returns breached triggers."""
        violations = []
        for r in rules:
            field = r.get("field")
            val = telemetry.get(field)
            if val is not None:
                breached = cls.evaluate_predicate(val, r.get("op", ">="), r.get("threshold"))
                if breached:
                    violations.append({
                        "rule_id": r.get("id"),
                        "rule_name": r.get("name"),
                        "field": field,
                        "observed_value": val,
                        "threshold": r.get("threshold"),
                        "severity": r.get("severity", "high"),
                        "recommended_action": r.get("action", "Review immediately"),
                    })
        return violations

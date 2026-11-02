"""AEGIS Decision Governance & Sign-Off Workflow Engine
Applies corporate delegation of authority policies based on capital allocation size and risk exposure.
"""
from typing import Dict, Any

class ApprovalWorkflowEngine:
    @staticmethod
    def determine_approval_hierarchy(
        capital_amount: float,
        risk_score: float,
        is_strategic: bool = False,
    ) -> Dict[str, Any]:
        """Determines required approval authority tier."""
        if capital_amount >= 1000000.0 or risk_score >= 80.0 or is_strategic:
            tier = "Board of Directors / Audit Committee"
            required_approvals = 2
        elif capital_amount >= 250000.0 or risk_score >= 60.0:
            tier = "Chief Executive Officer / Chief Financial Officer"
            required_approvals = 2
        elif capital_amount >= 50000.0:
            tier = "Vice President / Business Unit Head"
            required_approvals = 1
        else:
            tier = "Operational Team Lead / Manager"
            required_approvals = 1

        return {
            "capital_amount": capital_amount,
            "risk_score": risk_score,
            "approval_tier": tier,
            "required_approvers_count": required_approvals,
            "governance_status": "PENDING_APPROVAL",
        }

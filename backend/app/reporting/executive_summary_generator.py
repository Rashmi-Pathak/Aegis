"""AEGIS Executive Intelligence Briefing & Memo Generator
Synthesizes telemetry, risks, forecasts, and optimization results into C-suite executive briefs.
"""

from typing import Dict, Any, List
import datetime


class ExecutiveBriefingGenerator:
    """Produces structured executive memos formatted in Markdown and JSON."""

    @staticmethod
    def generate_briefing(
        organization_name: str,
        health_score: float,
        critical_risks: List[Dict[str, Any]],
        financial_kpis: Dict[str, Any],
        top_recommendations: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """Assembles a high-level briefing document for CEO, CFO, and Board members."""
        timestamp = datetime.datetime.now().strftime("%B %d, %Y - %H:%M UTC")

        # Markdown formatted briefing
        lines = [
            f"# AEGIS EXECUTIVE RISK INTELLIGENCE BRIEFING",
            f"**Organization:** {organization_name} | **Date:** {timestamp}",
            f"**Enterprise Health Score:** {health_score}/100",
            "",
            "## 1. Executive Summary & Core Posture",
            f"Overall health of {organization_name} is currently scored at **{health_score:.1f}/100**.",
            f"Active critical exposure points identified: **{len(critical_risks)}**.",
            "",
            "## 2. Key Financial & Operational Telemetry",
        ]

        for k, v in financial_kpis.items():
            val = v.get("value", "N/A") if isinstance(v, dict) else str(v)
            trend = v.get("trend", "") if isinstance(v, dict) else ""
            lines.append(f"- **{k.title()}:** {val} {f'({trend})' if trend else ''}")

        lines.extend([
            "",
            "## 3. High-Priority Threat Telemetry",
        ])

        for r in critical_risks[:4]:
            title = r.get("title", "Threat Trigger")
            score = r.get("score", r.get("risk_score", 0))
            category = r.get("category", "Operational")
            lines.append(f"- **[{category.upper()}] {title}** (Risk Index: {score})")

        lines.extend([
            "",
            "## 4. Recommended Decision Levers & Actions",
        ])

        for rec in top_recommendations[:3]:
            action = rec.get("title", rec.get("action", "Initiative"))
            roi = rec.get("roi", rec.get("roi_ratio", "N/A"))
            lines.append(f"1. **{action}** — Projected Risk-Adjusted ROI: {roi}")

        markdown_memo = "\n".join(lines)

        return {
            "title": f"AEGIS Executive Briefing — {organization_name}",
            "generated_at": timestamp,
            "health_score": health_score,
            "critical_risk_count": len(critical_risks),
            "markdown_content": markdown_memo,
            "status": "APPROVED_FOR_DISTRIBUTION",
        }

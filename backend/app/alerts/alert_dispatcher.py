"""AEGIS Multi-Channel Alert Dispatcher
Formats and routes enterprise risk alerts to Slack, Microsoft Teams, PagerDuty, and Webhooks.
"""
from typing import Dict, Any, List, Optional
import datetime

class AlertDispatcherService:
    @staticmethod
    def format_slack_block_kit(alert: Dict[str, Any]) -> Dict[str, Any]:
        """Builds Slack Block Kit JSON payload for critical risk alerts."""
        title = alert.get("title", "Threat Alert")
        score = alert.get("score", alert.get("risk_score", 0))
        severity = alert.get("severity", "critical").upper()

        return {
            "blocks": [
                {
                    "type": "header",
                    "text": {"type": "plain_text", "text": f":rotating_light: AEGIS ALERT: {title}"},
                },
                {
                    "type": "section",
                    "fields": [
                        {"type": "mrkdwn", "text": f"*Severity:* `{severity}`"},
                        {"type": "mrkdwn", "text": f"*Risk Index:* `{score}/100`"},
                    ],
                },
                {
                    "type": "section",
                    "text": {"type": "mrkdwn", "text": alert.get("message", "Operational break detected.")},
                },
            ]
        }

    @staticmethod
    def format_pagerduty_payload(alert: Dict[str, Any], routing_key: str) -> Dict[str, Any]:
        """Builds PagerDuty Events API v2 payload."""
        return {
            "routing_key": routing_key,
            "event_action": "trigger",
            "payload": {
                "summary": f"[AEGIS {alert.get('severity', 'critical').upper()}] {alert.get('title')}",
                "severity": "critical" if alert.get("severity") == "critical" else "warning",
                "source": "aegis-intelligence-engine",
                "custom_details": alert,
            },
        }

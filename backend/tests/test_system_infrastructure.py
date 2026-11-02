"""AEGIS System Infrastructure Test Suite
Verifies Immutable Audit Hash Chains, Alert Dispatcher Block Kit,
Admin Diagnostics, Background Job Runner, and Crypto Utilities.
"""
import pytest
from app.audit.audit_service import ImmutableAuditService
from app.alerts.alert_dispatcher import AlertDispatcherService
from app.admin.system_service import AdminSystemDiagnostics
from app.jobs.job_runner import BackgroundJobRunner
from app.utils.crypto import CryptoUtils

def test_immutable_audit_chain():
    entry1 = {
        "id": "1",
        "timestamp": "2026-11-01T10:00:00Z",
        "user_id": "usr_01",
        "organization_id": "org_01",
        "action": "LOGIN",
        "details": {"ip": "127.0.0.1"},
    }
    hash1 = ImmutableAuditService.compute_audit_hash(
        "GENESIS_BLOCK_AEGIS_2026", entry1["timestamp"], entry1["user_id"], entry1["organization_id"], entry1["action"], entry1["details"]
    )
    entry1["record_hash"] = hash1

    res = ImmutableAuditService.verify_chain_integrity([entry1])
    assert res["valid"] is True
    assert res["status"] == "CRYPTOGRAPHICALLY_VERIFIED"

def test_alert_dispatcher():
    alert = {"title": "Diesel Price Spike", "severity": "critical", "risk_score": 88}
    slack = AlertDispatcherService.format_slack_block_kit(alert)
    assert len(slack["blocks"]) >= 2
    pd_event = AlertDispatcherService.format_pagerduty_payload(alert, routing_key="test_key")
    assert pd_event["payload"]["severity"] == "critical"

def test_admin_diagnostics():
    metrics = AdminSystemDiagnostics.gather_system_metrics()
    assert metrics["database_status"] == "ONLINE_HEALTHY"
    assert "platform" in metrics

def test_background_job_runner():
    j_id = BackgroundJobRunner.create_job("INGEST_ZIP", "org_01", {"file": "demo.zip"})
    status = BackgroundJobRunner.get_job_status(j_id)
    assert status["status"] == "QUEUED"
    BackgroundJobRunner.update_progress(j_id, 100, "Processing complete.")
    status_done = BackgroundJobRunner.get_job_status(j_id)
    assert status_done["status"] == "COMPLETED"

def test_crypto_utils():
    key = CryptoUtils.generate_api_key()
    assert key.startswith("aegis_live_")
    secret = "test_secret"
    payload = b"test payload"
    import hmac, hashlib
    sig = hmac.new(secret.encode("utf-8"), payload, hashlib.sha256).hexdigest()
    assert CryptoUtils.verify_hmac_signature(secret, payload, sig) is True

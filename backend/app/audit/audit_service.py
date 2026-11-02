"""AEGIS Cryptographic Immutable Audit Trail Engine
Generates SHA-256 hash chains across corporate audit logs to guarantee tamper-evidence.
Hash_i = SHA256(Hash_{i-1} || Timestamp || UserID || OrgID || Action || Details)
"""
from typing import Dict, Any, List, Optional
import hashlib
import json
import datetime

class ImmutableAuditService:
    @staticmethod
    def compute_audit_hash(
        previous_hash: str,
        timestamp: str,
        user_id: str,
        organization_id: str,
        action: str,
        details: Dict[str, Any],
    ) -> str:
        """Computes SHA-256 block hash for an audit entry."""
        details_str = json.dumps(details, sort_keys=True)
        payload = f"{previous_hash}|{timestamp}|{user_id}|{organization_id}|{action}|{details_str}"
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()

    @classmethod
    def verify_chain_integrity(cls, audit_records: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Validates that no historical audit log entry has been altered or deleted."""
        if not audit_records:
            return {"valid": True, "record_count": 0, "status": "Empty Chain"}

        prev_hash = "GENESIS_BLOCK_AEGIS_2026"
        for i, rec in enumerate(audit_records):
            expected = cls.compute_audit_hash(
                previous_hash=prev_hash,
                timestamp=rec["timestamp"],
                user_id=rec["user_id"],
                organization_id=rec["organization_id"],
                action=rec["action"],
                details=rec["details"],
            )
            if rec.get("record_hash") != expected:
                return {
                    "valid": False,
                    "tampered_index": i,
                    "tampered_record_id": rec.get("id"),
                    "status": "TAMPERING_DETECTED",
                }
            prev_hash = expected

        return {
            "valid": True,
            "record_count": len(audit_records),
            "status": "CRYPTOGRAPHICALLY_VERIFIED",
        }

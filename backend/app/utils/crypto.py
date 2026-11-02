"""AEGIS Cryptographic Hashing, HMAC & Token Utilities."""
import hashlib
import hmac
import secrets

class CryptoUtils:
    @staticmethod
    def generate_api_key(prefix: str = "aegis_live_") -> str:
        """Generates cryptographically random 32-byte hexadecimal API key."""
        return f"{prefix}{secrets.token_hex(24)}"

    @staticmethod
    def verify_hmac_signature(secret: str, payload_bytes: bytes, signature_hex: str) -> bool:
        """Constant-time HMAC comparison to prevent timing attacks."""
        expected = hmac.new(secret.encode("utf-8"), payload_bytes, hashlib.sha256).hexdigest()
        return hmac.compare_digest(expected, signature_hex)

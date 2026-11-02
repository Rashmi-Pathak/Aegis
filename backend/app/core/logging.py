import logging
import sys
import json
import time
from typing import Any, Dict, Optional

class AegisJsonFormatter(logging.Formatter):
    """Structured JSON formatter for enterprise auditability and logging."""
    def format(self, record: logging.LogRecord) -> str:
        log_payload = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(record.created)),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        if hasattr(record, "stage"):
            log_payload["stage"] = record.stage
        if hasattr(record, "organization_id"):
            log_payload["organization_id"] = record.organization_id
        if hasattr(record, "job_id"):
            log_payload["job_id"] = record.job_id
        if hasattr(record, "dataset_id"):
            log_payload["dataset_id"] = record.dataset_id
        if hasattr(record, "extra_data"):
            log_payload["extra"] = record.extra_data
        if record.exc_info:
            log_payload["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_payload)

def setup_logging():
    logger = logging.getLogger("aegis")
    logger.setLevel(logging.INFO)
    logger.handlers.clear()
    
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(AegisJsonFormatter())
    logger.addHandler(handler)
    return logger

logger = setup_logging()

def log_pipeline_event(
    stage: str,
    message: str,
    organization_id: Optional[str] = None,
    job_id: Optional[str] = None,
    dataset_id: Optional[str] = None,
    extra_data: Optional[Dict[str, Any]] = None,
    level: int = logging.INFO,
):
    """Log an orchestrated intelligence pipeline milestone."""
    extra = {
        "stage": stage,
        "organization_id": organization_id or "system",
        "job_id": job_id or "direct",
        "dataset_id": dataset_id or "none",
        "extra_data": extra_data or {},
    }
    logger.log(level, message, extra=extra)

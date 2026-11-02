"""AEGIS Background Task & Ingestion Job Orchestrator
Tracks asynchronous processing jobs: pending, running, completed, and failed states with execution logs.
"""
from typing import Dict, Any, List, Optional
import uuid
import datetime

class BackgroundJobRunner:
    _jobs: Dict[str, Dict[str, Any]] = {}

    @classmethod
    def create_job(cls, job_type: str, organization_id: str, parameters: Dict[str, Any]) -> str:
        """Initializes tracked asynchronous background job."""
        job_id = f"job_{uuid.uuid4().hex[:12]}"
        cls._jobs[job_id] = {
            "job_id": job_id,
            "job_type": job_type,
            "organization_id": organization_id,
            "status": "QUEUED",
            "progress_pct": 0,
            "parameters": parameters,
            "created_at": datetime.datetime.now().isoformat(),
            "completed_at": None,
            "logs": ["Job queued into execution pipeline."],
        }
        return job_id

    @classmethod
    def update_progress(cls, job_id: str, progress: int, message: str):
        """Updates execution percentage and appends log message."""
        if job_id in cls._jobs:
            cls._jobs[job_id]["progress_pct"] = min(100, max(0, progress))
            cls._jobs[job_id]["status"] = "RUNNING" if progress < 100 else "COMPLETED"
            cls._jobs[job_id]["logs"].append(message)
            if progress >= 100:
                cls._jobs[job_id]["completed_at"] = datetime.datetime.now().isoformat()

    @classmethod
    def get_job_status(cls, job_id: str) -> Optional[Dict[str, Any]]:
        return cls._jobs.get(job_id)

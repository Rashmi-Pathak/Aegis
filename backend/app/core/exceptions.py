from typing import Any, Dict, Optional
from fastapi import Request, status
from fastapi.responses import JSONResponse

class AegisException(Exception):
    """Base exception for all AEGIS domain errors."""
    def __init__(
        self,
        message: str,
        code: str = "AEGIS_ERROR",
        status_code: int = status.HTTP_400_BAD_REQUEST,
        details: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(message)
        self.message = message
        self.code = code
        self.status_code = status_code
        self.details = details or {}

class AuthenticationError(AegisException):
    def __init__(self, message: str = "Invalid credentials or expired session", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, code="AUTHENTICATION_ERROR", status_code=status.HTTP_401_UNAUTHORIZED, details=details)

class AuthorizationError(AegisException):
    def __init__(self, message: str = "Insufficient permissions or organization mismatch", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, code="AUTHORIZATION_ERROR", status_code=status.HTTP_403_FORBIDDEN, details=details)

class NotFoundError(AegisException):
    def __init__(self, message: str = "Requested resource not found", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, code="NOT_FOUND_ERROR", status_code=status.HTTP_404_NOT_FOUND, details=details)

class DataValidationError(AegisException):
    def __init__(self, message: str = "Dataset or schema validation failed", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, code="DATA_VALIDATION_ERROR", status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, details=details)

class IngestionError(AegisException):
    def __init__(self, message: str = "Error extracting or processing business dataset", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, code="INGESTION_ERROR", status_code=status.HTTP_400_BAD_REQUEST, details=details)

class ModelExecutionError(AegisException):
    def __init__(self, message: str = "Machine learning model execution failed", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, code="MODEL_EXECUTION_ERROR", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, details=details)

async def aegis_exception_handler(request: Request, exc: AegisException) -> JSONResponse:
    """Centralized exception handler producing standard Aegis error payload."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "code": exc.code,
                "message": exc.message,
                "details": exc.details,
            },
        },
    )

async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Unhandled server exception handler."""
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "error": {
                "code": "INTERNAL_SERVER_ERROR",
                "message": "An unexpected server error occurred during processing.",
                "details": {"type": exc.__class__.__name__},
            },
        },
    )

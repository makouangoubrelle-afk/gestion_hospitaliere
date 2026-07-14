"""
Custom exceptions for CHLAB API
"""
from django.http import JsonResponse
from rest_framework import status


class CHLABAPIException(Exception):
    """Base exception for CHLAB API"""
    def __init__(self, message, code=None, status_code=status.HTTP_400_BAD_REQUEST):
        self.message = message
        self.code = code or "API_ERROR"
        self.status_code = status_code
        super().__init__(self.message)


class PatientNotFoundException(CHLABAPIException):
    """Raised when a patient is not found"""
    def __init__(self, patient_id):
        super().__init__(
            f"Patient with ID {patient_id} not found",
            code="PATIENT_NOT_FOUND",
            status_code=status.HTTP_404_NOT_FOUND
        )


class MedecinNotFoundException(CHLABAPIException):
    """Raised when a doctor is not found"""
    def __init__(self, medecin_id):
        super().__init__(
            f"Doctor with ID {medecin_id} not found",
            code="MEDECIN_NOT_FOUND",
            status_code=status.HTTP_404_NOT_FOUND
        )


class ConsultationNotFoundException(CHLABAPIException):
    """Raised when a consultation is not found"""
    def __init__(self, consultation_id):
        super().__init__(
            f"Consultation with ID {consultation_id} not found",
            code="CONSULTATION_NOT_FOUND",
            status_code=status.HTTP_404_NOT_FOUND
        )


class PaymentFailedException(CHLABAPIException):
    """Raised when a payment fails"""
    def __init__(self, reason):
        super().__init__(
            f"Payment failed: {reason}",
            code="PAYMENT_FAILED",
            status_code=status.HTTP_400_BAD_REQUEST
        )


class InvoiceNotFoundException(CHLABAPIException):
    """Raised when an invoice is not found"""
    def __init__(self, invoice_id):
        super().__init__(
            f"Invoice with ID {invoice_id} not found",
            code="INVOICE_NOT_FOUND",
            status_code=status.HTTP_404_NOT_FOUND
        )


class ValidationException(CHLABAPIException):
    """Raised for validation errors"""
    def __init__(self, message):
        super().__init__(
            message,
            code="VALIDATION_ERROR",
            status_code=status.HTTP_400_BAD_REQUEST
        )


def error_response(exception):
    """Generate a consistent error response"""
    if isinstance(exception, CHLABAPIException):
        return JsonResponse({
            "error": {
                "code": exception.code,
                "message": exception.message,
                "status": exception.status_code
            }
        }, status=exception.status_code)
    
    # Generic error response
    return JsonResponse({
        "error": {
            "code": "INTERNAL_SERVER_ERROR",
            "message": str(exception),
            "status": 500
        }
    }, status=500)

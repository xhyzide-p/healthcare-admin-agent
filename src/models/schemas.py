"""Pydantic schemas for request/response validation"""

from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional, List
from enum import Enum

class AppointmentType(str, Enum):
    CHECKUP = "checkup"
    FOLLOWUP = "followup"
    CONSULTATION = "consultation"
    PROCEDURE = "procedure"
    URGENT = "urgent"

class AppointmentStatus(str, Enum):
    SCHEDULED = "scheduled"
    CONFIRMED = "confirmed"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    RESCHEDULED = "rescheduled"

class PatientIntakeRequest(BaseModel):
    """New patient intake form"""
    first_name: str = Field(..., min_length=1)
    last_name: str = Field(..., min_length=1)
    email: EmailStr
    phone: str = Field(..., pattern=r"^\+?1?\d{9,15}$")
    date_of_birth: datetime
    gender: Optional[str] = None
    address: str
    city: str
    state: str
    zip_code: str
    medical_history: Optional[str] = None
    allergies: Optional[List[str]] = None
    current_medications: Optional[List[str]] = None
    insurance_provider: str
    insurance_id: str
    insurance_group_number: Optional[str] = None

class AppointmentRequest(BaseModel):
    """Appointment scheduling request"""
    patient_id: str
    appointment_type: AppointmentType
    preferred_date: datetime
    preferred_provider: Optional[str] = None
    notes: Optional[str] = None
    duration_minutes: int = 30

class RescheduleRequest(BaseModel):
    """Appointment reschedule request"""
    appointment_id: str
    new_date: datetime
    reason: Optional[str] = None

class InsuranceVerificationRequest(BaseModel):
    """Insurance verification request"""
    patient_id: str
    insurance_id: str
    provider: str

class AppointmentResponse(BaseModel):
    """Appointment confirmation response"""
    appointment_id: str
    patient_id: str
    appointment_type: AppointmentType
    scheduled_date: datetime
    provider_name: str
    location: str
    status: AppointmentStatus
    confirmation_sent: bool
    reminder_scheduled: bool

class InsuranceVerificationResponse(BaseModel):
    """Insurance verification response"""
    patient_id: str
    is_eligible: bool
    coverage_details: Optional[dict] = None
    copay: Optional[float] = None
    deductible: Optional[float] = None
    estimated_cost: Optional[float] = None
    message: str

"""Appointment data model"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from uuid import uuid4
from enum import Enum

class AppointmentStatus(str, Enum):
    SCHEDULED = "scheduled"
    CONFIRMED = "confirmed"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    RESCHEDULED = "rescheduled"
    NO_SHOW = "no_show"

class AppointmentType(str, Enum):
    CHECKUP = "checkup"
    FOLLOWUP = "followup"
    CONSULTATION = "consultation"
    PROCEDURE = "procedure"
    URGENT = "urgent"

class Appointment(BaseModel):
    """Appointment record model"""
    appointment_id: str = Field(default_factory=lambda: str(uuid4()))
    patient_id: str
    patient_name: str
    appointment_type: AppointmentType
    scheduled_datetime: datetime
    duration_minutes: int = 30
    provider_id: str
    provider_name: str
    location: str
    status: AppointmentStatus = AppointmentStatus.SCHEDULED
    notes: Optional[str] = None
    reminder_sent: bool = False
    reminder_24h_sent: bool = False
    reminder_1h_sent: bool = False
    insurance_verified: bool = False
    pre_visit_documents_sent: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_schema_extra = {
            "example": {
                "appointment_id": "apt_456",
                "patient_id": "pat_123",
                "patient_name": "John Doe",
                "appointment_type": "checkup",
                "scheduled_datetime": "2024-12-01T10:00:00",
                "provider_name": "Dr. Jane Smith",
                "location": "Downtown Clinic",
                "status": "scheduled"
            }
        }

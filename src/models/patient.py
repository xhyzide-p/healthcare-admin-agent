"""Patient data model"""

from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional, List
from uuid import uuid4

class Patient(BaseModel):
    """Patient profile model"""
    patient_id: str = Field(default_factory=lambda: str(uuid4()))
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    date_of_birth: datetime
    gender: Optional[str] = None
    address: str
    city: str
    state: str
    zip_code: str
    medical_history: Optional[List[str]] = None
    allergies: Optional[List[str]] = None
    current_medications: Optional[List[str]] = None
    insurance_provider: str
    insurance_id: str
    insurance_group_number: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_schema_extra = {
            "example": {
                "patient_id": "pat_123",
                "first_name": "John",
                "last_name": "Doe",
                "email": "john@example.com",
                "phone": "+12125551234",
                "date_of_birth": "1985-01-15",
                "insurance_provider": "Blue Shield",
                "insurance_id": "BSC123456"
            }
        }

    def full_name(self) -> str:
        """Return full name"""
        return f"{self.first_name} {self.last_name}"

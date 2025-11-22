"""Scheduling Agent - Manage appointment booking and rescheduling"""

import logging
from typing import Any, Dict, List
from datetime import datetime, timedelta
import asyncio

from .base_agent import BaseAgent

logger = logging.getLogger(__name__)

class SchedulingAgent(BaseAgent):
    """
    Scheduling Agent manages:
    - Provider availability queries
    - Appointment booking
    - Conflict detection
    - Rescheduling requests
    - Waitlist management
    """
    
    def __init__(self):
        super().__init__(
            name="SchedulingAgent",
            description="Manages appointment scheduling and calendar operations"
        )
        # Mock provider database
        self.providers = self._init_mock_providers()
        self.scheduled_appointments = {}
    
    async def process(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process scheduling request
        
        Args:
            request: Contains appointment details
        
        Returns:
            Response with appointment confirmation
        """
        request_id = request.get("request_id", "SCHEDULE_REQUEST")
        request_type = request.get("appointment_action", "schedule")
        
        logger.info(f"[{request_id}] Scheduling Agent - Action: {request_type}")
        
        try:
            if request_type == "check_availability":
                return await self._handle_availability_check(request, request_id)
            elif request_type == "book":
                return await self._handle_appointment_booking(request, request_id)
            elif request_type == "reschedule":
                return await self._handle_rescheduling(request, request_id)
            elif request_type == "cancel":
                return await self._handle_cancellation(request, request_id)
            else:
                return {
                    "success": False,
                    "error": f"Unknown appointment action: {request_type}"
                }
        
        except Exception as e:
            logger.error(f"[{request_id}] Scheduling Agent error: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to process scheduling request"
            }
    
    async def _handle_availability_check(self, request: Dict[str, Any], request_id: str) -> Dict[str, Any]:
        """Check provider availability for given date range"""
        logger.info(f"[{request_id}] Checking availability")
        
        preferred_date = request.get("preferred_date")
        appointment_type = request.get("appointment_type", "checkup")
        duration_minutes = request.get("duration_minutes", 30)
        
        # Mock: Generate available slots
        available_slots = self._get_available_slots(
            preferred_date, 
            appointment_type, 
            duration_minutes
        )
        
        return {
            "success": True,
            "available_slots": available_slots,
            "total_slots": len(available_slots),
            "message": f"Found {len(available_slots)} available slots"
        }
    
    async def _handle_appointment_booking(self, request: Dict[str, Any], request_id: str) -> Dict[str, Any]:
        """Book an appointment"""
        logger.info(f"[{request_id}] Booking appointment")
        
        patient_id = request.get("patient_id")
        appointment_type = request.get("appointment_type", "checkup")
        appointment_datetime = request.get("preferred_date")
        provider_id = request.get("preferred_provider", "PROV_001")
        
        # Generate appointment ID
        appointment_id = self._generate_appointment_id()
        
        # Mock: Book the appointment
        booking_result = {
            "appointment_id": appointment_id,
            "patient_id": patient_id,
            "provider_id": provider_id,
            "provider_name": self.providers.get(provider_id, {}).get("name", "Dr. Unknown"),
            "appointment_datetime": appointment_datetime,
            "appointment_type": appointment_type,
            "location": self.providers.get(provider_id, {}).get("location", "Downtown Clinic"),
            "duration_minutes": 30,
            "status": "scheduled",
            "booked_at": datetime.utcnow().isoformat()
        }
        
        # Store appointment
        self.scheduled_appointments[appointment_id] = booking_result
        
        self.log_action("appointment_booked", {
            "request_id": request_id,
            "appointment_id": appointment_id,
            "patient_id": patient_id,
            "appointment_datetime": appointment_datetime
        })
        
        return {
            "success": True,
            "appointment_id": appointment_id,
            "patient_id": patient_id,
            "provider_name": booking_result["provider_name"],
            "appointment_datetime": appointment_datetime,
            "location": booking_result["location"],
            "confirmation_token": f"CONF_{appointment_id}",
            "status": "scheduled",
            "next_steps": [
                "Insurance verification",
                "Send confirmation email",
                "Schedule reminders"
            ],
            "message": f"Appointment scheduled for {appointment_datetime}"
        }
    
    async def _handle_rescheduling(self, request: Dict[str, Any], request_id: str) -> Dict[str, Any]:
        """Reschedule an existing appointment"""
        logger.info(f"[{request_id}] Rescheduling appointment")
        
        appointment_id = request.get("appointment_id")
        new_date = request.get("new_date")
        
        # Check if appointment exists
        if appointment_id not in self.scheduled_appointments:
            return {
                "success": False,
                "error": f"Appointment {appointment_id} not found"
            }
        
        # Update appointment
        old_appointment = self.scheduled_appointments[appointment_id]
        old_appointment["status"] = "rescheduled"
        old_appointment["previous_datetime"] = old_appointment["appointment_datetime"]
        old_appointment["appointment_datetime"] = new_date
        old_appointment["updated_at"] = datetime.utcnow().isoformat()
        
        self.log_action("appointment_rescheduled", {
            "request_id": request_id,
            "appointment_id": appointment_id,
            "old_date": old_appointment["previous_datetime"],
            "new_date": new_date
        })
        
        return {
            "success": True,
            "appointment_id": appointment_id,
            "status": "rescheduled",
            "new_datetime": new_date,
            "old_datetime": old_appointment["previous_datetime"],
            "message": f"Appointment rescheduled to {new_date}",
            "next_steps": [
                "Cancel old reminders",
                "Schedule new reminders",
                "Send updated confirmation"
            ]
        }
    
    async def _handle_cancellation(self, request: Dict[str, Any], request_id: str) -> Dict[str, Any]:
        """Cancel an appointment"""
        logger.info(f"[{request_id}] Cancelling appointment")
        
        appointment_id = request.get("appointment_id")
        reason = request.get("reason", "No reason provided")
        
        # Check if appointment exists
        if appointment_id not in self.scheduled_appointments:
            return {
                "success": False,
                "error": f"Appointment {appointment_id} not found"
            }
        
        # Update appointment status
        appointment = self.scheduled_appointments[appointment_id]
        appointment["status"] = "cancelled"
        appointment["cancellation_reason"] = reason
        appointment["cancelled_at"] = datetime.utcnow().isoformat()
        
        self.log_action("appointment_cancelled", {
            "request_id": request_id,
            "appointment_id": appointment_id,
            "reason": reason
        })
        
        return {
            "success": True,
            "appointment_id": appointment_id,
            "status": "cancelled",
            "cancellation_timestamp": appointment["cancelled_at"],
            "message": "Appointment cancelled successfully"
        }
    
    def _get_available_slots(self, preferred_date: str, appointment_type: str, duration_minutes: int) -> List[Dict[str, Any]]:
        """Generate mock available appointment slots"""
        slots = []
        
        # Generate 5 available slots around preferred date
        base_date = datetime.fromisoformat(preferred_date.replace('Z', '+00:00'))
        
        for i in range(5):
            slot_time = base_date + timedelta(days=i)
            slot_time = slot_time.replace(hour=9 + (i % 3))  # 9 AM, 10 AM, 11 AM
            
            slots.append({
                "start_time": slot_time.isoformat(),
                "end_time": (slot_time + timedelta(minutes=duration_minutes)).isoformat(),
                "duration_minutes": duration_minutes,
                "provider_name": "Dr. Jane Smith",
                "location": "Downtown Clinic",
                "appointment_type": appointment_type,
                "availability_id": f"SLOT_{i}"
            })
        
        return slots
    
    def _generate_appointment_id(self) -> str:
        """Generate unique appointment ID"""
        import uuid
        return f"APT_{uuid.uuid4().hex[:8].upper()}"
    
    def _init_mock_providers(self) -> Dict[str, Dict[str, Any]]:
        """Initialize mock provider database"""
        return {
            "PROV_001": {
                "name": "Dr. Jane Smith",
                "specialty": "General Practice",
                "location": "Downtown Clinic",
                "phone": "+1-202-555-0123"
            },
            "PROV_002": {
                "name": "Dr. John Martinez",
                "specialty": "Cardiology",
                "location": "Medical Plaza",
                "phone": "+1-202-555-0124"
            },
            "PROV_003": {
                "name": "Dr. Sarah Chen",
                "specialty": "Dermatology",
                "location": "Downtown Clinic",
                "phone": "+1-202-555-0125"
            }
        }

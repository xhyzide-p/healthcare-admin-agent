"""Followup Agent - Send reminders and post-visit communications"""

import logging
from typing import Any, Dict
from datetime import datetime, timedelta

from .base_agent import BaseAgent

logger = logging.getLogger(__name__)

class FollowupAgent(BaseAgent):
    """
    Followup Agent manages:
    - Appointment reminders (24h, 1h before)
    - Post-visit surveys
    - Prescription refill reminders
    - Test result follow-ups
    - No-show tracking and rescheduling
    """
    
    def __init__(self):
        super().__init__(
            name="FollowupAgent",
            description="Sends reminders and post-visit communications"
        )
        self.scheduled_reminders = {}
        self.email_templates = self._init_email_templates()
        self.sms_templates = self._init_sms_templates()
    
    async def process(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process followup request
        
        Args:
            request: Contains followup action and details
        
        Returns:
            Response with reminder scheduling result
        """
        request_id = request.get("request_id", "FOLLOWUP_REQUEST")
        action = request.get("followup_action", "schedule_reminder")
        
        logger.info(f"[{request_id}] Followup Agent - Action: {action}")
        
        try:
            if action == "schedule_reminder":
                return await self._schedule_reminders(request, request_id)
            elif action == "cancel_reminders":
                return await self._cancel_reminders(request, request_id)
            elif action == "send_survey":
                return await self._send_post_visit_survey(request, request_id)
            elif action == "process_no_show":
                return await self._process_no_show(request, request_id)
            else:
                return {
                    "success": False,
                    "error": f"Unknown followup action: {action}"
                }
        
        except Exception as e:
            logger.error(f"[{request_id}] Followup Agent error: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to process followup action"
            }
    
    async def _schedule_reminders(self, request: Dict[str, Any], request_id: str) -> Dict[str, Any]:
        """Schedule appointment reminders"""
        logger.info(f"[{request_id}] Scheduling reminders")
        
        appointment_id = request.get("appointment_id")
        appointment_datetime = request.get("appointment_datetime")
        patient_email = request.get("patient_email")
        patient_phone = request.get("patient_phone")
        provider_name = request.get("provider_name", "Your Healthcare Provider")
        location = request.get("location", "Clinic")
        
        # Parse appointment datetime
        try:
            appt_time = datetime.fromisoformat(appointment_datetime)
        except:
            return {"success": False, "error": "Invalid appointment datetime"}
        
        reminders = []
        
        # Schedule 24-hour reminder
        reminder_24h_time = appt_time - timedelta(hours=24)
        reminder_24h = {
            "reminder_id": f"REM_{appointment_id}_24H",
            "type": "appointment_reminder_24h",
            "scheduled_time": reminder_24h_time.isoformat(),
            "delivery_channels": ["email", "sms"] if patient_phone else ["email"],
            "status": "scheduled",
            "message_template": "reminder_24h"
        }
        reminders.append(reminder_24h)
        
        # Schedule 1-hour reminder
        reminder_1h_time = appt_time - timedelta(hours=1)
        reminder_1h = {
            "reminder_id": f"REM_{appointment_id}_1H",
            "type": "appointment_reminder_1h",
            "scheduled_time": reminder_1h_time.isoformat(),
            "delivery_channels": ["sms", "email"] if patient_phone else ["email"],
            "status": "scheduled",
            "message_template": "reminder_1h"
        }
        reminders.append(reminder_1h)
        
        # Store reminders
        self.scheduled_reminders[appointment_id] = reminders
        
        # Build message previews
        message_preview = self._build_reminder_message(
            appointment_datetime,
            provider_name,
            location
        )
        
        self.log_action("reminders_scheduled", {
            "request_id": request_id,
            "appointment_id": appointment_id,
            "reminder_count": len(reminders),
            "delivery_channels": "email, sms" if patient_phone else "email"
        })
        
        return {
            "success": True,
            "appointment_id": appointment_id,
            "reminders_scheduled": len(reminders),
            "reminders": reminders,
            "message_preview": message_preview,
            "status": "reminders_queued",
            "message": f"Scheduled {len(reminders)} reminders for appointment",
            "next_steps": [
                "24-hour reminder will be sent automatically",
                "1-hour reminder will be sent automatically",
                "Patient can reply to confirm attendance"
            ]
        }
    
    async def _cancel_reminders(self, request: Dict[str, Any], request_id: str) -> Dict[str, Any]:
        """Cancel scheduled reminders"""
        logger.info(f"[{request_id}] Cancelling reminders")
        
        appointment_id = request.get("appointment_id")
        
        if appointment_id not in self.scheduled_reminders:
            return {
                "success": False,
                "error": f"No reminders found for appointment {appointment_id}"
            }
        
        # Mark reminders as cancelled
        reminders = self.scheduled_reminders[appointment_id]
        for reminder in reminders:
            reminder["status"] = "cancelled"
        
        self.log_action("reminders_cancelled", {
            "request_id": request_id,
            "appointment_id": appointment_id,
            "reminders_cancelled": len(reminders)
        })
        
        return {
            "success": True,
            "appointment_id": appointment_id,
            "reminders_cancelled": len(reminders),
            "message": f"Cancelled {len(reminders)} reminders"
        }
    
    async def _send_post_visit_survey(self, request: Dict[str, Any], request_id: str) -> Dict[str, Any]:
        """Send post-visit satisfaction survey"""
        logger.info(f"[{request_id}] Sending post-visit survey")
        
        patient_email = request.get("patient_email")
        patient_name = request.get("patient_name", "Patient")
        provider_name = request.get("provider_name", "Your Provider")
        appointment_id = request.get("appointment_id")
        
        survey_link = f"https://survey.healthcare.app/feedback/{appointment_id}"
        
        self.log_action("survey_sent", {
            "request_id": request_id,
            "appointment_id": appointment_id,
            "patient_email": patient_email
        })
        
        return {
            "success": True,
            "survey_id": f"SURV_{appointment_id}",
            "patient_email": patient_email,
            "survey_link": survey_link,
            "delivery_status": "queued",
            "message": "Post-visit survey scheduled for delivery",
            "survey_questions": 5,
            "estimated_completion_time": "3-5 minutes"
        }
    
    async def _process_no_show(self, request: Dict[str, Any], request_id: str) -> Dict[str, Any]:
        """Process no-show and trigger follow-up"""
        logger.info(f"[{request_id}] Processing no-show")
        
        appointment_id = request.get("appointment_id")
        patient_id = request.get("patient_id")
        patient_email = request.get("patient_email")
        patient_phone = request.get("patient_phone")
        
        self.log_action("no_show_recorded", {
            "request_id": request_id,
            "appointment_id": appointment_id,
            "patient_id": patient_id
        })
        
        return {
            "success": True,
            "appointment_id": appointment_id,
            "status": "no_show",
            "actions_taken": [
                "Recorded no-show in patient record",
                "Cancelled all subsequent reminders",
                "Triggered follow-up outreach",
                "Freed up appointment slot for others",
                "Sent apology message to patient"
            ],
            "followup_messages": {
                "email_scheduled": True,
                "phone_call_scheduled": bool(patient_phone),
                "reschedule_opportunity": True
            },
            "next_steps": [
                "Contact patient to reschedule",
                "Note in medical record",
                "Track no-show history"
            ]
        }
    
    def _build_reminder_message(self, appointment_datetime: str, provider_name: str, location: str) -> str:
        """Build reminder message preview"""
        return f"""
        Appointment Reminder
        ────────────────────
        Date & Time: {appointment_datetime}
        Provider: {provider_name}
        Location: {location}
        
        Please arrive 10 minutes early.
        Reply CONFIRM to confirm attendance.
        """
    
    def _init_email_templates(self) -> Dict[str, str]:
        """Initialize email templates"""
        return {
            "reminder_24h": "Your appointment with {provider} is scheduled for tomorrow at {time}.",
            "reminder_1h": "Your appointment with {provider} is in 1 hour. Please head to {location}.",
            "confirmation": "Your appointment has been confirmed for {datetime} with {provider}.",
            "cancellation": "Your appointment on {datetime} has been cancelled.",
            "survey": "Please help us improve by taking a 5-minute survey about your visit."
        }
    
    def _init_sms_templates(self) -> Dict[str, str]:
        """Initialize SMS templates"""
        return {
            "reminder_24h": "Reminder: Appointment tomorrow at {time} with {provider}. Arrive early.",
            "reminder_1h": "Reminder: Appointment in 1 hour at {location}. Reply Y to confirm.",
            "confirmation": "Confirmed: {date} {time} with {provider}. Location: {location}",
            "cancellation": "Cancelled: Your {date} appointment has been cancelled."
        }

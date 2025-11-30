"""Orchestrator Agent - Routes requests to appropriate sub-agents"""

import logging
from typing import Any, Dict, Optional
from datetime import datetime
import asyncio
from .base_agent import BaseAgent

logger = logging.getLogger(__name__)

class OrchestratorAgent(BaseAgent):
    """
    Master orchestrator agent that:
    - Routes patient requests to appropriate sub-agents
    - Manages workflow state and session context
    - Aggregates responses from sub-agents
    - Handles error recovery and fallbacks
    """
    
    def __init__(self):
        super().__init__(
            name="Orchestrator",
            description="Master agent that routes requests to specialized agents"
        )
        self.sub_agents = {}
        self.request_id_counter = 0
    
    async def process(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process incoming request by routing to appropriate agent(s)
        
        Args:
            request: Dictionary containing request details with keys:
                - patient_id or patient_info: Patient identification
                - request_type: Type of request (appointment, intake, verify, etc.)
                - details: Request-specific details
                - session_id: Optional existing session ID
        
        Returns:
            Response dictionary with aggregated results from sub-agents
        """
        self.request_id_counter += 1
        request_id = f"REQ_{datetime.utcnow().timestamp()}_{self.request_id_counter}"
        
        logger.info(f"[{request_id}] Orchestrator processing request: {request.get('request_type')}")
        
        try:
            # Classify the request
            request_type = request.get("request_type", "unknown")
            session_id = request.get("session_id", request_id)
            
            # Route to appropriate agent(s)
            response = await self._route_request(request_type, request, request_id, session_id)
            
            # Log the orchestration
            self.log_action("route_request", {
                "request_id": request_id,
                "request_type": request_type,
                "success": response.get("success", False)
            })
            
            return response
        
        except Exception as e:
            logger.error(f"[{request_id}] Orchestrator error: {str(e)}")
            return {
                "request_id": request_id,
                "success": False,
                "error": str(e),
                "message": "Failed to process request"
            }
    
    async def _route_request(
        self, 
        request_type: str, 
        request: Dict[str, Any],
        request_id: str,
        session_id: str
    ) -> Dict[str, Any]:
        """
        Route request to appropriate agent(s)
        
        Supported request types:
        - new_patient_appointment: Route to Intake + Scheduling (parallel)
        - schedule_appointment: Route to Scheduling
        - reschedule_appointment: Route to Scheduling
        - verify_insurance: Route to Verification
        - get_records: Route to Records
        - send_reminder: Route to Followup
        """
        
        routing_map = {
            "new_patient_appointment": self._handle_new_patient,
            "schedule_appointment": self._handle_schedule,
            "reschedule_appointment": self._handle_reschedule,
            "verify_insurance": self._handle_verify,
            "get_records": self._handle_records,
            "send_reminder": self._handle_reminder,
            "intake_form": self._handle_intake,
        }
        
        handler = routing_map.get(request_type)
        
        if not handler:
            logger.warning(f"[{request_id}] Unknown request type: {request_type}")
            return {
                "request_id": request_id,
                "success": False,
                "error": f"Unknown request type: {request_type}",
                "supported_types": list(routing_map.keys())
            }
        
        return await handler(request, request_id, session_id)
    
    async def _handle_new_patient(
        self, 
        request: Dict[str, Any], 
        request_id: str,
        session_id: str
    ) -> Dict[str, Any]:
        """Handle new patient appointment - Intake + Scheduling in parallel"""
        logger.info(f"[{request_id}] Routing to Intake + Scheduling agents (parallel)")
        
        # TODO: Implement parallel execution of Intake and Scheduling agents
        return {
            "request_id": request_id,
            "session_id": session_id,
            "success": True,
            "message": "New patient appointment workflow initiated",
            "agents_involved": ["Intake", "Scheduling", "Verification"],
            "workflow_steps": [
                "Parse patient intake form",
                "Query provider availability",
                "Verify insurance coverage",
                "Send appointment confirmation"
            ]
        }
    
    async def _handle_schedule(
        self, 
        request: Dict[str, Any], 
        request_id: str,
        session_id: str
    ) -> Dict[str, Any]:
        """Handle appointment scheduling"""
        logger.info(f"[{request_id}] Routing to Scheduling agent")
        
        # TODO: Implement Scheduling agent call
        return {
            "request_id": request_id,
            "session_id": session_id,
            "success": True,
            "message": "Appointment scheduling initiated",
            "agents_involved": ["Scheduling"]
        }
    
    async def _handle_reschedule(
        self, 
        request: Dict[str, Any], 
        request_id: str,
        session_id: str
    ) -> Dict[str, Any]:
        """Handle appointment rescheduling"""
        logger.info(f"[{request_id}] Routing to Scheduling + Followup agents")
        
        # TODO: Implement rescheduling workflow
        return {
            "request_id": request_id,
            "session_id": session_id,
            "success": True,
            "message": "Appointment rescheduling initiated",
            "agents_involved": ["Scheduling", "Followup"]
        }
    
    async def _handle_verify(
        self, 
        request: Dict[str, Any], 
        request_id: str,
        session_id: str
    ) -> Dict[str, Any]:
        """Handle insurance verification"""
        logger.info(f"[{request_id}] Routing to Verification agent")
        
        # TODO: Implement Verification agent call
        return {
            "request_id": request_id,
            "session_id": session_id,
            "success": True,
            "message": "Insurance verification initiated",
            "agents_involved": ["Verification"]
        }
    
    async def _handle_records(
        self, 
        request: Dict[str, Any], 
        request_id: str,
        session_id: str
    ) -> Dict[str, Any]:
        """Handle records retrieval"""
        logger.info(f"[{request_id}] Routing to Records agent")
        
        # TODO: Implement Records agent call
        return {
            "request_id": request_id,
            "session_id": session_id,
            "success": True,
            "message": "Records retrieval initiated",
            "agents_involved": ["Records"]
        }
    
    async def _handle_reminder(
        self, 
        request: Dict[str, Any], 
        request_id: str,
        session_id: str
    ) -> Dict[str, Any]:
        """Handle appointment reminder"""
        logger.info(f"[{request_id}] Routing to Followup agent")
        
        # TODO: Implement Followup agent call
        return {
            "request_id": request_id,
            "session_id": session_id,
            "success": True,
            "message": "Reminder scheduling initiated",
            "agents_involved": ["Followup"]
        }
    
    async def _handle_intake(
        self, 
        request: Dict[str, Any], 
        request_id: str,
        session_id: str
    ) -> Dict[str, Any]:
        """Handle patient intake form submission"""
        logger.info(f"[{request_id}] Routing to Intake agent")
        
        # TODO: Implement Intake agent call
        return {
            "request_id": request_id,
            "session_id": session_id,
            "success": True,
            "message": "Patient intake processing initiated",
            "agents_involved": ["Intake"]
        }

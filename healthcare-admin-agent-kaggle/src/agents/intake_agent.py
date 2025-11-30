"""Intake Agent - Process patient information and medical history"""

import logging
from typing import Any, Dict
from datetime import datetime
from .base_agent import BaseAgent
from src.models.schemas import PatientIntakeRequest

logger = logging.getLogger(__name__)

class IntakeAgent(BaseAgent):
    """
    Intake Agent processes new patient information including:
    - Parsing intake forms
    - Extracting demographics and medical history
    - Validating data completeness
    - Storing patient profiles in database
    - Flagging missing information
    """
    
    def __init__(self):
        super().__init__(
            name="IntakeAgent",
            description="Processes patient intake forms and medical history"
        )
        self.required_fields = [
            "first_name", "last_name", "email", "phone", 
            "date_of_birth", "insurance_provider", "insurance_id"
        ]
        self.optional_fields = [
            "middle_name", "gender", "address", "medical_history", 
            "allergies", "current_medications"
        ]
    
    async def process(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process patient intake request
        
        Args:
            request: Contains patient_info with form data
        
        Returns:
            Response with patient_id and validation results
        """
        request_id = request.get("request_id", "INTAKE_REQUEST")
        patient_info = request.get("patient_info", {})
        
        logger.info(f"[{request_id}] Intake Agent processing: {patient_info.get('first_name')} {patient_info.get('last_name')}")
        
        try:
            # Step 1: Validate required fields
            validation_result = self._validate_intake_data(patient_info)
            if not validation_result["is_valid"]:
                logger.warning(f"[{request_id}] Validation failed: {validation_result['missing_fields']}")
                return {
                    "success": False,
                    "error": "Missing required fields",
                    "missing_fields": validation_result["missing_fields"],
                    "message": "Please provide all required information"
                }
            
            # Step 2: Parse and structure intake data
            parsed_data = self._parse_intake_form(patient_info)
            
            # Step 3: Extract critical information
            critical_info = self._extract_critical_info(parsed_data)
            
            # Step 4: Generate patient ID
            patient_id = self._generate_patient_id()
            
            # Step 5: Store in database (mock)
            store_result = self._store_patient_record(patient_id, parsed_data)
            
            # Log the action
            self.log_action("intake_processed", {
                "request_id": request_id,
                "patient_id": patient_id,
                "patient_name": f"{parsed_data['first_name']} {parsed_data['last_name']}",
                "validation_passed": True,
                "allergies_count": len(parsed_data.get("allergies", [])),
                "medications_count": len(parsed_data.get("current_medications", []))
            })
            
            return {
                "success": True,
                "patient_id": patient_id,
                "patient_name": f"{parsed_data['first_name']} {parsed_data['last_name']}",
                "email": parsed_data["email"],
                "phone": parsed_data["phone"],
                "date_of_birth": parsed_data["date_of_birth"],
                "insurance_provider": parsed_data["insurance_provider"],
                "insurance_id": parsed_data["insurance_id"],
                "critical_info": critical_info,
                "status": "intake_complete",
                "next_steps": ["Insurance Verification", "Schedule Appointment"],
                "message": f"Patient {parsed_data['first_name']} {parsed_data['last_name']} registered successfully"
            }
        
        except Exception as e:
            logger.error(f"[{request_id}] Intake Agent error: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to process intake form"
            }
    
    def _validate_intake_data(self, patient_info: Dict[str, Any]) -> Dict[str, Any]:
        """Validate that all required fields are present"""
        missing_fields = []
        for field in self.required_fields:
            if field not in patient_info or not patient_info[field]:
                missing_fields.append(field)
        
        return {
            "is_valid": len(missing_fields) == 0,
            "missing_fields": missing_fields,
            "fields_provided": len([f for f in self.required_fields if f in patient_info])
        }
    
    def _parse_intake_form(self, patient_info: Dict[str, Any]) -> Dict[str, Any]:
        """Parse and structure intake form data"""
        return {
            "first_name": patient_info.get("first_name", "").strip(),
            "last_name": patient_info.get("last_name", "").strip(),
            "middle_name": patient_info.get("middle_name", "").strip(),
            "email": patient_info.get("email", "").lower(),
            "phone": patient_info.get("phone", "").strip(),
            "date_of_birth": patient_info.get("date_of_birth"),
            "gender": patient_info.get("gender", "Not specified"),
            "address": patient_info.get("address", ""),
            "city": patient_info.get("city", ""),
            "state": patient_info.get("state", ""),
            "zip_code": patient_info.get("zip_code", ""),
            "medical_history": patient_info.get("medical_history", ""),
            "allergies": patient_info.get("allergies", []) or [],
            "current_medications": patient_info.get("current_medications", []) or [],
            "insurance_provider": patient_info.get("insurance_provider", "").strip(),
            "insurance_id": patient_info.get("insurance_id", "").strip(),
            "insurance_group_number": patient_info.get("insurance_group_number", "").strip(),
            "created_at": datetime.utcnow().isoformat()
        }
    
    def _extract_critical_info(self, parsed_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract critical health information for quick reference"""
        critical_flags = []
        
        # Check for critical allergies
        high_risk_allergies = ["penicillin", "latex", "severe"]
        for allergy in parsed_data.get("allergies", []):
            if any(risk in allergy.lower() for risk in high_risk_allergies):
                critical_flags.append(f"⚠️ CRITICAL ALLERGY: {allergy}")
        
        # Check for critical medical conditions
        high_risk_conditions = ["diabetes", "heart", "cancer", "asthma"]
        history = parsed_data.get("medical_history", "").lower()
        for condition in high_risk_conditions:
            if condition in history:
                critical_flags.append(f"⚠️ SIGNIFICANT CONDITION: {condition}")
        
        return {
            "allergies": parsed_data.get("allergies", []),
            "medical_conditions": parsed_data.get("medical_history", "").split(",") if parsed_data.get("medical_history") else [],
            "current_medications": parsed_data.get("current_medications", []),
            "critical_flags": critical_flags,
            "requires_special_attention": len(critical_flags) > 0
        }
    
    def _generate_patient_id(self) -> str:
        """Generate unique patient ID"""
        import uuid
        return f"PAT_{uuid.uuid4().hex[:8].upper()}"
    
    def _store_patient_record(self, patient_id: str, patient_data: Dict[str, Any]) -> Dict[str, Any]:
        """Store patient record in database (mock implementation)"""
        logger.info(f"Storing patient record: {patient_id}")
        
        # TODO: Implement actual database storage
        # - Insert into PostgreSQL patients table
        # - Cache in Redis for fast lookup
        # - Log to audit trail
        
        return {
            "success": True,
            "patient_id": patient_id,
            "stored_at": datetime.utcnow().isoformat(),
            "record_type": "complete_intake"
        }

"""Insurance Verification Agent - Verify coverage and eligibility"""

import logging
from typing import Any, Dict
from datetime import datetime

from .base_agent import BaseAgent

logger = logging.getLogger(__name__)

class VerificationAgent(BaseAgent):
    """
    Insurance Verification Agent:
    - Verifies patient insurance coverage
    - Checks eligibility for services
    - Calculates copay and deductible
    - Estimates appointment costs
    - Identifies coverage gaps
    """
    
    def __init__(self):
        super().__init__(
            name="VerificationAgent",
            description="Verifies insurance coverage and eligibility"
        )
        self.insurance_providers = self._init_mock_insurance_db()
    
    async def process(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process insurance verification request
        
        Args:
            request: Contains insurance details
        
        Returns:
            Response with verification results
        """
        request_id = request.get("request_id", "VERIFY_REQUEST")
        
        logger.info(f"[{request_id}] Verification Agent processing insurance check")
        
        try:
            insurance_provider = request.get("insurance_provider", "").strip()
            insurance_id = request.get("insurance_id", "").strip()
            patient_id = request.get("patient_id")
            
            # Validate inputs
            if not insurance_provider or not insurance_id:
                return {
                    "success": False,
                    "error": "Missing insurance provider or ID",
                    "is_eligible": False
                }
            
            # Check insurance eligibility
            verification_result = self._verify_eligibility(
                insurance_provider,
                insurance_id
            )
            
            if not verification_result["is_eligible"]:
                self.log_action("insurance_verification_failed", {
                    "request_id": request_id,
                    "patient_id": patient_id,
                    "insurance_provider": insurance_provider,
                    "reason": verification_result.get("reason", "Unknown")
                })
                
                return {
                    "success": False,
                    "is_eligible": False,
                    "error": verification_result.get("reason", "Insurance verification failed"),
                    "coverage_status": "inactive",
                    "message": "Insurance coverage not active or invalid",
                    "action_items": [
                        "Verify insurance information with patient",
                        "Check for alternative coverage",
                        "Consider uninsured pricing"
                    ]
                }
            
            # Calculate costs
            cost_estimate = self._estimate_costs(insurance_provider, insurance_id)
            
            self.log_action("insurance_verified", {
                "request_id": request_id,
                "patient_id": patient_id,
                "insurance_provider": insurance_provider,
                "copay": cost_estimate.get("copay")
            })
            
            return {
                "success": True,
                "patient_id": patient_id,
                "is_eligible": True,
                "coverage_status": "active",
                "insurance_provider": insurance_provider,
                "insurance_id": insurance_id,
                "coverage_details": self.insurance_providers.get(
                    insurance_provider, {}
                ).get("coverage", {}),
                "copay": cost_estimate["copay"],
                "coinsurance": cost_estimate["coinsurance"],
                "deductible": cost_estimate["deductible"],
                "deductible_met": cost_estimate["deductible_met"],
                "out_of_pocket_max": cost_estimate["out_of_pocket_max"],
                "estimated_appointment_cost": cost_estimate["estimated_appointment_cost"],
                "verification_timestamp": datetime.utcnow().isoformat(),
                "valid_through": "2025-12-31",
                "message": "Insurance verified successfully",
                "action_items": [
                    "Proceed with appointment booking",
                    "Inform patient of copay amount",
                    "Schedule appointment confirmation"
                ],
                "disclaimers": [
                    "This is an estimate based on information available",
                    "Actual costs may vary based on specific services",
                    "Patient may have balance due after insurance processing"
                ]
            }
        
        except Exception as e:
            logger.error(f"[{request_id}] Verification Agent error: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to verify insurance"
            }
    
    def _verify_eligibility(self, provider: str, insurance_id: str) -> Dict[str, Any]:
        """Verify insurance eligibility"""
        # Mock verification - in production, would call insurance API
        
        if provider.upper() not in self.insurance_providers:
            return {
                "is_eligible": False,
                "reason": f"Insurance provider '{provider}' not found in system"
            }
        
        # Check insurance ID format
        if not insurance_id or len(insurance_id) < 6:
            return {
                "is_eligible": False,
                "reason": "Invalid insurance ID format"
            }
        
        # Mock: Verify status (90% of IDs are valid)
        import hashlib
        hash_value = int(hashlib.md5(insurance_id.encode()).hexdigest(), 16)
        is_valid = (hash_value % 100) < 90
        
        if not is_valid:
            return {
                "is_eligible": False,
                "reason": "Insurance coverage is inactive or expired"
            }
        
        return {
            "is_eligible": True
        }
    
    def _estimate_costs(self, provider: str, insurance_id: str) -> Dict[str, Any]:
        """Estimate appointment costs"""
        provider_data = self.insurance_providers.get(provider, {})
        coverage = provider_data.get("coverage", {})
        
        return {
            "copay": coverage.get("office_visit_copay", 30),
            "coinsurance": coverage.get("coinsurance_percentage", 20),
            "deductible": coverage.get("annual_deductible", 1000),
            "deductible_met": coverage.get("deductible_met", 500),
            "out_of_pocket_max": coverage.get("out_of_pocket_max", 5000),
            "estimated_appointment_cost": coverage.get("office_visit_copay", 30)
        }
    
    def _init_mock_insurance_db(self) -> Dict[str, Dict[str, Any]]:
        """Initialize mock insurance provider database"""
        return {
            "BLUE SHIELD": {
                "name": "Blue Shield of California",
                "coverage": {
                    "office_visit_copay": 30,
                    "specialist_copay": 50,
                    "prescription_copay": 10,
                    "emergency_copay": 250,
                    "coinsurance_percentage": 20,
                    "annual_deductible": 1000,
                    "deductible_met": 500,
                    "out_of_pocket_max": 5000
                }
            },
            "AETNA": {
                "name": "Aetna Health",
                "coverage": {
                    "office_visit_copay": 25,
                    "specialist_copay": 45,
                    "prescription_copay": 15,
                    "emergency_copay": 300,
                    "coinsurance_percentage": 15,
                    "annual_deductible": 750,
                    "deductible_met": 400,
                    "out_of_pocket_max": 4500
                }
            },
            "UNITED": {
                "name": "UnitedHealth Group",
                "coverage": {
                    "office_visit_copay": 35,
                    "specialist_copay": 60,
                    "prescription_copay": 20,
                    "emergency_copay": 350,
                    "coinsurance_percentage": 25,
                    "annual_deductible": 1200,
                    "deductible_met": 600,
                    "out_of_pocket_max": 5500
                }
            },
            "CIGNA": {
                "name": "Cigna Health",
                "coverage": {
                    "office_visit_copay": 28,
                    "specialist_copay": 48,
                    "prescription_copay": 12,
                    "emergency_copay": 280,
                    "coinsurance_percentage": 18,
                    "annual_deductible": 950,
                    "deductible_met": 550,
                    "out_of_pocket_max": 4800
                }
            }
        }

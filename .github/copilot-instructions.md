# Copilot Instructions for Healthcare Administrative Assistant Agent

## Project Overview

This is a **multi-agent AI system** that automates healthcare administrative workflows (patient intake, appointment scheduling, insurance verification, records management, and follow-ups) using Google's Gemini API and Google Agent Development Kit (ADK).

## Architecture

### Core Pattern: Orchestrator with Specialized Agents

```
OrchestratorAgent (request router/controller)
  ├─ IntakeAgent (patient data validation & storage)
  ├─ SchedulingAgent (appointment booking/management)
  ├─ VerificationAgent (insurance eligibility checks)
  ├─ FollowupAgent (reminders & post-visit communications)
  └─ RecordsAgent (patient record retrieval & organization)
```

**Key Design Decision:** The Orchestrator (`src/agents/orchestrator.py`) routes ALL incoming requests to appropriate agents. It maintains session context across the workflow and coordinates multi-agent workflows (e.g., new patient appointments run Intake → Scheduling → Verification in sequence).

### Agent Pattern

All agents inherit from `BaseAgent` (`src/agents/base_agent.py`):

```python
class BaseAgent(ABC):
    async def process(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """All agents implement this async method"""
        pass
    
    def set_session_context(self, session_id: str, context: Dict[str, Any]):
        """Agents receive shared session context from Orchestrator"""
        pass
    
    def log_action(self, action: str, details: Dict[str, Any]):
        """Audit logging pattern - all agent actions are logged"""
        pass
```

**Request Pattern:** Each agent receives a dict with `request_type`, `request_id`, `patient_id`, and action-specific details. Each returns a response dict with `success` boolean and action-specific data.

## Critical Data Models

All request/response validation uses **Pydantic models** (`src/models/schemas.py`):

- `PatientIntakeRequest` - validates first/last name, email, phone (regex: `^\+?1?\d{9,15}$`), address, medical history, allergies, medications, insurance details
- `AppointmentRequest` - includes `appointment_type` (enum: checkup/followup/consultation/procedure), preferred date/provider
- `AppointmentStatus` enum: scheduled → confirmed → completed (or cancelled/rescheduled)
- `InsuranceVerificationRequest/Response` - tracks eligibility, copay, deductible

**Critical: All schemas use `EmailStr` from pydantic, phone validation regex, and datetime ISO format for appointments.**

## Key Workflows

### Workflow 1: New Patient Appointment (3-step)
1. **Intake** - Parse patient form, validate fields, extract critical info (allergies: penicillin/latex, conditions: diabetes/heart/cancer), generate `PAT_{UUID}`
2. **Scheduling** - Query availability, check for conflicts, book appointment as `APT_{UUID}`
3. **Verification** - Check insurance coverage, calculate copay ($25-$35 office, $40-$75 specialist), deductible ($750-$1200)
4. **Confirmation** - Orchestrator aggregates results, sends confirmation

### Workflow 2: Appointment Reschedule (2-step)
- Scheduling Agent cancels old appointment, books new slot
- Followup Agent reschedules reminders

### Workflow 3: Automated Reminders
- Followup Agent schedules reminders at 24h and 1h before appointment
- Multi-channel delivery: email + SMS
- Can be cancelled/rescheduled with `schedule_reminder` action

## Development Patterns

### Request/Response Flow

**Orchestrator routes based on `request_type`:**
- `"new_patient_intake"` → IntakeAgent
- `"schedule_appointment"`, `"check_availability"`, `"reschedule"`, `"cancel"` → SchedulingAgent  
- `"verify_insurance"` → VerificationAgent
- `"schedule_reminder"`, `"send_followup"` → FollowupAgent

**Example orchestrator routing:**
```python
async def _route_request(self, request_type: str, request: Dict[str, Any], request_id: str, session_id: str):
    if request_type == "new_patient_intake":
        return await self.intake_agent.process(request)
    elif request_type in ["schedule_appointment", "check_availability"]:
        return await self.scheduling_agent.process(request)
```

### Session Context Pattern

Agents receive `session_id` + shared `context` dict from Orchestrator. This allows multi-step workflows to share data:
- Intake stores `patient_id`, medical flags, insurance info
- Scheduling retrieves `patient_id` from context for booking
- Verification uses `patient_id` to check coverage

### Error Handling Strategy

All agents wrap processing in try-except:
```python
try:
    # agent logic
    return {"success": True, "request_id": request_id, ...action_data}
except Exception as e:
    logger.error(f"Agent error: {str(e)}")
    return {"success": False, "error": str(e), "message": "Human-readable error"}
```

### Logging & Audit Trail

Use Python's `logging` module (imported in all agents). The `log_action()` method creates audit entries with:
- timestamp (ISO format)
- agent name
- action type
- session_id
- details dict

**Critical for healthcare compliance:** All actions that modify patient data must be logged.

## Database/Mock Data Patterns

The system uses **mock databases** (not real DB integration yet):

- **Providers** - `MockProviderDB` with 3 providers (Dr. Smith, Dr. Johnson, Dr. Williams)
- **Appointments** - stored by `APT_*` ID with patient/provider/datetime/status
- **Insurance** - mock database of 4 major providers (Blue Shield, Aetna, United, Cigna)
- **Patients** - stored by `PAT_*` ID with demographics, medical history, insurance

When implementing real database integration, maintain the same ID generation pattern (`PAT_{UUID}`, `APT_{UUID}`).

## Configuration & Dependencies

**Key Dependencies (`requirements.txt`):**
- `google-generativeai==0.6.0` - Gemini API
- `google-cloud-agentic-engine==0.0.1` - ADK
- `pydantic==2.5.0` - Schema validation
- `python-dotenv==1.0.0` - Environment variables
- `google-api-python-client==1.12.5` - Calendar/other Google APIs

**Environment Variables** (from `.env.example`):
- `GOOGLE_API_KEY` - Gemini API key
- `PROVIDER_API_KEY`, `INSURANCE_API_KEY` - external API credentials
- `DATABASE_URL` - PostgreSQL connection (when DB integration added)

## Running & Testing

**Entry point:** `src/main.py` - Demonstrates all 3 workflows end-to-end via `HealthcareAgentSystem` class

**Run example:** 
```bash
python src/main.py
```

**Test structure:** `tests/` directory exists but test files not yet added. Follow Pydantic validation pattern + mock data approach when adding tests.

## API Tools Reference

The system declares ~15 tools in `docs/API_SPECIFICATION.md` that agents will call:
- **Calendar:** `get_provider_availability`, `book_appointment`, `cancel_appointment`
- **Records:** `retrieve_patient_records`, `store_patient_intake`
- **Insurance:** `verify_insurance_eligibility`, `estimate_appointment_cost`
- **Notifications:** `send_email`, `send_sms`, `schedule_reminder`
- **Database:** `get_patient_by_id`, `get_appointment_by_id`, etc.

These are documented but not yet wired to real Google Calendar/insurance APIs. When implementing, match the OpenAPI schemas in the specification.

## Conventions

- **Session ID:** Unique identifier for multi-step workflows, passed from Orchestrator to all sub-agents
- **Request ID:** `REQ_{timestamp}_{counter}` for individual requests, used in logging
- **Date Format:** ISO 8601 (yyyy-MM-ddThh:mm:ss) for all datetime fields
- **Phone Validation:** regex `^\+?1?\d{9,15}$` (supports international formats)
- **Status Enums:** Use defined enums (AppointmentStatus) - never magic strings
- **Async/Await:** All agent methods are async; workflows use `asyncio.gather()` for parallel agents
- **Healthcare Flags:** Critical flags (penicillin/latex allergies, serious conditions) must be extracted during intake

## Common Customization Points

When adding features:

1. **New agent type?** Extend `BaseAgent`, implement `async def process()`, add routing case in Orchestrator
2. **New appointment action?** Add case to SchedulingAgent (check `appointment_action` in request)
3. **New data field?** Update Pydantic schema in `schemas.py`, then adjust Intake/Verification agents
4. **New workflow?** Orchestrator's `_route_request()` handles routing; add multi-step logic in `main.py` demo
5. **New tool?** Document OpenAPI spec in `docs/API_SPECIFICATION.md`, then implement in appropriate agent

## Healthcare & Compliance Notes

- **HIPAA:** All patient data handling must be logged (audit trail)
- **PII:** Phone, email, SSN should be validated (already have EmailStr + regex)
- **Allergies/Flags:** Critical medical info flagged during intake (hardcoded flags for penicillin, latex, serious conditions)
- **Insurance:** Verification response includes eligibility + copay/deductible estimates

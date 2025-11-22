# Healthcare Administrative Assistant Agent

A multi-agent AI system that automates healthcare administrative tasks including appointment scheduling, patient intake, records management, insurance verification, and appointment follow-ups.

## Project Overview

**Track:** Agents for Good (Healthcare)  
**Problem:** Healthcare providers spend 20-40% of time on administrative tasks, reducing patient care quality and increasing burnout.  
**Solution:** Multi-agent system powered by Google Gemini that automates key administrative workflows.

## Features

- **Orchestrator Agent** - Routes requests to appropriate specialized agents
- **Intake Agent** - Processes patient information and medical history
- **Scheduling Agent** - Manages appointment booking and rescheduling
- **Insurance Verification Agent** - Verifies coverage and eligibility
- **Records Management Agent** - Organizes and retrieves patient records
- **Followup Agent** - Sends reminders and post-visit communications

## Technology Stack

- **LLM:** Google Gemini API
- **Framework:** Google Agent Development Kit (ADK)
- **Language:** Python 3.10+
- **Deployment:** Google Cloud Run
- **Databases:** PostgreSQL, Redis, Firestore
- **APIs:** Google Calendar, HL7 FHIR, Twilio, SendGrid

## Project Structure

```
healthcare-admin-agent/
├── src/
│   ├── agents/
│   │   ├── orchestrator.py
│   │   ├── intake_agent.py
│   │   ├── scheduling_agent.py
│   │   ├── verification_agent.py
│   │   ├── records_agent.py
│   │   └── followup_agent.py
│   ├── tools/
│   │   ├── calendar_tools.py
│   │   ├── ehr_tools.py
│   │   ├── notification_tools.py
│   │   ├── insurance_tools.py
│   │   └── database_tools.py
│   ├── models/
│   │   ├── patient.py
│   │   ├── appointment.py
│   │   └── schemas.py
│   └── main.py
├── tests/
│   ├── test_agents.py
│   ├── test_tools.py
│   └── test_workflows.py
├── docs/
│   └── ARCHITECTURE.md
├── requirements.txt
├── .env.example
├── Dockerfile
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.10+
- Google Cloud Project with ADK enabled
- API Keys (Gemini, Calendar, Insurance APIs)

### Installation

1. Clone the repository
```bash
git clone https://github.com/yourusername/healthcare-admin-agent.git
cd healthcare-admin-agent
```

2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Configure environment variables
```bash
cp .env.example .env
# Edit .env with your API keys and configuration
```

5. Run the application
```bash
python src/main.py
```

## Usage

### Starting the Agent

```python
from src.agents.orchestrator import OrchestratorAgent

agent = OrchestratorAgent()
response = agent.process_request("I need to schedule a new patient appointment")
print(response)
```

### Example Workflows

#### New Patient Appointment
```
User: "I'm new and want to schedule a checkup next week"
→ Orchestrator routes to Intake + Scheduling agents (parallel)
→ Insurance Verification agent confirms coverage
→ Confirmation sent via email + calendar invite
```

#### Reschedule Appointment
```
User: "I need to reschedule my Thursday appointment"
→ Orchestrator routes to Scheduling agent
→ Followup agent cancels old reminder + schedules new one
```

## Configuration

### Environment Variables

See `.env.example` for required configuration:

- `GOOGLE_API_KEY` - Google Gemini API key
- `DATABASE_URL` - PostgreSQL connection string
- `REDIS_URL` - Redis cache connection
- `TWILIO_ACCOUNT_SID` - SMS gateway credentials
- `INSURANCE_API_KEY` - Insurance verification API key

## Testing

Run the test suite:
```bash
pytest tests/
```

Run with coverage:
```bash
pytest tests/ --cov=src
```

## Deployment

### Deploy to Google Cloud Run

```bash
gcloud builds submit --tag gcr.io/PROJECT_ID/healthcare-admin-agent
gcloud run deploy healthcare-admin-agent \
  --image gcr.io/PROJECT_ID/healthcare-admin-agent \
  --platform managed \
  --region us-central1
```

## API Documentation

### Agent Endpoints

- `POST /schedule` - Schedule new appointment
- `POST /reschedule` - Reschedule existing appointment
- `POST /verify-insurance` - Verify insurance coverage
- `GET /appointments/{patient_id}` - Get patient appointments
- `GET /records/{patient_id}` - Retrieve patient records

## Architecture

For detailed architecture documentation, see [ARCHITECTURE.md](docs/ARCHITECTURE.md)

## Agent Concepts Implemented

✅ **Multi-Agent System**
- Sequential agents (Intake → Scheduling → Verification)
- Parallel agents (Intake & Scheduling concurrent execution)
- Loop agents (Followup on schedule)
- Master orchestrator for routing

✅ **Tools**
- Custom tools for calendar, EHR, notifications, insurance
- Built-in Google Search for insurance plan info
- OpenAPI integration for external services

✅ **Sessions & Memory**
- Session-based patient context tracking
- Long-term memory for patient history
- Cache for frequent queries

## Compliance & Security

- HIPAA-compliant logging and audit trails
- No API keys or sensitive data in code
- Encrypted data in transit and at rest
- Role-based access control

## Performance Targets

- Appointment booking: < 2 minutes
- Insurance verification success: > 95%
- Reminder delivery: > 98%
- No-show reduction: 15-20% improvement
- System uptime: > 99.5%

## Contributing

Contributions welcome! Please follow the development guidelines and submit pull requests.

## License

MIT License - see LICENSE file for details

## Contact

For questions or issues, please open a GitHub issue or contact the development team.

## Acknowledgments

- Google AI Studio and ADK for agent development framework
- Course instructors from Google AI Agents Intensive
- Healthcare industry advisors for domain expertise

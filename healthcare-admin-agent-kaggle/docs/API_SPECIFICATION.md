"""Detailed API Specification for Healthcare Administrative Assistant Agent"""

# API SPECIFICATION
# Healthcare Administrative Assistant Agent
# Version 1.0

---

## 1. TOOL DEFINITIONS (OpenAPI Specifications)

### 1.1 Calendar Management Tools

#### Tool: `get_provider_availability`
**Purpose:** Query provider availability for appointment scheduling
**Input Schema:**
```json
{
  "type": "object",
  "properties": {
    "provider_id": {
      "type": "string",
      "description": "Healthcare provider identifier"
    },
    "date_range_start": {
      "type": "string",
      "format": "date-time",
      "description": "Start date for availability search"
    },
    "date_range_end": {
      "type": "string",
      "format": "date-time",
      "description": "End date for availability search"
    },
    "duration_minutes": {
      "type": "integer",
      "description": "Required appointment duration in minutes",
      "default": 30
    },
    "appointment_type": {
      "type": "string",
      "enum": ["checkup", "followup", "consultation", "procedure"],
      "description": "Type of appointment"
    }
  },
  "required": ["provider_id", "date_range_start", "date_range_end"]
}
```

**Output Schema:**
```json
{
  "type": "object",
  "properties": {
    "provider_id": {"type": "string"},
    "available_slots": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "start_time": {"type": "string", "format": "date-time"},
          "end_time": {"type": "string", "format": "date-time"},
          "location": {"type": "string"},
          "appointment_type": {"type": "string"}
        }
      }
    },
    "total_slots_found": {"type": "integer"},
    "next_available": {"type": "string", "format": "date-time"}
  }
}
```

**Error Handling:**
- 404: Provider not found
- 400: Invalid date range
- 503: Calendar service unavailable

---

#### Tool: `book_appointment`
**Purpose:** Book a confirmed appointment in the calendar system
**Input Schema:**
```json
{
  "type": "object",
  "properties": {
    "patient_id": {
      "type": "string",
      "description": "Patient identifier"
    },
    "provider_id": {
      "type": "string",
      "description": "Healthcare provider identifier"
    },
    "appointment_datetime": {
      "type": "string",
      "format": "date-time",
      "description": "Scheduled appointment time"
    },
    "appointment_type": {
      "type": "string",
      "enum": ["checkup", "followup", "consultation", "procedure", "urgent"]
    },
    "location": {
      "type": "string",
      "description": "Appointment location/clinic"
    },
    "notes": {
      "type": "string",
      "description": "Special notes or requirements"
    }
  },
  "required": ["patient_id", "provider_id", "appointment_datetime", "appointment_type"]
}
```

**Output Schema:**
```json
{
  "type": "object",
  "properties": {
    "appointment_id": {"type": "string"},
    "status": {"type": "string", "enum": ["scheduled", "confirmed", "failed"]},
    "appointment_datetime": {"type": "string", "format": "date-time"},
    "confirmation_token": {"type": "string"},
    "calendar_invite_sent": {"type": "boolean"},
    "message": {"type": "string"}
  }
}
```

---

#### Tool: `cancel_appointment`
**Purpose:** Cancel an existing appointment
**Input Schema:**
```json
{
  "type": "object",
  "properties": {
    "appointment_id": {"type": "string"},
    "reason": {"type": "string"},
    "notify_patient": {"type": "boolean", "default": true},
    "notify_provider": {"type": "boolean", "default": true}
  },
  "required": ["appointment_id"]
}
```

**Output Schema:**
```json
{
  "type": "object",
  "properties": {
    "appointment_id": {"type": "string"},
    "cancellation_status": {"type": "string", "enum": ["cancelled", "failed"]},
    "cancellation_time": {"type": "string", "format": "date-time"},
    "refund_status": {"type": "string"},
    "notifications_sent": {"type": "integer"}
  }
}
```

---

### 1.2 Patient Records & EHR Tools

#### Tool: `retrieve_patient_records`
**Purpose:** Retrieve patient medical records from EHR system
**Input Schema:**
```json
{
  "type": "object",
  "properties": {
    "patient_id": {"type": "string", "description": "Patient identifier"},
    "record_types": {
      "type": "array",
      "items": {
        "type": "string",
        "enum": ["visit_notes", "lab_results", "imaging", "medications", "allergies", "all"]
      },
      "description": "Specific record types to retrieve"
    },
    "date_range_start": {"type": "string", "format": "date", "description": "Optional: Start date"},
    "date_range_end": {"type": "string", "format": "date", "description": "Optional: End date"}
  },
  "required": ["patient_id"]
}
```

**Output Schema:**
```json
{
  "type": "object",
  "properties": {
    "patient_id": {"type": "string"},
    "records": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "record_id": {"type": "string"},
          "record_type": {"type": "string"},
          "record_date": {"type": "string", "format": "date"},
          "title": {"type": "string"},
          "content_summary": {"type": "string"},
          "critical_flags": {"type": "array", "items": {"type": "string"}},
          "file_url": {"type": "string"}
        }
      }
    },
    "total_records": {"type": "integer"},
    "allergies": {"type": "array", "items": {"type": "string"}},
    "current_medications": {"type": "array", "items": {"type": "string"}}
  }
}
```

---

#### Tool: `store_patient_intake`
**Purpose:** Store new patient intake information in the database
**Input Schema:**
```json
{
  "type": "object",
  "properties": {
    "first_name": {"type": "string"},
    "last_name": {"type": "string"},
    "email": {"type": "string", "format": "email"},
    "phone": {"type": "string", "pattern": "^\\+?1?\\d{9,15}$"},
    "date_of_birth": {"type": "string", "format": "date"},
    "gender": {"type": "string", "enum": ["M", "F", "Other", "Prefer not to say"]},
    "address": {"type": "string"},
    "city": {"type": "string"},
    "state": {"type": "string"},
    "zip_code": {"type": "string"},
    "medical_history": {"type": "string"},
    "allergies": {"type": "array", "items": {"type": "string"}},
    "current_medications": {"type": "array", "items": {"type": "string"}},
    "insurance_provider": {"type": "string"},
    "insurance_id": {"type": "string"},
    "insurance_group_number": {"type": "string"}
  },
  "required": ["first_name", "last_name", "email", "phone", "insurance_provider", "insurance_id"]
}
```

**Output Schema:**
```json
{
  "type": "object",
  "properties": {
    "patient_id": {"type": "string"},
    "status": {"type": "string", "enum": ["created", "updated", "failed"]},
    "message": {"type": "string"},
    "intake_complete": {"type": "boolean"},
    "missing_fields": {"type": "array", "items": {"type": "string"}},
    "next_steps": {"type": "array", "items": {"type": "string"}}
  }
}
```

---

### 1.3 Insurance Verification Tools

#### Tool: `verify_insurance_eligibility`
**Purpose:** Verify patient insurance coverage and eligibility
**Input Schema:**
```json
{
  "type": "object",
  "properties": {
    "patient_id": {"type": "string"},
    "insurance_provider": {"type": "string"},
    "insurance_id": {"type": "string"},
    "service_type": {
      "type": "string",
      "enum": ["office_visit", "procedure", "lab_work", "imaging", "prescription"]
    },
    "date_of_service": {"type": "string", "format": "date"}
  },
  "required": ["insurance_provider", "insurance_id"]
}
```

**Output Schema:**
```json
{
  "type": "object",
  "properties": {
    "is_eligible": {"type": "boolean"},
    "coverage_status": {"type": "string", "enum": ["active", "inactive", "suspended"]},
    "copay": {"type": "number"},
    "deductible": {"type": "number"},
    "deductible_met": {"type": "number"},
    "out_of_pocket_maximum": {"type": "number"},
    "out_of_pocket_used": {"type": "number"},
    "coverage_details": {
      "type": "object",
      "properties": {
        "office_visit_copay": {"type": "number"},
        "specialist_copay": {"type": "number"},
        "prescription_copay": {"type": "number"},
        "emergency_copay": {"type": "number"}
      }
    },
    "verification_timestamp": {"type": "string", "format": "date-time"},
    "message": {"type": "string"},
    "action_items": {"type": "array", "items": {"type": "string"}}
  }
}
```

---

#### Tool: `estimate_appointment_cost`
**Purpose:** Estimate patient costs for an appointment based on insurance
**Input Schema:**
```json
{
  "type": "object",
  "properties": {
    "patient_id": {"type": "string"},
    "appointment_type": {"type": "string", "enum": ["checkup", "followup", "consultation", "procedure"]},
    "provider_specialty": {"type": "string"},
    "estimated_procedure_cost": {"type": "number"}
  },
  "required": ["patient_id", "appointment_type"]
}
```

**Output Schema:**
```json
{
  "type": "object",
  "properties": {
    "patient_cost": {"type": "number"},
    "copay": {"type": "number"},
    "coinsurance": {"type": "number"},
    "deductible_applied": {"type": "number"},
    "estimated_total": {"type": "number"},
    "breakdown": {
      "type": "object",
      "properties": {
        "provider_charge": {"type": "number"},
        "insurance_covers": {"type": "number"},
        "patient_responsibility": {"type": "number"}
      }
    },
    "disclaimers": {"type": "array", "items": {"type": "string"}}
  }
}
```

---

### 1.4 Notification Tools

#### Tool: `send_email`
**Purpose:** Send email notifications to patient
**Input Schema:**
```json
{
  "type": "object",
  "properties": {
    "recipient_email": {"type": "string", "format": "email"},
    "subject": {"type": "string"},
    "template": {
      "type": "string",
      "enum": ["appointment_confirmation", "appointment_reminder", "insurance_verification", "documents_ready", "custom"]
    },
    "template_data": {
      "type": "object",
      "description": "Variables for email template"
    },
    "attachments": {
      "type": "array",
      "items": {"type": "string", "description": "File URLs to attach"}
    }
  },
  "required": ["recipient_email", "subject", "template"]
}
```

**Output Schema:**
```json
{
  "type": "object",
  "properties": {
    "email_id": {"type": "string"},
    "status": {"type": "string", "enum": ["sent", "queued", "failed"]},
    "recipient": {"type": "string"},
    "sent_timestamp": {"type": "string", "format": "date-time"},
    "delivery_status": {"type": "string"},
    "error_message": {"type": "string"}
  }
}
```

---

#### Tool: `send_sms`
**Purpose:** Send SMS reminder to patient
**Input Schema:**
```json
{
  "type": "object",
  "properties": {
    "phone_number": {"type": "string", "pattern": "^\\+?1?\\d{9,15}$"},
    "message": {"type": "string", "maxLength": 160},
    "message_type": {
      "type": "string",
      "enum": ["reminder_24h", "reminder_1h", "confirmation", "reschedule_notification"]
    },
    "appointment_id": {"type": "string"}
  },
  "required": ["phone_number", "message", "message_type"]
}
```

**Output Schema:**
```json
{
  "type": "object",
  "properties": {
    "sms_id": {"type": "string"},
    "status": {"type": "string", "enum": ["sent", "queued", "failed"]},
    "phone_number": {"type": "string"},
    "sent_timestamp": {"type": "string", "format": "date-time"},
    "delivery_status": {"type": "string"}
  }
}
```

---

#### Tool: `schedule_reminder`
**Purpose:** Schedule a reminder for future delivery
**Input Schema:**
```json
{
  "type": "object",
  "properties": {
    "appointment_id": {"type": "string"},
    "patient_id": {"type": "string"},
    "reminder_time": {"type": "string", "format": "date-time", "description": "When to send reminder"},
    "reminder_type": {"type": "string", "enum": ["email", "sms", "both"]},
    "appointment_datetime": {"type": "string", "format": "date-time"},
    "provider_name": {"type": "string"},
    "location": {"type": "string"}
  },
  "required": ["appointment_id", "reminder_time", "reminder_type"]
}
```

**Output Schema:**
```json
{
  "type": "object",
  "properties": {
    "reminder_id": {"type": "string"},
    "status": {"type": "string", "enum": ["scheduled", "failed"]},
    "appointment_id": {"type": "string"},
    "scheduled_send_time": {"type": "string", "format": "date-time"},
    "retry_count": {"type": "integer"},
    "message": {"type": "string"}
  }
}
```

---

### 1.5 Database Query Tools

#### Tool: `get_patient_by_id`
**Purpose:** Retrieve patient profile by ID
**Input Schema:**
```json
{
  "type": "object",
  "properties": {
    "patient_id": {"type": "string"}
  },
  "required": ["patient_id"]
}
```

**Output Schema:**
```json
{
  "type": "object",
  "properties": {
    "patient_id": {"type": "string"},
    "first_name": {"type": "string"},
    "last_name": {"type": "string"},
    "email": {"type": "string"},
    "phone": {"type": "string"},
    "date_of_birth": {"type": "string", "format": "date"},
    "insurance_provider": {"type": "string"},
    "insurance_id": {"type": "string"},
    "last_appointment": {"type": "string", "format": "date-time"},
    "upcoming_appointments": {"type": "integer"}
  }
}
```

---

#### Tool: `get_appointment_by_id`
**Purpose:** Retrieve appointment details
**Input Schema:**
```json
{
  "type": "object",
  "properties": {
    "appointment_id": {"type": "string"}
  },
  "required": ["appointment_id"]
}
```

**Output Schema:**
```json
{
  "type": "object",
  "properties": {
    "appointment_id": {"type": "string"},
    "patient_id": {"type": "string"},
    "patient_name": {"type": "string"},
    "provider_id": {"type": "string"},
    "provider_name": {"type": "string"},
    "appointment_datetime": {"type": "string", "format": "date-time"},
    "appointment_type": {"type": "string"},
    "location": {"type": "string"},
    "status": {"type": "string", "enum": ["scheduled", "confirmed", "completed", "cancelled"]},
    "notes": {"type": "string"},
    "insurance_verified": {"type": "boolean"},
    "reminders_scheduled": {"type": "array", "items": {"type": "string"}}
  }
}
```

---

## 2. WORKFLOW SPECIFICATIONS

### 2.1 New Patient Appointment Workflow

**Sequence:**
1. Orchestrator receives request type: `new_patient_appointment`
2. Route to **Intake Agent** (parallel)
   - Parse patient info from form/request
   - Validate completeness
   - Store in database → Returns patient_id
3. Route to **Scheduling Agent** (parallel with Intake)
   - Get provider availability
   - Hold appointment slot
4. Route to **Verification Agent** (sequential after Intake completes)
   - Verify insurance eligibility
   - Estimate costs
5. Route to **Followup Agent**
   - Schedule 24h reminder
   - Schedule 1h reminder
6. Send confirmation email + calendar invite

**Success Criteria:**
- patient_id created
- appointment_id scheduled
- Insurance verified
- Reminders queued

---

### 2.2 Reschedule Appointment Workflow

**Sequence:**
1. Orchestrator receives request type: `reschedule_appointment`
2. Route to **Scheduling Agent**
   - Retrieve current appointment
   - Release old time slot
   - Find new availability
   - Book new slot
3. Update appointment record
4. Route to **Followup Agent**
   - Cancel old reminders
   - Schedule new reminders for new time
5. Send updated confirmation

---

### 2.3 Insurance Verification Workflow

**Sequence:**
1. Route to **Verification Agent**
2. Check eligibility
3. Calculate copay/deductible
4. Estimate appointment cost
5. Update patient record
6. Alert patient if coverage gaps

---

## 3. ERROR HANDLING STRATEGY

| Error | Trigger | Handler | Fallback |
|-------|---------|---------|----------|
| Insurance API down | Verification timeout | Retry 3x with exponential backoff | Queue for manual review |
| Calendar unavailable | Scheduling timeout | Fallback dates offered | Email provider manually |
| Invalid patient data | Missing required fields | Prompt for missing info | Halt workflow, contact patient |
| Email/SMS fails | Notification timeout | Retry 2x after 5min | Log for manual follow-up |
| Insurance not found | API returns 404 | Search alternative providers | Uninsured rate applied |

---

## 4. RESPONSE TIME TARGETS

- **get_provider_availability:** < 2s
- **book_appointment:** < 3s
- **verify_insurance_eligibility:** < 5s (may retry)
- **send_email:** < 1s (async)
- **send_sms:** < 2s (async)
- **retrieve_patient_records:** < 4s

---

## 5. SECURITY & COMPLIANCE

### Data Protection
- No PHI in logs (use patient_id tokens only)
- Encrypt API responses in transit
- PII encrypted at rest in database

### Audit Trail
Every tool call logs:
- Request timestamp
- User/agent making call
- Input parameters (sanitized)
- Output (sanitized)
- Success/failure status
- Response time

### Rate Limiting
- Calendar: 100 req/min per provider
- Insurance: 50 req/min per API key
- Email: 1000 req/hour per domain
- SMS: 100 req/min per account

---

## 6. TESTING CHECKLIST

- [ ] Test each tool independently
- [ ] Test workflows end-to-end
- [ ] Test error conditions
- [ ] Test with mock data
- [ ] Load testing (100 concurrent requests)
- [ ] Security testing (SQL injection, XSS)


```
                                    GeminiZ Architecture

    ┌─────────────────────────────────────────────────────────────────────┐
    │                         USER PROMPT                                 │
    │         "Read my flight ticket and check in for me"                 │
    └──────────────────────────────┬──────────────────────────────────────┘
                                   │
                                   ▼
    ┌─────────────────────────────────────────────────────────────────────┐
    │                      🛡️  GEMINI Z CLI                               │
    │                                                                     │
    │   ┌───────────────┐    ┌──────────────┐    ┌───────────────────┐   │
    │   │  GEMINI 3 LLM │───▶│ PII-Awareness│───▶│    PIMS.md        │   │
    │   │  (reasoning)  │    │    SKILL     │    │  (policy file)    │   │
    │   └───────────────┘    └──────┬───────┘    │                   │   │
    │                               │            │  airline-checkin: │   │
    │                               │            │   ✅ BOOKING_CODE │   │
    │                               │            │   ✅ NAME         │   │
    │                               │            │   🚫 PASSPORT     │   │
    │                               │            │   🚫 CREDIT_CARD  │   │
    │                               │            └───────────────────┘   │
    │                               │                                     │
    │                               ▼                                     │
    │              ┌────────────────────────────────┐                     │
    │              │   📄 FILE READ                  │                     │
    │              │   flight_ticket.txt             │                     │
    │              │                                 │                     │
    │              │   "Michael Zurigo"              │                     │
    │              │   "GZ-2026-PAR"                 │                     │
    │              │   "X12345678" (passport)        │                     │
    │              │   "VISA ending 4242"            │                     │
    │              └────────────┬───────────────────┘                     │
    │                           │                                         │
    │                           ▼                                         │
    │              ┌────────────────────────────────┐                     │
    │              │   🤖 PII DETECTION ENGINE       │                     │
    │              │   (AI4Privacy - runs LOCAL)     │                     │
    │              │                                 │                     │
    │              │   Detected:                     │                     │
    │              │   NAME ─────────── Michael Z.   │                     │
    │              │   EMAIL ────────── michael@...  │                     │
    │              │   PASSPORT ─────── X12345678    │                     │
    │              │   CREDIT_CARD ──── ending 4242  │                     │
    │              │   BOOKING_CODE ─── GZ-2026-PAR  │                     │
    │              └────────────┬───────────────────┘                     │
    │                           │                                         │
    │                           ▼                                         │
    │              ┌────────────────────────────────┐                     │
    │              │   📋 POLICY ENFORCEMENT          │                     │
    │              │                                 │                     │
    │              │   Tool: airline-checkin          │                     │
    │              │                                 │                     │
    │              │   ✅ NAME          → ALLOWED    │                     │
    │              │   ✅ EMAIL         → ALLOWED    │                     │
    │              │   ✅ BOOKING_CODE  → ALLOWED    │                     │
    │              │   🚫 PASSPORT     → [REDACTED]  │                     │
    │              │   🚫 CREDIT_CARD  → [REDACTED]  │                     │
    │              │   🚫 ADDRESS      → [REDACTED]  │                     │
    │              └────────────┬───────────────────┘                     │
    │                           │                                         │
    └───────────────────────────┼─────────────────────────────────────────┘
                                │
                 ┌──────────────┼──────────────┐
                 │              │              │
                 ▼              ▼              ▼
    ┌────────────────┐ ┌──────────────┐ ┌─────────────────┐
    │  💬 RESPONSE    │ │ 📝 AUDIT LOG │ │ 🛡️ PIMS AUDITOR │
    │                │ │              │ │  (live panel)   │
    │ "Checked in!   │ │ 15:13 NAME   │ │                 │
    │  Booking:      │ │   ALLOWED    │ │  ✅✅✅🚫🚫🚫  │
    │  GZ-2026-PAR   │ │ 15:13 PASS   │ │                 │
    │  Seat: 12A     │ │   BLOCKED    │ │  Total: 6       │
    │  Passport:     │ │ 15:13 CC     │ │  Blocked: 50%   │
    │  [REDACTED]"   │ │   BLOCKED    │ │  ████░░░░ 50%   │
    └────────────────┘ └──────────────┘ └─────────────────┘


    ┌─────────────────────────────────────────────────────────────────────┐
    │                    🚨 UNREGISTERED TOOL?                            │
    │                                                                     │
    │   Tool NOT in PIMS.md  ──▶  ALL PII BLOCKED  ──▶  Zero data out   │
    │                                                                     │
    │   🚫 NAME        [REDACTED]     "Tool 'suspicious-analytics'       │
    │   🚫 EMAIL       [REDACTED]      not registered in PIMS.md"        │
    │   🚫 PASSPORT    [REDACTED]                                        │
    │   🚫 API_KEYS    [REDACTED]     💡 Register in PIMS.md to allow   │
    │   🚫 EVERYTHING  [REDACTED]                                        │
    └─────────────────────────────────────────────────────────────────────┘
```

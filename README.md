# AduanFlow AI 鈥?Autonomous Banking Dispute Resolution System

> **AI-powered, fully automated banking complaint handling** for the Tencent Cloud 脳 UTM Hackathon 2026 (AI Agent Track).

AduanFlow is an **agentic AI pipeline** that automatically ingests customer complaints from email, extracts evidence (even from scanned PDFs via OCR), classifies claims under Bank Negara Malaysia (BNM) rules, verifies against banking data, resolves eligible disputes, and responds with BNM/FMOS-compliant emails 鈥?all without human touch for high-confidence cases.

---

## Features

| Feature | Description |
|---------|-------------|
| <img src="https://cdn.simpleicons.org/gmail/EA4335" width="18" align="center"/> **Autonomous Gmail sync** | Polls the complaint mailbox every 30s and ingests unread complaints automatically. |
| <img src="https://cdn.simpleicons.org/googlegemini/8E75B2" width="18" align="center"/> **Agentic AI intake** | *Rhea* decides whether to call the PDF-OCR tool and extracts entities via Gemini tool-calling. |
| <img src="https://cdn.simpleicons.org/opencv/5C3EE8" width="18" align="center"/> **Multi-layer OCR** | text-layer *PyMuPDF* + **RapidOCR** (ONNX) + *Tesseract* fallback for scanned PDFs. |
| <img src="https://cdn.simpleicons.org/gnubash/4EAA25" width="18" align="center"/> **BNM/FMOS compliance** | classification mapped to mandatory SLA days, with governance stamps and audit trails. |
| <img src="https://cdn.simpleicons.org/githubactions/2088FF" width="18" align="center"/> **Three-state verdict engine** | PASS (auto-resolved), MANUAL (human escalation), FAIL (not upheld). |
| <img src="https://cdn.simpleicons.org/letsencrypt/003A70" width="18" align="center"/> **PII-at-rest encryption** | NRIC, account, card & amount encrypted with Fernet (AES-256). |
| <img src="https://cdn.simpleicons.org/react/61DAFB" width="18" align="center"/> **React dashboard** | real-time case list, statuses, pipeline trace, communication records. |
| <img src="https://cdn.simpleicons.org/supabase/3ECF8E" width="18" align="center"/> **Cloud storage** | Supabase PostgreSQL + automatic SQLite fallback. |

---

## System Architecture

```
Customer Email
      鈹?      鈻?[Gmail Sync Agent]  鈹€鈹€鈻? (IMAP / Gmail API, poll 30s)
      鈹?      鈻?[Rhea 鈥?Intake Agent]  鈹€鈹€鈻? tool: pdf_extract (PyMuPDF + RapidOCR)
      鈹?                     extracts account / card / amount / NRIC
      鈻?[Nadia 鈥?Classification]  鈹€鈹€鈻? BNM SLA category + urgency
      鈹?      鈻?[Faris 鈥?Verification/MCP]  鈹€鈹€鈻? PASS / MANUAL_REVIEW / FAIL
      鈹?      鈻?[Resolution + Communication] 鈹€鈹€鈻? compliant customer email (SMTP/Gmail)
      鈹?      鈻?[Supabase PostgreSQL]  鈼勨攢鈹€鈻? [React Dashboard]
```

**Multi-Agent cast** (inspired by the taskforce team playbook):

| Agent | Role |
|-------|------|
| **Rhea** | Intake & entity extraction, decides when to call OCR tool |
| **Nadia** | Dispute classifier & BNM compliance strategist |
| **Faris** | MCP verification & resolution analyst |
| **Sync Agent** | Autonomous Gmail mailbox poller |

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | FastAPI, Uvicorn, SQLModel, SQLAlchemy |
| AI | Google Gemini (via `google-genai`), native tool-calling |
| OCR | PyMuPDF, RapidOCR (ONNX), pytesseract (+ Tesseract engine) |
| Storage | Supabase PostgreSQL, SQLite fallback |
| Encryption | Fernet (cryptography, AES-256) |
| Email | Gmail IMAP + SMTP |
| Frontend | React 18, Vite, Tailwind CSS |
| Deploy | Render (free-tier) |

---

## Project Structure

```
aduanflow/
鈹溾攢鈹€ backend/
鈹?  鈹溾攢鈹€ app/
鈹?  鈹?  鈹溾攢鈹€ main.py                 # FastAPI entrypoint, router wiring, seed
鈹?  鈹?  鈹溾攢鈹€ config.py               # Env-driven settings (loads .env at import)
鈹?  鈹?  鈹溾攢鈹€ database.py             # Engine + Supabase/SQLite (+ IPv4 pooler fallback)
鈹?  鈹?  鈹溾攢鈹€ models/
鈹?  鈹?  鈹?  鈹溾攢鈹€ case.py             # Case (SQLModel ORM)
鈹?  鈹?  鈹?  鈹溾攢鈹€ audit.py            # AuditLog (SQLite/Audit)
鈹?  鈹?  鈹?  鈹斺攢鈹€ settings.py         # SystemSettings (Gmail/OAuth token store)
鈹?  鈹?  鈹溾攢鈹€ routes/                 # API routers (cases, audit, copilot, intake, taskforce, webhooks, mcp)
鈹?  鈹?  鈹斺攢鈹€ services/
鈹?  鈹?      鈹溾攢鈹€ gmail_sync_agent.py # Autonomous IMAP/Gmail poller
鈹?  鈹?      鈹溾攢鈹€ intake_agent.py     # Rhea: tool-calling entity extraction
鈹?  鈹?      鈹溾攢鈹€ intake_service.py   # 5-stage intake orchestration
鈹?  鈹?      鈹溾攢鈹€ classification_service.py  # Nadia: categorize + BNM SLA
鈹?  鈹?      鈹溾攢鈹€ verification_service.py    # Faris: PASS/FAIL/MANUAL_REVIEW
鈹?  鈹?      鈹溾攢鈹€ resolution_service.py      # financial posting
鈹?  鈹?      鈹溾攢鈹€ communication_service.py   # compliant email generation/dispatch
鈹?  鈹?      鈹溾攢鈹€ pdf_extractor.py    # OCR (RapidOCR/Tesseract)
鈹?  鈹?      鈹溾攢鈹€ gemini_client.py    # Gemini wrapper + tool-calling
鈹?  鈹?      鈹斺攢鈹€ encryption_service.py      # Fernet PII-at-rest
鈹?  鈹溾攢鈹€ requirements.txt
鈹?  鈹斺攢鈹€ mock_cases.json             # Seed data
鈹溾攢鈹€ frontend/
鈹?  鈹溾攢鈹€ src/                        # React app (Vite + Tailwind)
鈹?  鈹?  鈹斺攢鈹€ config.js               # API base URL (local vs Render)
鈹?  鈹斺攢鈹€ package.json
鈹溾攢鈹€ render.yaml                     # Render declarative deploy (backend + frontend)
鈹斺攢鈹€ .env.example                    # (see below) environment template
```

---

## Getting Started (Local Dev)

### Prerequisites
- Python 3.11+
- Node.js 18+
- A Gemini API key from [Google AI Studio](https://aistudio.google.com)
- (Optional) Gmail app password for live complaint sync

### 1. Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Create a `.env` in the project root (or `backend/.env`):

```env
# AI
GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=gemini-3.5-flash

# Gmail (optional, for live sync / outbound)
GMAIL_EMAIL=aduanflow@gmail.com
GMAIL_APP_PASSWORD=your_16_char_app_password

# Database
DATABASE_URL=postgresql://user:pass@host:5432/postgres   # optional; falls back to SQLite

# Encryption
ENCRYPTION_KEY=your_fernet_key
```

Run the API:

```bash
export PYTHONPATH=.              # Windows (PowerShell): $env:PYTHONPATH=...
uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload
```

API docs: `http://localhost:8000/docs`

### 2. Frontend

```bash
cd frontend
npm install
npm run dev                      # http://localhost:3000
```

The frontend auto-detects `localhost` and calls `http://127.0.0.1:8000`.

---

## Deploying to Render

This repo includes a `render.yaml` Blueprint that provisions both services on Render.

1. Push this repo to GitHub.
2. In Render 鈫?**Blueprints** 鈫?**New Blueprint**, select the repo.
3. Provide the env values flagged `sync: false`:
   - `DATABASE_URL` 鈥?Supabase PostgreSQL connection string
   - `GEMINI_API_KEY`
   - `GMAIL_EMAIL`, `GMAIL_APP_PASSWORD`
   - `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET` (OAuth only)
   - `ENCRYPTION_KEY` is auto-generated; update `frontend/src/config.js` to your backend URL.

> **Note:** Render's *free tier* may block outbound **SMTP :587**. Inbound Gmail/IMAP, outbound HTTPS (:443), Postgres, and the Gmail REST API all work. For real-time outbound email on the free tier, use the **Gmail API** (`messages.send`, over HTTPS) or a third-party email API (SendGrid/Mailgun).

---

## Demo Scenarios

Ready-to-send complaint templates to exercise the full pipeline:

| Scenario | What you send | Expected verdict |
|----------|---------------|------------------|
| **PASS** | Unauthorized card charge with legit details | `PASS` 鈥?auto-resolved & (if SMTP works) email sent |
| **FAIL** | Customer admits it was their own/authorized+OTP transaction | `FAIL` 鈥?claim not upheld |
| **MANUAL_REVIEW** | High-value dispute (> RM5k) or location inconsistency (login KL vs ATM JB) | `MANUAL_REVIEW` 鈥?escalates to human |

Example PASS body:

```
Subject: Unauthorized transaction RM1,280 on my account
Body: I did not authorize this charge. Account: 114002938471, Card: 4231-..., Amount: RM1,280
```

---

## BNM / Compliance Highlights

- Complaints mapped to BNM **mandatory SLA timelines** (e.g. Unauthorized Transactions = 5 working days).
- **FMOS** (Financial Mediation & Ombudsman Service) escalation notice embedded in every customer email.
- Full **audit log** per case: intake 鈫?OCR 鈫?classify 鈫?verify 鈫?resolve 鈫?respond.
- Governance field: `bnm_compliant: true`, `governance_status: STAMPED_PASS`.

---

## Roadmap / Notes

- [ ] Enable Gmail API (OAuth2) for HTTPS-based outbound mail on free tier.
- [ ] Add SendGrid fallback provider.
- [ ] Expand OCR to more document layouts.
- [ ] Add customer-facing status portal.

---

> Built for **Tencent Cloud 脳 UTM Hackathon 2026 鈥?AI Agent Track**.
> Team **AduanFlow** 鈥?Banking Dispute Automation.
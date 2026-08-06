import os
import json
import logging
from datetime import datetime
from dotenv import load_dotenv

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select

# Load .env at the very earliest point so all service modules read configured credentials
import os, pathlib
_dotenv_path = pathlib.Path(__file__).resolve().parents[1] / ".env"
if not _dotenv_path.exists():
    _dotenv_path = pathlib.Path(__file__).resolve().parents[2] / ".env"
load_dotenv(dotenv_path=_dotenv_path.as_posix())

from backend.app.config import settings
from backend.app.database import init_db, engine
from backend.app.models.case import Case
from backend.app.models.audit import AuditLog
from backend.app.routes import cases, audit, copilot, intake, taskforce, webhooks
from backend.app.routes import settings as settings_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('aduanflow')

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(cases.router, prefix=settings.API_V1_STR)
app.include_router(audit.router, prefix=settings.API_V1_STR)
app.include_router(copilot.router, prefix=settings.API_V1_STR)
app.include_router(intake.router, prefix=settings.API_V1_STR)
app.include_router(taskforce.router, prefix=settings.API_V1_STR)
app.include_router(webhooks.router, prefix=settings.API_V1_STR)
app.include_router(settings_router.router, prefix=settings.API_V1_STR)
from backend.app.routes import mcp
app.include_router(mcp.router)

@app.get("/api/db-status")
def check_db_status():
    from backend.app.database import engine, db_url, get_db_error
    err_trace = get_db_error()
    try:
        from sqlalchemy import text
        with engine.connect() as conn:
            res = conn.execute(text("SELECT 1")).scalar()
            from backend.app.database import init_db
            init_db()
        return {
            "status": "connected",
            "engine_url": str(engine.url),
            "db_type": "postgresql" if "postgresql" in str(engine.url) else "sqlite",
            "connection_error": err_trace
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "engine_url": str(engine.url),
            "connection_error": err_trace
        }


@app.on_event('startup')
def on_startup():
    logger.info('Initializing Database...')
    init_db()
    
    import threading
    threading.Thread(target=seed_database, daemon=True, name="SeedDatabaseThread").start()

    # Start autonomous Gmail background poller so complaints are processed automatically
    from backend.app.services.gmail_sync_agent import gmail_sync_agent
    poll_interval = int(os.getenv("GMAIL_POLL_INTERVAL", "30"))
    gmail_sync_agent.start_background_sync_loop(interval_seconds=poll_interval)
    logger.info(f'Gmail auto-sync worker started (poll every {poll_interval}s).')


def seed_database():
    """Seed initial mock cases from mock_cases.json if table is empty."""
    json_path = os.path.join(os.path.dirname(__file__), '..', 'mock_cases.json')
    if not os.path.exists(json_path):
        logger.info('mock_cases.json not found, skipping seed.')
        return

    with Session(engine) as session:
        # 1. Ensure SystemSettings is auto-seeded & connected on startup
        from backend.app.models.settings import SystemSettings
        from backend.app.services.encryption_service import encryption_service

        raw_token = os.getenv("GMAIL_REFRESH_TOKEN")
        if raw_token:
            settings_obj = session.get(SystemSettings, "global_settings")
            if not settings_obj or not settings_obj.is_gmail_connected:
                if not settings_obj:
                    settings_obj = SystemSettings(id="global_settings")
                target_email = os.getenv("GMAIL_EMAIL")
                if target_email:
                    settings_obj.gmail_email = target_email
                    settings_obj.gmail_refresh_token_encrypted = encryption_service.encrypt(raw_token)
                    settings_obj.is_gmail_connected = True
                    settings_obj.updated_at = datetime.utcnow()
                    session.add(settings_obj)
                    session.commit()

        existing = session.exec(select(Case)).first()
        if existing:
            logger.info('Database already seeded with case records.')
            return

        logger.info('Seeding database with mock cases...')
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                cases_data = json.load(f)

            for c in cases_data:
                received_str = c.get('receivedAt', '2026-07-22T08:15:00Z')
                due_str = c.get('dueDate', '2026-07-29T08:15:00Z')

                rec_dt = datetime.fromisoformat(received_str.replace('Z', '+00:00')) if received_str else datetime.utcnow()
                due_dt = datetime.fromisoformat(due_str.replace('Z', '+00:00')) if due_str else datetime.utcnow()

                case_obj = Case(
                    id=c['id'],
                    customer_name=c.get('customerName', 'Unknown'),
                    customer_email=c.get('customerEmail', 'unknown@email.com'),
                    masked_account=c.get('maskedAccount', '****0000'),
                    category=c.get('category', 'billing_errors'),
                    urgency=c.get('urgency', 'medium'),
                    status=c.get('status', 'PASS'),
                    verification_result=c.get('verificationResult'),
                    amount=float(c.get('amount', 0.0)),
                    assigned_to=c.get('assignedTo'),
                    received_at=rec_dt,
                    due_date=due_dt,
                    processing_time=c.get('processingTime', '—'),
                    email_subject=c.get('emailSubject'),
                    email_body=c.get('emailBody'),
                    ocr_results=c.get('ocrResults'),
                    classification=c.get('classification'),
                    verification=c.get('verification'),
                    financial_resolution=c.get('financialResolution'),
                    communication=c.get('communication'),
                    audit_log=c.get('auditLog'),
                )
                session.add(case_obj)

                if c.get('auditLog'):
                    for item in c['auditLog']:
                        audit_entry = AuditLog(
                            case_id=c['id'],
                            actor=item.get('actor', 'System'),
                            action=item.get('action', 'Operation'),
                            detail=item.get('detail'),
                        )
                        session.add(audit_entry)

            session.commit()
            logger.info('Database seeding complete!')
        except Exception as e:
            logger.error(f'Error seeding database: {e}')


@app.get('/')
def root():
    return {'message': 'AduanFlow AI Backend API is running', 'docs': '/docs'}


@app.post('/api/debug/sync')
def debug_sync():
    """Manually trigger one Gmail sync cycle and return the raw result/error."""
    import traceback
    from backend.app.services.gmail_sync_agent import gmail_sync_agent
    try:
        result = gmail_sync_agent.run_sync_cycle()
        return {"ok": True, "result": result}
    except Exception as e:
        return {"ok": False, "error": str(e), "traceback": traceback.format_exc()}

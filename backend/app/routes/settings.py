from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any
from sqlmodel import Session, select
from datetime import datetime
from backend.app.database import get_session
from backend.app.models.settings import SystemSettings, GmailTokenPayload, GmailStatusResponse
from backend.app.services.encryption_service import encryption_service

router = APIRouter(prefix="/auth", tags=["auth"])

import time

class ActiveSessionManager:
    def __init__(self):
        # client_id -> {"client_id": str, "last_seen": float, "is_testing": bool, "user_label": str}
        self.active_sessions: Dict[str, Dict[str, Any]] = {}

    def heartbeat(self, client_id: str, is_testing: bool = False, user_label: Optional[str] = None) -> Dict[str, Any]:
        now = time.time()
        # Clean expired sessions (> 15 seconds inactive)
        self.active_sessions = {
            cid: sess for cid, sess in self.active_sessions.items()
            if now - sess["last_seen"] < 15
        }
        
        self.active_sessions[client_id] = {
            "client_id": client_id,
            "last_seen": now,
            "is_testing": is_testing,
            "user_label": user_label or f"Teammate ({client_id[:6]})"
        }

        active_count = len(self.active_sessions)
        other_active_testing = any(
            cid != client_id and sess["is_testing"] 
            for cid, sess in self.active_sessions.items()
        )
        other_active_users = [
            sess["user_label"] for cid, sess in self.active_sessions.items() 
            if cid != client_id
        ]

        return {
            "active_teammates_count": active_count,
            "other_active_users": other_active_users,
            "is_another_user_active": len(other_active_users) > 0,
            "is_locked_by_testing": other_active_testing
        }

session_manager = ActiveSessionManager()

class HeartbeatPayload(BaseModel):
    client_id: str
    is_testing: Optional[bool] = False
    user_label: Optional[str] = None

@router.post("/heartbeat")
def record_heartbeat(payload: HeartbeatPayload):
    return session_manager.heartbeat(
        client_id=payload.client_id,
        is_testing=payload.is_testing,
        user_label=payload.user_label
    )

@router.get("/gmail-status", response_model=GmailStatusResponse)
def get_gmail_status(session: Session = Depends(get_session)):
    """Get current Gmail OAuth complaints mailbox connection status."""
    settings_obj = session.get(SystemSettings, "global_settings")
    if not settings_obj or not settings_obj.is_gmail_connected:
        return GmailStatusResponse(is_connected=False)
        
    return GmailStatusResponse(
        is_connected=True,
        email=settings_obj.gmail_email,
        updated_at=settings_obj.updated_at
    )

from fastapi.responses import RedirectResponse
import requests

import os

@router.get("/google/login")
def google_oauth_login(client_id: Optional[str] = None):
    """
    1-Click Automated Google OAuth Flow: Redirect user to Google Authorization Prompt.
    """
    cid = (client_id and client_id.strip()) or os.getenv("GOOGLE_CLIENT_ID") or "1041907708486-uvplue4dp8pl64bre8a36u0qs5vc8lsn.apps.googleusercontent.com"
    base_backend = os.getenv("RENDER_EXTERNAL_URL") or "https://aduanflow-backend.onrender.com"
    redirect_uri = f"{base_backend.rstrip('/')}/api/auth/google/callback"
    scope = "https://www.googleapis.com/auth/gmail.send https://mail.google.com/ https://www.googleapis.com/auth/userinfo.email"
    
    auth_url = (
        f"https://accounts.google.com/o/oauth2/v2/auth?"
        f"client_id={cid}&"
        f"redirect_uri={redirect_uri}&"
        f"response_type=code&"
        f"scope={scope}&"
        f"access_type=offline&"
        f"prompt=consent"
    )
    return RedirectResponse(url=auth_url)

@router.get("/google/callback")
def google_oauth_callback(
    code: Optional[str] = None, 
    error: Optional[str] = None, 
    session: Session = Depends(get_session)
):
    """
    1-Click Callback: Automatically exchanges authorization code for Permanent Refresh Token.
    If user cancels or error occurs, gracefully redirects back to FRONTEND_URL.
    """
    base_frontend = os.getenv("FRONTEND_URL") or "https://aduanflow-frontend-v4.onrender.com"

    if error or not code:
        return RedirectResponse(url=f"{base_frontend.rstrip('/')}?oauth_cancelled=true")

    try:
        client_id = os.getenv("GOOGLE_CLIENT_ID") or "1041907708486-uvplue4dp8pl64bre8a36u0qs5vc8lsn.apps.googleusercontent.com"
        raw_secret = os.getenv("GOOGLE_CLIENT_SECRET")
        base_backend = os.getenv("RENDER_EXTERNAL_URL") or "https://aduanflow-backend.onrender.com"
        redirect_uri = f"{base_backend.rstrip('/')}/api/auth/google/callback"

        settings_obj = session.get(SystemSettings, "global_settings")
        if not raw_secret and settings_obj and settings_obj.gmail_client_secret_encrypted:
            try:
                raw_secret = encryption_service.decrypt(settings_obj.gmail_client_secret_encrypted)
            except Exception:
                pass

        token_url = "https://oauth2.googleapis.com/token"
        data = {
            "code": code,
            "client_id": client_id,
            "redirect_uri": redirect_uri,
            "grant_type": "authorization_code"
        }
        if raw_secret:
            data["client_secret"] = raw_secret

        token_res = requests.post(token_url, data=data, timeout=10)
        if token_res.status_code != 200:
            err_msg = token_res.text.replace('"', "'").replace('\n', ' ')
            return RedirectResponse(url=f"{base_frontend.rstrip('/')}?oauth_error={err_msg}")

        token_data = token_res.json()
        refresh_token = token_data.get("refresh_token")
        access_token = token_data.get("access_token")

        user_email = None
        if access_token:
            try:
                user_info_res = requests.get("https://www.googleapis.com/oauth2/v2/userinfo", headers={"Authorization": f"Bearer {access_token}"}, timeout=5)
                if user_info_res.status_code == 200:
                    user_email = user_info_res.json().get("email")
            except Exception as u_err:
                logger.error(f"[GoogleOAuth] Failed to fetch userinfo email: {u_err}")

        if not user_email:
            logger.warning("[GoogleOAuth] Could not fetch useremail from Google OAuth profile, defaulting to connected account.")
            user_email = os.getenv("GMAIL_EMAIL")

        target_token = refresh_token or access_token
        if target_token:
            enc_refresh = encryption_service.encrypt(target_token)
            db_settings = session.get(SystemSettings, "global_settings")
            if not db_settings:
                db_settings = SystemSettings(id="global_settings")

            db_settings.gmail_email = user_email
            db_settings.gmail_refresh_token_encrypted = enc_refresh
            db_settings.is_gmail_connected = True
            db_settings.updated_at = datetime.utcnow()

            session.add(db_settings)
            session.commit()

        return RedirectResponse(url=f"{base_frontend.rstrip('/')}?oauth_success=true")
    except Exception as exc:
        err_str = str(exc).replace('"', "'").replace('\n', ' ')
        return RedirectResponse(url=f"{base_frontend.rstrip('/')}?oauth_error={err_str}")

@router.post("/gmail-token", response_model=GmailStatusResponse)
def save_gmail_token(payload: GmailTokenPayload, session: Session = Depends(get_session)):
    """
    Encrypt and store long-lived Gmail OAuth refresh token for automated email intake engine.
    """
    if not payload.refresh_token or not payload.email:
        raise HTTPException(status_code=400, detail="Both refresh_token and email are required.")

    # Encrypt sensitive tokens at rest using Fernet
    enc_refresh = encryption_service.encrypt(payload.refresh_token)
    enc_app_pass = encryption_service.encrypt(payload.app_password) if payload.app_password else None
    enc_client_id = encryption_service.encrypt(payload.client_id) if payload.client_id else None
    enc_client_secret = encryption_service.encrypt(payload.client_secret) if payload.client_secret else None

    settings_obj = session.get(SystemSettings, "global_settings")
    if not settings_obj:
        settings_obj = SystemSettings(id="global_settings")
    elif settings_obj.is_gmail_connected and settings_obj.gmail_email and settings_obj.gmail_email.lower() != payload.email.lower():
        raise HTTPException(
            status_code=400, 
            detail=f"Mailbox is currently locked & connected to {settings_obj.gmail_email}. Click 'Disconnect' first before switching to a new address."
        )

    settings_obj.gmail_email = payload.email
    settings_obj.gmail_refresh_token_encrypted = enc_refresh
    if enc_app_pass:
        settings_obj.gmail_app_password_encrypted = enc_app_pass
    settings_obj.gmail_client_id_encrypted = enc_client_id
    settings_obj.gmail_client_secret_encrypted = enc_client_secret
    settings_obj.is_gmail_connected = True
    settings_obj.updated_at = datetime.utcnow()

    session.add(settings_obj)
    session.commit()
    session.refresh(settings_obj)

    return GmailStatusResponse(
        is_connected=True,
        email=settings_obj.gmail_email,
        updated_at=settings_obj.updated_at
    )

@router.delete("/gmail-token")
def disconnect_gmail(session: Session = Depends(get_session)):
    """Disconnect Gmail mailbox integration."""
    settings_obj = session.get(SystemSettings, "global_settings")
    if settings_obj:
        settings_obj.is_gmail_connected = False
        settings_obj.gmail_refresh_token_encrypted = None
        settings_obj.gmail_email = None
        settings_obj.updated_at = datetime.utcnow()
        session.add(settings_obj)
        session.commit()
        
    return {"message": "Gmail integration disconnected successfully"}

@router.post("/gmail-sync")
def sync_gmail_inbox(session: Session = Depends(get_session)):
    """
    Independent Gmail Sync Agent reads the stored refresh token from DB,
    decrypts it safely in memory, polls unread emails, and passes cases to pipeline.
    """
    from backend.app.services.gmail_sync_agent import gmail_sync_agent
    result = gmail_sync_agent.run_sync_cycle()
    return result

class CustomEmailPayload(BaseModel):
    customer_name: str
    customer_email: Optional[str] = None
    amount: float
    account_number: str
    nric: str
    email_subject: str
    email_body: str
    attachment_name: Optional[str] = "Dispute_Receipt.pdf"

@router.post("/send-custom-email")
def dispatch_custom_email(payload: CustomEmailPayload, session: Session = Depends(get_session)):
    """
    Simulate an incoming dispute complaint email to the intake pipeline.
    """
    settings_obj = session.get(SystemSettings, "global_settings")
    mailbox_email = settings_obj.gmail_email if (settings_obj and settings_obj.is_gmail_connected) else "complaints@aduanflow.bank"
    target_customer_email = payload.customer_email or "customer@gmail.com"

    from backend.app.services.intake_service import intake_service

    case_obj = intake_service.process_incoming_complaint(
        customer_name=payload.customer_name,
        customer_email=target_customer_email,
        account_number=payload.account_number,
        nric=payload.nric,
        amount=payload.amount,
        email_subject=payload.email_subject,
        email_body=payload.email_body,
        attachment_name=payload.attachment_name
    )

    session.add(case_obj)
    session.commit()
    session.refresh(case_obj)

    return {
        "status": "success",
        "mailbox": mailbox_email,
        "customer_email": target_customer_email,
        "case_id": case_obj.id,
        "customer": case_obj.customer_name,
        "category": case_obj.category,
        "urgency": case_obj.urgency,
        "amount": case_obj.amount,
        "pipeline_status": case_obj.status
    }

class OutboundEmailPayload(BaseModel):
    recipient_email: str
    subject: str
    body: str
    app_password: Optional[str] = None

@router.post("/send-test-outbound-email")
def dispatch_test_outbound_email(payload: OutboundEmailPayload, session: Session = Depends(get_session)):
    """
    Test outbound email dispatching to target recipient Gmail address.
    """
    settings_obj = session.get(SystemSettings, "global_settings")
    sender_email = settings_obj.gmail_email if (settings_obj and settings_obj.is_gmail_connected) else None

    from backend.app.services.communication_service import communication_service

    res = communication_service.send_outbound_email(
        to_email=payload.recipient_email,
        subject=payload.subject,
        body=payload.body,
        sender_email=sender_email,
        app_password=payload.app_password
    )

    return res

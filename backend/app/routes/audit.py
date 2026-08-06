from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from typing import List, Optional
from backend.app.database import get_session
from backend.app.models.audit import AuditLog, AuditLogRead

router = APIRouter(prefix="/audit", tags=["audit"])

@router.get("", response_model=List[AuditLogRead])
def list_audit_logs(
    actor: Optional[str] = None,
    case_id: Optional[str] = None,
    session: Session = Depends(get_session)
):
    """Fetch system audit trail with actor and case filters."""
    statement = select(AuditLog).order_by(AuditLog.created_at.desc())
    if actor:
        statement = statement.where(AuditLog.actor == actor)
    if case_id:
        statement = statement.where(AuditLog.case_id == case_id)
        
    return session.exec(statement).all()

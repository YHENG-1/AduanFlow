from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field
import uuid

class AuditLogBase(SQLModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    case_id: str = Field(index=True)
    actor: str = Field(index=True) # Email MCP, Intake Agent, Security Agent, Classification Agent, Verification Agent, Financial Agent, Comms Agent, Investigator
    action: str
    detail: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

class AuditLog(AuditLogBase, table=True):
    __tablename__ = "audit_logs"

class AuditLogCreate(AuditLogBase):
    pass

class AuditLogRead(AuditLogBase):
    pass

from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field

class User(SQLModel, table=True):
    """
    User model for multi-investigator & compliance officer access control.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(index=True, unique=True)
    full_name: str
    role: str = Field(default="INVESTIGATOR")  # INVESTIGATOR, COMPLIANCE_OFFICER, AUDITOR, ADMIN
    department: str = Field(default="Dispute Resolution Taskforce")
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

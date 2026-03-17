from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional
from enum import Enum
from datetime import datetime

class BoardEnum(str, Enum):
    CBSE        = "CBSE"
    ICSE        = "ICSE"
    STATE_BOARD = "State Board"
    IB          = "IB"
    OTHER       = "Other"

class StatusEnum(str, Enum):
    PENDING  = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"

# ── Request schema (what the frontend sends) ──────────────────────────────────
class EnrollmentCreate(BaseModel):
    school_name:    str
    principal_name: str
    email:          EmailStr
    phone:          str
    address_line1:  Optional[str] = None
    address_line2:  Optional[str] = None
    city:           Optional[str] = None
    state:          Optional[str] = None
    country:        Optional[str] = "India"
    postal_code:    Optional[str] = None
    total_students: Optional[int] = 0
    board:          BoardEnum
    website:        Optional[str] = None

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v):
        if not v.isdigit() or len(v) < 10:
            raise ValueError("Phone must be at least 10 digits")
        return v

# ── Response schema (what we send back) ──────────────────────────────────────
class EnrollmentResponse(BaseModel):
    id:             int
    school_name:    str
    principal_name: str
    email:          str
    phone:          str
    address_line1:  Optional[str]
    address_line2:  Optional[str]
    city:           Optional[str]
    state:          Optional[str]
    country:        Optional[str]
    postal_code:    Optional[str]
    total_students: Optional[int]
    board:          str
    website:        Optional[str]
    status:         str
    created_at:     datetime
    updated_at:     datetime

    class Config:
        from_attributes = True

import enum
from sqlalchemy import Column, BigInteger, String, Integer, Enum, DateTime
from sqlalchemy.sql import func
from database import Base

class BoardEnum(str, enum.Enum):
    CBSE        = "CBSE"
    ICSE        = "ICSE"
    STATE_BOARD = "State Board"
    IB          = "IB"
    OTHER       = "Other"

class StatusEnum(str, enum.Enum):
    PENDING  = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"

class SchoolEnrollment(Base):
    __tablename__ = "school_enrollment"

    id             = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    school_name    = Column(String(255), nullable=False)
    principal_name = Column(String(255), nullable=False)
    email          = Column(String(255), nullable=False, unique=True)
    phone          = Column(String(20), nullable=False)
    address_line1  = Column(String(255), nullable=True)
    address_line2  = Column(String(255), nullable=True)
    city           = Column(String(100), nullable=True)
    state          = Column(String(100), nullable=True)
    country        = Column(String(100), default="India")
    postal_code    = Column(String(10), nullable=True)
    total_students = Column(Integer, default=0)
    board          = Column(Enum(BoardEnum), nullable=False)
    website        = Column(String(255), nullable=True)
    status         = Column(Enum(StatusEnum), default=StatusEnum.PENDING)
    created_at     = Column(DateTime(timezone=True), server_default=func.now())
    updated_at     = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

import os
import logging
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from database import get_db
from models import SchoolEnrollment
from schemas import EnrollmentCreate, EnrollmentResponse
from email_service import send_admin_notification
from typing import List

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/enrollment", tags=["Enrollment"])

ALLOW_INSERT = os.getenv("ALLOW_INSERT_OPERATION", "true").lower() == "true"
ALLOW_UPDATE = os.getenv("ALLOW_UPDATE_OPERATION", "true").lower() == "true"
ALLOW_DELETE = os.getenv("ALLOW_DELETE_OPERATION", "true").lower() == "true"


def _send_admin_email_bg(school_name, principal_name, email, phone,
                         board, city, state, total_students, enrollment_id):
    """Send admin notification in background — non-blocking."""
    try:
        send_admin_notification(
            school_name    = school_name,
            principal_name = principal_name,
            email          = email,
            phone          = phone,
            board          = board,
            city           = city,
            state          = state,
            total_students = total_students,
            enrollment_id  = enrollment_id
        )
        logger.info(f"✅ Admin notification sent for enrollment #{enrollment_id}")
    except Exception as e:
        logger.error(f"❌ Failed to send admin notification: {e}")


# ── POST /api/enrollment/enroll ───────────────────────────────────────────────
@router.post("/enroll", response_model=EnrollmentResponse, status_code=status.HTTP_201_CREATED)
def enroll_school(
    payload: EnrollmentCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    if not ALLOW_INSERT:
        raise HTTPException(status_code=403, detail="Insert operations are disabled")

    existing = db.query(SchoolEnrollment).filter(SchoolEnrollment.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="A school with this email already exists")

    new_school = SchoolEnrollment(**payload.model_dump())
    db.add(new_school)
    db.commit()
    db.refresh(new_school)

    # Send admin notification in background
    background_tasks.add_task(
        _send_admin_email_bg,
        school_name    = new_school.school_name,
        principal_name = new_school.principal_name,
        email          = new_school.email,
        phone          = new_school.phone,
        board          = new_school.board.value if hasattr(new_school.board, 'value') else str(new_school.board),
        city           = new_school.city or "",
        state          = new_school.state or "",
        total_students = new_school.total_students or 0,
        enrollment_id  = new_school.id
    )

    return new_school


# ── GET /api/enrollment/list ──────────────────────────────────────────────────
@router.get("/list", response_model=List[EnrollmentResponse])
def list_enrollments(db: Session = Depends(get_db)):
    return db.query(SchoolEnrollment).order_by(SchoolEnrollment.created_at.desc()).all()


# ── GET /api/enrollment/{id} ──────────────────────────────────────────────────
@router.get("/{enrollment_id}", response_model=EnrollmentResponse)
def get_enrollment(enrollment_id: int, db: Session = Depends(get_db)):
    school = db.query(SchoolEnrollment).filter(SchoolEnrollment.id == enrollment_id).first()
    if not school:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    return school


# ── DELETE /api/enrollment/{id} ───────────────────────────────────────────────
@router.delete("/{enrollment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_enrollment(enrollment_id: int, db: Session = Depends(get_db)):
    if not ALLOW_DELETE:
        raise HTTPException(status_code=403, detail="Delete operations are disabled")
    school = db.query(SchoolEnrollment).filter(SchoolEnrollment.id == enrollment_id).first()
    if not school:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    db.delete(school)
    db.commit()

from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db
from app.email_utils import send_contact_notification
from app.auth import require_admin

router = APIRouter(prefix="/api/contact", tags=["contact"])


@router.post("", response_model=schemas.ContactOut, status_code=201)
def create_contact_message(
    payload: schemas.ContactCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    entry = models.ContactMessage(name=payload.name, email=payload.email, message=payload.message)
    db.add(entry)
    db.commit()
    db.refresh(entry)

    background_tasks.add_task(send_contact_notification, payload.name, payload.email, payload.message)
    return entry


@router.get("", response_model=list[schemas.ContactOut])
def list_contact_messages(db: Session = Depends(get_db), _admin: str = Depends(require_admin)):
    return db.query(models.ContactMessage).order_by(models.ContactMessage.created_at.desc()).all()


@router.patch("/{message_id}/read", response_model=schemas.ContactOut)
def mark_read(message_id: int, db: Session = Depends(get_db), _admin: str = Depends(require_admin)):
    entry = db.query(models.ContactMessage).filter(models.ContactMessage.id == message_id).first()
    if not entry:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Message not found")
    entry.read = True
    db.commit()
    db.refresh(entry)
    return entry
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db
from app.config import settings
from app.auth import verify_password, create_access_token, require_admin

router = APIRouter(prefix="/api/admin", tags=["admin"])


@router.post("/login", response_model=schemas.Token)
def login(payload: schemas.LoginRequest):
    if payload.username != settings.ADMIN_USERNAME or not settings.ADMIN_PASSWORD_HASH:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    if not verify_password(payload.password, settings.ADMIN_PASSWORD_HASH):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    token = create_access_token(subject=payload.username)
    return schemas.Token(access_token=token)


@router.get("/stats")
def stats(db: Session = Depends(get_db), _admin: str = Depends(require_admin)):
    return {
        "total_messages": db.query(models.ContactMessage).count(),
        "unread_messages": db.query(models.ContactMessage).filter(models.ContactMessage.read.is_(False)).count(),
        "total_projects": db.query(models.Project).count(),
        "total_page_views": db.query(models.PageView).count(),
    }
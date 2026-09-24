from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db
from app.auth import require_admin

router = APIRouter(prefix="/api/certificates", tags=["certificates"])


@router.get("", response_model=list[schemas.CertificateOut])
def list_certificates(db: Session = Depends(get_db)):
    return db.query(models.Certificate).order_by(models.Certificate.sort_order, models.Certificate.id).all()


@router.post("", response_model=schemas.CertificateOut, status_code=201)
def create_certificate(
    payload: schemas.CertificateCreate,
    db: Session = Depends(get_db),
    _admin: str = Depends(require_admin),
):
    cert = models.Certificate(**payload.model_dump())
    db.add(cert)
    db.commit()
    db.refresh(cert)
    return cert


@router.put("/{certificate_id}", response_model=schemas.CertificateOut)
def update_certificate(
    certificate_id: int,
    payload: schemas.CertificateUpdate,
    db: Session = Depends(get_db),
    _admin: str = Depends(require_admin),
):
    cert = db.query(models.Certificate).filter(models.Certificate.id == certificate_id).first()
    if not cert:
        raise HTTPException(status_code=404, detail="Certificate not found")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(cert, field, value)
    db.commit()
    db.refresh(cert)
    return cert


@router.delete("/{certificate_id}", status_code=204)
def delete_certificate(
    certificate_id: int,
    db: Session = Depends(get_db),
    _admin: str = Depends(require_admin),
):
    cert = db.query(models.Certificate).filter(models.Certificate.id == certificate_id).first()
    if not cert:
        raise HTTPException(status_code=404, detail="Certificate not found")
    db.delete(cert)
    db.commit()
    return None
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, ConfigDict


class ContactCreate(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    email: EmailStr
    message: str = Field(min_length=10, max_length=4000)


class ContactOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    email: str
    message: str
    created_at: datetime
    read: bool


class ProjectBase(BaseModel):
    title: str = Field(min_length=1, max_length=160)
    kind: str = ""
    description: str = ""
    stack: str = ""
    code_url: Optional[str] = None
    live_url: Optional[str] = None
    sort_order: int = 0


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(BaseModel):
    title: Optional[str] = None
    kind: Optional[str] = None
    description: Optional[str] = None
    stack: Optional[str] = None
    code_url: Optional[str] = None
    live_url: Optional[str] = None
    sort_order: Optional[int] = None


class ProjectOut(ProjectBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime


class CertificateBase(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    issuer: str = ""
    when_text: str = ""
    sort_order: int = 0


class CertificateCreate(CertificateBase):
    pass


class CertificateUpdate(BaseModel):
    title: Optional[str] = None
    issuer: Optional[str] = None
    when_text: Optional[str] = None
    sort_order: Optional[int] = None


class CertificateOut(CertificateBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime


class LoginRequest(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
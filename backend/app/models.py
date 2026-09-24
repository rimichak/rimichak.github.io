from datetime import datetime

from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean

from app.database import Base


class ContactMessage(Base):
    __tablename__ = "contact_messages"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(120), nullable=False)
    email = Column(String(160), nullable=False)
    message = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    read = Column(Boolean, default=False)


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(160), nullable=False)
    kind = Column(String(80), nullable=False, default="")
    description = Column(Text, nullable=False, default="")
    stack = Column(String(200), nullable=False, default="")
    code_url = Column(String(300), nullable=True)
    live_url = Column(String(300), nullable=True)
    sort_order = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)


class Certificate(Base):
    __tablename__ = "certificates"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    issuer = Column(String(200), nullable=False, default="")
    when_text = Column(String(160), nullable=False, default="")
    sort_order = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)


class PageView(Base):
    __tablename__ = "page_views"

    id = Column(Integer, primary_key=True, index=True)
    path = Column(String(200), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.config import settings
from app.database import Base, engine, get_db
from app import models
from app.routers import contact, projects, certificates, admin

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Rimi Chakraborty Portfolio API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(contact.router)
app.include_router(projects.router)
app.include_router(certificates.router)
app.include_router(admin.router)


@app.get("/")
def root():
    return {"status": "ok", "service": "portfolio-api"}


@app.post("/api/views/{path:path}", status_code=204)
def log_view(path: str, db: Session = Depends(get_db)):
    db.add(models.PageView(path=f"/{path}"))
    db.commit()
    return None


@app.on_event("startup")
def seed_projects():
    db = next(get_db())
    if db.query(models.Project).count() == 0:
        seed = [
            models.Project(
                title="Repository security detector",
                kind="Backend service, 2026",
                description="A backend service that scans GitHub repositories for security vulnerabilities, "
                             "with JWT authentication and regex-based detection of exposed secrets.",
                stack="FastAPI, Python, JWT authentication",
                sort_order=1,
            ),
            models.Project(
                title="Network intrusion detection system",
                kind="Machine learning, 2025",
                description="A machine learning model that classifies network traffic as normal or malicious, "
                             "with preprocessing, feature engineering and visualized performance.",
                stack="Python, Scikit-learn, Pandas, NumPy, Matplotlib",
                sort_order=2,
            ),
            models.Project(
                title="Expense tracker API",
                kind="REST API, 2025",
                description="A RESTful expense management API with CRUD for income and expenses, "
                             "structured validation, and summarized financial insight endpoints.",
                stack="FastAPI, Python, Pydantic, JSON storage",
                sort_order=3,
            ),
            models.Project(
                title="Resume optimizer",
                kind="NLP tool, 2025",
                description="A resume analysis tool using keyword matching and NLP-based similarity scoring, "
                             "with automated feedback to improve ATS compatibility.",
                stack="Python, NLP",
                sort_order=4,
            ),
        ]
        db.add_all(seed)
        db.commit()

    if db.query(models.Certificate).count() == 0:
        cert_seed = [
            models.Certificate(
                title="AWS Cloud Practitioner Essentials",
                issuer="Amazon Web Services",
                when_text="March 2025",
                sort_order=1,
            ),
            models.Certificate(
                title="Introduction to Linux (LFS101)",
                issuer="The Linux Foundation",
                when_text="August 2025",
                sort_order=2,
            ),
            models.Certificate(
                title="Hackathon Participation",
                issuer="WeMakeDevs",
                when_text="2025",
                sort_order=3,
            ),
            models.Certificate(
                title="SQL (4 star)",
                issuer="HackerRank",
                when_text="2025",
                sort_order=4,
            ),
            models.Certificate(
                title="Diploma in Computer Science & Technology",
                issuer="Women's Polytechnic, West Bengal State Council of Technical and Vocational Education and Skill Development",
                when_text="2024 \u00b7 1st Class with Distinction, OGPA 8.10",
                sort_order=5,
            ),
        ]
        db.add_all(cert_seed)
        db.commit()
    db.close()
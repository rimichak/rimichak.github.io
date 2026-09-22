import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./portfolio.db")
    JWT_SECRET: str = os.getenv("JWT_SECRET", "change-this-secret")
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 60 * 12  # 12 hours

    ADMIN_USERNAME: str = os.getenv("ADMIN_USERNAME", "rimi")
    # Generate with: python -c "from app.auth import hash_password; print(hash_password('yourpassword'))"
    ADMIN_PASSWORD_HASH: str = os.getenv("ADMIN_PASSWORD_HASH", "")

    SMTP_HOST: str = os.getenv("SMTP_HOST", "")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USER: str = os.getenv("SMTP_USER", "")
    SMTP_PASS: str = os.getenv("SMTP_PASS", "")
    NOTIFY_EMAIL: str = os.getenv("NOTIFY_EMAIL", "rimi.reach@gmail.com")

    CORS_ORIGINS: list = [
        origin.strip()
        for origin in os.getenv(
            "CORS_ORIGINS", "https://rimichak.github.io,http://localhost:5500,http://127.0.0.1:5500"
        ).split(",")
        if origin.strip()
    ]


settings = Settings()
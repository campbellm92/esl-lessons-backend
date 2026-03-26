from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from app.core.config import settings
from app.api import auth
from app.db.database import engine
from app.models import user

user.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(TrustedHostMiddleware, allowed_hosts=["*"])

app.include_router(auth.router, prefix=f"/auth", tags=["authentication"])

@app.get("/")
def health_check():
    return {
        "message": f"{settings.PROJECT_NAME} is running.",
        "status": "healthy"
    }
from fastapi import FastAPI
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.cors import CORSMiddleware
from .database.database import engine, Base
from .routers import auth, events, conversions, admin
from .core.config import settings

# 创建数据库表
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Landing Page API",
    description="API for landing page tracking and conversions",
    version="1.0.0",
    root_path="",
    servers=[
        {"url": "https://zbfxa.xyz", "description": "Production server"},
        {"url": "http://localhost:8080", "description": "Development server"}
    ]
)

# Trust proxy headers
app.add_middleware(
    TrustedHostMiddleware, 
    allowed_hosts=["*"]
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api", tags=["auth"])
app.include_router(events.router, prefix="/api", tags=["events"])
app.include_router(conversions.router, prefix="/api", tags=["conversions"])
app.include_router(admin.router, prefix="/admin", tags=["admin"])

@app.get("/")
async def root():
    return {"message": "Landing Page API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
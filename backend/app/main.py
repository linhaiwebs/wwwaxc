from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from .database import engine, Base
from .routers import auth, events, conversions, admin
from .config import settings

# 创建数据库表
Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI股价診断 API", version="1.0.0")

# 信任的主机
app.add_middleware(
    TrustedHostMiddleware, 
    allowed_hosts=["*"]
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 路由
app.include_router(auth.router, prefix="/api")
app.include_router(events.router, prefix="/api") 
app.include_router(conversions.router, prefix="/api")
app.include_router(admin.router, prefix="/admin")

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get("/")
async def root():
    return {"message": "AI Stock Diagnosis API", "status": "running"}
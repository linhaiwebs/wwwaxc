from fastapi import APIRouter, Depends, HTTPException, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from urllib.parse import urljoin
from sqlalchemy.orm import Session
from typing import List
from datetime import timedelta
from ..database.database import get_db
from ..models.event import Event
from ..models.conversion import Conversion
from ..models.admin_user import AdminUser
from ..models.conversion_link import ConversionLink
from ..schemas import EventResponse, ConversionRecord, AdminLogin
from ..core.security import verify_password, create_access_token, verify_token

templates = Jinja2Templates(directory="app/templates")

router = APIRouter()

def get_base_url(request: Request) -> str:
    """获取正确的基础URL，考虑代理头信息"""
    # 检查代理头信息
    forwarded_proto = request.headers.get("X-Forwarded-Proto", "http")
    forwarded_host = request.headers.get("X-Forwarded-Host") or request.headers.get("Host")
    
    if forwarded_host:
        return f"{forwarded_proto}://{forwarded_host}"
    
    # 回退到请求的基础URL
    return str(request.base_url).rstrip('/')

def get_current_admin_user(request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get("admin_token")
    if not token:
        return None
    
    payload = verify_token(token)
    if not payload:
        return None
    
    admin_user = db.query(AdminUser).filter(AdminUser.username == payload.get("username")).first()
    return admin_user

@router.get("/", response_class=HTMLResponse)
async def admin_dashboard(request: Request, db: Session = Depends(get_db)):
    admin_user = get_current_admin_user(request, db)
    if not admin_user:
        base_url = get_base_url(request)
        response = RedirectResponse(url=f"{base_url}/admin/login", status_code=302)
        return response
    
    # 获取统计数据
    total_events = db.query(Event).count()
    total_conversions = db.query(Conversion).count()
    total_conversion_links = db.query(ConversionLink).count()
    
    # 最近的转换记录
    recent_conversions = db.query(Conversion).order_by(Conversion.created_at.desc()).limit(10).all()
    
    # 事件类型统计
    event_types = db.query(Event.event_type, db.func.count(Event.id)).group_by(Event.event_type).all()
    
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "admin_user": admin_user,
        "total_events": total_events,
        "total_conversions": total_conversions,
        "total_conversion_links": total_conversion_links,
        "recent_conversions": recent_conversions,
        "event_types": event_types
    })

@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.post("/login")
async def login(request: Request, username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    print(f"🔐 登录尝试: 用户名={username}")
    
    admin_user = db.query(AdminUser).filter(AdminUser.username == username).first()
    
    if not admin_user:
        print(f"❌ 用户不存在: {username}")
        return templates.TemplateResponse("login.html", {
            "request": request,
            "error": "用户名或密码错误"
        })
    
    print(f"✅ 找到用户: {admin_user.username}, 活跃状态: {admin_user.is_active}")
    
    password_valid = verify_password(password, admin_user.hashed_password)
    print(f"🔑 密码验证结果: {password_valid}")
    
    if not password_valid:
        print(f"❌ 密码错误")
        return templates.TemplateResponse("login.html", {
            "request": request,
            "error": "用户名或密码错误"
        })
    
    if not admin_user.is_active:
        print(f"❌ 账户已禁用")
        return templates.TemplateResponse("login.html", {
            "request": request,
            "error": "账户已被禁用"
        })
    
    # 创建token
    token_data = {"username": admin_user.username}
    token, _ = create_access_token(
        data=token_data,
        expires_delta=timedelta(hours=24)
    )
    
    print(f"✅ 登录成功，生成Token")
    
    base_url = get_base_url(request)
    response = RedirectResponse(url=f"{base_url}/admin/", status_code=302)
    response.set_cookie(key="admin_token", value=token, httponly=True, max_age=86400)
    return response

@router.get("/logout")
async def logout(request: Request):
    base_url = get_base_url(request)
    response = RedirectResponse(url=f"{base_url}/admin/login", status_code=302)
    response.delete_cookie(key="admin_token")
    return response

@router.get("/conversions-page", response_class=HTMLResponse)
async def conversions_page(request: Request, db: Session = Depends(get_db)):
    admin_user = get_current_admin_user(request, db)
    if not admin_user:
        base_url = get_base_url(request)
        return RedirectResponse(url=f"{base_url}/admin/login", status_code=302)
    
    conversions = db.query(Conversion).order_by(Conversion.created_at.desc()).all()
    return templates.TemplateResponse("conversions.html", {
        "request": request,
        "admin_user": admin_user,
        "conversions": conversions
    })

@router.get("/events-page", response_class=HTMLResponse)
async def events_page(request: Request, db: Session = Depends(get_db)):
    admin_user = get_current_admin_user(request, db)
    if not admin_user:
        base_url = get_base_url(request)
        return RedirectResponse(url=f"{base_url}/admin/login", status_code=302)
    
    events = db.query(Event).order_by(Event.created_at.desc()).limit(100).all()
    return templates.TemplateResponse("events.html", {
        "request": request,
        "admin_user": admin_user,
        "events": events
    })

@router.get("/conversion-links-page", response_class=HTMLResponse)
async def conversion_links_page(request: Request, db: Session = Depends(get_db)):
    admin_user = get_current_admin_user(request, db)
    if not admin_user:
        base_url = get_base_url(request)
        return RedirectResponse(url=f"{base_url}/admin/login", status_code=302)
    
    conversion_links = db.query(ConversionLink).order_by(ConversionLink.created_at.desc()).all()
    return templates.TemplateResponse("conversion_links.html", {
        "request": request,
        "admin_user": admin_user,
        "conversion_links": conversion_links
    })

# API endpoints (保持原有的API接口)
@router.get("/conversions", response_model=List[ConversionRecord])
async def get_all_conversions(db: Session = Depends(get_db)):
    """获取所有转换记录"""
    return db.query(Conversion).all()

@router.get("/events", response_model=List[EventResponse])
async def get_all_events(db: Session = Depends(get_db)):
    """获取所有事件记录"""
    return db.query(Event).all()

@router.get("/stats")
async def get_stats(db: Session = Depends(get_db)):
    """获取统计信息"""
    total_events = db.query(Event).count()
    total_conversions = db.query(Conversion).count()
    
    # 按事件类型统计
    event_types = db.query(Event.event_type, db.func.count(Event.id)).group_by(Event.event_type).all()
    
    return {
        "total_events": total_events,
        "total_conversions": total_conversions,
        "event_types": [{"type": et[0], "count": et[1]} for et in event_types]
    }
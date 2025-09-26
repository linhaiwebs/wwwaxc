from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict, Any

# Admin schemas
class AdminLogin(BaseModel):
    username: str
    password: str

class AdminUser(BaseModel):
    id: int
    username: str
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

# Token schemas
class TokenResponse(BaseModel):
    token: str
    expires_at: datetime

# Event schemas
class EventCreate(BaseModel):
    event_type: str
    meta: Optional[Dict[str, Any]] = None

class EventResponse(BaseModel):
    id: int
    session_id: str
    event_type: str
    meta: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

# Conversion schemas
class ConversionCreate(BaseModel):
    input_value: str

class ConversionResponse(BaseModel):
    redirect_url: str

class ConversionRecord(BaseModel):
    id: int
    input_value: str
    target_url: str
    session_id: str
    created_at: datetime
    
    class Config:
        from_attributes = True

# Conversion Link schemas
class ConversionLinkCreate(BaseModel):
    name: str
    target_url: str
    weight: Optional[float] = 1.0

class ConversionLinkUpdate(BaseModel):
    name: Optional[str] = None
    target_url: Optional[str] = None
    weight: Optional[float] = None

class ConversionLinkResponse(BaseModel):
    id: int
    name: str
    target_url: str
    weight: float
    created_at: datetime
    
    class Config:
        from_attributes = True
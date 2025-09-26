#!/usr/bin/env python3
"""
数据库初始化脚本
创建示例转换链接数据
"""

from sqlalchemy.orm import Session
from app.database.database import SessionLocal, engine
from app.models import Base, ConversionLink, AdminUser
from app.core.security import get_password_hash

def init_database():
    """初始化数据库并创建示例数据"""
    
    # 创建所有表
    Base.metadata.create_all(bind=engine)
    
    # 创建数据库会话
    db = SessionLocal()
    
    try:
        # 创建默认管理员账户
        existing_admin = db.query(AdminUser).filter(AdminUser.username == "admin").first()
        if not existing_admin:
            admin_user = AdminUser(
                username="admin",
                hashed_password=get_password_hash("admin123"),
                is_active=True
            )
            db.add(admin_user)
            print("✅ 已创建默认管理员账户: admin / admin123")
        
        # 检查是否已有转换链接
        existing_links = db.query(ConversionLink).count()
        
        if existing_links == 0:
            # 创建示例转换链接
            sample_links = [
                ConversionLink(
                    name="LINE官方账号1",
                    target_url="https://line.me/R/ti/p/@example1",
                    weight=3.0
                ),
                ConversionLink(
                    name="LINE官方账号2", 
                    target_url="https://line.me/R/ti/p/@example2",
                    weight=2.0
                ),
                ConversionLink(
                    name="LINE官方账号3",
                    target_url="https://line.me/R/ti/p/@example3", 
                    weight=1.0
                )
            ]
            
            for link in sample_links:
                db.add(link)
            
            print("✅ 数据库初始化完成，已创建示例转换链接")
        else:
            print("✅ 数据库已存在数据，跳过初始化")
        
        db.commit()
            
    except Exception as e:
        print(f"❌ 数据库初始化失败: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_database()
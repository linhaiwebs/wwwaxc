#!/usr/bin/env python3
"""
数据库初始化脚本
创建示例转换链接数据
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from app.database.database import SessionLocal, engine
from app.models import Base, ConversionLink, AdminUser
from app.core.security import get_password_hash

def init_database():
    """初始化数据库并创建示例数据"""
    
    print("🔄 开始初始化数据库...")
    
    # 创建所有表
    Base.metadata.create_all(bind=engine)
    print("✅ 数据库表创建完成")
    
    # 创建数据库会话
    db = SessionLocal()
    
    try:
        # 创建默认管理员账户
        existing_admin = db.query(AdminUser).filter(AdminUser.username == "admin").first()
        if not existing_admin:
            hashed_password = get_password_hash("admin123")
            print(f"🔐 生成密码哈希: {hashed_password[:50]}...")
            
            admin_user = AdminUser(
                username="admin",
                hashed_password=hashed_password,
                is_active=True
            )
            db.add(admin_user)
            db.commit()
            print("✅ 已创建默认管理员账户: admin / admin123")
        else:
            print("ℹ️  管理员账户已存在")
        
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
            
            db.commit()
            
            print("✅ 数据库初始化完成，已创建示例转换链接")
        else:
            print("✅ 数据库已存在数据，跳过初始化")
        
        # 验证管理员账户
        admin_count = db.query(AdminUser).count()
        print(f"📊 管理员账户数量: {admin_count}")
            
    except Exception as e:
        print(f"❌ 数据库初始化失败: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_database()
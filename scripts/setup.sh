#!/bin/bash

echo "🚀 设置AI股价診断项目..."

# 创建必要的目录
mkdir -p data
mkdir -p logs

# 复制环境变量文件
if [ ! -f backend/.env ]; then
    cp backend/.env.example backend/.env
    echo "✅ 已创建后端环境变量文件"
fi

if [ ! -f frontend/.env ]; then
    cp frontend/.env.example frontend/.env
    echo "✅ 已创建前端环境变量文件"
fi

# 设置权限
chmod +x scripts/*.sh
chmod 755 data

echo "✅ 项目设置完成！"
echo ""
echo "📋 下一步："
echo "1. 编辑 backend/.env 和 frontend/.env 配置文件"
echo "2. 运行 'docker-compose up -d --build' 启动服务"
echo "3. 访问 http://localhost:8080 查看应用"
echo ""
echo "📚 更多信息请查看 README.md"
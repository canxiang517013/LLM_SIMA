#!/bin/bash

# 学生信息管理助手 - 启动脚本 (Linux/Mac)

set -e

echo "========================================"
echo "  学生信息管理助手 - 启动脚本"
echo "========================================"
echo ""

# 检查Python是否安装
echo "[1/5] 检查Python环境..."
if ! command -v python3 &> /dev/null; then
    echo "[错误] 未检测到Python3，请先安装Python 3.12+"
    exit 1
fi
echo "[OK] Python版本: $(python3 --version)"

# 检查MySQL是否运行
echo ""
echo "[2/5] 检查MySQL服务状态..."
if ! command -v mysql &> /dev/null; then
    echo "[警告] 未检测到MySQL客户端，请确保MySQL已安装并运行"
else
    if mysqladmin ping -h localhost -uroot -psycsyc517013 &> /dev/null; then
        echo "[OK] MySQL服务运行正常"
    else
        echo "[警告] MySQL服务可能未启动，请确保MySQL正在运行"
    fi
fi

# 检查虚拟环境
echo ""
echo "[3/5] 检查Python虚拟环境..."
if [ ! -d "venv" ]; then
    echo "[信息] 未找到虚拟环境，创建虚拟环境..."
    python3 -m venv venv
fi

# 激活虚拟环境
echo "[信息] 激活虚拟环境..."
source venv/bin/activate

# 安装后端依赖
echo ""
echo "[4/5] 检查后端依赖..."
if ! pip show fastapi &> /dev/null; then
    echo "[信息] 安装后端依赖..."
    pip install -r requirements.txt
else
    echo "[OK] 后端依赖已安装"
fi

# 初始化数据库
echo ""
echo "[5/5] 初始化数据库..."
echo "[提示] 如果数据库已存在，将跳过此步骤"
if mysql -h localhost -uroot -psycsyc517013 student_db < database/init.sql 2>/dev/null; then
    echo "[OK] 数据库初始化成功"
else
    echo "[提示] 数据库可能已存在，继续启动服务..."
fi

echo ""
echo "========================================"
echo "  启动后端服务..."
echo "========================================"
echo ""
echo "后端服务地址: http://localhost:8000"
echo "API文档地址: http://localhost:8000/docs"
echo ""
echo "按 Ctrl+C 停止服务"
echo ""

python -m backend.main

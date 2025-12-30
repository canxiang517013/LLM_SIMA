@echo off
chcp 65001 > nul
echo ========================================
echo   学生信息管理助手 - 启动脚本
echo ========================================
echo.

REM 检查Python是否安装
python --version > nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 未检测到Python，请先安装Python 3.12+
    pause
    exit /b 1
)

REM 检查MySQL是否运行
echo [1/5] 检查MySQL服务状态...
mysqladmin ping -h localhost -u root -p%sycsyc517013% > nul 2>&1
if %errorlevel% neq 0 (
    echo [警告] MySQL服务可能未启动，请确保MySQL正在运行
    echo.
) else (
    echo [OK] MySQL服务运行正常
)

REM 检查虚拟环境
echo [2/5] 检查Python虚拟环境...
if not exist "venv" (
    echo [信息] 未找到虚拟环境，创建虚拟环境...
    python -m venv venv
    if %errorlevel% neq 0 (
        echo [错误] 虚拟环境创建失败
        pause
        exit /b 1
    )
)

REM 激活虚拟环境
echo [3/5] 激活虚拟环境...
call venv\Scripts\activate.bat

REM 安装后端依赖
echo [4/5] 检查后端依赖...
pip show fastapi > nul 2>&1
if %errorlevel% neq 0 (
    echo [信息] 安装后端依赖...
    pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo [错误] 依赖安装失败
        pause
        exit /b 1
    )
) else (
    echo [OK] 后端依赖已安装
)

REM 初始化数据库
echo [5/5] 初始化数据库...
echo [提示] 如果数据库已存在，将跳过此步骤
mysql -h localhost -u root -psycsyc517013 student_db < database\init.sql 2>nul
if %errorlevel% equ 0 (
    echo [OK] 数据库初始化成功
) else (
    echo [提示] 数据库可能已存在，继续启动服务...
)

echo.
echo ========================================
echo   启动后端服务...
echo ========================================
echo.
echo 后端服务地址: http://localhost:8000
echo API文档地址: http://localhost:8000/docs
echo.
echo 按 Ctrl+C 停止服务
echo.

python -m backend.main

pause

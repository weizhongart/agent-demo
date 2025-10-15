#!/bin/bash

# 多智能体客服系统快速启动脚本

echo "=========================================="
echo "  多智能体客服系统 - 快速启动"
echo "=========================================="
echo ""

# 检查Python版本
echo "检查Python版本..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Python版本: $python_version"

# 检查是否存在.env文件
if [ ! -f .env ]; then
    echo ""
    echo "⚠️  未找到.env文件"
    echo "正在从.env.example创建.env文件..."
    cp .env.example .env
    echo "✓ .env文件已创建"
    echo ""
    echo "⚠️  请编辑.env文件，填入您的DASHSCOPE_API_KEY"
    echo "   使用命令: nano .env  或  vi .env"
    echo ""
    read -p "按Enter继续（确保已配置API密钥）..."
fi

# 检查是否安装了依赖
echo ""
echo "检查依赖安装..."
if ! python3 -c "import agentscope" 2>/dev/null; then
    echo "未检测到agentscope，正在安装依赖..."
    pip install -r requirements.txt
    echo "✓ 依赖安装完成"
else
    echo "✓ 依赖已安装"
fi

# 创建日志目录
echo ""
echo "创建日志目录..."
mkdir -p logs
echo "✓ 日志目录已准备"

echo ""
echo "=========================================="
echo "  系统启动中..."
echo "=========================================="
echo ""

# 启动系统
python3 main.py

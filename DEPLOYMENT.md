# 多智能体客服系统 - 交付文档

## 项目信息

- **项目名称**: 多智能体客服系统 (AgentScope)
- **框架版本**: AgentScope 1.0+
- **开发语言**: Python 3.10+
- **交付日期**: 2025-10-15

## 系统概述

本系统是一个基于阿里开源AgentScope框架构建的智能客服系统,通过3个专业AI Agent的协作,实现电商场景下的自动化客户服务。系统具备意图识别、知识检索、订单查询和工单管理等核心功能。

## 核心特性

### 🤖 三大智能体

1. **接待Agent (Friday)**
   - 负责用户接待和意图识别
   - 协调其他Agent处理请求
   - 提供友好的对话体验

2. **检索Agent**
   - 处理知识库相关咨询
   - 基于TF-IDF的语义检索
   - 提供准确的知识解答

3. **工单Agent**
   - 处理订单查询和售后问题
   - 自动创建和分配工单
   - 智能优先级判断

### 🎯 主要功能

- ✅ 智能意图识别与任务路由
- ✅ 知识库语义检索 (6条预置知识)
- ✅ 订单查询 (4个测试订单)
- ✅ 工单创建与客服分配 (5个模拟客服)
- ✅ 多轮对话支持
- ✅ 完整的日志系统
- ✅ 异常处理机制

## 项目结构

```
agent-demo/
├── agents/              # 智能体实现 (3个Agent)
├── config/              # 配置管理
├── core/                # 核心系统 (初始化、协作)
├── models/              # 数据模型 (消息、工单、知识)
├── tools/               # 工具函数 (12个工具)
├── mock/                # 模拟外部系统
├── utils/               # 工具模块 (日志、异常)
├── examples/            # 示例脚本
├── main.py              # 主程序入口
├── verify_system.py     # 系统验证脚本
├── quickstart.sh        # 快速启动脚本
└── requirements.txt     # 依赖列表
```

## 使用指南

### 1. 环境准备

**系统要求**:
- Python 3.10 或更高版本
- 通义千问API密钥

### 2. 安装步骤

```bash
# 进入项目目录
cd agent-demo

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑.env文件，设置DASHSCOPE_API_KEY
```

### 3. 启动系统

**方式一: 直接运行**
```bash
python main.py
```

**方式二: 快速启动脚本**
```bash
./quickstart.sh
```

### 4. 系统验证

```bash
python verify_system.py
```

### 5. 运行示例

```bash
python examples/sample_conversations.py
```

## 测试数据

### 测试订单号

- `ORD001`: 正常发货中的订单 (¥299)
- `ORD002`: 延迟发货的订单 (¥1599, 库存不足)
- `ORD003`: 高价值订单 (¥5999)
- `ORD004`: 已送达订单 (¥199)

### 知识库内容

1. 如何查询订单物流信息
2. 退货退款流程说明
3. 无线蓝牙耳机使用教程
4. 配送时效说明
5. 支付方式说明
6. 账户安全设置

### 客服人员

- 王小明 (订单处理组)
- 李华 (订单处理组)
- 张丽 (售后处理组)
- 刘强 (售后处理组)
- 赵敏 (综合处理组)

## 使用示例

### 示例1: 知识咨询

```
用户: 蓝牙耳机怎么使用?
系统: [检索Agent从知识库中查找使用教程并返回详细说明]
```

### 示例2: 订单查询

```
用户: 查询订单ORD001的物流
系统: [工单Agent查询订单系统并返回物流信息]
```

### 示例3: 售后处理

```
用户: 我要退货，订单号ORD003
系统: [工单Agent创建退货工单并分配客服]
```

## 技术架构

### 核心技术栈

- **AgentScope 1.0**: 多智能体框架
- **通义千问**: 大语言模型
- **Pydantic**: 数据验证
- **Loguru**: 日志系统
- **Scikit-learn**: TF-IDF向量化

### 设计模式

- **ReAct模式**: 推理-行动循环
- **工具调用**: 函数式工具集成
- **消息传递**: Agent间通信
- **单例模式**: 模拟系统管理

## 系统配置

### 环境变量 (.env)

```env
# API配置
DASHSCOPE_API_KEY=your_api_key_here

# 模型配置
MODEL_NAME=qwen-max
MODEL_TEMPERATURE=0.7
MODEL_MAX_TOKENS=2000

# 系统配置
SESSION_TIMEOUT=1800
MAX_CONVERSATION_ROUNDS=20
KNOWLEDGE_RETRIEVAL_THRESHOLD=0.6
```

### Agent提示词

所有Agent的系统提示词都在 `config/settings.py` 中定义,可根据需要调整。

## 扩展指南

### 添加新的工具函数

1. 在 `tools/` 目录下创建工具函数
2. 在对应Agent中注册工具
3. 更新Agent的系统提示词

### 添加新的知识

在 `mock/knowledge_base.py` 的 `_init_knowledge_data` 方法中添加新的知识条目。

### 集成真实系统

替换 `mock/` 目录下的模拟系统为真实API调用。

## 已知限制

1. **模拟系统**: 当前使用模拟数据,生产环境需集成真实系统
2. **会话持久化**: 会话数据仅在内存中,重启后丢失
3. **并发限制**: 单进程运行,不支持高并发场景
4. **向量检索**: 使用简单的TF-IDF,可升级为专业向量数据库

## 后续优化建议

### 短期优化

1. ✅ 添加单元测试和集成测试
2. ✅ 实现会话持久化 (Redis/数据库)
3. ✅ 添加Web界面 (FastAPI + Vue)
4. ✅ 优化日志输出格式

### 中期优化

1. 🔄 集成向量数据库 (Milvus/Weaviate)
2. 🔄 实现真实的MsgHub协作
3. 🔄 添加性能监控 (Prometheus)
4. 🔄 支持多模态输入 (图片、语音)

### 长期优化

1. 📋 微服务架构改造
2. 📋 支持分布式部署
3. 📋 添加AI训练反馈循环
4. 📋 实现自动化测试流程

## 文件清单

### 核心文件 (必需)

- `main.py` - 主程序入口
- `requirements.txt` - Python依赖
- `.env` - 环境变量配置 (需创建)
- `README.md` - 项目文档

### 代码文件 (28个Python文件)

```
agents/          - 3个Agent实现
config/          - 配置模块
core/            - 系统核心
models/          - 数据模型
tools/           - 工具函数
mock/            - 模拟系统
utils/           - 工具模块
examples/        - 示例脚本
```

### 辅助文件

- `quickstart.sh` - 快速启动
- `verify_system.py` - 系统验证
- `PROJECT_SUMMARY.md` - 项目总结
- `DEPLOYMENT.md` - 本文档

## 常见问题

### Q1: API密钥错误?

**A**: 确保在 `.env` 文件中正确配置了 `DASHSCOPE_API_KEY`

### Q2: 依赖安装失败?

**A**: 升级pip后重试
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Q3: Agent无响应?

**A**: 检查网络连接和API配额,查看日志文件 `logs/customer_service.log`

### Q4: 如何修改Agent行为?

**A**: 编辑 `config/settings.py` 中的Agent提示词

## 联系与支持

- 项目文档: README.md
- 示例代码: examples/sample_conversations.py
- 问题反馈: 通过Issue提交

## 版本历史

- **v1.0.0** (2025-10-15)
  - 初始版本发布
  - 实现3个核心Agent
  - 完整的工具函数体系
  - 模拟系统支持

## 许可证

MIT License

---

**注意**: 本系统仅供学习和演示使用。生产环境部署需要:
1. 替换模拟系统为真实API
2. 添加安全认证机制
3. 实现会话持久化
4. 配置负载均衡
5. 完善错误处理和监控

---

**交付检查清单**:

- [x] 所有代码文件完整
- [x] 依赖配置文件完整
- [x] 环境变量示例文件
- [x] README文档完善
- [x] 示例脚本可运行
- [x] 快速启动脚本
- [x] 系统验证脚本
- [x] 项目总结文档
- [x] 部署文档 (本文件)

**系统已就绪,可以交付使用!** ✅

# 多智能体客服系统 (AgentScope)

基于阿里开源的 [AgentScope](https://github.com/modelscope/agentscope) 框架构建的智能客服系统，通过多个AI智能体协作，实现电商场景下的自动化客户服务。

## ✨ 项目特性

- 🤖 **多智能体协作**: 3个专业Agent分工协作
  - 接待Agent (Friday): 用户接待、意图识别、任务路由
  - 检索Agent: 知识库语义检索
  - 工单Agent: 订单查询、工单创建、客服分配

- 🎯 **智能意图识别**: 自动判断用户需求，路由到合适的处理流程

- 📚 **知识库检索**: 基于TF-IDF的语义检索，快速匹配用户问题

- 🎫 **工单管理**: 自动创建工单、智能分配客服、优先级判断

- 🔄 **ReAct框架**: 利用AgentScope的ReAct Agent实现推理-行动循环

- 🛠️ **工具调用**: 完整的工具函数体系，支持订单查询、知识检索、工单管理

## 🏗️ 系统架构

```
用户
  |
  v
接待Agent (Friday)
  |
  +-- 意图识别 --+
  |              |
  v              v
检索Agent    工单Agent
  |              |
知识库        订单系统
              工单系统
```

## 📁 项目结构

```
agent-demo/
├── agents/                 # Agent实现
│   ├── reception_agent.py # 接待Agent
│   ├── retrieval_agent.py # 检索Agent
│   └── ticket_agent.py    # 工单Agent
├── config/                 # 配置模块
│   └── settings.py        # 系统配置
├── core/                   # 核心模块
│   ├── initializer.py     # 系统初始化
│   └── collaboration.py   # Agent协作
├── models/                 # 数据模型
│   ├── message.py         # 消息模型
│   ├── ticket.py          # 工单模型
│   └── knowledge.py       # 知识库模型
├── tools/                  # 工具函数
│   ├── knowledge_tools.py # 知识库工具
│   ├── order_tools.py     # 订单工具
│   └── ticket_tools.py    # 工单工具
├── mock/                   # 模拟系统
│   ├── order_system.py    # 模拟订单系统
│   ├── ticket_system.py   # 模拟工单系统
│   └── knowledge_base.py  # 模拟知识库
├── utils/                  # 工具模块
│   ├── logger.py          # 日志系统
│   └── exceptions.py      # 异常定义
├── tests/                  # 测试用例
├── examples/               # 示例代码
├── main.py                 # 主程序入口
├── requirements.txt        # 依赖列表
├── .env.example            # 环境变量示例
└── README.md               # 项目文档
```

## 🚀 快速开始

### 1. 环境准备

**系统要求**:
- Python 3.10+
- 通义千问API密钥

### 2. 安装依赖

```bash
# 克隆项目
cd agent-demo

# 安装依赖
pip install -r requirements.txt
```

### 3. 配置环境变量

```bash
# 复制环境变量模板
cp .env.example .env

# 编辑.env文件，填入您的API密钥
# DASHSCOPE_API_KEY=your_dashscope_api_key_here
```

### 4. 运行系统

```bash
python main.py
```

## 💬 使用示例

### 知识咨询

```
👤 您: 蓝牙耳机怎么使用？
🤖 客服 Friday: [检索Agent会从知识库中查找相关使用教程]
```

### 订单查询

```
👤 您: 查询订单ORD001的物流
🤖 客服 Friday: [工单Agent会调用订单系统查询物流信息]
```

### 售后处理

```
👤 您: 我要退货
🤖 客服 Friday: [工单Agent会创建退货工单并分配客服]
```

## 🧪 测试数据

系统内置了测试数据供体验:

**测试订单号**:
- `ORD001`: 正常发货中的订单
- `ORD002`: 延迟发货的订单(库存不足)
- `ORD003`: 高价值订单(¥5999)
- `ORD004`: 已送达订单

**知识库内容**:
- 如何查询订单物流信息
- 退货退款流程说明
- 无线蓝牙耳机使用教程
- 配送时效说明
- 支付方式说明
- 账户安全设置

## 🔧 配置说明

系统配置在 `.env` 文件中:

```env
# 通义千问API配置
DASHSCOPE_API_KEY=your_api_key

# 模型配置
MODEL_NAME=qwen-max
MODEL_TEMPERATURE=0.7
MODEL_MAX_TOKENS=2000

# 系统配置
SESSION_TIMEOUT=1800
MAX_CONVERSATION_ROUNDS=20
KNOWLEDGE_RETRIEVAL_THRESHOLD=0.6
```

## 📊 技术栈

- **核心框架**: [AgentScope 1.0+](https://github.com/modelscope/agentscope)
- **大语言模型**: 通义千问 (qwen-max)
- **数据验证**: Pydantic
- **日志系统**: Loguru
- **向量检索**: Scikit-learn (TF-IDF)
- **异步支持**: asyncio

## 🎓 核心概念

### ReAct Agent

ReAct (Reasoning + Acting) 是一种Agent范式,结合推理和行动:
1. **Reasoning**: LLM分析任务,决定下一步行动
2. **Acting**: 调用工具函数执行操作
3. **Observing**: 观察工具执行结果
4. 循环迭代直到完成任务

### 工具函数 (Tools)

Agent可调用的函数,例如:
- `search_knowledge`: 检索知识库
- `query_order_status`: 查询订单状态
- `create_ticket`: 创建工单

### 多智能体协作

通过消息传递实现Agent间协作:
- 接待Agent识别意图并路由
- 专业Agent处理具体任务
- 结果返回给接待Agent统一响应

## 📝 开发指南

### 添加新的工具函数

1. 在 `tools/` 目录下定义工具函数:

```python
def new_tool(param: str) -> str:
    """工具函数说明"""
    # 实现逻辑
    return result
```

2. 在Agent创建时注册工具:

```python
toolkit.add(new_tool)
```

### 添加新的Agent

1. 在 `agents/` 目录下创建新Agent:

```python
from agentscope.agents import ReActAgent

def create_new_agent(model_config):
    toolkit = ServiceToolkit()
    # 注册工具...
    
    return ReActAgent(
        name="new_agent",
        model_config_name=model_config["config_name"],
        service_toolkit=toolkit,
        sys_prompt="Agent系统提示词",
    )
```

2. 在初始化模块中创建实例
3. 在协作模块中添加路由逻辑

## 🐛 故障排查

### API密钥错误

```
错误: DASHSCOPE_API_KEY 未设置
解决: 在.env文件中配置正确的API密钥
```

### 依赖安装失败

```bash
# 升级pip
pip install --upgrade pip

# 重新安装依赖
pip install -r requirements.txt
```

### 日志查看

日志文件位于 `logs/customer_service.log`,错误日志在 `logs/error.log`

## 🤝 贡献

欢迎提交Issue和Pull Request!

## 📄 许可证

MIT License

## 🙏 致谢

- [AgentScope](https://github.com/modelscope/agentscope) - 阿里开源的多智能体框架
- [通义千问](https://tongyi.aliyun.com/) - 阿里云大语言模型

## 📧 联系方式

如有问题或建议,欢迎提Issue讨论。

---

**注意**: 本项目仅供学习和演示使用,生产环境请根据实际需求进行优化和安全加固。

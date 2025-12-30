# 基于大语言模型的学生信息管理助手

这是一个基于大语言模型的学生信息管理智能助手系统，采用前后端分离架构，使用DeepSeek大模型实现自然语言交互。

## 功能特点

### （一）大模型交互界面
- 美观的聊天式UI界面
- 支持消息气泡展示
- 实时打字效果
- 支持Markdown渲染

### （二）基本对话功能
- 连接DeepSeek大语言模型
- 支持多轮对话
- 流式响应
- 完善的错误处理和重试机制

### （三）学生信息数据库
- MySQL数据库存储学生信息
- 完整的学生信息字段（姓名、学号、班级、学院、专业、年级、性别、手机号等）
- 数据验证和约束

### （四）数据库管理
- **Text2SQL技术**：自然语言转SQL查询
- 支持增、删、改、查四种操作
- 安全机制：
  - 写操作需要管理员令牌验证
  - SQL注入防护
  - 影响行数限制
- Few-shot examples提高准确性

### （五）查询结果绘图
- 自动判断适合的图表类型（柱状图、饼图、折线图）
- Matplotlib生成高质量图表
- Base64编码传输，前端直接展示

## 技术栈

### 后端
- **Python 3.12**
- **FastAPI** - 高性能Web框架
- **SQLAlchemy** - ORM框架
- **PyMySQL** - MySQL驱动
- **LangChain** - LLM应用框架
- **OpenAI SDK** - DeepSeek API客户端
- **Matplotlib** - 图表生成
- **Pandas** - 数据处理

### 前端
- **React 18** - UI框架
- **TypeScript** - 类型安全
- **Ant Design** - UI组件库
- **Axios** - HTTP客户端
- **Recharts** - 图表库
- **Vite** - 构建工具

## 项目结构

```
student_management_assistant/
├── backend/                    # 后端服务
│   ├── api/                    # API路由
│   │   ├── chat.py            # 聊天接口
│   │   ├── database.py        # 数据库管理接口
│   │   └── chart.py           # 图表生成接口
│   ├── core/                   # 核心功能
│   │   ├── llm_client.py      # LLM客户端
│   │   ├── text2sql.py        # Text2SQL转换
│   │   ├── database_manager.py # 数据库操作
│   │   └── chart_generator.py # 图表生成器
│   ├── models/                 # 数据模型
│   │   ├── database.py        # 数据库模型
│   │   └── schemas.py         # Pydantic模型
│   ├── utils/                  # 工具函数
│   │   ├── config.py          # 配置管理
│   │   └── logger.py          # 日志工具
│   └── main.py                # FastAPI主程序
├── frontend/                   # 前端应用
│   ├── src/
│   │   ├── components/        # React组件
│   │   ├── services/          # API服务
│   │   ├── types/             # TypeScript类型
│   │   ├── App.tsx            # 主应用
│   │   └── main.tsx           # 入口文件
│   ├── package.json
│   ├── vite.config.ts
│   └── tsconfig.json
├── database/                   # 数据库脚本
│   └── init.sql               # 初始化脚本
├── requirements.txt            # Python依赖
├── .env                       # 环境配置
└── README.md                  # 项目文档
```

## 快速开始

### 1. 环境要求

- Python 3.12+
- Node.js 18+
- MySQL 8.0+
- DeepSeek API Key

### 2. 配置环境变量

编辑 `.env` 文件，配置以下信息：

```env
# DeepSeek API配置
DEEPSEEK_API_KEY=your_api_key_here
DEEPSEEK_BASE_URL=https://api.deepseek.com
DEEPSEEK_MODEL=deepseek-chat

# 数据库配置
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=your_password_here
MYSQL_DATABASE=student_db

# 安全配置
ADMIN_TOKEN=student_project_2024
```

### 3. 初始化数据库

执行数据库初始化脚本：

```bash
mysql -u root -p < database/init.sql
```

或手动执行SQL命令：

```bash
mysql -u root -p
source database/init.sql
```

### 4. 安装后端依赖

```bash
pip install -r requirements.txt
```

### 5. 启动后端服务

```bash
python -m backend.main
```

后端服务将在 `http://localhost:8000` 启动

访问API文档：`http://localhost:8000/docs`

### 6. 安装前端依赖

```bash
cd frontend
npm install
```

### 7. 启动前端服务

```bash
npm run dev
```

前端服务将在 `http://localhost:3000` 启动

## 使用说明

### 查询操作（无需管理员令牌）

- 查询所有学生信息：`查询所有学生的信息`
- 按学院查询：`查询计算机学院的所有学生`
- 统计各年级人数：`统计每个年级的学生人数`
- 统计性别比例：`查询男女生的人数`
- 查询特定班级：`查询计算机1班的学生`

### 增删改操作（需要管理员令牌）

管理员令牌在 `.env` 文件中的 `ADMIN_TOKEN` 配置

- 添加学生：
  ```
  添加学生：张三，学号2025001，计算机1班，计算机学院，计算机科学与技术专业，2025级，男，手机13800138001
  ```
  
- 更新学生信息：
  ```
  更新学号2024001的学生的手机号为13900139001
  ```
  
- 删除学生：
  ```
  删除学号2024001的学生
  ```

## API接口

### 聊天接口
- **POST** `/api/chat/` - 发送消息，AI自动判断是普通对话还是数据库操作

### 数据库管理接口
- **GET** `/api/database/students` - 获取学生列表
- **GET** `/api/database/students/{student_id}` - 根据学号查询学生
- **POST** `/api/database/students` - 创建学生
- **PUT** `/api/database/students/{student_id}` - 更新学生信息
- **DELETE** `/api/database/students/{student_id}` - 删除学生
- **POST** `/api/database/query` - 自然语言查询（Text2SQL）

### 图表生成接口
- **POST** `/api/chart/generate` - 生成图表

## 安全说明

1. **管理员令牌**：增删改操作需要验证管理员令牌
2. **SQL注入防护**：使用参数化查询，禁止危险SQL操作
3. **影响行数限制**：单次操作最多影响100行
4. **查询行数限制**：单次查询最多返回1000行
5. **危险操作禁止**：DROP、TRUNCATE、ALTER等操作被禁止

## 常见问题

### 1. 数据库连接失败
检查 `.env` 文件中的数据库配置是否正确，确保MySQL服务已启动。

### 2. LLM调用失败
检查 `DEEPSEEK_API_KEY` 是否正确，网络是否可以访问DeepSeek API。

### 3. 图表显示异常
确保后端安装了matplotlib和中文字体支持。

### 4. 前端无法访问后端API
检查后端是否启动，端口是否正确（默认8000）。

## 开发说明

### 后端开发
- 使用FastAPI框架，支持自动生成API文档
- 使用SQLAlchemy ORM进行数据库操作
- 使用LangChain集成LLM功能

### 前端开发
- 使用React + TypeScript
- 使用Ant Design组件库
- 使用Vite作为开发服务器

## 许可证

MIT License

## 作者

学生信息管理助手开发团队

## 致谢

- DeepSeek - 提供大语言模型API
- Ant Design - 提供优秀的UI组件库
- FastAPI - 提供高性能Web框架

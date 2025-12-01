# AI Coding Teacher - 智能编程导师

一个AI驱动的编程学习平台，包含面试模拟、代码对战、个性化学习等功能。

## 核心功能

### AI 面试官模拟
- 支持 Google、Meta、Amazon 等公司风格
- 算法面试、系统设计、行为面试、前端专项
- 实时对话和代码编辑
- 详细评分报告和改进建议

### 智能题库系统
- 500+ 精选算法题
- AI 个性化推荐
- 渐进式提示系统
- 多语言支持 (Python, JavaScript, Java, C++)

### 代码对战
- 实时 1v1 对战
- ELO 评分系统
- 全球排行榜
- 好友挑战和锦标赛

### 知识图谱
- 可视化学习路径
- 掌握程度追踪
- 智能推荐下一步

## 快速开始

### 前提条件

- Node.js 18+
- Python 3.10+
- (可选) OpenAI API Key 或 Anthropic API Key

### 后端设置

```bash
# 进入后端目录
cd backend

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 创建 .env 文件
cp .env.example .env
# 编辑 .env 添加你的 API keys

# 初始化数据库并添加示例数据
python seed_data.py

# 启动服务器
uvicorn app.main:app --reload --port 8000
```

### 前端设置

```bash
# 进入前端目录
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

访问 http://localhost:3000 开始使用

## 技术栈

### 前端
- **框架**: Next.js 14 + TypeScript
- **样式**: Tailwind CSS
- **状态管理**: Zustand
- **代码编辑器**: Monaco Editor
- **可视化**: React Flow
- **动画**: Framer Motion

### 后端
- **框架**: FastAPI + Python
- **数据库**: SQLite (开发) / PostgreSQL (生产)
- **实时通信**: Socket.IO
- **AI**: OpenAI GPT-4 / Claude

### 代码执行
- Piston API (多语言支持)
- Docker 沙箱 (生产环境)

## 项目结构

```
AI-coding-teacher/
├── frontend/                 # Next.js 前端
│   ├── src/
│   │   ├── app/             # 页面和路由
│   │   │   ├── problems/    # 题库页面
│   │   │   ├── interview/   # 面试页面
│   │   │   ├── battle/      # 对战页面
│   │   │   └── dashboard/   # 仪表盘
│   │   ├── components/      # React 组件
│   │   ├── lib/             # 工具函数和 API
│   │   └── store/           # Zustand 状态
│   └── package.json
│
├── backend/                  # FastAPI 后端
│   ├── app/
│   │   ├── routers/         # API 路由
│   │   ├── services/        # 业务逻辑
│   │   ├── models/          # 数据模型
│   │   └── schemas/         # Pydantic 模式
│   ├── requirements.txt
│   └── seed_data.py         # 示例数据
│
└── README.md
```

## 配置

### 环境变量

后端 (`backend/.env`):
```env
# AI Services
OPENAI_API_KEY=sk-your-key
ANTHROPIC_API_KEY=sk-ant-your-key

# Database
DATABASE_URL=sqlite:///./coding_teacher.db

# JWT
SECRET_KEY=your-secret-key
```

### 不使用 AI API

系统可以在没有 AI API key 的情况下运行（演示模式）：
- 面试对话会返回预设的回复
- 代码分析功能会返回基本反馈

## 功能截图

### 首页
现代化的深色主题，展示核心功能。

### 题库
支持难度、主题、公司筛选的题目列表。

### AI 面试
实时对话界面，左侧代码编辑器，右侧对话区。

### 代码对战
分屏显示双方进度，实时状态同步。

### 知识图谱
可交互的知识点关系图，显示掌握程度。

## API 文档

启动后端后访问 http://localhost:8000/docs 查看完整的 API 文档。

### 主要端点

- `POST /api/users/register` - 用户注册
- `POST /api/users/login` - 用户登录
- `GET /api/problems` - 获取题目列表
- `GET /api/problems/{slug}` - 获取题目详情
- `POST /api/problems/{slug}/submit` - 提交代码
- `POST /api/interviews/start` - 开始面试
- `POST /api/interviews/{id}/message` - 发送消息
- `POST /api/battles/create` - 创建对战
- `POST /api/execute/run` - 运行代码

## 部署

### Vercel (前端)
```bash
cd frontend
vercel
```

### Railway/Fly.io (后端)
```bash
cd backend
# 按照平台文档部署
```

### 数据库
- 开发: SQLite
- 生产: PostgreSQL (推荐 Neon 或 Supabase)

## 贡献

欢迎提交 Pull Request

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

## 致谢

- [Monaco Editor](https://microsoft.github.io/monaco-editor/)
- [React Flow](https://reactflow.dev/)
- [Piston API](https://github.com/engineer-man/piston)
- [OpenAI](https://openai.com/)
- [Anthropic](https://anthropic.com/)

---

AI Coding Teacher Team

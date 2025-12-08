# Cok11 - AI Coding Teacher

<p align="center">
  <img src="./AI%20Coding%20Teacher.gif" alt="Cok11 Demo" width="800">
</p>

A modern coding education platform with algorithm problem library, real-time code battles, and knowledge graph visualization. Clean GitHub-style UI with bilingual support (English/Chinese) and all AI features running locally.

## Features

### Problem Library
- **49 curated algorithm problems** (Fundamental, Medium, Hard)
- Topics: Arrays, Strings, Hash Tables, Trees, Graphs, Dynamic Programming, Linked Lists, Binary Search, Sliding Window, Two Pointers, Bit Manipulation, Trie, Heap
- Multi-language support: Python, JavaScript, Java, C++, Go, Rust
- Progressive hint system with detailed solutions

### Authentication
- **Google OAuth Login** - One-click sign in with Google account
- Traditional email/password registration
- JWT-based session management

### Code Battle
- **Quick Battle**: Fill-in-the-blank and multiple choice code questions with timer
- **Code Battle**: Real-time 1v1 competitive coding
- ELO rating system for fair matchmaking
- Same problem, race to finish first
- Code similarity detection

### Dashboard
- Knowledge graph visualization of learning progress (React Flow)
- Topic mastery tracking
- Personal statistics (problems solved, battles won, streaks)
- **Submission History** - View all past submissions with code and AI feedback

### Local AI
- AST-based code analysis (Python, JavaScript)
- Cyclomatic and cognitive complexity metrics
- Time/Space complexity estimation
- Algorithm pattern detection (Two Pointers, Sliding Window, Binary Search, DFS, BFS, DP, etc.)
- Code quality scoring with actionable suggestions
- Plagiarism detection via Winnowing fingerprint algorithm

### Internationalization
- Bilingual UI: English and Chinese
- Persistent language preference

## Quick Start

### Requirements

- Node.js 18+
- Python 3.10+

### Backend

```bash
cd backend

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Linux/Mac: source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy environment config
cp .env.example .env

# Initialize database
python seed_data.py

# Start server
uvicorn app.main:app --reload --port 8000
```

### Frontend

```bash
cd frontend

npm install
npm run dev
```

Access the application at http://localhost:3000

## Tech Stack

### Frontend
- Next.js 14 with App Router and TypeScript
- Tailwind CSS with custom GitHub-style design
- Monaco Editor for code editing
- React Flow for knowledge graph visualization
- Framer Motion for animations
- Zustand for state management
- Socket.IO Client for real-time features
- Lucide React for icons

### Backend
- FastAPI with async support
- SQLAlchemy 2.0 with SQLite (dev) / PostgreSQL (prod)
- Python-SocketIO for real-time communication
- Piston API for secure code execution
- Custom AST-based code analyzer
- JWT authentication with bcrypt


## Configuration

### Backend Environment Variables

```env
DATABASE_URL=sqlite:///./coding_teacher.db
SECRET_KEY=your-secret-key-change-in-production
PISTON_API_URL=https://emkc.org/api/v2/piston
GOOGLE_CLIENT_ID=your-google-client-id  # Optional: for Google OAuth
```

### Frontend Environment Variables

```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api
NEXT_PUBLIC_SOCKET_URL=http://localhost:8000
NEXT_PUBLIC_GOOGLE_CLIENT_ID=your-google-client-id  # Optional: for Google OAuth
```

## API Endpoints

### Users
- `POST /api/users/register` - User registration
- `POST /api/users/login` - Authentication
- `POST /api/users/auth/google` - Google OAuth login
- `GET /api/users/me` - Current user profile
- `GET /api/users/me/stats` - User statistics (problems solved, etc.)
- `GET /api/users/me/submissions` - User submission history
- `GET /api/users/leaderboard` - Global rankings

### Problems
- `GET /api/problems` - List problems with filters
- `GET /api/problems/{slug}` - Problem details
- `POST /api/problems/{slug}/submit` - Submit solution
- `GET /api/problems/recommended` - Personalized recommendations

### Battles
- `POST /api/battles/create` - Create battle room
- `POST /api/battles/{id}/join` - Join battle
- `POST /api/battles/{id}/submit` - Submit battle solution
- `GET /api/battles/{id}/compare` - Compare solutions

### Code Execution
- `POST /api/execute/run` - Execute code
- `POST /api/execute/test` - Run test cases
- `POST /api/execute/analyze` - Analyze code quality

Full API documentation available at http://localhost:8000/docs

## Deployment

### Frontend (Vercel)

```bash
cd frontend
vercel
```

### Backend (Railway/Fly.io)

Configure environment variables and deploy following platform documentation.

### Database

- Development: SQLite (default)
- Production: PostgreSQL recommended

## License

MIT License - See LICENSE file for details

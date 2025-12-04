# Cok11 - AI Coding Teacher

<p align="center">
  <img src="./AI%20Coding%20Teacher.gif" alt="Cok11 Demo" width="800">
</p>

A modern coding education platform with algorithm problem library, real-time code battles, and knowledge graph visualization. Clean GitHub-style UI with all AI features running locally.

## Features

### Problem Library
- 500+ curated algorithm problems (Easy, Medium, Hard)
- Topics: Arrays, Strings, Hash Tables, Trees, Graphs, Dynamic Programming
- Multi-language support: Python, JavaScript, Java, C++, Go, Rust
- Progressive hint system

### Code Battle
- Real-time 1v1 competitive coding
- ELO rating system for fair matchmaking
- Same problem, race to finish first
- Code similarity detection

### Dashboard
- Knowledge graph visualization of learning progress
- Topic mastery tracking
- Personal statistics

### Local AI
- AST-based code analysis
- Complexity estimation (time/space)
- Algorithm pattern detection
- Plagiarism detection via Winnowing fingerprint

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
- Next.js 14 with TypeScript
- Tailwind CSS
- Monaco Editor
- React Flow
- Zustand
- Socket.IO Client

### Backend
- FastAPI
- SQLAlchemy with SQLite/PostgreSQL
- Socket.IO
- Piston API for code execution


## Configuration

### Backend Environment Variables

```env
DATABASE_URL=sqlite:///./coding_teacher.db
SECRET_KEY=your-secret-key-change-in-production
PISTON_API_URL=https://emkc.org/api/v2/piston
```

### Frontend Environment Variables

```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api
NEXT_PUBLIC_SOCKET_URL=http://localhost:8000
```

## API Endpoints

### Users
- `POST /api/users/register` - User registration
- `POST /api/users/login` - Authentication
- `GET /api/users/me` - Current user profile
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

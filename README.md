# AI Coding Teacher

An AI-powered coding education platform featuring interview simulation, code battles, and personalized learning.

## Core Features

### AI Interview Simulator
- Supports Google, Meta, Amazon interview styles
- Algorithm, System Design, Behavioral, and Frontend interviews
- Real-time conversation and code editing
- Detailed scoring reports and improvement suggestions

### Smart Problem Library
- 500+ curated algorithm problems
- AI-powered personalized recommendations
- Progressive hint system
- Multi-language support (Python, JavaScript, Java, C++)

### Code Battle
- Real-time 1v1 battles
- ELO rating system
- Global leaderboard
- Friend challenges and tournaments

### Knowledge Graph
- Visual learning paths
- Mastery level tracking
- Smart next-step recommendations

## Quick Start

### Prerequisites

- Node.js 18+
- Python 3.10+
- (Optional) OpenAI API Key or Anthropic API Key

### Backend Setup

```bash
# Enter backend directory
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env to add your API keys

# Initialize database and seed sample data
python seed_data.py

# Start the server
uvicorn app.main:app --reload --port 8000
```

### Frontend Setup

```bash
# Enter frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Visit http://localhost:3000 to get started.

## Tech Stack

### Frontend
- **Framework**: Next.js 14 + TypeScript
- **Styling**: Tailwind CSS
- **State Management**: Zustand
- **Code Editor**: Monaco Editor
- **Visualization**: React Flow
- **Animation**: Framer Motion

### Backend
- **Framework**: FastAPI + Python
- **Database**: SQLite (dev) / PostgreSQL (prod)
- **Real-time**: Socket.IO
- **AI**: OpenAI GPT-4 / Claude

### Code Execution
- Piston API (multi-language support)
- Docker sandbox (production)

## Project Structure

```
frontend/          Next.js 14 app
backend/           FastAPI server
```

## Configuration

### Environment Variables

Backend (`backend/.env`):
```env
# AI Services
OPENAI_API_KEY=sk-your-key
ANTHROPIC_API_KEY=sk-ant-your-key

# Database
DATABASE_URL=sqlite:///./coding_teacher.db

# JWT
SECRET_KEY=your-secret-key
```

### Running Without AI API

The system can run without AI API keys (demo mode):
- Interview conversations return preset responses
- Code analysis returns basic feedback

## Screenshots

### Home Page
Modern dark theme showcasing core features.

### Problem Library
Problem list with difficulty, topic, and company filters.

### AI Interview
Real-time conversation interface with code editor on the left and chat on the right.

### Code Battle
Split-screen showing both players' progress with real-time sync.

### Knowledge Graph
Interactive knowledge node graph showing mastery levels.

## API Documentation

Visit http://localhost:8000/docs after starting the backend for complete API documentation.

### Main Endpoints

- `POST /api/users/register` - User registration
- `POST /api/users/login` - User login
- `GET /api/problems` - Get problem list
- `GET /api/problems/{slug}` - Get problem details
- `POST /api/problems/{slug}/submit` - Submit code
- `POST /api/interviews/start` - Start interview
- `POST /api/interviews/{id}/message` - Send message
- `POST /api/battles/create` - Create battle
- `POST /api/execute/run` - Run code

## Deployment

### Vercel (Frontend)
```bash
cd frontend
vercel
```

### Railway/Fly.io (Backend)
```bash
cd backend
# Follow platform documentation
```

### Database
- Development: SQLite
- Production: PostgreSQL (Neon or Supabase recommended)

## Contributing

Pull requests are welcome.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

MIT License - See [LICENSE](LICENSE) file for details

## Acknowledgments

- [Monaco Editor](https://microsoft.github.io/monaco-editor/)
- [React Flow](https://reactflow.dev/)
- [Piston API](https://github.com/engineer-man/piston)
- [OpenAI](https://openai.com/)
- [Anthropic](https://anthropic.com/)

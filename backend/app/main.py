"""
AI Coding Teacher - Backend API
Main FastAPI Application
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import socketio

from app.routers import problems, interviews, battles, users, execution
from app.services.websocket_manager import sio


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler"""
    print("🚀 AI Coding Teacher Backend Starting...")
    yield
    print("👋 Shutting down...")


# Create FastAPI app
app = FastAPI(
    title="AI Coding Teacher API",
    description="AI-powered coding education platform with interview simulation, code battles, and personalized learning",
    version="1.0.0",
    lifespan=lifespan
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(users.router, prefix="/api/users", tags=["Users"])
app.include_router(problems.router, prefix="/api/problems", tags=["Problems"])
app.include_router(interviews.router, prefix="/api/interviews", tags=["Interviews"])
app.include_router(battles.router, prefix="/api/battles", tags=["Battles"])
app.include_router(execution.router, prefix="/api/execute", tags=["Code Execution"])

# Socket.IO app
socket_app = socketio.ASGIApp(sio, other_asgi_app=app)


@app.get("/")
async def root():
    return {
        "message": "AI Coding Teacher API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


# For running with Socket.IO support
def get_app():
    return socket_app


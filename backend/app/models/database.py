"""
Database configuration and models
"""

from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, DateTime, Text, JSON, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

from app.config import settings

engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# User Model
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True)
    username = Column(String(100), unique=True, index=True)
    hashed_password = Column(String(255), nullable=True)  # Nullable for OAuth users
    avatar_url = Column(String(500), nullable=True)
    
    # OAuth fields
    oauth_provider = Column(String(50), nullable=True)  # 'google', 'github', etc.
    oauth_id = Column(String(255), nullable=True)  # Provider's user ID
    
    # Skill tracking
    skill_level = Column(String(20), default="beginner")  # beginner, intermediate, advanced
    knowledge_state = Column(JSON, default={})  # Topic mastery scores
    elo_rating = Column(Integer, default=1200)
    
    # Statistics
    problems_solved = Column(Integer, default=0)
    interviews_completed = Column(Integer, default=0)
    battles_won = Column(Integer, default=0)
    current_streak = Column(Integer, default=0)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    submissions = relationship("Submission", back_populates="user")
    interviews = relationship("Interview", back_populates="user")


# Problem Model
class Problem(Base):
    __tablename__ = "problems"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), index=True)
    slug = Column(String(255), unique=True, index=True)
    description = Column(Text)
    difficulty = Column(String(20))  # easy, medium, hard
    
    # Problem content
    examples = Column(JSON)  # Input/output examples
    constraints = Column(JSON)  # Problem constraints
    starter_code = Column(JSON)  # Starter code for each language
    test_cases = Column(JSON)  # Test cases for validation
    hidden_test_cases = Column(JSON)  # Hidden test cases
    
    # Metadata
    topics = Column(JSON)  # ["array", "two_pointers", "hash_table"]
    companies = Column(JSON)  # ["google", "meta", "amazon"]
    patterns = Column(JSON)  # ["sliding_window", "binary_search"]
    
    # Solutions
    hints = Column(JSON)  # Progressive hints
    solutions = Column(JSON)  # Multiple solutions with explanations
    time_complexity = Column(String(50))
    space_complexity = Column(String(50))
    
    # Statistics
    acceptance_rate = Column(Float, default=0.0)
    submission_count = Column(Integer, default=0)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    submissions = relationship("Submission", back_populates="problem")


# Submission Model
class Submission(Base):
    __tablename__ = "submissions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    problem_id = Column(Integer, ForeignKey("problems.id"))
    
    code = Column(Text)
    language = Column(String(50))
    status = Column(String(50))  # accepted, wrong_answer, time_limit, etc.
    
    # Results
    runtime_ms = Column(Integer, nullable=True)
    memory_kb = Column(Integer, nullable=True)
    test_results = Column(JSON)  # Results for each test case
    
    # AI Feedback
    ai_feedback = Column(Text, nullable=True)
    code_quality_score = Column(Float, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="submissions")
    problem = relationship("Problem", back_populates="submissions")


# Interview Model
class Interview(Base):
    __tablename__ = "interviews"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    
    # Interview configuration
    interview_type = Column(String(50))  # algorithm, system_design, behavioral, frontend
    company = Column(String(100))  # google, meta, amazon, startup
    difficulty = Column(String(20))
    duration_minutes = Column(Integer)
    
    # Interview content
    problem_ids = Column(JSON)  # Problems used in interview
    conversation_history = Column(JSON)  # Full conversation log
    code_snapshots = Column(JSON)  # Code at different points
    
    # Results
    status = Column(String(20))  # in_progress, completed, abandoned
    overall_score = Column(Float, nullable=True)
    dimension_scores = Column(JSON)  # Scores for each dimension
    time_analysis = Column(JSON)  # Time spent on each phase
    feedback = Column(Text, nullable=True)
    ai_suggestions = Column(JSON)  # Improvement suggestions
    
    started_at = Column(DateTime, default=datetime.utcnow)
    ended_at = Column(DateTime, nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="interviews")


# Battle Model
class Battle(Base):
    __tablename__ = "battles"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Participants
    player1_id = Column(Integer, ForeignKey("users.id"))
    player2_id = Column(Integer, ForeignKey("users.id"))
    
    # Battle configuration
    problem_id = Column(Integer, ForeignKey("problems.id"))
    mode = Column(String(50))  # quick_match, tournament, friend_challenge
    time_limit_seconds = Column(Integer, default=900)  # 15 minutes
    
    # Progress tracking
    player1_progress = Column(JSON)  # {tests_passed, code_lines, attempts}
    player2_progress = Column(JSON)
    
    # Results
    winner_id = Column(Integer, nullable=True)
    player1_score = Column(Integer, nullable=True)
    player2_score = Column(Integer, nullable=True)
    player1_submission = Column(Text, nullable=True)
    player2_submission = Column(Text, nullable=True)
    
    status = Column(String(20), default="waiting")  # waiting, in_progress, completed
    
    started_at = Column(DateTime, nullable=True)
    ended_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


# Project Model
class Project(Base):
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255))
    slug = Column(String(255), unique=True)
    description = Column(Text)
    difficulty = Column(String(20))
    
    # Project content
    learning_objectives = Column(JSON)
    prerequisites = Column(JSON)
    weeks = Column(JSON)  # Weekly breakdown with tasks
    resources = Column(JSON)
    
    # Related problems
    problem_ids = Column(JSON)
    
    created_at = Column(DateTime, default=datetime.utcnow)


# Create all tables
def init_db():
    Base.metadata.create_all(bind=engine)


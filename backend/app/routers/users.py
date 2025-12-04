"""
User Routes - Authentication and Profile Management
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from jose import JWTError, jwt
from typing import Optional
import bcrypt

from app.models.database import get_db, User
from app.schemas.schemas import UserCreate, UserResponse, Token
from app.config import settings

router = APIRouter()

# OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/users/login")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    password_bytes = plain_password.encode('utf-8')[:72]
    hashed_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_bytes)


def get_password_hash(password: str) -> str:
    password_bytes = password.encode('utf-8')[:72]
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password_bytes, salt).decode('utf-8')


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: int = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise credentials_exception
    return user


@router.post("/register")
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """Register a new user and return token"""
    # Check if email exists
    if db.query(User).filter(User.email == user_data.email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Check if username exists
    if db.query(User).filter(User.username == user_data.username).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )
    
    # Create user
    hashed_password = get_password_hash(user_data.password)
    user = User(
        email=user_data.email,
        username=user_data.username,
        hashed_password=hashed_password,
        knowledge_state={}
    )
    
    db.add(user)
    db.commit()
    db.refresh(user)
    
    # Create token and return with user info
    access_token = create_access_token(data={"sub": str(user.id)})
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": str(user.id),
            "email": user.email,
            "name": user.username,
        }
    }


@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """Login and get access token (form data)"""
    # Find user by email or username
    user = db.query(User).filter(
        (User.email == form_data.username) | (User.username == form_data.username)
    ).first()
    
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email/username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data={"sub": str(user.id)})
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": str(user.id),
            "email": user.email,
            "name": user.username,
        }
    }


from pydantic import BaseModel

class LoginRequest(BaseModel):
    email: str
    password: str

@router.post("/login/json")
async def login_json(
    data: LoginRequest,
    db: Session = Depends(get_db)
):
    """Login with JSON body"""
    user = db.query(User).filter(
        (User.email == data.email) | (User.username == data.email)
    ).first()
    
    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email/username or password"
        )
    
    access_token = create_access_token(data={"sub": str(user.id)})
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": str(user.id),
            "email": user.email,
            "name": user.username,
        }
    }


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    """Get current user profile"""
    return current_user


@router.put("/me", response_model=UserResponse)
async def update_me(
    avatar_url: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update current user profile"""
    if avatar_url:
        current_user.avatar_url = avatar_url
    
    db.commit()
    db.refresh(current_user)
    return current_user


@router.get("/me/stats")
async def get_my_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user statistics"""
    from app.models.database import Submission, Interview, Battle
    
    # Get submission stats
    total_submissions = db.query(Submission).filter(
        Submission.user_id == current_user.id
    ).count()
    
    accepted_submissions = db.query(Submission).filter(
        Submission.user_id == current_user.id,
        Submission.status == "accepted"
    ).count()
    
    # Get interview stats
    interviews = db.query(Interview).filter(
        Interview.user_id == current_user.id
    ).all()
    
    avg_interview_score = 0
    if interviews:
        scores = [i.overall_score for i in interviews if i.overall_score]
        avg_interview_score = sum(scores) / len(scores) if scores else 0
    
    # Get battle stats
    battles_won = db.query(Battle).filter(
        Battle.winner_id == current_user.id
    ).count()
    
    battles_played = db.query(Battle).filter(
        (Battle.player1_id == current_user.id) | (Battle.player2_id == current_user.id),
        Battle.status == "completed"
    ).count()
    
    return {
        "user_id": current_user.id,
        "problems_solved": current_user.problems_solved,
        "total_submissions": total_submissions,
        "acceptance_rate": accepted_submissions / total_submissions if total_submissions > 0 else 0,
        "interviews_completed": current_user.interviews_completed,
        "average_interview_score": avg_interview_score,
        "battles_won": battles_won,
        "battles_played": battles_played,
        "win_rate": battles_won / battles_played if battles_played > 0 else 0,
        "current_streak": current_user.current_streak,
        "elo_rating": current_user.elo_rating,
        "skill_level": current_user.skill_level,
        "knowledge_state": current_user.knowledge_state
    }


@router.get("/leaderboard")
async def get_leaderboard(
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get global leaderboard"""
    users = db.query(User).order_by(User.elo_rating.desc()).limit(limit).all()
    
    return [
        {
            "rank": i + 1,
            "username": user.username,
            "avatar_url": user.avatar_url,
            "elo_rating": user.elo_rating,
            "problems_solved": user.problems_solved,
            "battles_won": user.battles_won
        }
        for i, user in enumerate(users)
    ]


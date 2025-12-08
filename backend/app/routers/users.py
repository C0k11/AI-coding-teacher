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
import httpx
import logging

from pydantic import BaseModel
from app.models.database import get_db, User
from app.schemas.schemas import UserCreate, UserResponse, Token
from app.config import settings

logger = logging.getLogger(__name__)

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
    from sqlalchemy import func
    
    # Get submission stats
    total_submissions = db.query(Submission).filter(
        Submission.user_id == current_user.id
    ).count()
    
    accepted_submissions = db.query(Submission).filter(
        Submission.user_id == current_user.id,
        Submission.status == "accepted"
    ).count()
    
    # Get unique problems solved (count distinct problem_ids with accepted status)
    problems_solved = db.query(func.count(func.distinct(Submission.problem_id))).filter(
        Submission.user_id == current_user.id,
        Submission.status == "accepted"
    ).scalar() or 0
    
    # Update user's problems_solved if different
    if current_user.problems_solved != problems_solved:
        current_user.problems_solved = problems_solved
        db.commit()
    
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
        "problems_solved": problems_solved,
        "total_submissions": total_submissions,
        "accepted_submissions": accepted_submissions,
        "acceptance_rate": round(accepted_submissions / total_submissions * 100, 1) if total_submissions > 0 else 0,
        "interviews_completed": current_user.interviews_completed,
        "average_interview_score": avg_interview_score,
        "battles_won": battles_won,
        "battles_played": battles_played,
        "win_rate": round(battles_won / battles_played * 100, 1) if battles_played > 0 else 0,
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


# Google OAuth
class GoogleAuthRequest(BaseModel):
    credential: str  # Google ID token


@router.post("/auth/google")
async def google_auth(request: GoogleAuthRequest, db: Session = Depends(get_db)):
    """
    Authenticate with Google ID token
    """
    try:
        # Verify the Google ID token
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"https://oauth2.googleapis.com/tokeninfo?id_token={request.credential}"
            )
            
            if response.status_code != 200:
                raise HTTPException(status_code=401, detail="Invalid Google token")
            
            google_user = response.json()
            
            # Validate the token is for our app
            if settings.GOOGLE_CLIENT_ID and google_user.get("aud") != settings.GOOGLE_CLIENT_ID:
                logger.warning(f"Token audience mismatch: {google_user.get('aud')}")
                # In development, we might skip this check
                if settings.ENVIRONMENT != "development":
                    raise HTTPException(status_code=401, detail="Invalid token audience")
        
        google_id = google_user.get("sub")
        email = google_user.get("email")
        name = google_user.get("name", email.split("@")[0])
        avatar = google_user.get("picture")
        
        # Find existing user by oauth_id or email
        existing_user = db.query(User).filter(User.oauth_id == google_id).first()
        if not existing_user:
            existing_user = db.query(User).filter(User.email == email).first()
        
        if existing_user:
            # Update existing user
            if avatar and avatar != existing_user.avatar_url:
                existing_user.avatar_url = avatar
            if not existing_user.oauth_id:
                existing_user.oauth_id = google_id
                existing_user.oauth_provider = "google"
            db.commit()
            user = existing_user
        else:
            # Create new user
            user = User(
                email=email,
                username=name.replace(" ", "_").lower() + "_" + google_id[-6:],
                hashed_password=None,
                avatar_url=avatar,
                oauth_provider="google",
                oauth_id=google_id,
                knowledge_state={}
            )
            db.add(user)
            db.commit()
            db.refresh(user)
        
        access_token = create_access_token(data={"sub": str(user.id)})
        
        logger.info(f"Google auth successful for: {email}")
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "id": str(user.id),
                "email": user.email,
                "name": user.username,
                "avatar": user.avatar_url,
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Google auth error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Authentication failed: {str(e)}")


# Get all submissions for a user
@router.get("/me/submissions")
async def get_my_all_submissions(
    status: Optional[str] = None,
    limit: int = 50,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all user's submissions (刷题记录)"""
    from app.models.database import Submission, Problem
    
    query = db.query(Submission).filter(Submission.user_id == current_user.id)
    
    if status:
        query = query.filter(Submission.status == status)
    
    submissions = query.order_by(Submission.created_at.desc()).limit(limit).all()
    
    result = []
    for sub in submissions:
        problem = db.query(Problem).filter(Problem.id == sub.problem_id).first()
        result.append({
            "id": sub.id,
            "problem_id": sub.problem_id,
            "problem_title": problem.title if problem else "Unknown",
            "problem_slug": problem.slug if problem else "",
            "problem_difficulty": problem.difficulty if problem else "",
            "code": sub.code,
            "language": sub.language,
            "status": sub.status,
            "runtime_ms": sub.runtime_ms,
            "memory_kb": sub.memory_kb,
            "ai_feedback": sub.ai_feedback,
            "created_at": sub.created_at.isoformat() if sub.created_at else None
        })
    
    return {
        "submissions": result,
        "total": len(result)
    }


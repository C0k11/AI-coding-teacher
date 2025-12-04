"""
Battle Routes - Code Battle System
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional
import uuid

from app.models.database import get_db, Battle, Problem, User
from app.schemas.schemas import BattleCreate, BattleStatus
from app.routers.users import get_current_user
from app.services.ai_service import ai_service

router = APIRouter()


@router.post("/create")
async def create_battle(
    config: BattleCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new battle room"""
    
    # Get a random problem for the battle
    problems = db.query(Problem).filter(Problem.difficulty == "medium").all()
    if not problems:
        problems = db.query(Problem).all()
    
    if not problems:
        raise HTTPException(status_code=404, detail="No problems available")
    
    import random
    problem = random.choice(problems)
    
    # Find opponent if friend challenge
    player2_id = None
    if config.mode == "friend_challenge" and config.friend_username:
        friend = db.query(User).filter(User.username == config.friend_username).first()
        if not friend:
            raise HTTPException(status_code=404, detail="Friend not found")
        player2_id = friend.id
    
    # Create battle
    battle = Battle(
        player1_id=current_user.id,
        player2_id=player2_id,
        problem_id=problem.id,
        mode=config.mode,
        time_limit_seconds=900,  # 15 minutes
        player1_progress={"tests_passed": 0, "code_lines": 0, "attempts": 0},
        player2_progress={"tests_passed": 0, "code_lines": 0, "attempts": 0},
        status="waiting"
    )
    
    db.add(battle)
    db.commit()
    db.refresh(battle)
    
    return {
        "battle_id": battle.id,
        "problem": {
            "id": problem.id,
            "title": problem.title,
            "slug": problem.slug,
            "difficulty": problem.difficulty
        },
        "mode": battle.mode,
        "status": battle.status
    }


@router.post("/{battle_id}/join")
async def join_battle(
    battle_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Join an existing battle"""
    
    battle = db.query(Battle).filter(Battle.id == battle_id).first()
    if not battle:
        raise HTTPException(status_code=404, detail="Battle not found")
    
    if battle.status != "waiting":
        raise HTTPException(status_code=400, detail="Battle already started or completed")
    
    if battle.player1_id == current_user.id:
        raise HTTPException(status_code=400, detail="Cannot join your own battle")
    
    if battle.player2_id and battle.player2_id != current_user.id:
        raise HTTPException(status_code=400, detail="Battle is for another player")
    
    # Join battle
    battle.player2_id = current_user.id
    battle.status = "in_progress"
    battle.started_at = datetime.utcnow()
    
    db.commit()
    
    problem = db.query(Problem).filter(Problem.id == battle.problem_id).first()
    
    return {
        "battle_id": battle.id,
        "problem": {
            "id": problem.id,
            "title": problem.title,
            "slug": problem.slug,
            "difficulty": problem.difficulty,
            "description": problem.description,
            "examples": problem.examples,
            "starter_code": problem.starter_code
        },
        "opponent": db.query(User).filter(User.id == battle.player1_id).first().username,
        "time_limit_seconds": battle.time_limit_seconds,
        "status": battle.status
    }


@router.get("/{battle_id}")
async def get_battle(
    battle_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get battle status"""
    
    battle = db.query(Battle).filter(Battle.id == battle_id).first()
    if not battle:
        raise HTTPException(status_code=404, detail="Battle not found")
    
    # Check if user is participant
    if battle.player1_id != current_user.id and battle.player2_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not a participant")
    
    problem = db.query(Problem).filter(Problem.id == battle.problem_id).first()
    player1 = db.query(User).filter(User.id == battle.player1_id).first()
    player2 = db.query(User).filter(User.id == battle.player2_id).first() if battle.player2_id else None
    winner = db.query(User).filter(User.id == battle.winner_id).first() if battle.winner_id else None
    
    # Calculate time remaining
    time_remaining = battle.time_limit_seconds
    if battle.started_at:
        elapsed = (datetime.utcnow() - battle.started_at).total_seconds()
        time_remaining = max(0, int(battle.time_limit_seconds - elapsed))
    
    return {
        "id": battle.id,
        "problem": {
            "id": problem.id,
            "title": problem.title,
            "slug": problem.slug,
            "difficulty": problem.difficulty,
            "description": problem.description if battle.status == "in_progress" else None,
            "examples": problem.examples if battle.status == "in_progress" else None,
            "starter_code": problem.starter_code if battle.status == "in_progress" else None
        },
        "player1": {"username": player1.username, "progress": battle.player1_progress},
        "player2": {"username": player2.username, "progress": battle.player2_progress} if player2 else None,
        "mode": battle.mode,
        "status": battle.status,
        "time_remaining_seconds": time_remaining,
        "winner": winner.username if winner else None
    }


@router.post("/{battle_id}/submit")
async def submit_battle_solution(
    battle_id: int,
    code: str,
    language: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Submit solution in battle"""
    from app.services.code_executor import code_executor, local_executor
    
    battle = db.query(Battle).filter(Battle.id == battle_id).first()
    if not battle:
        raise HTTPException(status_code=404, detail="Battle not found")
    
    if battle.status != "in_progress":
        raise HTTPException(status_code=400, detail="Battle not in progress")
    
    # Check if time is up
    if battle.started_at:
        elapsed = (datetime.utcnow() - battle.started_at).total_seconds()
        if elapsed > battle.time_limit_seconds:
            battle.status = "completed"
            db.commit()
            raise HTTPException(status_code=400, detail="Time is up")
    
    # Run tests
    problem = db.query(Problem).filter(Problem.id == battle.problem_id).first()
    test_cases = (problem.test_cases or []) + (problem.hidden_test_cases or [])
    
    try:
        result = await code_executor.run_test_cases(code, language, test_cases)
    except Exception:
        result = await local_executor.run_test_cases(code, language, test_cases)
    
    # Update progress
    is_player1 = battle.player1_id == current_user.id
    progress_field = "player1_progress" if is_player1 else "player2_progress"
    submission_field = "player1_submission" if is_player1 else "player2_submission"
    score_field = "player1_score" if is_player1 else "player2_score"
    
    progress = getattr(battle, progress_field) or {}
    progress["tests_passed"] = result["passed_count"]
    progress["code_lines"] = len(code.split("\n"))
    progress["attempts"] = progress.get("attempts", 0) + 1
    setattr(battle, progress_field, progress)
    
    # Calculate score
    base_score = result["passed_count"] * 100
    time_bonus = max(0, (battle.time_limit_seconds - elapsed) / battle.time_limit_seconds * 200) if battle.started_at else 0
    score = int(base_score + time_bonus)
    
    setattr(battle, submission_field, code)
    setattr(battle, score_field, score)
    
    # Check for winner
    all_passed = result["passed_count"] == result["total_count"]
    if all_passed and not battle.winner_id:
        battle.winner_id = current_user.id
        battle.status = "completed"
        battle.ended_at = datetime.utcnow()
        
        # Update user stats
        current_user.battles_won += 1
        # Update ELO (simplified)
        current_user.elo_rating += 25
    
    db.commit()
    
    return {
        "passed": all_passed,
        "tests_passed": result["passed_count"],
        "total_tests": result["total_count"],
        "score": score,
        "is_winner": battle.winner_id == current_user.id,
        "test_results": result["test_results"][:3]  # Only show first 3 test results
    }


@router.get("/")
async def list_battles(
    status: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List user's battles"""
    
    query = db.query(Battle).filter(
        (Battle.player1_id == current_user.id) | (Battle.player2_id == current_user.id)
    )
    
    if status:
        query = query.filter(Battle.status == status)
    
    battles = query.order_by(Battle.created_at.desc()).limit(50).all()
    
    result = []
    for b in battles:
        problem = db.query(Problem).filter(Problem.id == b.problem_id).first()
        opponent_id = b.player2_id if b.player1_id == current_user.id else b.player1_id
        opponent = db.query(User).filter(User.id == opponent_id).first() if opponent_id else None
        
        result.append({
            "id": b.id,
            "problem_title": problem.title if problem else "Unknown",
            "opponent": opponent.username if opponent else "Waiting...",
            "status": b.status,
            "won": b.winner_id == current_user.id if b.winner_id else None,
            "created_at": b.created_at
        })
    
    return result


@router.get("/matchmaking/queue")
async def get_queue_status(current_user: User = Depends(get_current_user)):
    """Get matchmaking queue status"""
    from app.services.websocket_manager import battle_manager
    
    queue_length = len(battle_manager.waiting_queue)
    
    return {
        "queue_length": queue_length,
        "estimated_wait_seconds": queue_length * 30  # Rough estimate
    }


@router.get("/{battle_id}/compare")
async def compare_battle_solutions(
    battle_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Compare solutions from both players in a completed battle"""
    
    battle = db.query(Battle).filter(Battle.id == battle_id).first()
    if not battle:
        raise HTTPException(status_code=404, detail="Battle not found")
    
    if battle.status != "completed":
        raise HTTPException(status_code=400, detail="Battle not completed yet")
    
    # Check if user is participant
    if battle.player1_id != current_user.id and battle.player2_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not a participant")
    
    # Compare solutions using local AI
    if battle.player1_submission and battle.player2_submission:
        comparison = ai_service.compare_solutions(
            battle.player1_submission,
            battle.player2_submission,
            "python"
        )
        
        return {
            "battle_id": battle_id,
            "similarity": comparison,
            "player1_score": battle.player1_score,
            "player2_score": battle.player2_score,
            "is_suspicious": comparison.get("is_suspicious", False)
        }
    
    return {
        "battle_id": battle_id,
        "similarity": None,
        "message": "One or both players did not submit"
    }


"""
Problem Routes - Problem listing, details, and submissions
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.models.database import get_db, Problem, Submission, User
from app.schemas.schemas import (
    ProblemListItem, ProblemDetail, SubmissionCreate, SubmissionResponse
)
from app.routers.users import get_current_user
from app.services.code_executor import code_executor, local_executor
from app.services.ai_service import ai_service
from app.services.recommendation import recommendation_engine, UserSkillModel

router = APIRouter()


@router.get("/", response_model=List[ProblemListItem])
async def list_problems(
    difficulty: Optional[str] = None,
    topic: Optional[str] = None,
    company: Optional[str] = None,
    search: Optional[str] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """List all problems with filtering"""
    query = db.query(Problem)
    
    if difficulty:
        query = query.filter(Problem.difficulty == difficulty)
    
    if topic:
        query = query.filter(Problem.topics.contains([topic]))
    
    if company:
        query = query.filter(Problem.companies.contains([company]))
    
    if search:
        query = query.filter(Problem.title.ilike(f"%{search}%"))
    
    problems = query.offset(skip).limit(limit).all()
    return problems


@router.get("/recommended")
async def get_recommended_problems(
    limit: int = Query(5, ge=1, le=20),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get personalized problem recommendations"""
    # Get user's solved problem IDs
    solved_ids = set(
        s.problem_id for s in db.query(Submission).filter(
            Submission.user_id == current_user.id,
            Submission.status == "accepted"
        ).all()
    )
    
    # Get all problems
    problems = db.query(Problem).all()
    
    # Get recommendations
    recommendations = recommendation_engine.recommend_problems(
        current_user, problems, solved_ids, limit
    )
    
    return [
        {
            "problem": ProblemListItem.model_validate(rec["problem"]),
            "reason": rec["reason"]
        }
        for rec in recommendations
    ]


@router.get("/topics")
async def get_topics(db: Session = Depends(get_db)):
    """Get all available topics"""
    problems = db.query(Problem).all()
    topics = set()
    for p in problems:
        if p.topics:
            topics.update(p.topics)
    return sorted(list(topics))


@router.get("/companies")
async def get_companies(db: Session = Depends(get_db)):
    """Get all available companies"""
    problems = db.query(Problem).all()
    companies = set()
    for p in problems:
        if p.companies:
            companies.update(p.companies)
    return sorted(list(companies))


@router.get("/{slug}", response_model=ProblemDetail)
async def get_problem(slug: str, db: Session = Depends(get_db)):
    """Get problem details by slug"""
    problem = db.query(Problem).filter(Problem.slug == slug).first()
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")
    return problem


@router.get("/{slug}/hints")
async def get_hints(
    slug: str,
    hint_level: int = Query(1, ge=1, le=3),
    db: Session = Depends(get_db)
):
    """Get progressive hints for a problem"""
    problem = db.query(Problem).filter(Problem.slug == slug).first()
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")
    
    hints = problem.hints or []
    return {"hints": hints[:hint_level]}


@router.get("/{slug}/solutions")
async def get_solutions(
    slug: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get solutions (only if user has solved or attempted)"""
    problem = db.query(Problem).filter(Problem.slug == slug).first()
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")
    
    # Check if user has attempted this problem
    submission = db.query(Submission).filter(
        Submission.user_id == current_user.id,
        Submission.problem_id == problem.id
    ).first()
    
    if not submission:
        raise HTTPException(
            status_code=403,
            detail="You must attempt this problem before viewing solutions"
        )
    
    return {
        "solutions": problem.solutions,
        "time_complexity": problem.time_complexity,
        "space_complexity": problem.space_complexity
    }


@router.post("/{slug}/submit", response_model=SubmissionResponse)
async def submit_solution(
    slug: str,
    submission: SubmissionCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Submit a solution for a problem"""
    problem = db.query(Problem).filter(Problem.slug == slug).first()
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")
    
    # Run test cases
    test_cases = problem.test_cases or []
    hidden_cases = problem.hidden_test_cases or []
    all_tests = test_cases + hidden_cases
    
    # Try Piston API first, then local executor
    try:
        result = await code_executor.run_test_cases(
            submission.code,
            submission.language,
            all_tests
        )
    except Exception:
        # Fallback to local executor
        result = await local_executor.run_test_cases(
            submission.code,
            submission.language,
            all_tests
        )
    
    # Get AI feedback if passed all tests
    ai_feedback = None
    if result["status"] == "accepted":
        try:
            analysis = await ai_service.analyze_code(
                submission.code,
                submission.language,
                {"title": problem.title, "description": problem.description},
                result["test_results"]
            )
            ai_feedback = analysis.get("feedback", str(analysis))
        except Exception:
            pass
    
    # Save submission
    db_submission = Submission(
        user_id=current_user.id,
        problem_id=problem.id,
        code=submission.code,
        language=submission.language,
        status=result["status"],
        runtime_ms=result.get("total_runtime_ms"),
        test_results=result["test_results"],
        ai_feedback=ai_feedback
    )
    
    db.add(db_submission)
    
    # Update problem stats
    problem.submission_count += 1
    if result["status"] == "accepted":
        problem.acceptance_rate = (
            (problem.acceptance_rate * (problem.submission_count - 1) + 100)
            / problem.submission_count
        )
        
        # Update user stats
        # Check if this is first accepted submission for this problem
        existing_accepted = db.query(Submission).filter(
            Submission.user_id == current_user.id,
            Submission.problem_id == problem.id,
            Submission.status == "accepted"
        ).first()
        
        if not existing_accepted:
            current_user.problems_solved += 1
            
            # Update knowledge state
            skill_model = UserSkillModel(current_user)
            skill_model.update_after_problem(problem, True, 1, 0)
            current_user.knowledge_state = skill_model.knowledge_state
    else:
        problem.acceptance_rate = (
            problem.acceptance_rate * (problem.submission_count - 1)
            / problem.submission_count
        )
    
    db.commit()
    db.refresh(db_submission)
    
    return db_submission


@router.get("/{slug}/submissions")
async def get_my_submissions(
    slug: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's submissions for a problem"""
    problem = db.query(Problem).filter(Problem.slug == slug).first()
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")
    
    submissions = db.query(Submission).filter(
        Submission.user_id == current_user.id,
        Submission.problem_id == problem.id
    ).order_by(Submission.created_at.desc()).all()
    
    return submissions


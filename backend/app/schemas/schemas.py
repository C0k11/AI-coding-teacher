"""
Pydantic schemas for API request/response validation
"""

from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict, Any
from datetime import datetime


# ============== User Schemas ==============

class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    avatar_url: Optional[str]
    skill_level: str
    knowledge_state: Dict[str, float]
    elo_rating: int
    problems_solved: int
    interviews_completed: int
    battles_won: int
    current_streak: int
    created_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


# ============== Problem Schemas ==============

class ProblemBase(BaseModel):
    title: str
    description: str
    difficulty: str
    examples: List[Dict[str, Any]]
    constraints: List[str]
    topics: List[str]
    companies: List[str]


class ProblemCreate(ProblemBase):
    slug: str
    starter_code: Dict[str, str]
    test_cases: List[Dict[str, Any]]
    hidden_test_cases: List[Dict[str, Any]]
    hints: List[str]
    solutions: List[Dict[str, Any]]
    time_complexity: str
    space_complexity: str


class ProblemListItem(BaseModel):
    id: int
    title: str
    slug: str
    difficulty: str
    topics: List[str]
    companies: List[str]
    acceptance_rate: float
    submission_count: int

    class Config:
        from_attributes = True


class ProblemDetail(BaseModel):
    id: int
    title: str
    slug: str
    description: str
    difficulty: str
    examples: List[Dict[str, Any]]
    constraints: List[str]
    starter_code: Dict[str, str]
    topics: List[str]
    companies: List[str]
    patterns: List[str]
    hints: List[str]
    acceptance_rate: float

    class Config:
        from_attributes = True


# ============== Code Execution Schemas ==============

class CodeExecutionRequest(BaseModel):
    code: str
    language: str
    test_cases: Optional[List[Dict[str, Any]]] = None
    problem_id: Optional[int] = None


class TestCaseResult(BaseModel):
    input: str
    expected_output: str
    actual_output: str
    passed: bool
    runtime_ms: Optional[int]
    error: Optional[str]


class CodeExecutionResponse(BaseModel):
    status: str  # accepted, wrong_answer, time_limit, runtime_error, compile_error
    test_results: List[TestCaseResult]
    total_runtime_ms: Optional[int]
    memory_kb: Optional[int]
    passed_count: int
    total_count: int


# ============== Submission Schemas ==============

class SubmissionCreate(BaseModel):
    problem_id: int
    code: str
    language: str


class SubmissionResponse(BaseModel):
    id: int
    problem_id: int
    code: str
    language: str
    status: str
    runtime_ms: Optional[int]
    memory_kb: Optional[int]
    test_results: List[Dict[str, Any]]
    ai_feedback: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


# ============== Interview Schemas ==============

class InterviewStart(BaseModel):
    interview_type: str  # algorithm, system_design, behavioral, frontend
    company: str
    difficulty: str
    duration_minutes: int = 45


class InterviewMessage(BaseModel):
    interview_id: int
    message: str
    code: Optional[str] = None


class InterviewMessageResponse(BaseModel):
    role: str  # interviewer, candidate
    content: str
    timestamp: datetime
    hints_used: Optional[int] = 0


class InterviewReport(BaseModel):
    interview_id: int
    overall_score: float
    dimension_scores: Dict[str, float]
    time_analysis: Dict[str, int]
    strengths: List[str]
    improvements: List[str]
    ai_suggestions: List[str]
    recommended_problems: List[int]


# ============== Battle Schemas ==============

class BattleCreate(BaseModel):
    mode: str = "quick_match"  # quick_match, friend_challenge
    friend_username: Optional[str] = None


class BattleJoin(BaseModel):
    battle_id: int


class BattleProgress(BaseModel):
    battle_id: int
    tests_passed: int
    code_lines: int


class BattleStatus(BaseModel):
    id: int
    player1_username: str
    player2_username: Optional[str]
    problem: ProblemListItem
    mode: str
    time_limit_seconds: int
    status: str
    player1_progress: Optional[Dict[str, Any]]
    player2_progress: Optional[Dict[str, Any]]
    winner_username: Optional[str]
    started_at: Optional[datetime]
    time_remaining_seconds: Optional[int]


# ============== Knowledge Graph Schemas ==============

class KnowledgeNode(BaseModel):
    id: str
    label: str
    mastery: float
    problems_solved: int
    total_problems: int
    color: str


class KnowledgeEdge(BaseModel):
    source: str
    target: str
    type: str  # prerequisite, related


class KnowledgeGraph(BaseModel):
    nodes: List[KnowledgeNode]
    edges: List[KnowledgeEdge]


# ============== Recommendation Schemas ==============

class ProblemRecommendation(BaseModel):
    problems: List[ProblemListItem]
    reason: str
    target_skill: str


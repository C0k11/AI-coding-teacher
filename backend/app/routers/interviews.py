"""
Interview Routes - AI Interview Simulation
"""

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List, Optional
import json

from app.models.database import get_db, Interview, Problem, User
from app.schemas.schemas import InterviewStart, InterviewMessage, InterviewReport
from app.routers.users import get_current_user
from app.services.ai_service import ai_service

router = APIRouter()


# Sample problems for different interview types
INTERVIEW_PROBLEMS = {
    "algorithm": {
        "easy": [
            {"title": "Two Sum", "description": "给定一个整数数组 nums 和一个整数目标值 target，请你在该数组中找出和为目标值 target 的那两个整数，并返回它们的数组下标。"},
            {"title": "Valid Palindrome", "description": "给定一个字符串，验证它是否是回文串，只考虑字母和数字字符，可以忽略字母的大小写。"}
        ],
        "medium": [
            {"title": "LRU Cache", "description": "请你设计并实现一个满足 LRU (最近最少使用) 缓存约束的数据结构。实现 LRUCache 类：LRUCache(int capacity) 以正整数作为容量 capacity 初始化 LRU 缓存。int get(int key) 如果关键字 key 存在于缓存中，则返回关键字的值，否则返回 -1。void put(int key, int value) 如果关键字 key 已经存在，则变更其数据值 value；如果不存在，则向缓存中插入该组 key-value。"},
            {"title": "3Sum", "description": "给你一个整数数组 nums ，判断是否存在三元组 [nums[i], nums[j], nums[k]] 满足 i != j、i != k 且 j != k，同时还满足 nums[i] + nums[j] + nums[k] == 0。请你返回所有和为 0 且不重复的三元组。"}
        ],
        "hard": [
            {"title": "Median of Two Sorted Arrays", "description": "给定两个大小分别为 m 和 n 的正序（从小到大）数组 nums1 和 nums2。请你找出并返回这两个正序数组的中位数。"},
            {"title": "Merge K Sorted Lists", "description": "给你一个链表数组，每个链表都已经按升序排列。请你将所有链表合并到一个升序链表中，返回合并后的链表。"}
        ]
    },
    "system_design": {
        "medium": [
            {"title": "设计 URL 短链接服务", "description": "设计一个 URL 短链接服务（如 bit.ly）。要求：1. 能将长 URL 转换为短 URL。2. 能通过短 URL 重定向到原始长 URL。3. 考虑高并发场景。"},
            {"title": "设计 Twitter", "description": "设计一个简化版的 Twitter。要求：1. 发布推文。2. 关注/取关用户。3. 获取关注用户的最新推文（Feed）。"}
        ],
        "hard": [
            {"title": "设计分布式消息队列", "description": "设计一个类似 Kafka 的分布式消息队列系统。要求：1. 支持发布/订阅模式。2. 保证消息顺序。3. 支持消息持久化。4. 高可用和可扩展。"},
            {"title": "设计 YouTube", "description": "设计一个视频分享平台。要求：1. 视频上传和存储。2. 视频播放（支持不同清晰度）。3. 推荐系统。4. 评论和点赞。"}
        ]
    },
    "behavioral": {
        "all": [
            {"title": "团队合作", "description": "请描述一次你与团队成员意见不合的经历，你是如何处理的？"},
            {"title": "困难项目", "description": "请描述你参与过的最有挑战性的项目。你遇到了什么困难？如何克服的？"},
            {"title": "失败经历", "description": "请分享一次你失败的经历。你从中学到了什么？"}
        ]
    },
    "frontend": {
        "easy": [
            {"title": "实现防抖函数", "description": "请实现一个 debounce 函数，用于限制函数的执行频率。"},
            {"title": "实现深拷贝", "description": "请实现一个深拷贝函数，能够正确处理对象、数组、Date 等类型。"}
        ],
        "medium": [
            {"title": "实现虚拟滚动", "description": "实现一个虚拟滚动列表组件，只渲染可视区域内的元素，提高长列表的渲染性能。"},
            {"title": "实现拖拽排序", "description": "实现一个支持拖拽排序的列表组件，用户可以通过拖拽改变列表项的顺序。"}
        ]
    }
}


def get_problem_for_interview(interview_type: str, difficulty: str) -> dict:
    """Select a problem based on interview type and difficulty"""
    problems = INTERVIEW_PROBLEMS.get(interview_type, {})
    
    if interview_type == "behavioral":
        available = problems.get("all", [])
    else:
        available = problems.get(difficulty, problems.get("medium", []))
    
    if available:
        import random
        return random.choice(available)
    
    return {"title": "General Interview", "description": "请准备好自我介绍。"}


@router.post("/start")
async def start_interview(
    config: InterviewStart,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Start a new interview session"""
    
    # Select problem based on config
    problem = get_problem_for_interview(config.interview_type, config.difficulty)
    
    # Create interview record
    interview = Interview(
        user_id=current_user.id,
        interview_type=config.interview_type,
        company=config.company,
        difficulty=config.difficulty,
        duration_minutes=config.duration_minutes,
        problem_ids=[],  # Will be populated with actual problem IDs if using DB problems
        conversation_history=[],
        code_snapshots=[],
        status="in_progress"
    )
    
    db.add(interview)
    db.commit()
    db.refresh(interview)
    
    # Generate initial interviewer message
    initial_message = await ai_service.chat_with_interviewer(
        interview_type=config.interview_type,
        company=config.company,
        difficulty=config.difficulty,
        duration=config.duration_minutes,
        problem=problem,
        conversation_history=[],
        user_message="面试开始了，请开始自我介绍并说明面试题目。"
    )
    
    # Save initial message to history
    interview.conversation_history = [{
        "role": "assistant",
        "content": initial_message,
        "timestamp": datetime.utcnow().isoformat()
    }]
    db.commit()
    
    return {
        "interview_id": interview.id,
        "interview_type": config.interview_type,
        "company": config.company,
        "difficulty": config.difficulty,
        "duration_minutes": config.duration_minutes,
        "problem": problem,
        "initial_message": initial_message
    }


@router.post("/{interview_id}/message")
async def send_message(
    interview_id: int,
    message: InterviewMessage,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Send a message in the interview"""
    
    interview = db.query(Interview).filter(
        Interview.id == interview_id,
        Interview.user_id == current_user.id
    ).first()
    
    if not interview:
        raise HTTPException(status_code=404, detail="Interview not found")
    
    if interview.status != "in_progress":
        raise HTTPException(status_code=400, detail="Interview is not in progress")
    
    # Get problem info
    problem = get_problem_for_interview(interview.interview_type, interview.difficulty)
    
    # Add user message to history
    history = interview.conversation_history or []
    history.append({
        "role": "user",
        "content": message.message,
        "timestamp": datetime.utcnow().isoformat()
    })
    
    # Save code snapshot if provided
    if message.code:
        snapshots = interview.code_snapshots or []
        snapshots.append({
            "code": message.code,
            "timestamp": datetime.utcnow().isoformat()
        })
        interview.code_snapshots = snapshots
    
    # Get AI response
    ai_response = await ai_service.chat_with_interviewer(
        interview_type=interview.interview_type,
        company=interview.company,
        difficulty=interview.difficulty,
        duration=interview.duration_minutes,
        problem=problem,
        conversation_history=history,
        user_message=message.message,
        user_code=message.code
    )
    
    # Add AI response to history
    history.append({
        "role": "assistant",
        "content": ai_response,
        "timestamp": datetime.utcnow().isoformat()
    })
    
    interview.conversation_history = history
    db.commit()
    
    return {
        "response": ai_response,
        "timestamp": datetime.utcnow().isoformat()
    }


@router.post("/{interview_id}/message/stream")
async def send_message_stream(
    interview_id: int,
    message: InterviewMessage,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Send a message and get streaming response"""
    
    interview = db.query(Interview).filter(
        Interview.id == interview_id,
        Interview.user_id == current_user.id
    ).first()
    
    if not interview:
        raise HTTPException(status_code=404, detail="Interview not found")
    
    problem = get_problem_for_interview(interview.interview_type, interview.difficulty)
    history = interview.conversation_history or []
    
    async def generate():
        full_response = ""
        async for chunk in ai_service.stream_interviewer_response(
            interview_type=interview.interview_type,
            company=interview.company,
            difficulty=interview.difficulty,
            duration=interview.duration_minutes,
            problem=problem,
            conversation_history=history,
            user_message=message.message,
            user_code=message.code
        ):
            full_response += chunk
            yield f"data: {json.dumps({'chunk': chunk})}\n\n"
        
        # Save to history after streaming completes
        history.append({"role": "user", "content": message.message, "timestamp": datetime.utcnow().isoformat()})
        history.append({"role": "assistant", "content": full_response, "timestamp": datetime.utcnow().isoformat()})
        interview.conversation_history = history
        db.commit()
        
        yield f"data: {json.dumps({'done': True})}\n\n"
    
    return StreamingResponse(generate(), media_type="text/event-stream")


@router.post("/{interview_id}/end")
async def end_interview(
    interview_id: int,
    final_code: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """End the interview and get report"""
    
    interview = db.query(Interview).filter(
        Interview.id == interview_id,
        Interview.user_id == current_user.id
    ).first()
    
    if not interview:
        raise HTTPException(status_code=404, detail="Interview not found")
    
    # Get problem info
    problem = get_problem_for_interview(interview.interview_type, interview.difficulty)
    
    # Generate interview report
    report = await ai_service.generate_interview_report(
        interview_type=interview.interview_type,
        company=interview.company,
        conversation_history=interview.conversation_history or [],
        code_snapshots=interview.code_snapshots or [],
        problem=problem,
        final_submission={"status": "completed", "code": final_code}
    )
    
    # Update interview record
    interview.status = "completed"
    interview.ended_at = datetime.utcnow()
    interview.overall_score = report.get("overall_score", 0)
    interview.dimension_scores = report.get("dimension_scores", {})
    interview.time_analysis = report.get("time_analysis", {})
    interview.ai_suggestions = report.get("suggestions", [])
    interview.feedback = json.dumps(report, ensure_ascii=False)
    
    # Update user stats
    current_user.interviews_completed += 1
    
    db.commit()
    
    return {
        "interview_id": interview_id,
        "report": report
    }


@router.get("/{interview_id}")
async def get_interview(
    interview_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get interview details"""
    
    interview = db.query(Interview).filter(
        Interview.id == interview_id,
        Interview.user_id == current_user.id
    ).first()
    
    if not interview:
        raise HTTPException(status_code=404, detail="Interview not found")
    
    return {
        "id": interview.id,
        "interview_type": interview.interview_type,
        "company": interview.company,
        "difficulty": interview.difficulty,
        "duration_minutes": interview.duration_minutes,
        "status": interview.status,
        "conversation_history": interview.conversation_history,
        "overall_score": interview.overall_score,
        "dimension_scores": interview.dimension_scores,
        "time_analysis": interview.time_analysis,
        "ai_suggestions": interview.ai_suggestions,
        "started_at": interview.started_at,
        "ended_at": interview.ended_at
    }


@router.get("/")
async def list_interviews(
    status: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List user's interviews"""
    
    query = db.query(Interview).filter(Interview.user_id == current_user.id)
    
    if status:
        query = query.filter(Interview.status == status)
    
    interviews = query.order_by(Interview.started_at.desc()).all()
    
    return [
        {
            "id": i.id,
            "interview_type": i.interview_type,
            "company": i.company,
            "difficulty": i.difficulty,
            "status": i.status,
            "overall_score": i.overall_score,
            "started_at": i.started_at,
            "ended_at": i.ended_at
        }
        for i in interviews
    ]


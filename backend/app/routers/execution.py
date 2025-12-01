"""
Code Execution Routes - Run and test code
"""

from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from pydantic import BaseModel

from app.schemas.schemas import CodeExecutionRequest, CodeExecutionResponse
from app.services.code_executor import code_executor, local_executor

router = APIRouter()


class RunCodeRequest(BaseModel):
    code: str
    language: str
    stdin: str = ""


class RunCodeResponse(BaseModel):
    success: bool
    output: str
    error: Optional[str]


@router.post("/run", response_model=RunCodeResponse)
async def run_code(request: RunCodeRequest):
    """Run code and return output (no test cases)"""
    
    try:
        result = await code_executor.execute(
            code=request.code,
            language=request.language,
            stdin=request.stdin
        )
    except Exception:
        # Fallback to local executor
        result = await local_executor.execute(
            code=request.code,
            language=request.language,
            stdin=request.stdin
        )
    
    return RunCodeResponse(
        success=result["success"],
        output=result["output"],
        error=result.get("error")
    )


@router.post("/test", response_model=CodeExecutionResponse)
async def test_code(request: CodeExecutionRequest):
    """Run code against test cases"""
    
    if not request.test_cases:
        raise HTTPException(status_code=400, detail="Test cases required")
    
    try:
        result = await code_executor.run_test_cases(
            code=request.code,
            language=request.language,
            test_cases=request.test_cases
        )
    except Exception:
        result = await local_executor.run_test_cases(
            code=request.code,
            language=request.language,
            test_cases=request.test_cases
        )
    
    return CodeExecutionResponse(
        status=result["status"],
        test_results=result["test_results"],
        total_runtime_ms=result.get("total_runtime_ms"),
        memory_kb=result.get("memory_kb"),
        passed_count=result["passed_count"],
        total_count=result["total_count"]
    )


@router.get("/languages")
async def get_supported_languages():
    """Get list of supported programming languages"""
    
    return {
        "languages": [
            {"id": "python", "name": "Python 3", "version": "3.10"},
            {"id": "javascript", "name": "JavaScript", "version": "Node 18"},
            {"id": "typescript", "name": "TypeScript", "version": "5.0"},
            {"id": "java", "name": "Java", "version": "15"},
            {"id": "cpp", "name": "C++", "version": "GCC 10"},
            {"id": "go", "name": "Go", "version": "1.16"},
            {"id": "rust", "name": "Rust", "version": "1.68"},
        ]
    }


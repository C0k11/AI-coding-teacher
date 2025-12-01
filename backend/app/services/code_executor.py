"""
Code Execution Service
Executes user code in a secure sandboxed environment
"""

import httpx
import asyncio
from typing import List, Dict, Optional
from app.config import settings


# Language configurations for Piston API
LANGUAGE_CONFIG = {
    "python": {"language": "python", "version": "3.10"},
    "python3": {"language": "python", "version": "3.10"},
    "javascript": {"language": "javascript", "version": "18.15.0"},
    "typescript": {"language": "typescript", "version": "5.0.3"},
    "java": {"language": "java", "version": "15.0.2"},
    "cpp": {"language": "c++", "version": "10.2.0"},
    "c++": {"language": "c++", "version": "10.2.0"},
    "go": {"language": "go", "version": "1.16.2"},
    "rust": {"language": "rust", "version": "1.68.2"},
}


class CodeExecutor:
    """Code execution service using Piston API"""
    
    def __init__(self):
        self.piston_url = settings.PISTON_API_URL
        self.timeout = 10  # seconds
    
    async def execute(
        self,
        code: str,
        language: str,
        stdin: str = "",
        timeout: int = 5
    ) -> Dict:
        """Execute code using Piston API"""
        
        lang_config = LANGUAGE_CONFIG.get(language.lower())
        if not lang_config:
            return {
                "success": False,
                "error": f"Unsupported language: {language}",
                "output": "",
                "stderr": ""
            }
        
        payload = {
            "language": lang_config["language"],
            "version": lang_config["version"],
            "files": [{"content": code}],
            "stdin": stdin,
            "run_timeout": timeout * 1000  # Convert to milliseconds
        }
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout + timeout) as client:
                response = await client.post(
                    f"{self.piston_url}/execute",
                    json=payload
                )
                
                if response.status_code != 200:
                    return {
                        "success": False,
                        "error": f"Execution service error: {response.status_code}",
                        "output": "",
                        "stderr": ""
                    }
                
                result = response.json()
                run_result = result.get("run", {})
                
                return {
                    "success": run_result.get("code", 1) == 0,
                    "output": run_result.get("stdout", "").strip(),
                    "stderr": run_result.get("stderr", "").strip(),
                    "error": run_result.get("stderr", "") if run_result.get("code", 0) != 0 else ""
                }
                
        except httpx.TimeoutException:
            return {
                "success": False,
                "error": "Time Limit Exceeded",
                "output": "",
                "stderr": ""
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "output": "",
                "stderr": ""
            }
    
    async def run_test_cases(
        self,
        code: str,
        language: str,
        test_cases: List[Dict],
        timeout_per_case: int = 5
    ) -> Dict:
        """Run code against multiple test cases"""
        
        results = []
        total_runtime = 0
        passed_count = 0
        
        for i, test_case in enumerate(test_cases):
            input_data = test_case.get("input", "")
            expected_output = test_case.get("expected_output", "").strip()
            
            # Wrap code with input handling based on language
            wrapped_code = self._wrap_code_for_test(code, language, input_data)
            
            start_time = asyncio.get_event_loop().time()
            result = await self.execute(wrapped_code, language, input_data, timeout_per_case)
            runtime = int((asyncio.get_event_loop().time() - start_time) * 1000)
            total_runtime += runtime
            
            actual_output = result["output"].strip()
            passed = self._compare_outputs(actual_output, expected_output)
            
            if passed:
                passed_count += 1
            
            results.append({
                "test_case": i + 1,
                "input": input_data[:100] + ("..." if len(input_data) > 100 else ""),
                "expected_output": expected_output[:100] + ("..." if len(expected_output) > 100 else ""),
                "actual_output": actual_output[:100] + ("..." if len(actual_output) > 100 else ""),
                "passed": passed,
                "runtime_ms": runtime,
                "error": result.get("error", "") if not result["success"] else None
            })
        
        # Determine overall status
        if passed_count == len(test_cases):
            status = "accepted"
        elif any(r.get("error") and "Time Limit" in r["error"] for r in results):
            status = "time_limit_exceeded"
        elif any(r.get("error") for r in results):
            status = "runtime_error"
        else:
            status = "wrong_answer"
        
        return {
            "status": status,
            "test_results": results,
            "passed_count": passed_count,
            "total_count": len(test_cases),
            "total_runtime_ms": total_runtime
        }
    
    def _wrap_code_for_test(self, code: str, language: str, input_data: str) -> str:
        """Wrap user code to handle input for testing"""
        # For most cases, we use stdin, so no wrapping needed
        # But we can add language-specific input handling here if needed
        return code
    
    def _compare_outputs(self, actual: str, expected: str) -> bool:
        """Compare actual output with expected output"""
        # Normalize whitespace and compare
        actual_lines = [line.strip() for line in actual.strip().split('\n')]
        expected_lines = [line.strip() for line in expected.strip().split('\n')]
        
        if len(actual_lines) != len(expected_lines):
            return False
        
        for a, e in zip(actual_lines, expected_lines):
            # Try numeric comparison for floating point
            try:
                if abs(float(a) - float(e)) < 1e-6:
                    continue
            except ValueError:
                pass
            
            if a != e:
                return False
        
        return True


# Local execution fallback (for demo without Piston API)
class LocalCodeExecutor:
    """Local code executor for demo purposes"""
    
    async def execute(self, code: str, language: str, stdin: str = "") -> Dict:
        """Execute Python code locally (demo only)"""
        if language.lower() not in ["python", "python3"]:
            return {
                "success": False,
                "error": "Local execution only supports Python for demo",
                "output": "",
                "stderr": ""
            }
        
        import subprocess
        import sys
        
        try:
            result = subprocess.run(
                [sys.executable, "-c", code],
                input=stdin,
                capture_output=True,
                text=True,
                timeout=5
            )
            
            return {
                "success": result.returncode == 0,
                "output": result.stdout.strip(),
                "stderr": result.stderr.strip(),
                "error": result.stderr if result.returncode != 0 else ""
            }
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "error": "Time Limit Exceeded",
                "output": "",
                "stderr": ""
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "output": "",
                "stderr": ""
            }
    
    async def run_test_cases(
        self,
        code: str,
        language: str,
        test_cases: List[Dict],
        timeout_per_case: int = 5
    ) -> Dict:
        """Run test cases locally"""
        results = []
        passed_count = 0
        
        for i, test_case in enumerate(test_cases):
            input_data = test_case.get("input", "")
            expected_output = test_case.get("expected_output", "").strip()
            
            result = await self.execute(code, language, input_data)
            actual_output = result["output"].strip()
            passed = actual_output == expected_output
            
            if passed:
                passed_count += 1
            
            results.append({
                "test_case": i + 1,
                "input": input_data,
                "expected_output": expected_output,
                "actual_output": actual_output,
                "passed": passed,
                "runtime_ms": 0,
                "error": result.get("error")
            })
        
        status = "accepted" if passed_count == len(test_cases) else "wrong_answer"
        
        return {
            "status": status,
            "test_results": results,
            "passed_count": passed_count,
            "total_count": len(test_cases)
        }


# Create executor instance
code_executor = CodeExecutor()
local_executor = LocalCodeExecutor()


"""
AI Service - Local AI algorithms for code analysis
No external API required - fully self-contained
"""

from typing import List, Dict

from app.services.code_analyzer import analyze_code
from app.services.code_similarity import compare_code, check_plagiarism


class AIService:
    """
    AI Service for code analysis and similarity detection.
    Uses local algorithms - no external API required.
    """
    
    def __init__(self):
        pass
    
    async def analyze_code(
        self,
        code: str,
        language: str,
        problem: Dict,
        test_results: List[Dict]
    ) -> Dict:
        """Analyze submitted code using local analyzer"""
        
        # Use local code analyzer
        analysis = analyze_code(code, language)
        
        # Combine with test results
        passed = sum(1 for t in test_results if t.get('passed', False))
        total = len(test_results) if test_results else 1
        
        # Adjust score based on test results
        test_score_factor = passed / total if total > 0 else 0.5
        adjusted_score = analysis['quality_score'] * (0.6 + 0.4 * test_score_factor)
        
        return {
            "quality_score": round(adjusted_score, 1),
            "time_complexity": analysis['time_complexity'],
            "space_complexity": analysis['space_complexity'],
            "cyclomatic_complexity": analysis['cyclomatic_complexity'],
            "detected_patterns": analysis['detected_patterns'],
            "strengths": analysis['strengths'],
            "improvements": analysis['improvements'],
            "potential_bugs": analysis['potential_bugs'],
            "issues": analysis['issues'],
            "suggestions": analysis['suggestions'],
            "test_results": {
                "passed": passed,
                "total": total
            }
        }
    
    def compare_solutions(self, code1: str, code2: str, language: str = 'python') -> Dict:
        """Compare two code solutions"""
        return compare_code(code1, code2, language)
    
    def check_code_similarity(
        self, 
        code: str, 
        submissions: List[Dict], 
        language: str = 'python'
    ) -> List[Dict]:
        """Check code against previous submissions for similarity"""
        return check_plagiarism(code, submissions, language)


# Global AI service instance
ai_service = AIService()


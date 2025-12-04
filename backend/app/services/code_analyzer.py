"""
Local Code Analyzer - AST-based code analysis without external AI
Provides code quality scoring, complexity analysis, and feedback generation
"""

import ast
import re
import math
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, field
from collections import defaultdict


@dataclass
class ComplexityMetrics:
    """Cyclomatic and cognitive complexity metrics"""
    cyclomatic: int = 1
    cognitive: int = 0
    nesting_depth: int = 0
    lines_of_code: int = 0
    comment_lines: int = 0
    blank_lines: int = 0


@dataclass
class CodeQualityMetrics:
    """Code quality assessment"""
    naming_score: float = 0.0  # 0-1
    structure_score: float = 0.0  # 0-1
    readability_score: float = 0.0  # 0-1
    documentation_score: float = 0.0  # 0-1
    overall_score: float = 0.0  # 1-10
    issues: List[str] = field(default_factory=list)
    suggestions: List[str] = field(default_factory=list)


@dataclass
class AnalysisResult:
    """Complete code analysis result"""
    complexity: ComplexityMetrics
    quality: CodeQualityMetrics
    time_complexity: str
    space_complexity: str
    detected_patterns: List[str]
    potential_bugs: List[str]
    strengths: List[str]
    improvements: List[str]


class PythonCodeAnalyzer:
    """Analyze Python code using AST"""
    
    # Common algorithm patterns
    ALGORITHM_PATTERNS = {
        'two_pointers': [
            r'while\s+\w+\s*<\s*\w+',
            r'left.*right|right.*left',
            r'\[\w+\].*\[\w+\]',
        ],
        'sliding_window': [
            r'for.*range.*while',
            r'window|slide',
            r'\[i:j\]|\[start:end\]',
        ],
        'binary_search': [
            r'mid\s*=.*//\s*2',
            r'low.*high|left.*right',
            r'while.*<=',
        ],
        'dfs': [
            r'def.*\(.*\).*:.*\1',  # recursion
            r'stack\s*=|\.append\(|\.pop\(',
            r'visited',
        ],
        'bfs': [
            r'queue|deque',
            r'\.popleft\(|\.append\(',
            r'level|layer',
        ],
        'dynamic_programming': [
            r'dp\s*=|memo\s*=',
            r'\[.*\]\s*\*\s*\d+',
            r'dp\[.*\]\s*=.*dp\[',
        ],
        'hash_table': [
            r'dict\(|{}|\{\}',
            r'\.get\(|in\s+\w+',
            r'Counter\(|defaultdict',
        ],
        'greedy': [
            r'sorted\(|\.sort\(',
            r'max\(|min\(',
            r'for.*in.*sorted',
        ],
        'recursion': [
            r'def\s+(\w+).*:\s*.*\1\(',
            r'return.*\+.*return|return.*\*.*return',
        ],
        'backtracking': [
            r'\.append\(.*\.pop\(',
            r'backtrack|dfs',
            r'if.*return.*else.*return',
        ],
    }
    
    # Time complexity indicators
    TIME_COMPLEXITY_PATTERNS = {
        'O(1)': [
            (r'^[^for\s+while]*$', 'no loops'),
            (r'return\s+\w+\[', 'direct access'),
        ],
        'O(log n)': [
            (r'//\s*2|>>\s*1', 'halving'),
            (r'binary.*search', 'binary search'),
        ],
        'O(n)': [
            (r'for\s+\w+\s+in\s+\w+[^:]*:', 'single loop'),
            (r'while\s+\w+\s*[<>]=?\s*\w+', 'single while'),
        ],
        'O(n log n)': [
            (r'\.sort\(|sorted\(', 'sorting'),
            (r'heapq\.|heap', 'heap operations'),
        ],
        'O(n²)': [
            (r'for.*:[\s\S]*for.*:', 'nested loops'),
            (r'for.*for', 'double loop'),
        ],
        'O(2^n)': [
            (r'def\s+\w+\(.*\)[\s\S]*\1\(.*\)[\s\S]*\1\(', 'double recursion'),
            (r'fibonacci|fib|subset|powerset', 'exponential pattern'),
        ],
    }
    
    def __init__(self):
        self.tree = None
        self.source = ""
        self.lines = []
    
    def analyze(self, code: str) -> AnalysisResult:
        """Perform complete code analysis"""
        self.source = code
        self.lines = code.split('\n')
        
        try:
            self.tree = ast.parse(code)
        except SyntaxError as e:
            return self._create_error_result(f"Syntax error: {e}")
        
        complexity = self._analyze_complexity()
        quality = self._analyze_quality()
        time_complexity = self._estimate_time_complexity()
        space_complexity = self._estimate_space_complexity()
        patterns = self._detect_patterns()
        bugs = self._find_potential_bugs()
        strengths = self._identify_strengths(complexity, quality)
        improvements = self._identify_improvements(complexity, quality, bugs)
        
        return AnalysisResult(
            complexity=complexity,
            quality=quality,
            time_complexity=time_complexity,
            space_complexity=space_complexity,
            detected_patterns=patterns,
            potential_bugs=bugs,
            strengths=strengths,
            improvements=improvements
        )
    
    def _analyze_complexity(self) -> ComplexityMetrics:
        """Calculate cyclomatic and cognitive complexity"""
        metrics = ComplexityMetrics()
        
        # Lines analysis
        for line in self.lines:
            stripped = line.strip()
            if not stripped:
                metrics.blank_lines += 1
            elif stripped.startswith('#'):
                metrics.comment_lines += 1
            else:
                metrics.lines_of_code += 1
        
        # AST-based complexity
        for node in ast.walk(self.tree):
            # Cyclomatic complexity: count decision points
            if isinstance(node, (ast.If, ast.While, ast.For, ast.ExceptHandler)):
                metrics.cyclomatic += 1
            elif isinstance(node, ast.BoolOp):
                metrics.cyclomatic += len(node.values) - 1
            elif isinstance(node, (ast.And, ast.Or)):
                metrics.cyclomatic += 1
            
            # Cognitive complexity: consider nesting
            if isinstance(node, (ast.If, ast.While, ast.For, ast.Try)):
                metrics.cognitive += 1
        
        # Calculate max nesting depth
        metrics.nesting_depth = self._calculate_nesting_depth(self.tree)
        
        return metrics
    
    def _calculate_nesting_depth(self, node, depth=0) -> int:
        """Calculate maximum nesting depth"""
        max_depth = depth
        
        for child in ast.iter_child_nodes(node):
            if isinstance(child, (ast.If, ast.While, ast.For, ast.With, ast.Try)):
                child_depth = self._calculate_nesting_depth(child, depth + 1)
                max_depth = max(max_depth, child_depth)
            else:
                child_depth = self._calculate_nesting_depth(child, depth)
                max_depth = max(max_depth, child_depth)
        
        return max_depth
    
    def _analyze_quality(self) -> CodeQualityMetrics:
        """Analyze code quality aspects"""
        quality = CodeQualityMetrics()
        
        # Naming analysis
        naming_issues = self._check_naming()
        quality.naming_score = max(0, 1 - len(naming_issues) * 0.1)
        quality.issues.extend(naming_issues)
        
        # Structure analysis
        structure_issues = self._check_structure()
        quality.structure_score = max(0, 1 - len(structure_issues) * 0.15)
        quality.issues.extend(structure_issues)
        
        # Readability analysis
        readability_issues = self._check_readability()
        quality.readability_score = max(0, 1 - len(readability_issues) * 0.1)
        quality.issues.extend(readability_issues)
        
        # Documentation analysis
        quality.documentation_score = self._check_documentation()
        
        # Overall score (1-10)
        quality.overall_score = round(
            (quality.naming_score * 2.5 +
             quality.structure_score * 3.0 +
             quality.readability_score * 2.5 +
             quality.documentation_score * 2.0), 1
        )
        
        # Generate suggestions
        quality.suggestions = self._generate_suggestions(quality)
        
        return quality
    
    def _check_naming(self) -> List[str]:
        """Check variable and function naming conventions"""
        issues = []
        
        for node in ast.walk(self.tree):
            if isinstance(node, ast.FunctionDef):
                if not re.match(r'^[a-z_][a-z0-9_]*$', node.name):
                    issues.append(f"函数名 '{node.name}' 不符合 snake_case 规范")
                if len(node.name) == 1:
                    issues.append(f"函数名 '{node.name}' 过短，建议使用有意义的名称")
            
            elif isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store):
                name = node.id
                # Allow single char for loop variables
                if len(name) == 1 and name not in 'ijkxyn':
                    issues.append(f"变量名 '{name}' 过短，考虑使用更有意义的名称")
        
        return issues[:5]  # Limit issues
    
    def _check_structure(self) -> List[str]:
        """Check code structure"""
        issues = []
        
        for node in ast.walk(self.tree):
            if isinstance(node, ast.FunctionDef):
                # Check function length
                func_lines = node.end_lineno - node.lineno if hasattr(node, 'end_lineno') else 0
                if func_lines > 50:
                    issues.append(f"函数 '{node.name}' 过长 ({func_lines} 行)，考虑拆分")
                
                # Check parameter count
                if len(node.args.args) > 5:
                    issues.append(f"函数 '{node.name}' 参数过多，考虑使用对象封装")
        
        # Check nesting depth
        depth = self._calculate_nesting_depth(self.tree)
        if depth > 4:
            issues.append(f"代码嵌套层级过深 ({depth} 层)，考虑重构")
        
        return issues
    
    def _check_readability(self) -> List[str]:
        """Check code readability"""
        issues = []
        
        for i, line in enumerate(self.lines):
            # Line length
            if len(line) > 100:
                issues.append(f"第 {i+1} 行过长 ({len(line)} 字符)")
            
            # Magic numbers
            if re.search(r'[^0-9\.][0-9]{2,}[^0-9\.]', line) and 'range' not in line:
                if '#' not in line:  # Not in comment
                    issues.append(f"第 {i+1} 行可能存在魔法数字，考虑使用常量")
        
        return issues[:3]
    
    def _check_documentation(self) -> float:
        """Check documentation coverage"""
        total_functions = 0
        documented_functions = 0
        
        for node in ast.walk(self.tree):
            if isinstance(node, ast.FunctionDef):
                total_functions += 1
                if ast.get_docstring(node):
                    documented_functions += 1
        
        if total_functions == 0:
            return 0.5  # No functions, neutral score
        
        return documented_functions / total_functions
    
    def _estimate_time_complexity(self) -> str:
        """Estimate time complexity based on code patterns"""
        code_lower = self.source.lower()
        
        # Check for common patterns (in order of complexity)
        complexities = ['O(2^n)', 'O(n²)', 'O(n log n)', 'O(n)', 'O(log n)', 'O(1)']
        
        for complexity in complexities:
            patterns = self.TIME_COMPLEXITY_PATTERNS.get(complexity, [])
            for pattern, _ in patterns:
                if re.search(pattern, self.source, re.MULTILINE):
                    return complexity
        
        # Default based on loop counting
        loop_count = self.source.count('for ') + self.source.count('while ')
        if loop_count == 0:
            return 'O(1)'
        elif loop_count == 1:
            return 'O(n)'
        elif loop_count >= 2:
            # Check if nested
            if re.search(r'for.*:[\s\S]*?for.*:', self.source):
                return 'O(n²)'
            return 'O(n)'
        
        return 'O(n)'
    
    def _estimate_space_complexity(self) -> str:
        """Estimate space complexity"""
        # Check for common space patterns
        if re.search(r'dp\s*=\s*\[\[', self.source):
            return 'O(n²)'
        if re.search(r'\[.*\]\s*\*\s*n|\[.*for.*in.*range', self.source):
            return 'O(n)'
        if 'dict()' in self.source or '{}' in self.source or 'set()' in self.source:
            return 'O(n)'
        if 'deque' in self.source or 'queue' in self.source.lower():
            return 'O(n)'
        
        # Check recursion depth
        for node in ast.walk(self.tree):
            if isinstance(node, ast.FunctionDef):
                body_str = ast.unparse(node) if hasattr(ast, 'unparse') else ""
                if node.name in body_str:
                    return 'O(n)'  # Recursive call stack
        
        return 'O(1)'
    
    def _detect_patterns(self) -> List[str]:
        """Detect algorithm patterns in code"""
        detected = []
        
        for pattern_name, regexes in self.ALGORITHM_PATTERNS.items():
            matches = 0
            for regex in regexes:
                if re.search(regex, self.source, re.IGNORECASE | re.MULTILINE):
                    matches += 1
            if matches >= 2:  # At least 2 pattern matches
                detected.append(pattern_name)
        
        return detected
    
    def _find_potential_bugs(self) -> List[str]:
        """Find potential bugs and issues"""
        bugs = []
        
        # Check for common issues
        if re.search(r'\[\s*-1\s*\]', self.source) and 'if' not in self.source:
            bugs.append("访问 [-1] 可能导致空数组错误")
        
        if re.search(r'/\s*\w+', self.source) and 'if' not in self.source:
            bugs.append("除法操作可能存在除零风险")
        
        if re.search(r'while\s+True', self.source):
            if 'break' not in self.source and 'return' not in self.source:
                bugs.append("无限循环风险：while True 没有 break")
        
        # Index out of bounds risk
        if re.search(r'\[\w+\s*\+\s*1\]|\[\w+\s*-\s*1\]', self.source):
            bugs.append("索引偏移可能导致越界，建议添加边界检查")
        
        # Empty input handling
        if 'len(' not in self.source and 'if not' not in self.source:
            bugs.append("建议添加空输入检查")
        
        return bugs[:5]
    
    def _identify_strengths(self, complexity: ComplexityMetrics, quality: CodeQualityMetrics) -> List[str]:
        """Identify code strengths"""
        strengths = []
        
        if quality.naming_score > 0.8:
            strengths.append("变量和函数命名清晰有意义")
        
        if quality.structure_score > 0.8:
            strengths.append("代码结构合理，函数划分恰当")
        
        if complexity.nesting_depth <= 2:
            strengths.append("代码层级清晰，嵌套较浅")
        
        if complexity.comment_lines > 0:
            strengths.append("包含有用的注释说明")
        
        if quality.documentation_score > 0.5:
            strengths.append("函数有文档字符串说明")
        
        if complexity.cyclomatic < 5:
            strengths.append("逻辑简洁，圈复杂度低")
        
        if not strengths:
            strengths.append("代码能够运行")
        
        return strengths
    
    def _identify_improvements(
        self, 
        complexity: ComplexityMetrics, 
        quality: CodeQualityMetrics,
        bugs: List[str]
    ) -> List[str]:
        """Identify areas for improvement"""
        improvements = []
        
        if quality.naming_score < 0.7:
            improvements.append("改善变量命名，使用更有意义的名称")
        
        if complexity.nesting_depth > 3:
            improvements.append("减少代码嵌套层级，考虑提前返回或拆分函数")
        
        if complexity.cyclomatic > 10:
            improvements.append("降低代码复杂度，拆分复杂函数")
        
        if quality.documentation_score < 0.3:
            improvements.append("添加函数文档字符串和关键注释")
        
        if complexity.lines_of_code > 50 and len(list(ast.walk(self.tree))) < 3:
            improvements.append("考虑将代码模块化，提取辅助函数")
        
        if bugs:
            improvements.append("修复潜在的边界情况和错误")
        
        return improvements[:5]
    
    def _generate_suggestions(self, quality: CodeQualityMetrics) -> List[str]:
        """Generate improvement suggestions"""
        suggestions = []
        
        if quality.naming_score < 0.8:
            suggestions.append("使用 snake_case 命名变量和函数")
        
        if quality.readability_score < 0.8:
            suggestions.append("保持每行代码在 80-100 字符以内")
        
        if quality.documentation_score < 0.5:
            suggestions.append("为主要函数添加 docstring 说明")
        
        return suggestions
    
    def _create_error_result(self, error_msg: str) -> AnalysisResult:
        """Create result for code with syntax errors"""
        return AnalysisResult(
            complexity=ComplexityMetrics(),
            quality=CodeQualityMetrics(
                overall_score=1,
                issues=[error_msg]
            ),
            time_complexity="N/A",
            space_complexity="N/A",
            detected_patterns=[],
            potential_bugs=[error_msg],
            strengths=[],
            improvements=["修复语法错误"]
        )


class JavaScriptCodeAnalyzer:
    """Analyze JavaScript code using regex patterns"""
    
    def analyze(self, code: str) -> AnalysisResult:
        """Analyze JavaScript code"""
        lines = code.split('\n')
        
        # Basic metrics
        loc = len([l for l in lines if l.strip() and not l.strip().startswith('//')])
        comments = len([l for l in lines if l.strip().startswith('//')])
        
        complexity = ComplexityMetrics(
            lines_of_code=loc,
            comment_lines=comments,
            cyclomatic=self._estimate_cyclomatic(code),
            nesting_depth=self._estimate_nesting(code)
        )
        
        quality = self._analyze_quality(code, lines)
        
        return AnalysisResult(
            complexity=complexity,
            quality=quality,
            time_complexity=self._estimate_time_complexity(code),
            space_complexity=self._estimate_space_complexity(code),
            detected_patterns=self._detect_patterns(code),
            potential_bugs=self._find_bugs(code),
            strengths=["代码结构基本合理"],
            improvements=self._get_improvements(quality)
        )
    
    def _estimate_cyclomatic(self, code: str) -> int:
        """Estimate cyclomatic complexity for JS"""
        cc = 1
        cc += len(re.findall(r'\bif\b|\belse\s+if\b', code))
        cc += len(re.findall(r'\bfor\b|\bwhile\b', code))
        cc += len(re.findall(r'\bcase\b', code))
        cc += len(re.findall(r'\bcatch\b', code))
        cc += len(re.findall(r'&&|\|\|', code))
        return cc
    
    def _estimate_nesting(self, code: str) -> int:
        """Estimate max nesting depth"""
        max_depth = 0
        current_depth = 0
        for char in code:
            if char == '{':
                current_depth += 1
                max_depth = max(max_depth, current_depth)
            elif char == '}':
                current_depth = max(0, current_depth - 1)
        return max_depth
    
    def _analyze_quality(self, code: str, lines: List[str]) -> CodeQualityMetrics:
        """Analyze JS code quality"""
        issues = []
        
        # Check for var instead of let/const
        if re.search(r'\bvar\b', code):
            issues.append("使用 let/const 替代 var")
        
        # Check for == instead of ===
        if re.search(r'[^=!]==[^=]', code):
            issues.append("使用 === 替代 == 进行严格比较")
        
        # Long lines
        for i, line in enumerate(lines):
            if len(line) > 100:
                issues.append(f"第 {i+1} 行过长")
                break
        
        score = max(1, 10 - len(issues) * 1.5)
        
        return CodeQualityMetrics(
            overall_score=score,
            issues=issues,
            naming_score=0.8,
            structure_score=0.7,
            readability_score=0.7 if len(issues) < 3 else 0.5,
            documentation_score=0.5 if '//' in code or '/*' in code else 0.2
        )
    
    def _estimate_time_complexity(self, code: str) -> str:
        """Estimate time complexity for JS"""
        if re.search(r'\.sort\(', code):
            return 'O(n log n)'
        
        nested_loops = len(re.findall(r'for.*{[^}]*for', code, re.DOTALL))
        if nested_loops > 0:
            return 'O(n²)'
        
        if re.search(r'\bfor\b|\bwhile\b|\.forEach|\.map|\.filter|\.reduce', code):
            return 'O(n)'
        
        return 'O(1)'
    
    def _estimate_space_complexity(self, code: str) -> str:
        """Estimate space complexity for JS"""
        if re.search(r'new Array\(.*\)|Array\(.*\)\.fill|\.map\(|\.filter\(', code):
            return 'O(n)'
        if re.search(r'new Map|new Set|{}|\[\]', code):
            return 'O(n)'
        return 'O(1)'
    
    def _detect_patterns(self, code: str) -> List[str]:
        """Detect algorithm patterns"""
        patterns = []
        if 'left' in code.lower() and 'right' in code.lower():
            patterns.append('two_pointers')
        if '.sort(' in code:
            patterns.append('sorting')
        if 'Map(' in code or 'Set(' in code or '{}' in code:
            patterns.append('hash_table')
        return patterns
    
    def _find_bugs(self, code: str) -> List[str]:
        """Find potential bugs"""
        bugs = []
        if '[i+1]' in code or '[i-1]' in code:
            bugs.append("数组索引偏移可能越界")
        if '/ ' in code and 'if' not in code:
            bugs.append("可能存在除零风险")
        return bugs
    
    def _get_improvements(self, quality: CodeQualityMetrics) -> List[str]:
        """Get improvement suggestions"""
        improvements = []
        if quality.documentation_score < 0.5:
            improvements.append("添加 JSDoc 注释")
        if quality.issues:
            improvements.append("修复代码质量问题")
        return improvements


class CodeAnalyzerFactory:
    """Factory to create appropriate analyzer based on language"""
    
    ANALYZERS = {
        'python': PythonCodeAnalyzer,
        'python3': PythonCodeAnalyzer,
        'javascript': JavaScriptCodeAnalyzer,
        'js': JavaScriptCodeAnalyzer,
        'typescript': JavaScriptCodeAnalyzer,
        'ts': JavaScriptCodeAnalyzer,
    }
    
    @classmethod
    def get_analyzer(cls, language: str):
        """Get appropriate analyzer for language"""
        analyzer_class = cls.ANALYZERS.get(language.lower(), PythonCodeAnalyzer)
        return analyzer_class()
    
    @classmethod
    def analyze(cls, code: str, language: str) -> AnalysisResult:
        """Analyze code with appropriate analyzer"""
        analyzer = cls.get_analyzer(language)
        return analyzer.analyze(code)


# Convenience function
def analyze_code(code: str, language: str = 'python') -> Dict:
    """
    Analyze code and return results as dictionary
    
    Args:
        code: Source code to analyze
        language: Programming language (python, javascript, etc.)
    
    Returns:
        Dictionary with analysis results
    """
    result = CodeAnalyzerFactory.analyze(code, language)
    
    return {
        "quality_score": result.quality.overall_score,
        "time_complexity": result.time_complexity,
        "space_complexity": result.space_complexity,
        "cyclomatic_complexity": result.complexity.cyclomatic,
        "nesting_depth": result.complexity.nesting_depth,
        "lines_of_code": result.complexity.lines_of_code,
        "detected_patterns": result.detected_patterns,
        "strengths": result.strengths,
        "improvements": result.improvements,
        "potential_bugs": result.potential_bugs,
        "issues": result.quality.issues,
        "suggestions": result.quality.suggestions,
    }

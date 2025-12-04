"""
Code Similarity Detection - Local algorithms for code comparison
Uses AST-based and token-based similarity detection
"""

import ast
import re
import hashlib
from typing import Dict, List, Tuple, Set
from dataclasses import dataclass
from collections import Counter, defaultdict
from difflib import SequenceMatcher


@dataclass
class SimilarityResult:
    """Result of similarity comparison"""
    overall_score: float  # 0-1
    structural_similarity: float  # AST-based
    token_similarity: float  # Token-based
    fingerprint_similarity: float  # Winnowing fingerprint
    details: Dict


class CodeNormalizer:
    """Normalize code for comparison"""
    
    @staticmethod
    def normalize_python(code: str) -> str:
        """Normalize Python code by removing comments, whitespace variations"""
        lines = []
        for line in code.split('\n'):
            # Remove inline comments
            if '#' in line:
                line = line[:line.index('#')]
            line = line.strip()
            if line:
                lines.append(line)
        return '\n'.join(lines)
    
    @staticmethod
    def normalize_javascript(code: str) -> str:
        """Normalize JavaScript code"""
        # Remove single-line comments
        code = re.sub(r'//.*$', '', code, flags=re.MULTILINE)
        # Remove multi-line comments
        code = re.sub(r'/\*.*?\*/', '', code, flags=re.DOTALL)
        # Normalize whitespace
        lines = [line.strip() for line in code.split('\n') if line.strip()]
        return '\n'.join(lines)
    
    @staticmethod
    def normalize(code: str, language: str = 'python') -> str:
        """Normalize code based on language"""
        if language.lower() in ['python', 'python3']:
            return CodeNormalizer.normalize_python(code)
        elif language.lower() in ['javascript', 'js', 'typescript', 'ts']:
            return CodeNormalizer.normalize_javascript(code)
        return code


class TokenBasedSimilarity:
    """Token-based similarity using n-grams"""
    
    @staticmethod
    def tokenize_python(code: str) -> List[str]:
        """Tokenize Python code"""
        # Simple tokenization based on significant tokens
        tokens = []
        
        # Keywords and operators
        patterns = [
            r'\bdef\b', r'\bclass\b', r'\bif\b', r'\belse\b', r'\belif\b',
            r'\bfor\b', r'\bwhile\b', r'\breturn\b', r'\bin\b', r'\bnot\b',
            r'\band\b', r'\bor\b', r'\bTrue\b', r'\bFalse\b', r'\bNone\b',
            r'\btry\b', r'\bexcept\b', r'\bfinally\b', r'\bwith\b', r'\bas\b',
            r'\blambda\b', r'\bimport\b', r'\bfrom\b', r'\byield\b',
            r'==', r'!=', r'<=', r'>=', r'\+=', r'-=', r'\*=', r'/=',
            r'\+\+', r'--', r'->', r'\.', r'\[', r'\]', r'\(', r'\)',
            r'\{', r'\}', r':', r',', r';',
        ]
        
        # Extract tokens
        for pattern in patterns:
            matches = re.findall(pattern, code)
            tokens.extend(matches)
        
        # Add identifiers (normalized)
        identifiers = re.findall(r'\b[a-zA-Z_][a-zA-Z0-9_]*\b', code)
        # Normalize variable names to placeholders
        name_map = {}
        for ident in identifiers:
            if ident not in name_map:
                if ident not in ['def', 'class', 'if', 'else', 'elif', 'for', 'while',
                                 'return', 'in', 'not', 'and', 'or', 'True', 'False',
                                 'None', 'try', 'except', 'finally', 'with', 'as',
                                 'lambda', 'import', 'from', 'yield', 'print', 'len',
                                 'range', 'str', 'int', 'list', 'dict', 'set', 'tuple']:
                    name_map[ident] = f'VAR{len(name_map)}'
        
        normalized_tokens = []
        for ident in identifiers:
            normalized_tokens.append(name_map.get(ident, ident))
        
        tokens.extend(normalized_tokens)
        return tokens
    
    @staticmethod
    def get_ngrams(tokens: List[str], n: int = 3) -> List[Tuple]:
        """Get n-grams from tokens"""
        return [tuple(tokens[i:i+n]) for i in range(len(tokens) - n + 1)]
    
    @staticmethod
    def jaccard_similarity(set1: Set, set2: Set) -> float:
        """Calculate Jaccard similarity"""
        if not set1 and not set2:
            return 1.0
        if not set1 or not set2:
            return 0.0
        intersection = len(set1 & set2)
        union = len(set1 | set2)
        return intersection / union if union > 0 else 0.0
    
    @classmethod
    def compare(cls, code1: str, code2: str, n: int = 3) -> float:
        """Compare two code snippets using token n-grams"""
        tokens1 = cls.tokenize_python(code1)
        tokens2 = cls.tokenize_python(code2)
        
        if not tokens1 or not tokens2:
            return 0.0
        
        ngrams1 = set(cls.get_ngrams(tokens1, n))
        ngrams2 = set(cls.get_ngrams(tokens2, n))
        
        return cls.jaccard_similarity(ngrams1, ngrams2)


class ASTSimilarity:
    """AST-based structural similarity"""
    
    @staticmethod
    def get_ast_structure(node, depth: int = 0) -> List[Tuple[str, int]]:
        """Extract AST structure as a list of (node_type, depth) tuples"""
        structure = [(type(node).__name__, depth)]
        
        for child in ast.iter_child_nodes(node):
            structure.extend(ASTSimilarity.get_ast_structure(child, depth + 1))
        
        return structure
    
    @staticmethod
    def tree_edit_distance_approximation(struct1: List, struct2: List) -> float:
        """Approximate tree similarity using structure sequences"""
        if not struct1 and not struct2:
            return 1.0
        if not struct1 or not struct2:
            return 0.0
        
        # Convert to comparable strings
        str1 = '|'.join(f"{t}:{d}" for t, d in struct1)
        str2 = '|'.join(f"{t}:{d}" for t, d in struct2)
        
        return SequenceMatcher(None, str1, str2).ratio()
    
    @classmethod
    def compare(cls, code1: str, code2: str) -> float:
        """Compare two code snippets using AST similarity"""
        try:
            tree1 = ast.parse(code1)
            tree2 = ast.parse(code2)
        except SyntaxError:
            return 0.0
        
        struct1 = cls.get_ast_structure(tree1)
        struct2 = cls.get_ast_structure(tree2)
        
        return cls.tree_edit_distance_approximation(struct1, struct2)


class WinnowingFingerprint:
    """
    Winnowing algorithm for code fingerprinting
    Used for plagiarism detection
    """
    
    def __init__(self, k: int = 5, w: int = 4):
        """
        Args:
            k: k-gram size
            w: window size for fingerprint selection
        """
        self.k = k
        self.w = w
    
    def get_kgrams(self, text: str) -> List[str]:
        """Get k-grams from text"""
        return [text[i:i+self.k] for i in range(len(text) - self.k + 1)]
    
    def hash_kgram(self, kgram: str) -> int:
        """Hash a k-gram"""
        return int(hashlib.md5(kgram.encode()).hexdigest()[:8], 16)
    
    def get_fingerprints(self, text: str) -> Set[int]:
        """Get fingerprints using winnowing algorithm"""
        # Remove all whitespace for comparison
        text = re.sub(r'\s+', '', text.lower())
        
        if len(text) < self.k:
            return set()
        
        kgrams = self.get_kgrams(text)
        hashes = [self.hash_kgram(kg) for kg in kgrams]
        
        if len(hashes) < self.w:
            return set(hashes)
        
        # Winnowing: select minimum hash in each window
        fingerprints = set()
        prev_min_idx = -1
        
        for i in range(len(hashes) - self.w + 1):
            window = hashes[i:i+self.w]
            min_val = min(window)
            min_idx = i + window.index(min_val)
            
            # Only add if it's a new minimum position
            if min_idx != prev_min_idx:
                fingerprints.add(min_val)
                prev_min_idx = min_idx
        
        return fingerprints
    
    def compare(self, text1: str, text2: str) -> float:
        """Compare two texts using fingerprint similarity"""
        fp1 = self.get_fingerprints(text1)
        fp2 = self.get_fingerprints(text2)
        
        if not fp1 and not fp2:
            return 1.0
        if not fp1 or not fp2:
            return 0.0
        
        intersection = len(fp1 & fp2)
        union = len(fp1 | fp2)
        
        return intersection / union if union > 0 else 0.0


class CodeSimilarityChecker:
    """Main class for code similarity checking"""
    
    def __init__(self):
        self.winnowing = WinnowingFingerprint()
    
    def compare(self, code1: str, code2: str, language: str = 'python') -> SimilarityResult:
        """
        Compare two code snippets and return similarity metrics
        
        Args:
            code1: First code snippet
            code2: Second code snippet
            language: Programming language
        
        Returns:
            SimilarityResult with various similarity metrics
        """
        # Normalize code
        norm1 = CodeNormalizer.normalize(code1, language)
        norm2 = CodeNormalizer.normalize(code2, language)
        
        # Calculate different similarity metrics
        structural = 0.0
        if language.lower() in ['python', 'python3']:
            try:
                structural = ASTSimilarity.compare(norm1, norm2)
            except:
                structural = 0.0
        
        token_sim = TokenBasedSimilarity.compare(norm1, norm2)
        fingerprint_sim = self.winnowing.compare(norm1, norm2)
        
        # Combined score with weights
        overall = (
            structural * 0.4 +
            token_sim * 0.35 +
            fingerprint_sim * 0.25
        )
        
        # Determine similarity level
        if overall >= 0.9:
            level = "几乎相同"
        elif overall >= 0.7:
            level = "高度相似"
        elif overall >= 0.5:
            level = "中度相似"
        elif overall >= 0.3:
            level = "轻度相似"
        else:
            level = "基本不同"
        
        return SimilarityResult(
            overall_score=round(overall, 3),
            structural_similarity=round(structural, 3),
            token_similarity=round(token_sim, 3),
            fingerprint_similarity=round(fingerprint_sim, 3),
            details={
                "level": level,
                "is_suspicious": overall >= 0.8,
                "code1_lines": len(code1.split('\n')),
                "code2_lines": len(code2.split('\n')),
            }
        )
    
    def find_similar_in_database(
        self, 
        code: str, 
        code_database: List[Dict],
        threshold: float = 0.7,
        language: str = 'python'
    ) -> List[Dict]:
        """
        Find similar code in a database
        
        Args:
            code: Code to check
            code_database: List of {id, code, ...} dicts
            threshold: Minimum similarity threshold
            language: Programming language
        
        Returns:
            List of similar code entries with similarity scores
        """
        results = []
        
        for entry in code_database:
            db_code = entry.get('code', '')
            if not db_code:
                continue
            
            similarity = self.compare(code, db_code, language)
            
            if similarity.overall_score >= threshold:
                results.append({
                    "entry_id": entry.get('id'),
                    "similarity_score": similarity.overall_score,
                    "details": similarity.details
                })
        
        # Sort by similarity score
        results.sort(key=lambda x: x['similarity_score'], reverse=True)
        return results


# Convenience functions
def compare_code(code1: str, code2: str, language: str = 'python') -> Dict:
    """
    Compare two code snippets
    
    Returns:
        Dictionary with similarity metrics
    """
    checker = CodeSimilarityChecker()
    result = checker.compare(code1, code2, language)
    
    return {
        "overall_similarity": result.overall_score,
        "structural_similarity": result.structural_similarity,
        "token_similarity": result.token_similarity,
        "fingerprint_similarity": result.fingerprint_similarity,
        "level": result.details["level"],
        "is_suspicious": result.details["is_suspicious"]
    }


def check_plagiarism(code: str, submissions: List[Dict], language: str = 'python') -> List[Dict]:
    """
    Check code against a list of previous submissions
    
    Args:
        code: Code to check
        submissions: List of previous submissions [{id, code, user_id, ...}]
        language: Programming language
    
    Returns:
        List of potentially plagiarized submissions
    """
    checker = CodeSimilarityChecker()
    return checker.find_similar_in_database(code, submissions, threshold=0.7, language=language)

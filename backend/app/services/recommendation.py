"""
Recommendation Service
Personalized problem recommendations based on user skill model
"""

import random
from typing import List, Dict, Optional
from app.models.database import Problem, User, Submission


# Knowledge topics and their prerequisites
KNOWLEDGE_GRAPH = {
    "array": {"prerequisites": [], "related": ["two_pointers", "sliding_window"]},
    "string": {"prerequisites": ["array"], "related": ["two_pointers"]},
    "hash_table": {"prerequisites": ["array"], "related": []},
    "two_pointers": {"prerequisites": ["array"], "related": ["sliding_window"]},
    "sliding_window": {"prerequisites": ["two_pointers"], "related": []},
    "linked_list": {"prerequisites": [], "related": ["two_pointers"]},
    "stack": {"prerequisites": ["array"], "related": ["monotonic_stack"]},
    "queue": {"prerequisites": ["array"], "related": ["bfs"]},
    "binary_search": {"prerequisites": ["array"], "related": []},
    "tree": {"prerequisites": ["linked_list"], "related": ["bfs", "dfs"]},
    "binary_tree": {"prerequisites": ["tree"], "related": ["bst"]},
    "bst": {"prerequisites": ["binary_tree", "binary_search"], "related": []},
    "heap": {"prerequisites": ["tree", "array"], "related": ["priority_queue"]},
    "graph": {"prerequisites": ["tree"], "related": ["bfs", "dfs"]},
    "bfs": {"prerequisites": ["queue", "graph"], "related": ["dfs"]},
    "dfs": {"prerequisites": ["stack", "graph"], "related": ["bfs", "backtracking"]},
    "backtracking": {"prerequisites": ["dfs"], "related": ["recursion"]},
    "recursion": {"prerequisites": [], "related": ["dp", "divide_conquer"]},
    "dp": {"prerequisites": ["recursion"], "related": ["memoization"]},
    "greedy": {"prerequisites": [], "related": []},
    "sort": {"prerequisites": ["array"], "related": []},
    "divide_conquer": {"prerequisites": ["recursion"], "related": ["merge_sort"]},
    "bit_manipulation": {"prerequisites": [], "related": []},
    "math": {"prerequisites": [], "related": []},
    "trie": {"prerequisites": ["tree", "string"], "related": []},
    "union_find": {"prerequisites": ["graph"], "related": []},
}

# Default knowledge state for new users
DEFAULT_KNOWLEDGE_STATE = {topic: 0.0 for topic in KNOWLEDGE_GRAPH.keys()}


class UserSkillModel:
    """Model user's skill level and knowledge state"""
    
    def __init__(self, user: User):
        self.user = user
        self.knowledge_state = user.knowledge_state or DEFAULT_KNOWLEDGE_STATE.copy()
    
    def update_after_problem(self, problem: Problem, passed: bool, attempts: int, time_spent: int):
        """Update knowledge state after solving a problem"""
        difficulty_weight = {"easy": 0.05, "medium": 0.08, "hard": 0.12}
        base_weight = difficulty_weight.get(problem.difficulty, 0.05)
        
        for topic in problem.topics:
            if topic not in self.knowledge_state:
                self.knowledge_state[topic] = 0.0
            
            current = self.knowledge_state[topic]
            
            if passed:
                # Increase mastery based on difficulty and attempts
                gain = base_weight * (1.0 / attempts) * (1.0 if time_spent < 1800 else 0.8)
                self.knowledge_state[topic] = min(1.0, current + gain)
            else:
                # Slight decrease on failure
                self.knowledge_state[topic] = max(0.0, current - 0.02)
        
        return self.knowledge_state
    
    def get_weak_areas(self, n: int = 3) -> List[str]:
        """Get n weakest topics"""
        # Only consider topics user has some exposure to
        exposed = {k: v for k, v in self.knowledge_state.items() if v > 0}
        if not exposed:
            # For new users, recommend foundational topics
            return ["array", "string", "hash_table"][:n]
        
        sorted_topics = sorted(exposed.items(), key=lambda x: x[1])
        return [t[0] for t in sorted_topics[:n]]
    
    def get_strong_areas(self, n: int = 3) -> List[str]:
        """Get n strongest topics"""
        sorted_topics = sorted(self.knowledge_state.items(), key=lambda x: x[1], reverse=True)
        return [t[0] for t in sorted_topics[:n] if t[1] > 0]
    
    def get_recommended_difficulty(self, topic: str) -> str:
        """Get recommended difficulty for a topic"""
        mastery = self.knowledge_state.get(topic, 0.0)
        
        if mastery < 0.3:
            return "easy"
        elif mastery < 0.7:
            return "medium"
        else:
            return "hard"
    
    def get_next_topics_to_learn(self) -> List[str]:
        """Get topics user should learn next based on prerequisites"""
        learnable = []
        
        for topic, info in KNOWLEDGE_GRAPH.items():
            # Skip topics already well-known
            if self.knowledge_state.get(topic, 0) > 0.5:
                continue
            
            # Check if prerequisites are met
            prereqs_met = all(
                self.knowledge_state.get(prereq, 0) >= 0.5
                for prereq in info["prerequisites"]
            )
            
            if prereqs_met:
                learnable.append(topic)
        
        return learnable


class RecommendationEngine:
    """Engine for recommending problems to users"""
    
    def recommend_problems(
        self,
        user: User,
        problems: List[Problem],
        solved_ids: set,
        n: int = 5
    ) -> List[Dict]:
        """Recommend n problems for user"""
        
        skill_model = UserSkillModel(user)
        recommendations = []
        
        # Available problems (not solved)
        available = [p for p in problems if p.id not in solved_ids]
        
        if not available:
            return []
        
        # Strategy distribution
        strategies = [
            ("weak_area", 0.5),      # 50% - target weak areas
            ("consolidate", 0.3),    # 30% - consolidate strong areas
            ("explore", 0.2),        # 20% - explore new topics
        ]
        
        for strategy, ratio in strategies:
            count = max(1, int(n * ratio))
            
            if strategy == "weak_area":
                weak_topics = skill_model.get_weak_areas(3)
                recs = self._find_problems_by_topics(
                    available, weak_topics, 
                    skill_model, count, "challenge"
                )
            elif strategy == "consolidate":
                strong_topics = skill_model.get_strong_areas(2)
                recs = self._find_problems_by_topics(
                    available, strong_topics,
                    skill_model, count, "consolidate"
                )
            else:  # explore
                next_topics = skill_model.get_next_topics_to_learn()
                if next_topics:
                    recs = self._find_problems_by_topics(
                        available, next_topics[:2],
                        skill_model, count, "explore"
                    )
                else:
                    recs = []
            
            recommendations.extend(recs)
        
        # Remove duplicates while preserving order
        seen = set()
        unique_recs = []
        for rec in recommendations:
            if rec["problem"].id not in seen:
                seen.add(rec["problem"].id)
                unique_recs.append(rec)
        
        return unique_recs[:n]
    
    def _find_problems_by_topics(
        self,
        problems: List[Problem],
        topics: List[str],
        skill_model: UserSkillModel,
        n: int,
        strategy: str
    ) -> List[Dict]:
        """Find problems matching topics"""
        matching = []
        
        for problem in problems:
            problem_topics = set(problem.topics or [])
            if problem_topics & set(topics):
                # Calculate fit score
                difficulty = problem.difficulty
                recommended_diff = skill_model.get_recommended_difficulty(topics[0])
                
                if strategy == "challenge":
                    # Slightly harder than recommended
                    diff_score = 1.0 if difficulty == recommended_diff else 0.5
                elif strategy == "consolidate":
                    # At or below recommended level
                    diff_order = {"easy": 0, "medium": 1, "hard": 2}
                    if diff_order.get(difficulty, 1) <= diff_order.get(recommended_diff, 1):
                        diff_score = 1.0
                    else:
                        diff_score = 0.3
                else:  # explore
                    # Easy difficulty for new topics
                    diff_score = 1.0 if difficulty == "easy" else 0.5
                
                matching.append({
                    "problem": problem,
                    "score": diff_score,
                    "reason": f"{strategy}: {', '.join(topics)}"
                })
        
        # Sort by score and return top n
        matching.sort(key=lambda x: x["score"], reverse=True)
        return matching[:n]
    
    def get_learning_path(
        self,
        user: User,
        target_topic: str,
        problems: List[Problem]
    ) -> List[Dict]:
        """Generate a learning path to master a topic"""
        
        skill_model = UserSkillModel(user)
        path = []
        
        # Find prerequisites chain
        def get_prereq_chain(topic: str, visited: set = None) -> List[str]:
            if visited is None:
                visited = set()
            if topic in visited:
                return []
            visited.add(topic)
            
            prereqs = KNOWLEDGE_GRAPH.get(topic, {}).get("prerequisites", [])
            chain = []
            for prereq in prereqs:
                chain.extend(get_prereq_chain(prereq, visited))
            chain.append(topic)
            return chain
        
        topic_chain = get_prereq_chain(target_topic)
        
        for topic in topic_chain:
            mastery = skill_model.knowledge_state.get(topic, 0)
            if mastery < 0.7:  # Need more practice
                # Find problems for this topic
                topic_problems = [p for p in problems if topic in (p.topics or [])]
                
                # Sort by difficulty
                topic_problems.sort(key=lambda p: {"easy": 0, "medium": 1, "hard": 2}.get(p.difficulty, 1))
                
                path.append({
                    "topic": topic,
                    "current_mastery": mastery,
                    "target_mastery": 0.7,
                    "problems": topic_problems[:5]
                })
        
        return path


# Global recommendation engine instance
recommendation_engine = RecommendationEngine()


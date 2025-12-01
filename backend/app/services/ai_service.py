"""
AI Service - GPT-4/Claude integration for interview simulation
"""

import json
from typing import List, Dict, AsyncGenerator
from openai import AsyncOpenAI
from anthropic import AsyncAnthropic

from app.config import settings


# Company interview styles
COMPANY_STYLES = {
    "google": "友好但追求最优解，喜欢讨论多种解法和时间复杂度优化",
    "meta": "注重代码简洁和实际工作场景，喜欢追问边缘情况",
    "amazon": "注重沟通和权衡，强调Leadership Principles",
    "microsoft": "技术深度和广度并重，喜欢系统设计问题",
    "startup": "务实高效，关注快速解决问题的能力"
}

# Interview type templates
INTERVIEW_PROMPTS = {
    "algorithm": """你是{company}的资深软件工程师,正在进行算法面试。

面试风格:
- {company_style}
- 时长: {duration}分钟
- 难度: {difficulty}

当前题目: {problem_title}
题目描述: {problem_description}

你的职责:
1. 简短自我介绍和破冰(1-2分钟)
2. 清晰描述问题,回答候选人的澄清问题
3. 观察候选人的思考过程,适时给出提示
4. 如果候选人卡住超过3分钟,给予渐进式提示(不直接给答案)
5. 代码完成后,询问时间/空间复杂度
6. 提出优化问题或边缘情况
7. 保持鼓励和积极的态度

评估维度:
- 问题理解和澄清能力
- 算法思路和沟通表达
- 代码质量和风格
- 时间/空间复杂度分析
- 测试和边缘情况处理
- 优化能力

回复格式要求:
- 保持自然对话,像真人面试官
- 每次回复控制在2-4句话
- 候选人紧张时给予鼓励
- 用中文交流""",

    "system_design": """你是{company}的资深系统架构师,正在进行系统设计面试。

面试风格:
- {company_style}
- 时长: {duration}分钟
- 难度: {difficulty}

设计题目: {problem_title}
题目描述: {problem_description}

你的职责:
1. 介绍自己并说明面试流程
2. 让候选人先澄清需求和约束
3. 引导候选人从高层设计开始,逐步深入
4. 适时提问:扩展性、可靠性、性能优化
5. 讨论权衡和取舍
6. 评估候选人的系统设计思维

关注点:
- 需求分析和估算能力
- 高层架构设计
- 数据模型设计
- API设计
- 扩展性考虑
- 容错和可靠性

用中文交流,保持专业但友好。""",

    "behavioral": """你是{company}的HR和技术经理,正在进行行为面试。

面试风格:
- {company_style}
- 时长: {duration}分钟

你的职责:
1. 自我介绍,营造轻松氛围
2. 使用STAR方法提问(Situation, Task, Action, Result)
3. 深入追问细节和具体行动
4. 评估候选人的软技能

常问问题类型:
- 团队合作经历
- 解决冲突的经历
- 处理困难项目的经历
- 领导力展示
- 失败和学习的经历

用中文交流,表现出真诚的兴趣。""",

    "frontend": """你是{company}的资深前端工程师,正在进行前端技术面试。

面试风格:
- {company_style}
- 时长: {duration}分钟
- 难度: {difficulty}

题目: {problem_title}
描述: {problem_description}

关注点:
- HTML/CSS/JavaScript基础
- React/Vue框架理解
- 性能优化
- 浏览器原理
- 代码实现能力

用中文交流,注重实际工作场景。"""
}


class AIService:
    """AI Service for interview simulation and code analysis"""
    
    def __init__(self):
        self.openai_client = None
        self.anthropic_client = None
        
        if settings.OPENAI_API_KEY:
            self.openai_client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        if settings.ANTHROPIC_API_KEY:
            self.anthropic_client = AsyncAnthropic(api_key=settings.ANTHROPIC_API_KEY)
    
    def _build_interview_prompt(
        self,
        interview_type: str,
        company: str,
        difficulty: str,
        duration: int,
        problem: Dict
    ) -> str:
        """Build interview system prompt"""
        template = INTERVIEW_PROMPTS.get(interview_type, INTERVIEW_PROMPTS["algorithm"])
        company_style = COMPANY_STYLES.get(company.lower(), COMPANY_STYLES["startup"])
        
        return template.format(
            company=company,
            company_style=company_style,
            difficulty=difficulty,
            duration=duration,
            problem_title=problem.get("title", ""),
            problem_description=problem.get("description", "")
        )
    
    async def chat_with_interviewer(
        self,
        interview_type: str,
        company: str,
        difficulty: str,
        duration: int,
        problem: Dict,
        conversation_history: List[Dict],
        user_message: str,
        user_code: str = None
    ) -> str:
        """Generate interviewer response"""
        
        system_prompt = self._build_interview_prompt(
            interview_type, company, difficulty, duration, problem
        )
        
        messages = [{"role": "system", "content": system_prompt}]
        
        # Add conversation history
        for msg in conversation_history[-10:]:  # Keep last 10 messages
            messages.append({
                "role": msg["role"],
                "content": msg["content"]
            })
        
        # Add current user message with code if provided
        user_content = user_message
        if user_code:
            user_content += f"\n\n我的当前代码:\n```\n{user_code}\n```"
        
        messages.append({"role": "user", "content": user_content})
        
        # Try OpenAI first, then Anthropic
        if self.openai_client:
            response = await self.openai_client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=messages,
                temperature=0.7,
                max_tokens=500
            )
            return response.choices[0].message.content
        elif self.anthropic_client:
            response = await self.anthropic_client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=500,
                system=system_prompt,
                messages=[{"role": m["role"], "content": m["content"]} 
                         for m in messages[1:]]  # Skip system message
            )
            return response.content[0].text
        else:
            # Fallback response for demo
            return self._generate_demo_response(interview_type, user_message, user_code)
    
    async def stream_interviewer_response(
        self,
        interview_type: str,
        company: str,
        difficulty: str,
        duration: int,
        problem: Dict,
        conversation_history: List[Dict],
        user_message: str,
        user_code: str = None
    ) -> AsyncGenerator[str, None]:
        """Stream interviewer response for real-time effect"""
        
        system_prompt = self._build_interview_prompt(
            interview_type, company, difficulty, duration, problem
        )
        
        messages = [{"role": "system", "content": system_prompt}]
        
        for msg in conversation_history[-10:]:
            messages.append({"role": msg["role"], "content": msg["content"]})
        
        user_content = user_message
        if user_code:
            user_content += f"\n\n我的当前代码:\n```\n{user_code}\n```"
        messages.append({"role": "user", "content": user_content})
        
        if self.openai_client:
            stream = await self.openai_client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=messages,
                temperature=0.7,
                max_tokens=500,
                stream=True
            )
            
            async for chunk in stream:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
        else:
            # Demo fallback
            response = self._generate_demo_response(interview_type, user_message, user_code)
            for char in response:
                yield char
    
    async def analyze_code(
        self,
        code: str,
        language: str,
        problem: Dict,
        test_results: List[Dict]
    ) -> Dict:
        """Analyze submitted code and provide feedback"""
        
        prompt = f"""分析以下代码并提供反馈:

题目: {problem.get('title', '')}
语言: {language}

代码:
```{language}
{code}
```

测试结果: {json.dumps(test_results, ensure_ascii=False)}

请提供:
1. 代码质量评分 (1-10)
2. 时间复杂度分析
3. 空间复杂度分析
4. 代码优点
5. 改进建议
6. 潜在的bug或边缘情况

以JSON格式返回结果。"""

        if self.openai_client:
            response = await self.openai_client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=1000
            )
            try:
                return json.loads(response.choices[0].message.content)
            except json.JSONDecodeError:
                return {"feedback": response.choices[0].message.content}
        else:
            # Demo fallback
            return self._generate_demo_analysis(code, test_results)
    
    async def generate_interview_report(
        self,
        interview_type: str,
        company: str,
        conversation_history: List[Dict],
        code_snapshots: List[Dict],
        problem: Dict,
        final_submission: Dict
    ) -> Dict:
        """Generate comprehensive interview report"""
        
        prompt = f"""基于以下面试记录,生成详细的面试报告:

面试类型: {interview_type}
目标公司: {company}
题目: {problem.get('title', '')}

对话记录:
{json.dumps(conversation_history, ensure_ascii=False, indent=2)}

最终提交:
- 状态: {final_submission.get('status', 'unknown')}
- 通过测试: {final_submission.get('passed_count', 0)}/{final_submission.get('total_count', 0)}

请生成包含以下内容的报告:
1. 总体评分 (1-10)
2. 各维度得分:
   - 问题理解
   - 算法设计
   - 代码实现
   - 沟通能力
   - 优化意识
3. 时间分配分析
4. 做得好的方面 (列表)
5. 需要改进的方面 (列表)
6. 具体建议
7. 推荐练习的题目类型

以JSON格式返回。"""

        if self.openai_client:
            response = await self.openai_client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=1500
            )
            try:
                return json.loads(response.choices[0].message.content)
            except json.JSONDecodeError:
                return self._generate_demo_report()
        else:
            return self._generate_demo_report()
    
    def _generate_demo_response(
        self,
        interview_type: str,
        user_message: str,
        user_code: str = None
    ) -> str:
        """Generate demo response when no API key is configured"""
        
        if "你好" in user_message or len(user_message) < 20:
            return "你好!我是今天的面试官。在开始之前,你想先澄清一下题目要求吗?有什么问题随时问我。"
        
        if user_code:
            return "我看到你的代码了。思路看起来不错!你能解释一下这个算法的时间复杂度吗?还有,你考虑过边缘情况吗?比如空输入或者只有一个元素的情况。"
        
        return "好的,这个思路挺好的。你能把它转化成代码吗?别担心一开始不完美,我们可以一起优化。"
    
    def _generate_demo_analysis(self, code: str, test_results: List[Dict]) -> Dict:
        """Generate demo analysis when no API key is configured"""
        passed = sum(1 for t in test_results if t.get('passed', False))
        total = len(test_results)
        
        return {
            "quality_score": 7 if passed == total else 5,
            "time_complexity": "O(n)",
            "space_complexity": "O(1)",
            "strengths": ["代码结构清晰", "变量命名合理"],
            "improvements": ["可以考虑边缘情况", "添加注释说明"],
            "potential_bugs": []
        }
    
    def _generate_demo_report(self) -> Dict:
        """Generate demo interview report"""
        return {
            "overall_score": 7.5,
            "dimension_scores": {
                "problem_understanding": 8,
                "algorithm_design": 7,
                "code_implementation": 7,
                "communication": 8,
                "optimization": 6
            },
            "time_analysis": {
                "understanding": 5,
                "designing": 10,
                "coding": 25,
                "testing": 5
            },
            "strengths": [
                "主动澄清问题要求",
                "沟通思路清晰",
                "代码风格良好"
            ],
            "improvements": [
                "需要更多关注边缘情况",
                "优化意识可以加强",
                "可以更主动讨论复杂度"
            ],
            "suggestions": [
                "多练习动态规划题目",
                "加强时间复杂度分析",
                "练习口头表达算法思路"
            ],
            "recommended_topics": ["dynamic_programming", "graph", "binary_search"]
        }


# Global AI service instance
ai_service = AIService()


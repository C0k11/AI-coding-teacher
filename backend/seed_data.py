"""
Seed database with sample problems
"""

from app.models.database import init_db, SessionLocal, Problem

SAMPLE_PROBLEMS = [
    {
        "title": "Two Sum",
        "slug": "two-sum",
        "description": """给定一个整数数组 nums 和一个整数目标值 target，请你在该数组中找出和为目标值 target 的那两个整数，并返回它们的数组下标。

你可以假设每种输入只会对应一个答案。但是，数组中同一个元素在答案里不能重复出现。

你可以按任意顺序返回答案。""",
        "difficulty": "easy",
        "examples": [
            {"input": "nums = [2,7,11,15], target = 9", "output": "[0,1]", "explanation": "因为 nums[0] + nums[1] == 9，返回 [0, 1]。"},
            {"input": "nums = [3,2,4], target = 6", "output": "[1,2]", "explanation": ""},
            {"input": "nums = [3,3], target = 6", "output": "[0,1]", "explanation": ""}
        ],
        "constraints": ["2 <= nums.length <= 10^4", "-10^9 <= nums[i] <= 10^9", "-10^9 <= target <= 10^9", "只会存在一个有效答案"],
        "starter_code": {
            "python": "class Solution:\n    def twoSum(self, nums: list[int], target: int) -> list[int]:\n        pass",
            "javascript": "/**\n * @param {number[]} nums\n * @param {number} target\n * @return {number[]}\n */\nvar twoSum = function(nums, target) {\n    \n};",
            "java": "class Solution {\n    public int[] twoSum(int[] nums, int target) {\n        \n    }\n}"
        },
        "test_cases": [
            {"input": "[2,7,11,15]\n9", "expected_output": "[0, 1]"},
            {"input": "[3,2,4]\n6", "expected_output": "[1, 2]"},
            {"input": "[3,3]\n6", "expected_output": "[0, 1]"}
        ],
        "hidden_test_cases": [
            {"input": "[1,2,3,4,5]\n9", "expected_output": "[3, 4]"},
            {"input": "[-1,-2,-3,-4,-5]\n-8", "expected_output": "[2, 4]"}
        ],
        "topics": ["array", "hash_table"],
        "companies": ["google", "amazon", "meta", "microsoft"],
        "patterns": ["two_pointers", "hash_map"],
        "hints": [
            "可以使用暴力法，遍历每对数字检查它们的和",
            "考虑使用哈希表来优化查找时间",
            "遍历数组时，对于每个元素，检查 target - nums[i] 是否在哈希表中"
        ],
        "solutions": [
            {
                "approach": "暴力法",
                "code": "class Solution:\n    def twoSum(self, nums, target):\n        for i in range(len(nums)):\n            for j in range(i + 1, len(nums)):\n                if nums[i] + nums[j] == target:\n                    return [i, j]",
                "time_complexity": "O(n²)",
                "space_complexity": "O(1)",
                "explanation": "使用两层循环检查所有数字对"
            },
            {
                "approach": "哈希表",
                "code": "class Solution:\n    def twoSum(self, nums, target):\n        seen = {}\n        for i, num in enumerate(nums):\n            complement = target - num\n            if complement in seen:\n                return [seen[complement], i]\n            seen[num] = i",
                "time_complexity": "O(n)",
                "space_complexity": "O(n)",
                "explanation": "使用哈希表存储已遍历的数字及其索引，一次遍历即可找到答案"
            }
        ],
        "time_complexity": "O(n)",
        "space_complexity": "O(n)"
    },
    {
        "title": "Valid Parentheses",
        "slug": "valid-parentheses",
        "description": """给定一个只包括 '('，')'，'{'，'}'，'['，']' 的字符串 s ，判断字符串是否有效。

有效字符串需满足：
1. 左括号必须用相同类型的右括号闭合。
2. 左括号必须以正确的顺序闭合。
3. 每个右括号都有一个对应的相同类型的左括号。""",
        "difficulty": "easy",
        "examples": [
            {"input": 's = "()"', "output": "true", "explanation": ""},
            {"input": 's = "()[]{}"', "output": "true", "explanation": ""},
            {"input": 's = "(]"', "output": "false", "explanation": ""}
        ],
        "constraints": ["1 <= s.length <= 10^4", "s 仅由括号 '()[]{}' 组成"],
        "starter_code": {
            "python": "class Solution:\n    def isValid(self, s: str) -> bool:\n        pass",
            "javascript": "/**\n * @param {string} s\n * @return {boolean}\n */\nvar isValid = function(s) {\n    \n};"
        },
        "test_cases": [
            {"input": "()", "expected_output": "True"},
            {"input": "()[]{}", "expected_output": "True"},
            {"input": "(]", "expected_output": "False"}
        ],
        "hidden_test_cases": [
            {"input": "((()))", "expected_output": "True"},
            {"input": "([)]", "expected_output": "False"}
        ],
        "topics": ["string", "stack"],
        "companies": ["google", "amazon", "meta"],
        "patterns": ["stack"],
        "hints": [
            "使用栈来跟踪左括号",
            "遇到右括号时，检查栈顶是否是匹配的左括号"
        ],
        "solutions": [
            {
                "approach": "栈",
                "code": "class Solution:\n    def isValid(self, s):\n        stack = []\n        mapping = {')': '(', '}': '{', ']': '['}\n        for char in s:\n            if char in mapping:\n                if not stack or stack.pop() != mapping[char]:\n                    return False\n            else:\n                stack.append(char)\n        return len(stack) == 0",
                "time_complexity": "O(n)",
                "space_complexity": "O(n)",
                "explanation": "使用栈存储左括号，遇到右括号时检查是否匹配"
            }
        ],
        "time_complexity": "O(n)",
        "space_complexity": "O(n)"
    },
    {
        "title": "LRU Cache",
        "slug": "lru-cache",
        "description": """请你设计并实现一个满足 LRU (最近最少使用) 缓存约束的数据结构。

实现 LRUCache 类：
- LRUCache(int capacity) 以正整数作为容量 capacity 初始化 LRU 缓存
- int get(int key) 如果关键字 key 存在于缓存中，则返回关键字的值，否则返回 -1 。
- void put(int key, int value) 如果关键字 key 已经存在，则变更其数据值 value ；如果不存在，则向缓存中插入该组 key-value 。如果插入操作导致关键字数量超过 capacity ，则应该逐出最久未使用的关键字。

函数 get 和 put 必须以 O(1) 的平均时间复杂度运行。""",
        "difficulty": "medium",
        "examples": [
            {
                "input": '["LRUCache", "put", "put", "get", "put", "get", "put", "get", "get", "get"]\n[[2], [1, 1], [2, 2], [1], [3, 3], [2], [4, 4], [1], [3], [4]]',
                "output": "[null, null, null, 1, null, -1, null, -1, 3, 4]",
                "explanation": "LRUCache lRUCache = new LRUCache(2);\nlRUCache.put(1, 1); // 缓存是 {1=1}\nlRUCache.put(2, 2); // 缓存是 {1=1, 2=2}\nlRUCache.get(1);    // 返回 1\nlRUCache.put(3, 3); // 该操作会使得关键字 2 作废，缓存是 {1=1, 3=3}\nlRUCache.get(2);    // 返回 -1 (未找到)\nlRUCache.put(4, 4); // 该操作会使得关键字 1 作废，缓存是 {4=4, 3=3}\nlRUCache.get(1);    // 返回 -1 (未找到)\nlRUCache.get(3);    // 返回 3\nlRUCache.get(4);    // 返回 4"
            }
        ],
        "constraints": ["1 <= capacity <= 3000", "0 <= key <= 10^4", "0 <= value <= 10^5", "最多调用 2 * 10^5 次 get 和 put"],
        "starter_code": {
            "python": "class LRUCache:\n\n    def __init__(self, capacity: int):\n        pass\n\n    def get(self, key: int) -> int:\n        pass\n\n    def put(self, key: int, value: int) -> None:\n        pass",
            "javascript": "/**\n * @param {number} capacity\n */\nvar LRUCache = function(capacity) {\n    \n};\n\n/** \n * @param {number} key\n * @return {number}\n */\nLRUCache.prototype.get = function(key) {\n    \n};\n\n/** \n * @param {number} key \n * @param {number} value\n * @return {void}\n */\nLRUCache.prototype.put = function(key, value) {\n    \n};"
        },
        "test_cases": [
            {"input": "2\nput 1 1\nput 2 2\nget 1\nput 3 3\nget 2", "expected_output": "1\n-1"}
        ],
        "hidden_test_cases": [],
        "topics": ["hash_table", "linked_list", "design"],
        "companies": ["google", "amazon", "meta", "microsoft"],
        "patterns": ["hash_map", "doubly_linked_list"],
        "hints": [
            "需要同时使用哈希表和双向链表",
            "哈希表用于O(1)查找，双向链表用于维护访问顺序",
            "get和put操作后，需要将节点移到链表头部"
        ],
        "solutions": [
            {
                "approach": "哈希表 + 双向链表",
                "code": "class ListNode:\n    def __init__(self, key=0, val=0):\n        self.key = key\n        self.val = val\n        self.prev = None\n        self.next = None\n\nclass LRUCache:\n    def __init__(self, capacity):\n        self.capacity = capacity\n        self.cache = {}\n        self.head = ListNode()\n        self.tail = ListNode()\n        self.head.next = self.tail\n        self.tail.prev = self.head\n    \n    def _remove(self, node):\n        node.prev.next = node.next\n        node.next.prev = node.prev\n    \n    def _add_to_head(self, node):\n        node.next = self.head.next\n        node.prev = self.head\n        self.head.next.prev = node\n        self.head.next = node\n    \n    def get(self, key):\n        if key in self.cache:\n            node = self.cache[key]\n            self._remove(node)\n            self._add_to_head(node)\n            return node.val\n        return -1\n    \n    def put(self, key, value):\n        if key in self.cache:\n            node = self.cache[key]\n            node.val = value\n            self._remove(node)\n            self._add_to_head(node)\n        else:\n            if len(self.cache) >= self.capacity:\n                lru = self.tail.prev\n                self._remove(lru)\n                del self.cache[lru.key]\n            node = ListNode(key, value)\n            self.cache[key] = node\n            self._add_to_head(node)",
                "time_complexity": "O(1)",
                "space_complexity": "O(capacity)",
                "explanation": "使用哈希表存储键到节点的映射，双向链表维护访问顺序。最近访问的节点在链表头部，最久未访问的在尾部。"
            }
        ],
        "time_complexity": "O(1)",
        "space_complexity": "O(capacity)"
    },
    {
        "title": "Maximum Subarray",
        "slug": "maximum-subarray",
        "description": """给你一个整数数组 nums ，请你找出一个具有最大和的连续子数组（子数组最少包含一个元素），返回其最大和。

子数组是数组中的一个连续部分。""",
        "difficulty": "medium",
        "examples": [
            {"input": "nums = [-2,1,-3,4,-1,2,1,-5,4]", "output": "6", "explanation": "连续子数组 [4,-1,2,1] 的和最大，为 6。"},
            {"input": "nums = [1]", "output": "1", "explanation": ""},
            {"input": "nums = [5,4,-1,7,8]", "output": "23", "explanation": ""}
        ],
        "constraints": ["1 <= nums.length <= 10^5", "-10^4 <= nums[i] <= 10^4"],
        "starter_code": {
            "python": "class Solution:\n    def maxSubArray(self, nums: list[int]) -> int:\n        pass",
            "javascript": "/**\n * @param {number[]} nums\n * @return {number}\n */\nvar maxSubArray = function(nums) {\n    \n};"
        },
        "test_cases": [
            {"input": "[-2,1,-3,4,-1,2,1,-5,4]", "expected_output": "6"},
            {"input": "[1]", "expected_output": "1"},
            {"input": "[5,4,-1,7,8]", "expected_output": "23"}
        ],
        "hidden_test_cases": [
            {"input": "[-1]", "expected_output": "-1"},
            {"input": "[-2,-1]", "expected_output": "-1"}
        ],
        "topics": ["array", "dp", "divide_conquer"],
        "companies": ["google", "amazon", "microsoft"],
        "patterns": ["kadane", "dp"],
        "hints": [
            "考虑动态规划：dp[i]表示以nums[i]结尾的最大子数组和",
            "状态转移：dp[i] = max(dp[i-1] + nums[i], nums[i])",
            "可以优化空间复杂度到O(1)"
        ],
        "solutions": [
            {
                "approach": "Kadane算法",
                "code": "class Solution:\n    def maxSubArray(self, nums):\n        max_sum = current_sum = nums[0]\n        for num in nums[1:]:\n            current_sum = max(num, current_sum + num)\n            max_sum = max(max_sum, current_sum)\n        return max_sum",
                "time_complexity": "O(n)",
                "space_complexity": "O(1)",
                "explanation": "维护当前子数组和和最大子数组和。如果当前和变为负数，则重新开始计数。"
            }
        ],
        "time_complexity": "O(n)",
        "space_complexity": "O(1)"
    },
    {
        "title": "Binary Tree Level Order Traversal",
        "slug": "binary-tree-level-order-traversal",
        "description": """给你二叉树的根节点 root ，返回其节点值的层序遍历。（即逐层地，从左到右访问所有节点）。""",
        "difficulty": "medium",
        "examples": [
            {"input": "root = [3,9,20,null,null,15,7]", "output": "[[3],[9,20],[15,7]]", "explanation": ""},
            {"input": "root = [1]", "output": "[[1]]", "explanation": ""},
            {"input": "root = []", "output": "[]", "explanation": ""}
        ],
        "constraints": ["树中节点数目在范围 [0, 2000] 内", "-1000 <= Node.val <= 1000"],
        "starter_code": {
            "python": "# Definition for a binary tree node.\n# class TreeNode:\n#     def __init__(self, val=0, left=None, right=None):\n#         self.val = val\n#         self.left = left\n#         self.right = right\n\nclass Solution:\n    def levelOrder(self, root) -> list[list[int]]:\n        pass",
            "javascript": "/**\n * Definition for a binary tree node.\n * function TreeNode(val, left, right) {\n *     this.val = (val===undefined ? 0 : val)\n *     this.left = (left===undefined ? null : left)\n *     this.right = (right===undefined ? null : right)\n * }\n */\n/**\n * @param {TreeNode} root\n * @return {number[][]}\n */\nvar levelOrder = function(root) {\n    \n};"
        },
        "test_cases": [
            {"input": "[3,9,20,null,null,15,7]", "expected_output": "[[3], [9, 20], [15, 7]]"}
        ],
        "hidden_test_cases": [],
        "topics": ["tree", "bfs", "binary_tree"],
        "companies": ["google", "amazon", "meta"],
        "patterns": ["bfs", "level_order"],
        "hints": [
            "使用BFS（广度优先搜索）",
            "使用队列存储每一层的节点",
            "每次处理一层的所有节点"
        ],
        "solutions": [
            {
                "approach": "BFS",
                "code": "from collections import deque\n\nclass Solution:\n    def levelOrder(self, root):\n        if not root:\n            return []\n        \n        result = []\n        queue = deque([root])\n        \n        while queue:\n            level_size = len(queue)\n            level = []\n            \n            for _ in range(level_size):\n                node = queue.popleft()\n                level.append(node.val)\n                \n                if node.left:\n                    queue.append(node.left)\n                if node.right:\n                    queue.append(node.right)\n            \n            result.append(level)\n        \n        return result",
                "time_complexity": "O(n)",
                "space_complexity": "O(n)",
                "explanation": "使用队列进行BFS，每次处理一层的所有节点"
            }
        ],
        "time_complexity": "O(n)",
        "space_complexity": "O(n)"
    }
]


def seed_problems():
    """Seed the database with sample problems"""
    init_db()
    db = SessionLocal()
    
    try:
        for problem_data in SAMPLE_PROBLEMS:
            # Check if problem already exists
            existing = db.query(Problem).filter(Problem.slug == problem_data["slug"]).first()
            if existing:
                print(f"Problem '{problem_data['title']}' already exists, skipping...")
                continue
            
            problem = Problem(**problem_data)
            db.add(problem)
            print(f"Added problem: {problem_data['title']}")
        
        db.commit()
        print("\nDatabase seeded successfully!")
        
    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    seed_problems()


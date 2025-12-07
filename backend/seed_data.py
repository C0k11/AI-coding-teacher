"""
Seed database with sample problems
"""

from app.models.database import init_db, SessionLocal, Problem

SAMPLE_PROBLEMS = [
    # ============== EASY - Fundamentals ==============
    {
        "title": "Hello World",
        "slug": "hello-world",
        "description": """Write a function that returns the string "Hello, World!".""",
        "difficulty": "easy",
        "examples": [
            {"input": "(no input)", "output": "Hello, World!", "explanation": "Simply return the greeting string."}
        ],
        "constraints": ["Return exactly 'Hello, World!' with correct capitalization and punctuation."],
        "starter_code": {
            "python": "class Solution:\n    def helloWorld(self) -> str:\n        pass",
            "javascript": "var helloWorld = function() {\n    \n};"
        },
        "test_cases": [
            {"input": "", "expected_output": "Hello, World!"}
        ],
        "hidden_test_cases": [],
        "topics": ["string", "basics"],
        "companies": [],
        "patterns": ["basics"],
        "hints": ["Just return a string literal."],
        "solutions": [
            {
                "approach": "Direct Return",
                "code": "class Solution:\n    def helloWorld(self) -> str:\n        return 'Hello, World!'",
                "time_complexity": "O(1)",
                "space_complexity": "O(1)",
                "explanation": "Simply return the string literal."
            }
        ],
        "time_complexity": "O(1)",
        "space_complexity": "O(1)"
    },
    {
        "title": "Add Two Numbers",
        "slug": "add-two-integers",
        "description": """Given two integers num1 and num2, return their sum.""",
        "difficulty": "easy",
        "examples": [
            {"input": "num1 = 12, num2 = 5", "output": "17", "explanation": "12 + 5 = 17"},
            {"input": "num1 = -10, num2 = 4", "output": "-6", "explanation": "-10 + 4 = -6"}
        ],
        "constraints": ["-100 <= num1, num2 <= 100"],
        "starter_code": {
            "python": "class Solution:\n    def sum(self, num1: int, num2: int) -> int:\n        pass",
            "javascript": "var sum = function(num1, num2) {\n    \n};"
        },
        "test_cases": [
            {"input": "12\n5", "expected_output": "17"},
            {"input": "-10\n4", "expected_output": "-6"}
        ],
        "hidden_test_cases": [
            {"input": "0\n0", "expected_output": "0"}
        ],
        "topics": ["math", "basics"],
        "companies": [],
        "patterns": ["basics"],
        "hints": ["Use the + operator."],
        "solutions": [
            {
                "approach": "Addition",
                "code": "class Solution:\n    def sum(self, num1: int, num2: int) -> int:\n        return num1 + num2",
                "time_complexity": "O(1)",
                "space_complexity": "O(1)",
                "explanation": "Use the addition operator to add the two numbers."
            }
        ],
        "time_complexity": "O(1)",
        "space_complexity": "O(1)"
    },
    {
        "title": "Find Maximum",
        "slug": "find-maximum",
        "description": """Given an array of integers nums, return the maximum value in the array.""",
        "difficulty": "easy",
        "examples": [
            {"input": "nums = [3, 1, 4, 1, 5, 9]", "output": "9", "explanation": "9 is the largest number."},
            {"input": "nums = [-5, -2, -10]", "output": "-2", "explanation": "-2 is the largest among negative numbers."}
        ],
        "constraints": ["1 <= nums.length <= 100", "-1000 <= nums[i] <= 1000"],
        "starter_code": {
            "python": "class Solution:\n    def findMax(self, nums: list[int]) -> int:\n        pass",
            "javascript": "var findMax = function(nums) {\n    \n};"
        },
        "test_cases": [
            {"input": "[3, 1, 4, 1, 5, 9]", "expected_output": "9"},
            {"input": "[-5, -2, -10]", "expected_output": "-2"}
        ],
        "hidden_test_cases": [
            {"input": "[42]", "expected_output": "42"}
        ],
        "topics": ["array", "basics"],
        "companies": [],
        "patterns": ["iteration"],
        "hints": [
            "You can use a built-in function like max().",
            "Or iterate through the array keeping track of the largest value seen."
        ],
        "solutions": [
            {
                "approach": "Built-in Function",
                "code": "class Solution:\n    def findMax(self, nums: list[int]) -> int:\n        return max(nums)",
                "time_complexity": "O(n)",
                "space_complexity": "O(1)",
                "explanation": "Use Python's built-in max() function."
            },
            {
                "approach": "Loop",
                "code": "class Solution:\n    def findMax(self, nums: list[int]) -> int:\n        result = nums[0]\n        for num in nums:\n            if num > result:\n                result = num\n        return result",
                "time_complexity": "O(n)",
                "space_complexity": "O(1)",
                "explanation": "Iterate through the array and keep track of the maximum."
            }
        ],
        "time_complexity": "O(n)",
        "space_complexity": "O(1)"
    },
    {
        "title": "Reverse String",
        "slug": "reverse-string",
        "description": """Given a string s, return the string reversed.""",
        "difficulty": "easy",
        "examples": [
            {"input": 's = "hello"', "output": '"olleh"', "explanation": "Reverse the characters."},
            {"input": 's = "Python"', "output": '"nohtyP"', "explanation": ""}
        ],
        "constraints": ["1 <= s.length <= 1000"],
        "starter_code": {
            "python": "class Solution:\n    def reverseString(self, s: str) -> str:\n        pass",
            "javascript": "var reverseString = function(s) {\n    \n};"
        },
        "test_cases": [
            {"input": "hello", "expected_output": "olleh"},
            {"input": "Python", "expected_output": "nohtyP"}
        ],
        "hidden_test_cases": [
            {"input": "a", "expected_output": "a"}
        ],
        "topics": ["string", "basics"],
        "companies": [],
        "patterns": ["basics"],
        "hints": [
            "Python has slicing: s[::-1]",
            "Or use a loop to build the reversed string."
        ],
        "solutions": [
            {
                "approach": "Slicing",
                "code": "class Solution:\n    def reverseString(self, s: str) -> str:\n        return s[::-1]",
                "time_complexity": "O(n)",
                "space_complexity": "O(n)",
                "explanation": "Use Python's slice notation with step -1 to reverse."
            }
        ],
        "time_complexity": "O(n)",
        "space_complexity": "O(n)"
    },
    {
        "title": "Count Even Numbers",
        "slug": "count-even-numbers",
        "description": """Given an array of integers nums, return the count of even numbers.""",
        "difficulty": "easy",
        "examples": [
            {"input": "nums = [1, 2, 3, 4, 5, 6]", "output": "3", "explanation": "2, 4, 6 are even."},
            {"input": "nums = [1, 3, 5]", "output": "0", "explanation": "No even numbers."}
        ],
        "constraints": ["1 <= nums.length <= 100", "-100 <= nums[i] <= 100"],
        "starter_code": {
            "python": "class Solution:\n    def countEvens(self, nums: list[int]) -> int:\n        pass",
            "javascript": "var countEvens = function(nums) {\n    \n};"
        },
        "test_cases": [
            {"input": "[1, 2, 3, 4, 5, 6]", "expected_output": "3"},
            {"input": "[1, 3, 5]", "expected_output": "0"}
        ],
        "hidden_test_cases": [
            {"input": "[0, 2, 4]", "expected_output": "3"}
        ],
        "topics": ["array", "basics"],
        "companies": [],
        "patterns": ["iteration"],
        "hints": [
            "A number is even if num % 2 == 0.",
            "Use a counter variable or list comprehension."
        ],
        "solutions": [
            {
                "approach": "Loop",
                "code": "class Solution:\n    def countEvens(self, nums: list[int]) -> int:\n        count = 0\n        for num in nums:\n            if num % 2 == 0:\n                count += 1\n        return count",
                "time_complexity": "O(n)",
                "space_complexity": "O(1)",
                "explanation": "Iterate through array and count numbers divisible by 2."
            },
            {
                "approach": "List Comprehension",
                "code": "class Solution:\n    def countEvens(self, nums: list[int]) -> int:\n        return sum(1 for num in nums if num % 2 == 0)",
                "time_complexity": "O(n)",
                "space_complexity": "O(1)",
                "explanation": "Use generator expression with sum."
            }
        ],
        "time_complexity": "O(n)",
        "space_complexity": "O(1)"
    },
    {
        "title": "FizzBuzz",
        "slug": "fizzbuzz",
        "description": """Given an integer n, return a list of strings where:
- "FizzBuzz" if i is divisible by 3 and 5
- "Fizz" if i is divisible by 3
- "Buzz" if i is divisible by 5
- The number as a string otherwise

for each i from 1 to n.""",
        "difficulty": "easy",
        "examples": [
            {"input": "n = 5", "output": '["1", "2", "Fizz", "4", "Buzz"]', "explanation": "3 is divisible by 3, 5 is divisible by 5."},
            {"input": "n = 15", "output": '["1", "2", "Fizz", "4", "Buzz", "Fizz", "7", "8", "Fizz", "Buzz", "11", "Fizz", "13", "14", "FizzBuzz"]', "explanation": "15 is divisible by both 3 and 5."}
        ],
        "constraints": ["1 <= n <= 100"],
        "starter_code": {
            "python": "class Solution:\n    def fizzBuzz(self, n: int) -> list[str]:\n        pass",
            "javascript": "var fizzBuzz = function(n) {\n    \n};"
        },
        "test_cases": [
            {"input": "5", "expected_output": "['1', '2', 'Fizz', '4', 'Buzz']"},
            {"input": "3", "expected_output": "['1', '2', 'Fizz']"}
        ],
        "hidden_test_cases": [],
        "topics": ["array", "string", "basics"],
        "companies": [],
        "patterns": ["iteration"],
        "hints": [
            "Check divisibility by 15 first (or both 3 and 5).",
            "Use the modulo operator %."
        ],
        "solutions": [
            {
                "approach": "Conditional Checks",
                "code": "class Solution:\n    def fizzBuzz(self, n: int) -> list[str]:\n        result = []\n        for i in range(1, n + 1):\n            if i % 15 == 0:\n                result.append('FizzBuzz')\n            elif i % 3 == 0:\n                result.append('Fizz')\n            elif i % 5 == 0:\n                result.append('Buzz')\n            else:\n                result.append(str(i))\n        return result",
                "time_complexity": "O(n)",
                "space_complexity": "O(n)",
                "explanation": "Check each number for divisibility and append appropriate string."
            }
        ],
        "time_complexity": "O(n)",
        "space_complexity": "O(n)"
    },
    
    # ============== MEDIUM - Algorithms ==============
    {
        "title": "Two Sum",
        "slug": "two-sum",
        "description": """Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.

You may assume that each input would have exactly one solution, and you may not use the same element twice.

You can return the answer in any order.""",
        "difficulty": "medium",
        "examples": [
            {"input": "nums = [2,7,11,15], target = 9", "output": "[0,1]", "explanation": "Because nums[0] + nums[1] == 9, we return [0, 1]."},
            {"input": "nums = [3,2,4], target = 6", "output": "[1,2]", "explanation": ""},
            {"input": "nums = [3,3], target = 6", "output": "[0,1]", "explanation": ""}
        ],
        "constraints": ["2 <= nums.length <= 10^4", "-10^9 <= nums[i] <= 10^9", "-10^9 <= target <= 10^9", "Only one valid answer exists."],
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
            "A brute force approach would iterate through each pair to check their sum.",
            "Consider using a hash table to optimize lookup time.",
            "While iterating, for each element check if target - nums[i] exists in the hash table."
        ],
        "solutions": [
            {
                "approach": "Brute Force",
                "code": "class Solution:\n    def twoSum(self, nums, target):\n        for i in range(len(nums)):\n            for j in range(i + 1, len(nums)):\n                if nums[i] + nums[j] == target:\n                    return [i, j]",
                "time_complexity": "O(n²)",
                "space_complexity": "O(1)",
                "explanation": "Use two nested loops to check all pairs of numbers."
            },
            {
                "approach": "Hash Table",
                "code": "class Solution:\n    def twoSum(self, nums, target):\n        seen = {}\n        for i, num in enumerate(nums):\n            complement = target - num\n            if complement in seen:\n                return [seen[complement], i]\n            seen[num] = i",
                "time_complexity": "O(n)",
                "space_complexity": "O(n)",
                "explanation": "Use a hash table to store visited numbers and their indices, finding the answer in a single pass."
            }
        ],
        "time_complexity": "O(n)",
        "space_complexity": "O(n)"
    },
    {
        "title": "Valid Parentheses",
        "slug": "valid-parentheses",
        "description": """Given a string s containing just the characters '(', ')', '{', '}', '[' and ']', determine if the input string is valid.

An input string is valid if:
1. Open brackets must be closed by the same type of brackets.
2. Open brackets must be closed in the correct order.
3. Every close bracket has a corresponding open bracket of the same type.""",
        "difficulty": "medium",
        "examples": [
            {"input": 's = "()"', "output": "true", "explanation": ""},
            {"input": 's = "()[]{}"', "output": "true", "explanation": ""},
            {"input": 's = "(]"', "output": "false", "explanation": ""}
        ],
        "constraints": ["1 <= s.length <= 10^4", "s consists of parentheses only '()[]{}'"],
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
            "Use a stack to keep track of opening brackets.",
            "When encountering a closing bracket, check if the top of the stack is the matching opening bracket."
        ],
        "solutions": [
            {
                "approach": "Stack",
                "code": "class Solution:\n    def isValid(self, s):\n        stack = []\n        mapping = {')': '(', '}': '{', ']': '['}\n        for char in s:\n            if char in mapping:\n                if not stack or stack.pop() != mapping[char]:\n                    return False\n            else:\n                stack.append(char)\n        return len(stack) == 0",
                "time_complexity": "O(n)",
                "space_complexity": "O(n)",
                "explanation": "Use a stack to store opening brackets, and check for matches when encountering closing brackets."
            }
        ],
        "time_complexity": "O(n)",
        "space_complexity": "O(n)"
    },
    {
        "title": "LRU Cache",
        "slug": "lru-cache",
        "description": """Design a data structure that follows the constraints of a Least Recently Used (LRU) cache.

Implement the LRUCache class:
- LRUCache(int capacity) Initialize the LRU cache with positive size capacity.
- int get(int key) Return the value of the key if the key exists, otherwise return -1.
- void put(int key, int value) Update the value of the key if the key exists. Otherwise, add the key-value pair to the cache. If the number of keys exceeds the capacity from this operation, evict the least recently used key.

The functions get and put must each run in O(1) average time complexity.""",
        "difficulty": "hard",
        "examples": [
            {
                "input": '["LRUCache", "put", "put", "get", "put", "get", "put", "get", "get", "get"]\n[[2], [1, 1], [2, 2], [1], [3, 3], [2], [4, 4], [1], [3], [4]]',
                "output": "[null, null, null, 1, null, -1, null, -1, 3, 4]",
                "explanation": "LRUCache lRUCache = new LRUCache(2);\nlRUCache.put(1, 1); // cache is {1=1}\nlRUCache.put(2, 2); // cache is {1=1, 2=2}\nlRUCache.get(1);    // return 1\nlRUCache.put(3, 3); // LRU key was 2, evicts key 2, cache is {1=1, 3=3}\nlRUCache.get(2);    // returns -1 (not found)\nlRUCache.put(4, 4); // LRU key was 1, evicts key 1, cache is {4=4, 3=3}\nlRUCache.get(1);    // return -1 (not found)\nlRUCache.get(3);    // return 3\nlRUCache.get(4);    // return 4"
            }
        ],
        "constraints": ["1 <= capacity <= 3000", "0 <= key <= 10^4", "0 <= value <= 10^5", "At most 2 * 10^5 calls will be made to get and put."],
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
            "You need to use both a hash table and a doubly linked list.",
            "Hash table for O(1) lookup, doubly linked list to maintain access order.",
            "After get and put operations, move the node to the head of the list."
        ],
        "solutions": [
            {
                "approach": "Hash Table + Doubly Linked List",
                "code": "class ListNode:\n    def __init__(self, key=0, val=0):\n        self.key = key\n        self.val = val\n        self.prev = None\n        self.next = None\n\nclass LRUCache:\n    def __init__(self, capacity):\n        self.capacity = capacity\n        self.cache = {}\n        self.head = ListNode()\n        self.tail = ListNode()\n        self.head.next = self.tail\n        self.tail.prev = self.head\n    \n    def _remove(self, node):\n        node.prev.next = node.next\n        node.next.prev = node.prev\n    \n    def _add_to_head(self, node):\n        node.next = self.head.next\n        node.prev = self.head\n        self.head.next.prev = node\n        self.head.next = node\n    \n    def get(self, key):\n        if key in self.cache:\n            node = self.cache[key]\n            self._remove(node)\n            self._add_to_head(node)\n            return node.val\n        return -1\n    \n    def put(self, key, value):\n        if key in self.cache:\n            node = self.cache[key]\n            node.val = value\n            self._remove(node)\n            self._add_to_head(node)\n        else:\n            if len(self.cache) >= self.capacity:\n                lru = self.tail.prev\n                self._remove(lru)\n                del self.cache[lru.key]\n            node = ListNode(key, value)\n            self.cache[key] = node\n            self._add_to_head(node)",
                "time_complexity": "O(1)",
                "space_complexity": "O(capacity)",
                "explanation": "Use a hash table to map keys to nodes, and a doubly linked list to maintain access order. Most recently accessed nodes are at the head, least recently used at the tail."
            }
        ],
        "time_complexity": "O(1)",
        "space_complexity": "O(capacity)"
    },
    {
        "title": "Maximum Subarray",
        "slug": "maximum-subarray",
        "description": """Given an integer array nums, find the subarray with the largest sum, and return its sum.

A subarray is a contiguous non-empty sequence of elements within an array.""",
        "difficulty": "medium",
        "examples": [
            {"input": "nums = [-2,1,-3,4,-1,2,1,-5,4]", "output": "6", "explanation": "The subarray [4,-1,2,1] has the largest sum 6."},
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
            "Consider dynamic programming: dp[i] represents the maximum subarray sum ending at nums[i].",
            "State transition: dp[i] = max(dp[i-1] + nums[i], nums[i])",
            "You can optimize space complexity to O(1)."
        ],
        "solutions": [
            {
                "approach": "Kadane's Algorithm",
                "code": "class Solution:\n    def maxSubArray(self, nums):\n        max_sum = current_sum = nums[0]\n        for num in nums[1:]:\n            current_sum = max(num, current_sum + num)\n            max_sum = max(max_sum, current_sum)\n        return max_sum",
                "time_complexity": "O(n)",
                "space_complexity": "O(1)",
                "explanation": "Maintain current subarray sum and maximum subarray sum. If current sum becomes negative, start a new subarray."
            }
        ],
        "time_complexity": "O(n)",
        "space_complexity": "O(1)"
    },
    {
        "title": "Binary Tree Level Order Traversal",
        "slug": "binary-tree-level-order-traversal",
        "description": """Given the root of a binary tree, return the level order traversal of its nodes' values. (i.e., from left to right, level by level).""",
        "difficulty": "medium",
        "examples": [
            {"input": "root = [3,9,20,null,null,15,7]", "output": "[[3],[9,20],[15,7]]", "explanation": ""},
            {"input": "root = [1]", "output": "[[1]]", "explanation": ""},
            {"input": "root = []", "output": "[]", "explanation": ""}
        ],
        "constraints": ["The number of nodes in the tree is in the range [0, 2000].", "-1000 <= Node.val <= 1000"],
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
            "Use BFS (Breadth-First Search).",
            "Use a queue to store nodes at each level.",
            "Process all nodes at one level before moving to the next."
        ],
        "solutions": [
            {
                "approach": "BFS",
                "code": "from collections import deque\n\nclass Solution:\n    def levelOrder(self, root):\n        if not root:\n            return []\n        \n        result = []\n        queue = deque([root])\n        \n        while queue:\n            level_size = len(queue)\n            level = []\n            \n            for _ in range(level_size):\n                node = queue.popleft()\n                level.append(node.val)\n                \n                if node.left:\n                    queue.append(node.left)\n                if node.right:\n                    queue.append(node.right)\n            \n            result.append(level)\n        \n        return result",
                "time_complexity": "O(n)",
                "space_complexity": "O(n)",
                "explanation": "Use a queue for BFS, processing all nodes at each level before moving to the next."
            }
        ],
        "time_complexity": "O(n)",
        "space_complexity": "O(n)"
    },
    
    # ============== Additional EASY Problems ==============
    {
        "title": "Palindrome Check",
        "slug": "palindrome-check",
        "description": """Given a string s, return true if it is a palindrome, false otherwise.

A palindrome is a string that reads the same forward and backward. Ignore case and non-alphanumeric characters.""",
        "difficulty": "easy",
        "examples": [
            {"input": 's = "A man, a plan, a canal: Panama"', "output": "true", "explanation": "After removing non-alphanumeric and ignoring case: 'amanaplanacanalpanama' is a palindrome."},
            {"input": 's = "race a car"', "output": "false", "explanation": "'raceacar' is not a palindrome."}
        ],
        "constraints": ["1 <= s.length <= 2 * 10^5", "s consists only of printable ASCII characters."],
        "starter_code": {
            "python": "class Solution:\n    def isPalindrome(self, s: str) -> bool:\n        pass",
            "javascript": "var isPalindrome = function(s) {\n    \n};"
        },
        "test_cases": [
            {"input": "A man, a plan, a canal: Panama", "expected_output": "True"},
            {"input": "race a car", "expected_output": "False"}
        ],
        "hidden_test_cases": [
            {"input": " ", "expected_output": "True"}
        ],
        "topics": ["string", "two_pointers"],
        "companies": ["meta", "microsoft"],
        "patterns": ["two_pointers"],
        "hints": [
            "Filter out non-alphanumeric characters first.",
            "Compare the string with its reverse.",
            "Or use two pointers from both ends."
        ],
        "solutions": [
            {
                "approach": "Two Pointers",
                "code": "class Solution:\n    def isPalindrome(self, s: str) -> bool:\n        cleaned = ''.join(c.lower() for c in s if c.isalnum())\n        return cleaned == cleaned[::-1]",
                "time_complexity": "O(n)",
                "space_complexity": "O(n)",
                "explanation": "Clean the string and compare with its reverse."
            }
        ],
        "time_complexity": "O(n)",
        "space_complexity": "O(n)"
    },
    {
        "title": "Contains Duplicate",
        "slug": "contains-duplicate",
        "description": """Given an integer array nums, return true if any value appears at least twice in the array, and return false if every element is distinct.""",
        "difficulty": "easy",
        "examples": [
            {"input": "nums = [1,2,3,1]", "output": "true", "explanation": "1 appears twice."},
            {"input": "nums = [1,2,3,4]", "output": "false", "explanation": "All elements are distinct."},
            {"input": "nums = [1,1,1,3,3,4,3,2,4,2]", "output": "true", "explanation": ""}
        ],
        "constraints": ["1 <= nums.length <= 10^5", "-10^9 <= nums[i] <= 10^9"],
        "starter_code": {
            "python": "class Solution:\n    def containsDuplicate(self, nums: list[int]) -> bool:\n        pass",
            "javascript": "var containsDuplicate = function(nums) {\n    \n};"
        },
        "test_cases": [
            {"input": "[1,2,3,1]", "expected_output": "True"},
            {"input": "[1,2,3,4]", "expected_output": "False"}
        ],
        "hidden_test_cases": [
            {"input": "[1]", "expected_output": "False"}
        ],
        "topics": ["array", "hash_table", "sorting"],
        "companies": ["amazon", "google"],
        "patterns": ["hash_set"],
        "hints": [
            "Use a hash set to track seen numbers.",
            "Or sort the array and check adjacent elements."
        ],
        "solutions": [
            {
                "approach": "Hash Set",
                "code": "class Solution:\n    def containsDuplicate(self, nums: list[int]) -> bool:\n        return len(nums) != len(set(nums))",
                "time_complexity": "O(n)",
                "space_complexity": "O(n)",
                "explanation": "Convert to set and compare lengths."
            }
        ],
        "time_complexity": "O(n)",
        "space_complexity": "O(n)"
    },
    {
        "title": "Single Number",
        "slug": "single-number",
        "description": """Given a non-empty array of integers nums, every element appears twice except for one. Find that single one.

You must implement a solution with O(n) runtime complexity and O(1) space complexity.""",
        "difficulty": "easy",
        "examples": [
            {"input": "nums = [2,2,1]", "output": "1", "explanation": ""},
            {"input": "nums = [4,1,2,1,2]", "output": "4", "explanation": ""},
            {"input": "nums = [1]", "output": "1", "explanation": ""}
        ],
        "constraints": ["1 <= nums.length <= 3 * 10^4", "-3 * 10^4 <= nums[i] <= 3 * 10^4", "Each element appears twice except for one."],
        "starter_code": {
            "python": "class Solution:\n    def singleNumber(self, nums: list[int]) -> int:\n        pass",
            "javascript": "var singleNumber = function(nums) {\n    \n};"
        },
        "test_cases": [
            {"input": "[2,2,1]", "expected_output": "1"},
            {"input": "[4,1,2,1,2]", "expected_output": "4"}
        ],
        "hidden_test_cases": [],
        "topics": ["array", "bit_manipulation"],
        "companies": ["amazon", "google", "meta"],
        "patterns": ["xor"],
        "hints": [
            "XOR of a number with itself is 0.",
            "XOR of a number with 0 is the number itself.",
            "XOR all numbers together."
        ],
        "solutions": [
            {
                "approach": "XOR",
                "code": "class Solution:\n    def singleNumber(self, nums: list[int]) -> int:\n        result = 0\n        for num in nums:\n            result ^= num\n        return result",
                "time_complexity": "O(n)",
                "space_complexity": "O(1)",
                "explanation": "XOR all numbers. Pairs cancel out, leaving the single number."
            }
        ],
        "time_complexity": "O(n)",
        "space_complexity": "O(1)"
    },
    {
        "title": "Merge Two Sorted Lists",
        "slug": "merge-two-sorted-lists",
        "description": """You are given the heads of two sorted linked lists list1 and list2.

Merge the two lists into one sorted list. The list should be made by splicing together the nodes of the first two lists.

Return the head of the merged linked list.""",
        "difficulty": "easy",
        "examples": [
            {"input": "list1 = [1,2,4], list2 = [1,3,4]", "output": "[1,1,2,3,4,4]", "explanation": ""},
            {"input": "list1 = [], list2 = []", "output": "[]", "explanation": ""},
            {"input": "list1 = [], list2 = [0]", "output": "[0]", "explanation": ""}
        ],
        "constraints": ["The number of nodes in both lists is in the range [0, 50].", "-100 <= Node.val <= 100", "Both lists are sorted in non-decreasing order."],
        "starter_code": {
            "python": "# Definition for singly-linked list.\n# class ListNode:\n#     def __init__(self, val=0, next=None):\n#         self.val = val\n#         self.next = next\n\nclass Solution:\n    def mergeTwoLists(self, list1, list2):\n        pass",
            "javascript": "/**\n * Definition for singly-linked list.\n * function ListNode(val, next) {\n *     this.val = (val===undefined ? 0 : val)\n *     this.next = (next===undefined ? null : next)\n * }\n */\nvar mergeTwoLists = function(list1, list2) {\n    \n};"
        },
        "test_cases": [
            {"input": "[1,2,4]\n[1,3,4]", "expected_output": "[1, 1, 2, 3, 4, 4]"}
        ],
        "hidden_test_cases": [],
        "topics": ["linked_list", "recursion"],
        "companies": ["amazon", "microsoft", "meta"],
        "patterns": ["two_pointers", "recursion"],
        "hints": [
            "Use a dummy head node to simplify the code.",
            "Compare the heads of both lists and add the smaller one.",
            "Move the pointer forward in the list from which you took the node."
        ],
        "solutions": [
            {
                "approach": "Iterative",
                "code": "class Solution:\n    def mergeTwoLists(self, list1, list2):\n        dummy = ListNode()\n        current = dummy\n        while list1 and list2:\n            if list1.val <= list2.val:\n                current.next = list1\n                list1 = list1.next\n            else:\n                current.next = list2\n                list2 = list2.next\n            current = current.next\n        current.next = list1 or list2\n        return dummy.next",
                "time_complexity": "O(n + m)",
                "space_complexity": "O(1)",
                "explanation": "Use a dummy node and iterate through both lists."
            }
        ],
        "time_complexity": "O(n + m)",
        "space_complexity": "O(1)"
    },
    {
        "title": "Best Time to Buy and Sell Stock",
        "slug": "best-time-to-buy-sell-stock",
        "description": """You are given an array prices where prices[i] is the price of a given stock on the ith day.

You want to maximize your profit by choosing a single day to buy one stock and choosing a different day in the future to sell that stock.

Return the maximum profit you can achieve from this transaction. If you cannot achieve any profit, return 0.""",
        "difficulty": "easy",
        "examples": [
            {"input": "prices = [7,1,5,3,6,4]", "output": "5", "explanation": "Buy on day 2 (price = 1) and sell on day 5 (price = 6), profit = 6-1 = 5."},
            {"input": "prices = [7,6,4,3,1]", "output": "0", "explanation": "No profit possible, prices keep decreasing."}
        ],
        "constraints": ["1 <= prices.length <= 10^5", "0 <= prices[i] <= 10^4"],
        "starter_code": {
            "python": "class Solution:\n    def maxProfit(self, prices: list[int]) -> int:\n        pass",
            "javascript": "var maxProfit = function(prices) {\n    \n};"
        },
        "test_cases": [
            {"input": "[7,1,5,3,6,4]", "expected_output": "5"},
            {"input": "[7,6,4,3,1]", "expected_output": "0"}
        ],
        "hidden_test_cases": [],
        "topics": ["array", "dp"],
        "companies": ["amazon", "google", "meta", "microsoft"],
        "patterns": ["kadane", "sliding_window"],
        "hints": [
            "Keep track of the minimum price seen so far.",
            "At each day, calculate the profit if you sell today.",
            "Update the maximum profit."
        ],
        "solutions": [
            {
                "approach": "One Pass",
                "code": "class Solution:\n    def maxProfit(self, prices: list[int]) -> int:\n        min_price = float('inf')\n        max_profit = 0\n        for price in prices:\n            min_price = min(min_price, price)\n            max_profit = max(max_profit, price - min_price)\n        return max_profit",
                "time_complexity": "O(n)",
                "space_complexity": "O(1)",
                "explanation": "Track minimum price and maximum profit in one pass."
            }
        ],
        "time_complexity": "O(n)",
        "space_complexity": "O(1)"
    },
    
    # ============== Additional MEDIUM Problems ==============
    {
        "title": "3Sum",
        "slug": "3sum",
        "description": """Given an integer array nums, return all the triplets [nums[i], nums[j], nums[k]] such that i != j, i != k, and j != k, and nums[i] + nums[j] + nums[k] == 0.

Notice that the solution set must not contain duplicate triplets.""",
        "difficulty": "medium",
        "examples": [
            {"input": "nums = [-1,0,1,2,-1,-4]", "output": "[[-1,-1,2],[-1,0,1]]", "explanation": "The distinct triplets are [-1,0,1] and [-1,-1,2]."},
            {"input": "nums = [0,1,1]", "output": "[]", "explanation": "No triplet sums to 0."},
            {"input": "nums = [0,0,0]", "output": "[[0,0,0]]", "explanation": ""}
        ],
        "constraints": ["3 <= nums.length <= 3000", "-10^5 <= nums[i] <= 10^5"],
        "starter_code": {
            "python": "class Solution:\n    def threeSum(self, nums: list[int]) -> list[list[int]]:\n        pass",
            "javascript": "var threeSum = function(nums) {\n    \n};"
        },
        "test_cases": [
            {"input": "[-1,0,1,2,-1,-4]", "expected_output": "[[-1, -1, 2], [-1, 0, 1]]"},
            {"input": "[0,0,0]", "expected_output": "[[0, 0, 0]]"}
        ],
        "hidden_test_cases": [],
        "topics": ["array", "two_pointers", "sorting"],
        "companies": ["amazon", "google", "meta", "microsoft"],
        "patterns": ["two_pointers"],
        "hints": [
            "Sort the array first.",
            "Fix one element and use two pointers for the remaining two.",
            "Skip duplicates to avoid duplicate triplets."
        ],
        "solutions": [
            {
                "approach": "Two Pointers",
                "code": "class Solution:\n    def threeSum(self, nums: list[int]) -> list[list[int]]:\n        nums.sort()\n        result = []\n        for i in range(len(nums) - 2):\n            if i > 0 and nums[i] == nums[i-1]:\n                continue\n            left, right = i + 1, len(nums) - 1\n            while left < right:\n                total = nums[i] + nums[left] + nums[right]\n                if total < 0:\n                    left += 1\n                elif total > 0:\n                    right -= 1\n                else:\n                    result.append([nums[i], nums[left], nums[right]])\n                    while left < right and nums[left] == nums[left+1]:\n                        left += 1\n                    while left < right and nums[right] == nums[right-1]:\n                        right -= 1\n                    left += 1\n                    right -= 1\n        return result",
                "time_complexity": "O(n^2)",
                "space_complexity": "O(1)",
                "explanation": "Sort and use two pointers for each fixed element."
            }
        ],
        "time_complexity": "O(n^2)",
        "space_complexity": "O(1)"
    },
    {
        "title": "Longest Substring Without Repeating Characters",
        "slug": "longest-substring-without-repeating",
        "description": """Given a string s, find the length of the longest substring without repeating characters.""",
        "difficulty": "medium",
        "examples": [
            {"input": 's = "abcabcbb"', "output": "3", "explanation": "The answer is 'abc', with the length of 3."},
            {"input": 's = "bbbbb"', "output": "1", "explanation": "The answer is 'b', with the length of 1."},
            {"input": 's = "pwwkew"', "output": "3", "explanation": "The answer is 'wke', with the length of 3."}
        ],
        "constraints": ["0 <= s.length <= 5 * 10^4", "s consists of English letters, digits, symbols and spaces."],
        "starter_code": {
            "python": "class Solution:\n    def lengthOfLongestSubstring(self, s: str) -> int:\n        pass",
            "javascript": "var lengthOfLongestSubstring = function(s) {\n    \n};"
        },
        "test_cases": [
            {"input": "abcabcbb", "expected_output": "3"},
            {"input": "bbbbb", "expected_output": "1"},
            {"input": "pwwkew", "expected_output": "3"}
        ],
        "hidden_test_cases": [
            {"input": "", "expected_output": "0"}
        ],
        "topics": ["string", "hash_table", "sliding_window"],
        "companies": ["amazon", "google", "meta", "microsoft"],
        "patterns": ["sliding_window"],
        "hints": [
            "Use a sliding window approach.",
            "Use a hash map to store the last index of each character.",
            "When you find a repeat, move the left pointer."
        ],
        "solutions": [
            {
                "approach": "Sliding Window",
                "code": "class Solution:\n    def lengthOfLongestSubstring(self, s: str) -> int:\n        char_index = {}\n        left = max_len = 0\n        for right, char in enumerate(s):\n            if char in char_index and char_index[char] >= left:\n                left = char_index[char] + 1\n            char_index[char] = right\n            max_len = max(max_len, right - left + 1)\n        return max_len",
                "time_complexity": "O(n)",
                "space_complexity": "O(min(m, n))",
                "explanation": "Sliding window with hash map to track character positions."
            }
        ],
        "time_complexity": "O(n)",
        "space_complexity": "O(min(m, n))"
    },
    {
        "title": "Product of Array Except Self",
        "slug": "product-of-array-except-self",
        "description": """Given an integer array nums, return an array answer such that answer[i] is equal to the product of all the elements of nums except nums[i].

The product of any prefix or suffix of nums is guaranteed to fit in a 32-bit integer.

You must write an algorithm that runs in O(n) time and without using the division operation.""",
        "difficulty": "medium",
        "examples": [
            {"input": "nums = [1,2,3,4]", "output": "[24,12,8,6]", "explanation": ""},
            {"input": "nums = [-1,1,0,-3,3]", "output": "[0,0,9,0,0]", "explanation": ""}
        ],
        "constraints": ["2 <= nums.length <= 10^5", "-30 <= nums[i] <= 30", "The product of any prefix or suffix fits in a 32-bit integer."],
        "starter_code": {
            "python": "class Solution:\n    def productExceptSelf(self, nums: list[int]) -> list[int]:\n        pass",
            "javascript": "var productExceptSelf = function(nums) {\n    \n};"
        },
        "test_cases": [
            {"input": "[1,2,3,4]", "expected_output": "[24, 12, 8, 6]"},
            {"input": "[-1,1,0,-3,3]", "expected_output": "[0, 0, 9, 0, 0]"}
        ],
        "hidden_test_cases": [],
        "topics": ["array", "prefix_sum"],
        "companies": ["amazon", "google", "meta"],
        "patterns": ["prefix_product"],
        "hints": [
            "Think about left and right products for each position.",
            "First pass: calculate prefix products.",
            "Second pass: multiply by suffix products."
        ],
        "solutions": [
            {
                "approach": "Prefix and Suffix",
                "code": "class Solution:\n    def productExceptSelf(self, nums: list[int]) -> list[int]:\n        n = len(nums)\n        result = [1] * n\n        prefix = 1\n        for i in range(n):\n            result[i] = prefix\n            prefix *= nums[i]\n        suffix = 1\n        for i in range(n - 1, -1, -1):\n            result[i] *= suffix\n            suffix *= nums[i]\n        return result",
                "time_complexity": "O(n)",
                "space_complexity": "O(1)",
                "explanation": "Calculate prefix products, then multiply by suffix products."
            }
        ],
        "time_complexity": "O(n)",
        "space_complexity": "O(1)"
    },
    {
        "title": "Container With Most Water",
        "slug": "container-with-most-water",
        "description": """You are given an integer array height of length n. There are n vertical lines drawn such that the two endpoints of the ith line are (i, 0) and (i, height[i]).

Find two lines that together with the x-axis form a container, such that the container contains the most water.

Return the maximum amount of water a container can store.""",
        "difficulty": "medium",
        "examples": [
            {"input": "height = [1,8,6,2,5,4,8,3,7]", "output": "49", "explanation": "The max area is between index 1 and 8."},
            {"input": "height = [1,1]", "output": "1", "explanation": ""}
        ],
        "constraints": ["n == height.length", "2 <= n <= 10^5", "0 <= height[i] <= 10^4"],
        "starter_code": {
            "python": "class Solution:\n    def maxArea(self, height: list[int]) -> int:\n        pass",
            "javascript": "var maxArea = function(height) {\n    \n};"
        },
        "test_cases": [
            {"input": "[1,8,6,2,5,4,8,3,7]", "expected_output": "49"},
            {"input": "[1,1]", "expected_output": "1"}
        ],
        "hidden_test_cases": [],
        "topics": ["array", "two_pointers", "greedy"],
        "companies": ["amazon", "google", "meta"],
        "patterns": ["two_pointers"],
        "hints": [
            "Use two pointers starting from both ends.",
            "Area = min(height[left], height[right]) * (right - left).",
            "Move the pointer with smaller height inward."
        ],
        "solutions": [
            {
                "approach": "Two Pointers",
                "code": "class Solution:\n    def maxArea(self, height: list[int]) -> int:\n        left, right = 0, len(height) - 1\n        max_area = 0\n        while left < right:\n            area = min(height[left], height[right]) * (right - left)\n            max_area = max(max_area, area)\n            if height[left] < height[right]:\n                left += 1\n            else:\n                right -= 1\n        return max_area",
                "time_complexity": "O(n)",
                "space_complexity": "O(1)",
                "explanation": "Two pointers from both ends, move the shorter one."
            }
        ],
        "time_complexity": "O(n)",
        "space_complexity": "O(1)"
    },
    {
        "title": "Group Anagrams",
        "slug": "group-anagrams",
        "description": """Given an array of strings strs, group the anagrams together. You can return the answer in any order.

An Anagram is a word or phrase formed by rearranging the letters of a different word or phrase, typically using all the original letters exactly once.""",
        "difficulty": "medium",
        "examples": [
            {"input": 'strs = ["eat","tea","tan","ate","nat","bat"]', "output": '[["bat"],["nat","tan"],["ate","eat","tea"]]', "explanation": ""},
            {"input": 'strs = [""]', "output": '[[""]]', "explanation": ""},
            {"input": 'strs = ["a"]', "output": '[["a"]]', "explanation": ""}
        ],
        "constraints": ["1 <= strs.length <= 10^4", "0 <= strs[i].length <= 100", "strs[i] consists of lowercase English letters."],
        "starter_code": {
            "python": "class Solution:\n    def groupAnagrams(self, strs: list[str]) -> list[list[str]]:\n        pass",
            "javascript": "var groupAnagrams = function(strs) {\n    \n};"
        },
        "test_cases": [
            {"input": '["eat","tea","tan","ate","nat","bat"]', "expected_output": '[["eat", "tea", "ate"], ["tan", "nat"], ["bat"]]'}
        ],
        "hidden_test_cases": [],
        "topics": ["array", "hash_table", "string", "sorting"],
        "companies": ["amazon", "google", "meta"],
        "patterns": ["hash_map"],
        "hints": [
            "Anagrams have the same sorted characters.",
            "Use sorted string as key in a hash map.",
            "Or use character count tuple as key."
        ],
        "solutions": [
            {
                "approach": "Sorted Key",
                "code": "from collections import defaultdict\n\nclass Solution:\n    def groupAnagrams(self, strs: list[str]) -> list[list[str]]:\n        groups = defaultdict(list)\n        for s in strs:\n            key = ''.join(sorted(s))\n            groups[key].append(s)\n        return list(groups.values())",
                "time_complexity": "O(n * k log k)",
                "space_complexity": "O(n * k)",
                "explanation": "Use sorted string as key to group anagrams."
            }
        ],
        "time_complexity": "O(n * k log k)",
        "space_complexity": "O(n * k)"
    },
    {
        "title": "Coin Change",
        "slug": "coin-change",
        "description": """You are given an integer array coins representing coins of different denominations and an integer amount representing a total amount of money.

Return the fewest number of coins that you need to make up that amount. If that amount of money cannot be made up by any combination of the coins, return -1.

You may assume that you have an infinite number of each kind of coin.""",
        "difficulty": "medium",
        "examples": [
            {"input": "coins = [1,2,5], amount = 11", "output": "3", "explanation": "11 = 5 + 5 + 1"},
            {"input": "coins = [2], amount = 3", "output": "-1", "explanation": "Cannot make 3 with only 2s."},
            {"input": "coins = [1], amount = 0", "output": "0", "explanation": ""}
        ],
        "constraints": ["1 <= coins.length <= 12", "1 <= coins[i] <= 2^31 - 1", "0 <= amount <= 10^4"],
        "starter_code": {
            "python": "class Solution:\n    def coinChange(self, coins: list[int], amount: int) -> int:\n        pass",
            "javascript": "var coinChange = function(coins, amount) {\n    \n};"
        },
        "test_cases": [
            {"input": "[1,2,5]\n11", "expected_output": "3"},
            {"input": "[2]\n3", "expected_output": "-1"}
        ],
        "hidden_test_cases": [],
        "topics": ["array", "dp", "bfs"],
        "companies": ["amazon", "google", "microsoft"],
        "patterns": ["dp", "bfs"],
        "hints": [
            "Use dynamic programming.",
            "dp[i] = minimum coins needed to make amount i.",
            "For each coin, update dp[i] = min(dp[i], dp[i-coin] + 1)."
        ],
        "solutions": [
            {
                "approach": "Dynamic Programming",
                "code": "class Solution:\n    def coinChange(self, coins: list[int], amount: int) -> int:\n        dp = [float('inf')] * (amount + 1)\n        dp[0] = 0\n        for i in range(1, amount + 1):\n            for coin in coins:\n                if coin <= i:\n                    dp[i] = min(dp[i], dp[i - coin] + 1)\n        return dp[amount] if dp[amount] != float('inf') else -1",
                "time_complexity": "O(amount * n)",
                "space_complexity": "O(amount)",
                "explanation": "Bottom-up DP to find minimum coins for each amount."
            }
        ],
        "time_complexity": "O(amount * n)",
        "space_complexity": "O(amount)"
    },
    {
        "title": "Number of Islands",
        "slug": "number-of-islands",
        "description": """Given an m x n 2D binary grid which represents a map of '1's (land) and '0's (water), return the number of islands.

An island is surrounded by water and is formed by connecting adjacent lands horizontally or vertically. You may assume all four edges of the grid are all surrounded by water.""",
        "difficulty": "medium",
        "examples": [
            {"input": 'grid = [\n  ["1","1","1","1","0"],\n  ["1","1","0","1","0"],\n  ["1","1","0","0","0"],\n  ["0","0","0","0","0"]\n]', "output": "1", "explanation": ""},
            {"input": 'grid = [\n  ["1","1","0","0","0"],\n  ["1","1","0","0","0"],\n  ["0","0","1","0","0"],\n  ["0","0","0","1","1"]\n]', "output": "3", "explanation": ""}
        ],
        "constraints": ["m == grid.length", "n == grid[i].length", "1 <= m, n <= 300", "grid[i][j] is '0' or '1'."],
        "starter_code": {
            "python": "class Solution:\n    def numIslands(self, grid: list[list[str]]) -> int:\n        pass",
            "javascript": "var numIslands = function(grid) {\n    \n};"
        },
        "test_cases": [
            {"input": '[["1","1","1","1","0"],["1","1","0","1","0"],["1","1","0","0","0"],["0","0","0","0","0"]]', "expected_output": "1"},
            {"input": '[["1","1","0","0","0"],["1","1","0","0","0"],["0","0","1","0","0"],["0","0","0","1","1"]]', "expected_output": "3"}
        ],
        "hidden_test_cases": [],
        "topics": ["array", "dfs", "bfs", "union_find", "matrix"],
        "companies": ["amazon", "google", "meta", "microsoft"],
        "patterns": ["dfs", "bfs", "flood_fill"],
        "hints": [
            "Use DFS or BFS to explore each island.",
            "Mark visited cells to avoid counting twice.",
            "Count how many times you start a new DFS/BFS."
        ],
        "solutions": [
            {
                "approach": "DFS",
                "code": "class Solution:\n    def numIslands(self, grid: list[list[str]]) -> int:\n        if not grid:\n            return 0\n        \n        rows, cols = len(grid), len(grid[0])\n        count = 0\n        \n        def dfs(r, c):\n            if r < 0 or r >= rows or c < 0 or c >= cols or grid[r][c] == '0':\n                return\n            grid[r][c] = '0'\n            dfs(r+1, c)\n            dfs(r-1, c)\n            dfs(r, c+1)\n            dfs(r, c-1)\n        \n        for r in range(rows):\n            for c in range(cols):\n                if grid[r][c] == '1':\n                    count += 1\n                    dfs(r, c)\n        \n        return count",
                "time_complexity": "O(m * n)",
                "space_complexity": "O(m * n)",
                "explanation": "DFS to flood fill each island and count."
            }
        ],
        "time_complexity": "O(m * n)",
        "space_complexity": "O(m * n)"
    },
    {
        "title": "Validate Binary Search Tree",
        "slug": "validate-binary-search-tree",
        "description": """Given the root of a binary tree, determine if it is a valid binary search tree (BST).

A valid BST is defined as follows:
- The left subtree of a node contains only nodes with keys less than the node's key.
- The right subtree of a node contains only nodes with keys greater than the node's key.
- Both the left and right subtrees must also be binary search trees.""",
        "difficulty": "medium",
        "examples": [
            {"input": "root = [2,1,3]", "output": "true", "explanation": ""},
            {"input": "root = [5,1,4,null,null,3,6]", "output": "false", "explanation": "The root's right child is 4, which is less than 5."}
        ],
        "constraints": ["The number of nodes is in the range [1, 10^4].", "-2^31 <= Node.val <= 2^31 - 1"],
        "starter_code": {
            "python": "# Definition for a binary tree node.\n# class TreeNode:\n#     def __init__(self, val=0, left=None, right=None):\n#         self.val = val\n#         self.left = left\n#         self.right = right\n\nclass Solution:\n    def isValidBST(self, root) -> bool:\n        pass",
            "javascript": "/**\n * Definition for a binary tree node.\n * function TreeNode(val, left, right) {\n *     this.val = (val===undefined ? 0 : val)\n *     this.left = (left===undefined ? null : left)\n *     this.right = (right===undefined ? null : right)\n * }\n */\nvar isValidBST = function(root) {\n    \n};"
        },
        "test_cases": [
            {"input": "[2,1,3]", "expected_output": "True"},
            {"input": "[5,1,4,null,null,3,6]", "expected_output": "False"}
        ],
        "hidden_test_cases": [],
        "topics": ["tree", "dfs", "binary_search_tree", "binary_tree"],
        "companies": ["amazon", "google", "meta"],
        "patterns": ["dfs", "inorder"],
        "hints": [
            "Keep track of valid range for each node.",
            "Left child must be in range (min, parent).",
            "Right child must be in range (parent, max)."
        ],
        "solutions": [
            {
                "approach": "Recursive with Bounds",
                "code": "class Solution:\n    def isValidBST(self, root) -> bool:\n        def validate(node, low, high):\n            if not node:\n                return True\n            if not (low < node.val < high):\n                return False\n            return validate(node.left, low, node.val) and validate(node.right, node.val, high)\n        \n        return validate(root, float('-inf'), float('inf'))",
                "time_complexity": "O(n)",
                "space_complexity": "O(n)",
                "explanation": "Recursively validate with updated bounds for each subtree."
            }
        ],
        "time_complexity": "O(n)",
        "space_complexity": "O(n)"
    },
    
    # ============== Additional HARD Problems ==============
    {
        "title": "Merge K Sorted Lists",
        "slug": "merge-k-sorted-lists",
        "description": """You are given an array of k linked-lists lists, each linked-list is sorted in ascending order.

Merge all the linked-lists into one sorted linked-list and return it.""",
        "difficulty": "hard",
        "examples": [
            {"input": "lists = [[1,4,5],[1,3,4],[2,6]]", "output": "[1,1,2,3,4,4,5,6]", "explanation": "Merge all lists into one sorted list."},
            {"input": "lists = []", "output": "[]", "explanation": ""},
            {"input": "lists = [[]]", "output": "[]", "explanation": ""}
        ],
        "constraints": ["k == lists.length", "0 <= k <= 10^4", "0 <= lists[i].length <= 500", "-10^4 <= lists[i][j] <= 10^4", "lists[i] is sorted in ascending order.", "The sum of lists[i].length will not exceed 10^4."],
        "starter_code": {
            "python": "# Definition for singly-linked list.\n# class ListNode:\n#     def __init__(self, val=0, next=None):\n#         self.val = val\n#         self.next = next\n\nclass Solution:\n    def mergeKLists(self, lists):\n        pass",
            "javascript": "/**\n * Definition for singly-linked list.\n * function ListNode(val, next) {\n *     this.val = (val===undefined ? 0 : val)\n *     this.next = (next===undefined ? null : next)\n * }\n */\nvar mergeKLists = function(lists) {\n    \n};"
        },
        "test_cases": [
            {"input": "[[1,4,5],[1,3,4],[2,6]]", "expected_output": "[1, 1, 2, 3, 4, 4, 5, 6]"}
        ],
        "hidden_test_cases": [],
        "topics": ["linked_list", "divide_conquer", "heap", "merge_sort"],
        "companies": ["amazon", "google", "meta", "microsoft"],
        "patterns": ["heap", "divide_conquer"],
        "hints": [
            "Use a min-heap to always get the smallest element.",
            "Or use divide and conquer to merge pairs of lists.",
            "Merge two lists at a time, reducing k lists to k/2."
        ],
        "solutions": [
            {
                "approach": "Min Heap",
                "code": "import heapq\n\nclass Solution:\n    def mergeKLists(self, lists):\n        heap = []\n        for i, lst in enumerate(lists):\n            if lst:\n                heapq.heappush(heap, (lst.val, i, lst))\n        \n        dummy = ListNode()\n        current = dummy\n        \n        while heap:\n            val, i, node = heapq.heappop(heap)\n            current.next = node\n            current = current.next\n            if node.next:\n                heapq.heappush(heap, (node.next.val, i, node.next))\n        \n        return dummy.next",
                "time_complexity": "O(n log k)",
                "space_complexity": "O(k)",
                "explanation": "Use min-heap to efficiently get the smallest element among k lists."
            }
        ],
        "time_complexity": "O(n log k)",
        "space_complexity": "O(k)"
    },
    {
        "title": "Trapping Rain Water",
        "slug": "trapping-rain-water",
        "description": """Given n non-negative integers representing an elevation map where the width of each bar is 1, compute how much water it can trap after raining.""",
        "difficulty": "hard",
        "examples": [
            {"input": "height = [0,1,0,2,1,0,1,3,2,1,2,1]", "output": "6", "explanation": "The elevation map can trap 6 units of rain water."},
            {"input": "height = [4,2,0,3,2,5]", "output": "9", "explanation": ""}
        ],
        "constraints": ["n == height.length", "1 <= n <= 2 * 10^4", "0 <= height[i] <= 10^5"],
        "starter_code": {
            "python": "class Solution:\n    def trap(self, height: list[int]) -> int:\n        pass",
            "javascript": "var trap = function(height) {\n    \n};"
        },
        "test_cases": [
            {"input": "[0,1,0,2,1,0,1,3,2,1,2,1]", "expected_output": "6"},
            {"input": "[4,2,0,3,2,5]", "expected_output": "9"}
        ],
        "hidden_test_cases": [],
        "topics": ["array", "two_pointers", "dp", "stack", "monotonic_stack"],
        "companies": ["amazon", "google", "meta", "microsoft"],
        "patterns": ["two_pointers", "monotonic_stack"],
        "hints": [
            "Water at position i = min(max_left, max_right) - height[i].",
            "Use two pointers from both ends.",
            "Track max height from left and right."
        ],
        "solutions": [
            {
                "approach": "Two Pointers",
                "code": "class Solution:\n    def trap(self, height: list[int]) -> int:\n        if not height:\n            return 0\n        \n        left, right = 0, len(height) - 1\n        left_max, right_max = height[left], height[right]\n        water = 0\n        \n        while left < right:\n            if left_max < right_max:\n                left += 1\n                left_max = max(left_max, height[left])\n                water += left_max - height[left]\n            else:\n                right -= 1\n                right_max = max(right_max, height[right])\n                water += right_max - height[right]\n        \n        return water",
                "time_complexity": "O(n)",
                "space_complexity": "O(1)",
                "explanation": "Two pointers track max heights from both sides."
            }
        ],
        "time_complexity": "O(n)",
        "space_complexity": "O(1)"
    },
    {
        "title": "Word Search II",
        "slug": "word-search-ii",
        "description": """Given an m x n board of characters and a list of strings words, return all words on the board.

Each word must be constructed from letters of sequentially adjacent cells, where adjacent cells are horizontally or vertically neighboring. The same letter cell may not be used more than once in a word.""",
        "difficulty": "hard",
        "examples": [
            {"input": 'board = [["o","a","a","n"],["e","t","a","e"],["i","h","k","r"],["i","f","l","v"]], words = ["oath","pea","eat","rain"]', "output": '["eat","oath"]', "explanation": ""},
            {"input": 'board = [["a","b"],["c","d"]], words = ["abcb"]', "output": "[]", "explanation": ""}
        ],
        "constraints": ["m == board.length", "n == board[i].length", "1 <= m, n <= 12", "board[i][j] is a lowercase English letter.", "1 <= words.length <= 3 * 10^4", "1 <= words[i].length <= 10", "words[i] consists of lowercase English letters."],
        "starter_code": {
            "python": "class Solution:\n    def findWords(self, board: list[list[str]], words: list[str]) -> list[str]:\n        pass",
            "javascript": "var findWords = function(board, words) {\n    \n};"
        },
        "test_cases": [
            {"input": '[["o","a","a","n"],["e","t","a","e"],["i","h","k","r"],["i","f","l","v"]]\n["oath","pea","eat","rain"]', "expected_output": '["oath", "eat"]'}
        ],
        "hidden_test_cases": [],
        "topics": ["array", "string", "backtracking", "trie", "matrix"],
        "companies": ["amazon", "google", "meta", "microsoft"],
        "patterns": ["trie", "backtracking", "dfs"],
        "hints": [
            "Build a Trie from the words list.",
            "DFS from each cell, following the Trie.",
            "Prune branches when no words can be formed."
        ],
        "solutions": [
            {
                "approach": "Trie + Backtracking",
                "code": "class TrieNode:\n    def __init__(self):\n        self.children = {}\n        self.word = None\n\nclass Solution:\n    def findWords(self, board, words):\n        root = TrieNode()\n        for word in words:\n            node = root\n            for char in word:\n                if char not in node.children:\n                    node.children[char] = TrieNode()\n                node = node.children[char]\n            node.word = word\n        \n        rows, cols = len(board), len(board[0])\n        result = []\n        \n        def dfs(r, c, node):\n            char = board[r][c]\n            if char not in node.children:\n                return\n            \n            next_node = node.children[char]\n            if next_node.word:\n                result.append(next_node.word)\n                next_node.word = None\n            \n            board[r][c] = '#'\n            for dr, dc in [(0,1), (0,-1), (1,0), (-1,0)]:\n                nr, nc = r + dr, c + dc\n                if 0 <= nr < rows and 0 <= nc < cols and board[nr][nc] != '#':\n                    dfs(nr, nc, next_node)\n            board[r][c] = char\n        \n        for r in range(rows):\n            for c in range(cols):\n                dfs(r, c, root)\n        \n        return result",
                "time_complexity": "O(m * n * 4^L)",
                "space_complexity": "O(W * L)",
                "explanation": "Build Trie from words, then DFS with backtracking on the board."
            }
        ],
        "time_complexity": "O(m * n * 4^L)",
        "space_complexity": "O(W * L)"
    },
    {
        "title": "Median of Two Sorted Arrays",
        "slug": "median-of-two-sorted-arrays",
        "description": """Given two sorted arrays nums1 and nums2 of size m and n respectively, return the median of the two sorted arrays.

The overall run time complexity should be O(log (m+n)).""",
        "difficulty": "hard",
        "examples": [
            {"input": "nums1 = [1,3], nums2 = [2]", "output": "2.00000", "explanation": "merged array = [1,2,3] and median is 2."},
            {"input": "nums1 = [1,2], nums2 = [3,4]", "output": "2.50000", "explanation": "merged array = [1,2,3,4] and median is (2 + 3) / 2 = 2.5."}
        ],
        "constraints": ["nums1.length == m", "nums2.length == n", "0 <= m <= 1000", "0 <= n <= 1000", "1 <= m + n <= 2000", "-10^6 <= nums1[i], nums2[i] <= 10^6"],
        "starter_code": {
            "python": "class Solution:\n    def findMedianSortedArrays(self, nums1: list[int], nums2: list[int]) -> float:\n        pass",
            "javascript": "var findMedianSortedArrays = function(nums1, nums2) {\n    \n};"
        },
        "test_cases": [
            {"input": "[1,3]\n[2]", "expected_output": "2.0"},
            {"input": "[1,2]\n[3,4]", "expected_output": "2.5"}
        ],
        "hidden_test_cases": [],
        "topics": ["array", "binary_search", "divide_conquer"],
        "companies": ["amazon", "google", "meta", "microsoft"],
        "patterns": ["binary_search"],
        "hints": [
            "Binary search on the shorter array.",
            "Partition both arrays such that left parts have half of total elements.",
            "Check if partition is valid by comparing boundary elements."
        ],
        "solutions": [
            {
                "approach": "Binary Search",
                "code": "class Solution:\n    def findMedianSortedArrays(self, nums1, nums2):\n        if len(nums1) > len(nums2):\n            nums1, nums2 = nums2, nums1\n        \n        m, n = len(nums1), len(nums2)\n        left, right = 0, m\n        \n        while left <= right:\n            i = (left + right) // 2\n            j = (m + n + 1) // 2 - i\n            \n            left1 = float('-inf') if i == 0 else nums1[i-1]\n            right1 = float('inf') if i == m else nums1[i]\n            left2 = float('-inf') if j == 0 else nums2[j-1]\n            right2 = float('inf') if j == n else nums2[j]\n            \n            if left1 <= right2 and left2 <= right1:\n                if (m + n) % 2 == 0:\n                    return (max(left1, left2) + min(right1, right2)) / 2\n                else:\n                    return max(left1, left2)\n            elif left1 > right2:\n                right = i - 1\n            else:\n                left = i + 1\n        \n        return 0",
                "time_complexity": "O(log(min(m,n)))",
                "space_complexity": "O(1)",
                "explanation": "Binary search to find correct partition point."
            }
        ],
        "time_complexity": "O(log(min(m,n)))",
        "space_complexity": "O(1)"
    },
    {
        "title": "Longest Valid Parentheses",
        "slug": "longest-valid-parentheses",
        "description": """Given a string containing just the characters '(' and ')', return the length of the longest valid (well-formed) parentheses substring.""",
        "difficulty": "hard",
        "examples": [
            {"input": 's = "(()"', "output": "2", "explanation": "The longest valid parentheses substring is '()'."},
            {"input": 's = ")()())"', "output": "4", "explanation": "The longest valid parentheses substring is '()()'."},
            {"input": 's = ""', "output": "0", "explanation": ""}
        ],
        "constraints": ["0 <= s.length <= 3 * 10^4", "s[i] is '(' or ')'."],
        "starter_code": {
            "python": "class Solution:\n    def longestValidParentheses(self, s: str) -> int:\n        pass",
            "javascript": "var longestValidParentheses = function(s) {\n    \n};"
        },
        "test_cases": [
            {"input": "(()", "expected_output": "2"},
            {"input": ")()())", "expected_output": "4"}
        ],
        "hidden_test_cases": [
            {"input": "", "expected_output": "0"}
        ],
        "topics": ["string", "dp", "stack"],
        "companies": ["amazon", "google", "meta"],
        "patterns": ["stack", "dp"],
        "hints": [
            "Use a stack to track indices of unmatched parentheses.",
            "Push index of '(' onto stack.",
            "For ')', pop and calculate length if stack not empty."
        ],
        "solutions": [
            {
                "approach": "Stack",
                "code": "class Solution:\n    def longestValidParentheses(self, s: str) -> int:\n        stack = [-1]\n        max_len = 0\n        \n        for i, char in enumerate(s):\n            if char == '(':\n                stack.append(i)\n            else:\n                stack.pop()\n                if not stack:\n                    stack.append(i)\n                else:\n                    max_len = max(max_len, i - stack[-1])\n        \n        return max_len",
                "time_complexity": "O(n)",
                "space_complexity": "O(n)",
                "explanation": "Use stack to track unmatched indices and calculate valid lengths."
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


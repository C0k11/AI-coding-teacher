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


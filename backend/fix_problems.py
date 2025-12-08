"""Fix incomplete problem descriptions"""
from app.models.database import SessionLocal, Problem

db = SessionLocal()

updates = {
    'subtract-integers': {
        'description': 'Given two integers num1 and num2, return num1 minus num2.',
        'examples': [{'input': 'num1 = 10, num2 = 3', 'output': '7', 'explanation': '10 - 3 = 7'}],
        'constraints': ['-100 <= num1, num2 <= 100'],
        'starter_code': {'python': 'class Solution:\n    def subtract(self, num1: int, num2: int) -> int:\n        # Write your code here\n        pass', 'javascript': 'var subtract = function(num1, num2) {\n    // Write your code here\n};'},
        'test_cases': [{'input': '10\n3', 'expected_output': '7'}, {'input': '5\n10', 'expected_output': '-5'}],
        'hints': ['Use the - operator to subtract two numbers.'],
        'solutions': [{'approach': 'Direct Subtraction', 'code': 'class Solution:\n    def subtract(self, num1: int, num2: int) -> int:\n        return num1 - num2', 'time_complexity': 'O(1)', 'space_complexity': 'O(1)', 'explanation': 'Simply use the subtraction operator.'}],
    },
    'multiply-integers': {
        'description': 'Given two integers num1 and num2, return their product (num1 * num2).',
        'examples': [{'input': 'num1 = 6, num2 = 7', 'output': '42', 'explanation': '6 * 7 = 42'}],
        'constraints': ['-100 <= num1, num2 <= 100'],
        'starter_code': {'python': 'class Solution:\n    def multiply(self, num1: int, num2: int) -> int:\n        # Write your code here\n        pass', 'javascript': 'var multiply = function(num1, num2) {\n    // Write your code here\n};'},
        'test_cases': [{'input': '6\n7', 'expected_output': '42'}, {'input': '-3\n4', 'expected_output': '-12'}],
        'hints': ['Use the * operator to multiply two numbers.'],
        'solutions': [{'approach': 'Direct Multiplication', 'code': 'class Solution:\n    def multiply(self, num1: int, num2: int) -> int:\n        return num1 * num2', 'time_complexity': 'O(1)', 'space_complexity': 'O(1)', 'explanation': 'Simply use the multiplication operator.'}],
    },
    'check-even-odd': {
        'description': "Given an integer n, return 'Even' if n is divisible by 2, otherwise return 'Odd'.",
        'examples': [{'input': 'n = 4', 'output': 'Even', 'explanation': '4 / 2 = 2 with no remainder'}, {'input': 'n = 7', 'output': 'Odd', 'explanation': '7 / 2 = 3 with remainder 1'}],
        'constraints': ['-1000 <= n <= 1000'],
        'starter_code': {'python': 'class Solution:\n    def checkEvenOdd(self, n: int) -> str:\n        # Write your code here\n        pass', 'javascript': 'var checkEvenOdd = function(n) {\n    // Write your code here\n};'},
        'test_cases': [{'input': '4', 'expected_output': 'Even'}, {'input': '7', 'expected_output': 'Odd'}, {'input': '0', 'expected_output': 'Even'}],
        'hints': ['Use the modulo operator % to check if n % 2 equals 0.'],
        'solutions': [{'approach': 'Modulo Check', 'code': "class Solution:\n    def checkEvenOdd(self, n: int) -> str:\n        return 'Even' if n % 2 == 0 else 'Odd'", 'time_complexity': 'O(1)', 'space_complexity': 'O(1)', 'explanation': 'A number is even if it has no remainder when divided by 2.'}],
    },
    'absolute-value': {
        'description': 'Given an integer n, return its absolute value (the non-negative value of n).',
        'examples': [{'input': 'n = -5', 'output': '5', 'explanation': '|-5| = 5'}, {'input': 'n = 3', 'output': '3', 'explanation': '|3| = 3'}],
        'constraints': ['-1000 <= n <= 1000'],
        'starter_code': {'python': 'class Solution:\n    def absoluteValue(self, n: int) -> int:\n        # Write your code here\n        pass', 'javascript': 'var absoluteValue = function(n) {\n    // Write your code here\n};'},
        'test_cases': [{'input': '-5', 'expected_output': '5'}, {'input': '3', 'expected_output': '3'}, {'input': '0', 'expected_output': '0'}],
        'hints': ['Use the abs() function or check if n < 0 and return -n.'],
        'solutions': [{'approach': 'Built-in Function', 'code': 'class Solution:\n    def absoluteValue(self, n: int) -> int:\n        return abs(n)', 'time_complexity': 'O(1)', 'space_complexity': 'O(1)', 'explanation': 'Use the built-in abs() function.'}],
    },
    'max-of-two': {
        'description': 'Given two integers a and b, return the larger one.',
        'examples': [{'input': 'a = 5, b = 3', 'output': '5', 'explanation': '5 > 3'}, {'input': 'a = 2, b = 8', 'output': '8', 'explanation': '8 > 2'}],
        'constraints': ['-1000 <= a, b <= 1000'],
        'starter_code': {'python': 'class Solution:\n    def maxOfTwo(self, a: int, b: int) -> int:\n        # Write your code here\n        pass', 'javascript': 'var maxOfTwo = function(a, b) {\n    // Write your code here\n};'},
        'test_cases': [{'input': '5\n3', 'expected_output': '5'}, {'input': '2\n8', 'expected_output': '8'}, {'input': '5\n5', 'expected_output': '5'}],
        'hints': ['Use the max() function or compare with if-else.'],
        'solutions': [{'approach': 'Built-in Function', 'code': 'class Solution:\n    def maxOfTwo(self, a: int, b: int) -> int:\n        return max(a, b)', 'time_complexity': 'O(1)', 'space_complexity': 'O(1)', 'explanation': 'Use the built-in max() function.'}],
    },
    'min-of-two': {
        'description': 'Given two integers a and b, return the smaller one.',
        'examples': [{'input': 'a = 5, b = 3', 'output': '3', 'explanation': '3 < 5'}, {'input': 'a = 2, b = 8', 'output': '2', 'explanation': '2 < 8'}],
        'constraints': ['-1000 <= a, b <= 1000'],
        'starter_code': {'python': 'class Solution:\n    def minOfTwo(self, a: int, b: int) -> int:\n        # Write your code here\n        pass', 'javascript': 'var minOfTwo = function(a, b) {\n    // Write your code here\n};'},
        'test_cases': [{'input': '5\n3', 'expected_output': '3'}, {'input': '2\n8', 'expected_output': '2'}],
        'hints': ['Use the min() function or compare with if-else.'],
        'solutions': [{'approach': 'Built-in Function', 'code': 'class Solution:\n    def minOfTwo(self, a: int, b: int) -> int:\n        return min(a, b)', 'time_complexity': 'O(1)', 'space_complexity': 'O(1)', 'explanation': 'Use the built-in min() function.'}],
    },
    'square-number': {
        'description': 'Given an integer n, return n squared (n * n).',
        'examples': [{'input': 'n = 5', 'output': '25', 'explanation': '5 * 5 = 25'}, {'input': 'n = -3', 'output': '9', 'explanation': '-3 * -3 = 9'}],
        'constraints': ['-100 <= n <= 100'],
        'starter_code': {'python': 'class Solution:\n    def square(self, n: int) -> int:\n        # Write your code here\n        pass', 'javascript': 'var square = function(n) {\n    // Write your code here\n};'},
        'test_cases': [{'input': '5', 'expected_output': '25'}, {'input': '-3', 'expected_output': '9'}, {'input': '0', 'expected_output': '0'}],
        'hints': ['Multiply n by itself or use n ** 2.'],
        'solutions': [{'approach': 'Multiplication', 'code': 'class Solution:\n    def square(self, n: int) -> int:\n        return n * n', 'time_complexity': 'O(1)', 'space_complexity': 'O(1)', 'explanation': 'Multiply n by itself.'}],
    },
    'sum-of-array': {
        'description': 'Given an array of integers nums, return the sum of all elements.',
        'examples': [{'input': 'nums = [1, 2, 3, 4, 5]', 'output': '15', 'explanation': '1 + 2 + 3 + 4 + 5 = 15'}],
        'constraints': ['1 <= nums.length <= 100', '-1000 <= nums[i] <= 1000'],
        'starter_code': {'python': 'class Solution:\n    def sumArray(self, nums: list[int]) -> int:\n        # Write your code here\n        pass', 'javascript': 'var sumArray = function(nums) {\n    // Write your code here\n};'},
        'test_cases': [{'input': '[1, 2, 3, 4, 5]', 'expected_output': '15'}, {'input': '[10, -5, 3]', 'expected_output': '8'}],
        'hints': ['Use the sum() function or loop through the array adding each element.'],
        'solutions': [{'approach': 'Built-in Function', 'code': 'class Solution:\n    def sumArray(self, nums: list[int]) -> int:\n        return sum(nums)', 'time_complexity': 'O(n)', 'space_complexity': 'O(1)', 'explanation': 'Use the built-in sum() function.'}],
    },
    'average-of-array': {
        'description': 'Given an array of integers nums, return the average (mean) of all elements.',
        'examples': [{'input': 'nums = [1, 2, 3, 4, 5]', 'output': '3.0', 'explanation': '15 / 5 = 3.0'}],
        'constraints': ['1 <= nums.length <= 100'],
        'starter_code': {'python': 'class Solution:\n    def average(self, nums: list[int]) -> float:\n        # Write your code here\n        pass', 'javascript': 'var average = function(nums) {\n    // Write your code here\n};'},
        'test_cases': [{'input': '[1, 2, 3, 4, 5]', 'expected_output': '3.0'}, {'input': '[10, 20]', 'expected_output': '15.0'}],
        'hints': ['Calculate sum divided by the number of elements.'],
        'solutions': [{'approach': 'Sum/Length', 'code': 'class Solution:\n    def average(self, nums: list[int]) -> float:\n        return sum(nums) / len(nums)', 'time_complexity': 'O(n)', 'space_complexity': 'O(1)', 'explanation': 'Sum all elements and divide by count.'}],
    },
    'count-elements': {
        'description': 'Given an array nums, return the number of elements in the array.',
        'examples': [{'input': 'nums = [1, 2, 3, 4, 5]', 'output': '5', 'explanation': 'Array has 5 elements'}],
        'constraints': ['0 <= nums.length <= 100'],
        'starter_code': {'python': 'class Solution:\n    def countElements(self, nums: list[int]) -> int:\n        # Write your code here\n        pass', 'javascript': 'var countElements = function(nums) {\n    // Write your code here\n};'},
        'test_cases': [{'input': '[1, 2, 3, 4, 5]', 'expected_output': '5'}, {'input': '[]', 'expected_output': '0'}],
        'hints': ['Use the len() function.'],
        'solutions': [{'approach': 'Length Function', 'code': 'class Solution:\n    def countElements(self, nums: list[int]) -> int:\n        return len(nums)', 'time_complexity': 'O(1)', 'space_complexity': 'O(1)', 'explanation': 'Use built-in len() function.'}],
    },
    'first-element': {
        'description': 'Given a non-empty array nums, return the first element.',
        'examples': [{'input': 'nums = [5, 2, 8, 1]', 'output': '5', 'explanation': 'First element is at index 0'}],
        'constraints': ['1 <= nums.length <= 100'],
        'starter_code': {'python': 'class Solution:\n    def firstElement(self, nums: list[int]) -> int:\n        # Write your code here\n        pass', 'javascript': 'var firstElement = function(nums) {\n    // Write your code here\n};'},
        'test_cases': [{'input': '[5, 2, 8, 1]', 'expected_output': '5'}, {'input': '[42]', 'expected_output': '42'}],
        'hints': ['Access the element at index 0.'],
        'solutions': [{'approach': 'Index Access', 'code': 'class Solution:\n    def firstElement(self, nums: list[int]) -> int:\n        return nums[0]', 'time_complexity': 'O(1)', 'space_complexity': 'O(1)', 'explanation': 'Access first element using index 0.'}],
    },
    'last-element': {
        'description': 'Given a non-empty array nums, return the last element.',
        'examples': [{'input': 'nums = [5, 2, 8, 1]', 'output': '1', 'explanation': 'Last element is at index -1'}],
        'constraints': ['1 <= nums.length <= 100'],
        'starter_code': {'python': 'class Solution:\n    def lastElement(self, nums: list[int]) -> int:\n        # Write your code here\n        pass', 'javascript': 'var lastElement = function(nums) {\n    // Write your code here\n};'},
        'test_cases': [{'input': '[5, 2, 8, 1]', 'expected_output': '1'}, {'input': '[42]', 'expected_output': '42'}],
        'hints': ['Use index -1 to access the last element.'],
        'solutions': [{'approach': 'Index Access', 'code': 'class Solution:\n    def lastElement(self, nums: list[int]) -> int:\n        return nums[-1]', 'time_complexity': 'O(1)', 'space_complexity': 'O(1)', 'explanation': 'Access last element using index -1.'}],
    },
    'string-length': {
        'description': 'Given a string s, return its length (number of characters).',
        'examples': [{'input': 's = "hello"', 'output': '5', 'explanation': '5 characters'}],
        'constraints': ['0 <= s.length <= 1000'],
        'starter_code': {'python': 'class Solution:\n    def stringLength(self, s: str) -> int:\n        # Write your code here\n        pass', 'javascript': 'var stringLength = function(s) {\n    // Write your code here\n};'},
        'test_cases': [{'input': 'hello', 'expected_output': '5'}, {'input': '', 'expected_output': '0'}],
        'hints': ['Use the len() function.'],
        'solutions': [{'approach': 'Length Function', 'code': 'class Solution:\n    def stringLength(self, s: str) -> int:\n        return len(s)', 'time_complexity': 'O(1)', 'space_complexity': 'O(1)', 'explanation': 'Use built-in len() function.'}],
    },
    'to-uppercase': {
        'description': 'Given a string s, return the string converted to uppercase.',
        'examples': [{'input': 's = "hello"', 'output': 'HELLO', 'explanation': 'All letters uppercase'}],
        'constraints': ['0 <= s.length <= 1000'],
        'starter_code': {'python': 'class Solution:\n    def toUppercase(self, s: str) -> str:\n        # Write your code here\n        pass', 'javascript': 'var toUppercase = function(s) {\n    // Write your code here\n};'},
        'test_cases': [{'input': 'hello', 'expected_output': 'HELLO'}, {'input': 'World', 'expected_output': 'WORLD'}],
        'hints': ['Use the upper() method on strings.'],
        'solutions': [{'approach': 'String Method', 'code': 'class Solution:\n    def toUppercase(self, s: str) -> str:\n        return s.upper()', 'time_complexity': 'O(n)', 'space_complexity': 'O(n)', 'explanation': 'Use built-in upper() method.'}],
    },
    'to-lowercase': {
        'description': 'Given a string s, return the string converted to lowercase.',
        'examples': [{'input': 's = "HELLO"', 'output': 'hello', 'explanation': 'All letters lowercase'}],
        'constraints': ['0 <= s.length <= 1000'],
        'starter_code': {'python': 'class Solution:\n    def toLowercase(self, s: str) -> str:\n        # Write your code here\n        pass', 'javascript': 'var toLowercase = function(s) {\n    // Write your code here\n};'},
        'test_cases': [{'input': 'HELLO', 'expected_output': 'hello'}, {'input': 'World', 'expected_output': 'world'}],
        'hints': ['Use the lower() method on strings.'],
        'solutions': [{'approach': 'String Method', 'code': 'class Solution:\n    def toLowercase(self, s: str) -> str:\n        return s.lower()', 'time_complexity': 'O(n)', 'space_complexity': 'O(n)', 'explanation': 'Use built-in lower() method.'}],
    },
}

for slug, data in updates.items():
    prob = db.query(Problem).filter(Problem.slug == slug).first()
    if prob:
        for key, value in data.items():
            setattr(prob, key, value)
        print(f'Updated: {prob.title}')

db.commit()
db.close()
print('Done!')

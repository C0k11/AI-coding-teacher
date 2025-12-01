'use client'

import { useState, useEffect } from 'react'
import { useParams } from 'next/navigation'
import Link from 'next/link'
import { 
  Code2, 
  ChevronLeft, 
  Play, 
  Send, 
  CheckCircle, 
  XCircle,
  Terminal,
  FileText,
  MessageSquare
} from 'lucide-react'
import CodeEditor from '@/components/CodeEditor'
import ProblemDescription from '@/components/ProblemDescription'
import TestResults from '@/components/TestResults'
import { cn } from '@/lib/utils'
import { problems as problemsApi, execution, type Problem } from '@/lib/api'
import { useAuthStore } from '@/store/useStore'

// Sample problem for demo
const SAMPLE_PROBLEM: Problem = {
  id: 1,
  title: 'Two Sum',
  slug: 'two-sum',
  description: `给定一个整数数组 nums 和一个整数目标值 target，请你在该数组中找出和为目标值 target 的那两个整数，并返回它们的数组下标。

你可以假设每种输入只会对应一个答案。但是，数组中同一个元素在答案里不能重复出现。

你可以按任意顺序返回答案。`,
  difficulty: 'easy',
  examples: [
    { input: 'nums = [2,7,11,15], target = 9', output: '[0,1]', explanation: '因为 nums[0] + nums[1] == 9，返回 [0, 1]。' },
    { input: 'nums = [3,2,4], target = 6', output: '[1,2]' },
    { input: 'nums = [3,3], target = 6', output: '[0,1]' },
  ],
  constraints: [
    '2 <= nums.length <= 10^4',
    '-10^9 <= nums[i] <= 10^9',
    '-10^9 <= target <= 10^9',
    '只会存在一个有效答案',
  ],
  starter_code: {
    python: `class Solution:
    def twoSum(self, nums: list[int], target: int) -> list[int]:
        # 在这里写你的代码
        pass`,
    javascript: `/**
 * @param {number[]} nums
 * @param {number} target
 * @return {number[]}
 */
var twoSum = function(nums, target) {
    // 在这里写你的代码
};`,
    java: `class Solution {
    public int[] twoSum(int[] nums, int target) {
        // 在这里写你的代码
        return new int[]{};
    }
}`,
  },
  topics: ['array', 'hash_table'],
  companies: ['google', 'amazon', 'meta', 'microsoft'],
  patterns: ['two_pointers', 'hash_map'],
  hints: [
    '可以使用暴力法，遍历每对数字检查它们的和',
    '考虑使用哈希表来优化查找时间',
    '遍历数组时，对于每个元素，检查 target - nums[i] 是否在哈希表中',
  ],
  acceptance_rate: 48.2,
  submission_count: 15234,
}

type TabType = 'description' | 'output' | 'submissions'

export default function ProblemPage() {
  const params = useParams()
  const slug = params.slug as string
  const { token } = useAuthStore()

  const [problem, setProblem] = useState<Problem>(SAMPLE_PROBLEM)
  const [loading, setLoading] = useState(true)
  const [code, setCode] = useState('')
  const [language, setLanguage] = useState('python')
  const [activeTab, setActiveTab] = useState<TabType>('description')
  const [isRunning, setIsRunning] = useState(false)
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [testResults, setTestResults] = useState<any>(null)
  const [consoleOutput, setConsoleOutput] = useState('')

  // Fetch problem
  useEffect(() => {
    const fetchProblem = async () => {
      try {
        const data = await problemsApi.get(slug)
        setProblem(data)
        setCode(data.starter_code[language] || '')
      } catch (error) {
        console.error('Failed to fetch problem:', error)
        // Use sample problem for demo
        setCode(SAMPLE_PROBLEM.starter_code[language] || '')
      } finally {
        setLoading(false)
      }
    }

    fetchProblem()
  }, [slug])

  // Update code when language changes
  useEffect(() => {
    if (problem.starter_code[language]) {
      setCode(problem.starter_code[language])
    }
  }, [language, problem])

  const handleRun = async () => {
    setIsRunning(true)
    setActiveTab('output')
    setConsoleOutput('运行中...')

    try {
      const result = await execution.run(code, language, '')
      if (result.success) {
        setConsoleOutput(result.output || '(无输出)')
      } else {
        setConsoleOutput(`错误:\n${result.error}`)
      }
    } catch (error) {
      setConsoleOutput('执行失败，请检查代码')
    } finally {
      setIsRunning(false)
    }
  }

  const handleSubmit = async () => {
    setIsSubmitting(true)
    setActiveTab('output')

    try {
      // Run against test cases
      const testCases = problem.examples.map((ex) => ({
        input: ex.input.split(', ').map(s => s.split(' = ')[1]).join('\n'),
        expected_output: ex.output,
      }))

      const result = await execution.test(code, language, testCases)
      setTestResults(result)
    } catch (error) {
      console.error('Submit failed:', error)
      setTestResults({
        status: 'error',
        test_results: [],
        passed_count: 0,
        total_count: 0,
      })
    } finally {
      setIsSubmitting(false)
    }
  }

  const handleReset = () => {
    setCode(problem.starter_code[language] || '')
  }

  const handleGetHint = async (level: number): Promise<string[]> => {
    try {
      const data = await problemsApi.getHints(slug, level)
      return data.hints
    } catch (error) {
      return problem.hints.slice(0, level)
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-dark-900 flex items-center justify-center">
        <div className="animate-pulse text-dark-400">加载题目中...</div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-dark-900 flex flex-col">
      {/* Navigation */}
      <nav className="sticky top-0 z-50 bg-dark-900/80 backdrop-blur-xl border-b border-dark-700">
        <div className="px-4 py-3 flex items-center justify-between">
          <div className="flex items-center gap-4">
            <Link href="/problems" className="p-2 hover:bg-dark-700 rounded-lg transition">
              <ChevronLeft className="w-5 h-5" />
            </Link>
            <Link href="/" className="flex items-center gap-2">
              <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-purple-500 to-pink-500 flex items-center justify-center">
                <Code2 className="w-5 h-5 text-white" />
              </div>
            </Link>
            <div className="flex items-center gap-2">
              <span className="font-semibold">{problem.id}. {problem.title}</span>
            </div>
          </div>

          <div className="flex items-center gap-2">
            <button
              onClick={handleRun}
              disabled={isRunning}
              className={cn(
                'flex items-center gap-2 px-4 py-2 rounded-lg font-medium transition',
                isRunning
                  ? 'bg-dark-600 text-dark-400 cursor-not-allowed'
                  : 'bg-dark-700 text-white hover:bg-dark-600'
              )}
            >
              <Play className="w-4 h-4" />
              {isRunning ? '运行中...' : '运行'}
            </button>
            <button
              onClick={handleSubmit}
              disabled={isSubmitting}
              className={cn(
                'flex items-center gap-2 px-4 py-2 rounded-lg font-medium transition',
                isSubmitting
                  ? 'bg-green-900 text-green-400 cursor-not-allowed'
                  : 'bg-green-600 text-white hover:bg-green-500'
              )}
            >
              <Send className="w-4 h-4" />
              {isSubmitting ? '提交中...' : '提交'}
            </button>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <div className="flex-1 flex">
        {/* Left Panel - Problem Description */}
        <div className="w-1/2 border-r border-dark-700 overflow-hidden flex flex-col">
          {/* Tabs */}
          <div className="flex items-center border-b border-dark-700 bg-dark-800">
            <button
              onClick={() => setActiveTab('description')}
              className={cn(
                'flex items-center gap-2 px-4 py-3 border-b-2 transition',
                activeTab === 'description'
                  ? 'border-purple-500 text-white'
                  : 'border-transparent text-dark-400 hover:text-white'
              )}
            >
              <FileText className="w-4 h-4" />
              题目描述
            </button>
            <button
              onClick={() => setActiveTab('output')}
              className={cn(
                'flex items-center gap-2 px-4 py-3 border-b-2 transition',
                activeTab === 'output'
                  ? 'border-purple-500 text-white'
                  : 'border-transparent text-dark-400 hover:text-white'
              )}
            >
              <Terminal className="w-4 h-4" />
              输出
              {testResults && (
                testResults.status === 'accepted' 
                  ? <CheckCircle className="w-4 h-4 text-green-400" />
                  : <XCircle className="w-4 h-4 text-red-400" />
              )}
            </button>
            <button
              onClick={() => setActiveTab('submissions')}
              className={cn(
                'flex items-center gap-2 px-4 py-3 border-b-2 transition',
                activeTab === 'submissions'
                  ? 'border-purple-500 text-white'
                  : 'border-transparent text-dark-400 hover:text-white'
              )}
            >
              <MessageSquare className="w-4 h-4" />
              提交记录
            </button>
          </div>

          {/* Tab Content */}
          <div className="flex-1 overflow-hidden">
            {activeTab === 'description' && (
              <ProblemDescription 
                problem={problem} 
                onGetHint={handleGetHint}
              />
            )}
            {activeTab === 'output' && (
              <div className="h-full">
                {testResults ? (
                  <TestResults
                    status={testResults.status}
                    testResults={testResults.test_results}
                    passedCount={testResults.passed_count}
                    totalCount={testResults.total_count}
                  />
                ) : (
                  <div className="p-4">
                    <div className="font-mono text-sm bg-dark-800 rounded-lg p-4 whitespace-pre-wrap">
                      {consoleOutput || '点击"运行"执行代码'}
                    </div>
                  </div>
                )}
              </div>
            )}
            {activeTab === 'submissions' && (
              <div className="p-6 text-center text-dark-400">
                登录后查看提交记录
              </div>
            )}
          </div>
        </div>

        {/* Right Panel - Code Editor */}
        <div className="w-1/2 flex flex-col">
          <CodeEditor
            code={code}
            language={language}
            onChange={setCode}
            onReset={handleReset}
            onLanguageChange={setLanguage}
            height="calc(100vh - 120px)"
            showActions={false}
            languages={Object.keys(problem.starter_code)}
          />
        </div>
      </div>
    </div>
  )
}


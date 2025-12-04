'use client'

import { useState, useEffect } from 'react'
import { useParams, useRouter } from 'next/navigation'
import Link from 'next/link'
import { 
  ChevronLeft, 
  Play, 
  Send, 
  CheckCircle, 
  XCircle,
  Terminal,
  FileText,
  Trophy,
  ChevronRight
} from 'lucide-react'
import CodeEditor from '@/components/CodeEditor'
import ProblemDescription from '@/components/ProblemDescription'
import TestResults from '@/components/TestResults'
import { cn } from '@/lib/utils'
import { problems as problemsApi, execution, type Problem } from '@/lib/api'
import { useAuthStore } from '@/store/useStore'

const SAMPLE_PROBLEM: Problem = {
  id: 1,
  title: 'Two Sum',
  slug: 'two-sum',
  description: `Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.

You may assume that each input would have exactly one solution, and you may not use the same element twice.

You can return the answer in any order.`,
  difficulty: 'medium',
  examples: [
    { input: 'nums = [2,7,11,15], target = 9', output: '[0,1]', explanation: 'Because nums[0] + nums[1] == 9, we return [0, 1].' },
    { input: 'nums = [3,2,4], target = 6', output: '[1,2]' },
    { input: 'nums = [3,3], target = 6', output: '[0,1]' },
  ],
  constraints: [
    '2 <= nums.length <= 10^4',
    '-10^9 <= nums[i] <= 10^9',
    '-10^9 <= target <= 10^9',
    'Only one valid answer exists.',
  ],
  starter_code: {
    python: `class Solution:
    def twoSum(self, nums: list[int], target: int) -> list[int]:
        pass`,
    javascript: `var twoSum = function(nums, target) {
    
};`,
    java: `class Solution {
    public int[] twoSum(int[] nums, int target) {
        return new int[]{};
    }
}`,
  },
  test_cases: [
    { input: '[2,7,11,15]\n9', expected_output: '[0, 1]' },
    { input: '[3,2,4]\n6', expected_output: '[1, 2]' },
    { input: '[3,3]\n6', expected_output: '[0, 1]' },
  ],
  topics: ['array', 'hash_table'],
  companies: [],
  patterns: ['two_pointers', 'hash_map'],
  hints: [
    'A brute force approach would be to iterate through each pair of numbers and check if they sum to target.',
    'Can you use a hash table to optimize the lookup time?',
    'For each element, check if target - nums[i] exists in the hash table.',
  ],
  acceptance_rate: 48.2,
  submission_count: 0,
}

type TabType = 'description' | 'output' | 'submissions'

export default function ProblemPage() {
  const params = useParams()
  const router = useRouter()
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
  const [showSuccess, setShowSuccess] = useState(false)
  const [allProblems, setAllProblems] = useState<any[]>([])

  // Fetch all problems for navigation
  useEffect(() => {
    problemsApi.list().then(setAllProblems).catch(() => {})
  }, [])

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
    setTestResults(null)
    setConsoleOutput('Running...')

    try {
      // Use test_cases from problem data (first one only for Run)
      const testCases = problem.test_cases?.slice(0, 1) || []
      
      if (testCases.length === 0) {
        setConsoleOutput('No test cases available')
        return
      }

      const result = await execution.test(code, language, testCases)
      setTestResults(result)
    } catch (error: any) {
      setConsoleOutput(`Error: ${error.message || 'Execution failed'}`)
    } finally {
      setIsRunning(false)
    }
  }

  const handleSubmit = async () => {
    setIsSubmitting(true)
    setActiveTab('output')

    try {
      // Use all test_cases from problem data
      const testCases = problem.test_cases || []
      
      if (testCases.length === 0) {
        setTestResults({
          status: 'error',
          test_results: [],
          passed_count: 0,
          total_count: 0,
        })
        return
      }

      const result = await execution.test(code, language, testCases)
      setTestResults(result)
      
      // Show success modal if all tests passed
      if (result.status === 'accepted') {
        setShowSuccess(true)
      }
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

  // Get next problem
  const getNextProblem = () => {
    const currentIndex = allProblems.findIndex(p => p.slug === slug)
    if (currentIndex >= 0 && currentIndex < allProblems.length - 1) {
      return allProblems[currentIndex + 1]
    }
    return null
  }

  const handleNextProblem = () => {
    const next = getNextProblem()
    if (next) {
      setShowSuccess(false)
      setTestResults(null)
      router.push(`/problems/${next.slug}`)
    } else {
      router.push('/problems')
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
      <div className="min-h-screen bg-white flex items-center justify-center">
        <div className="text-slate-400">Loading...</div>
      </div>
    )
  }

  const nextProblem = getNextProblem()

  return (
    <div className="min-h-screen bg-white flex flex-col">
      {/* Success Modal */}
      {showSuccess && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50">
          <div className="bg-white rounded-xl p-8 max-w-md w-full mx-4 shadow-2xl">
            <div className="text-center mb-6">
              <div className="w-16 h-16 bg-emerald-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <Trophy className="w-8 h-8 text-emerald-600" />
              </div>
              <h2 className="text-2xl font-bold text-slate-900 mb-2">Congratulations!</h2>
              <p className="text-slate-500">You solved {problem.title} successfully!</p>
            </div>
            
            <div className="bg-emerald-50 rounded-lg p-4 mb-6">
              <div className="text-center">
                <div className="text-emerald-600 font-bold text-lg">All Tests Passed</div>
                <div className="text-emerald-500 text-sm">{testResults?.passed_count}/{testResults?.total_count} test cases</div>
              </div>
            </div>

            <div className="flex gap-3">
              <button
                onClick={() => setShowSuccess(false)}
                className="flex-1 px-4 py-3 bg-slate-100 text-slate-700 rounded-lg hover:bg-slate-200 transition font-medium"
              >
                Stay Here
              </button>
              <button
                onClick={handleNextProblem}
                className="flex-1 flex items-center justify-center gap-2 px-4 py-3 bg-emerald-600 text-white rounded-lg hover:bg-emerald-700 transition font-medium"
              >
                {nextProblem ? (
                  <>Next Problem <ChevronRight className="w-4 h-4" /></>
                ) : (
                  'Back to Problems'
                )}
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Navigation */}
      <nav className="sticky top-0 z-50 bg-white border-b border-slate-200">
        <div className="px-4 py-3 flex items-center justify-between">
          <div className="flex items-center gap-4">
            <Link href="/problems" className="p-2 hover:bg-slate-100 rounded-md transition text-slate-600">
              <ChevronLeft className="w-5 h-5" />
            </Link>
            <Link href="/" className="text-lg font-bold">
              <span className="text-slate-800">Cok</span>
              <span className="text-blue-500">11</span>
            </Link>
            <span className="text-slate-300">|</span>
            <span className="font-medium text-slate-900">{problem.id}. {problem.title}</span>
            <span className={cn(
              'px-2 py-0.5 rounded text-xs font-medium',
              problem.difficulty === 'easy' ? 'bg-emerald-100 text-emerald-700' :
              problem.difficulty === 'medium' ? 'bg-amber-100 text-amber-700' : 'bg-red-100 text-red-700'
            )}>
              {problem.difficulty.charAt(0).toUpperCase() + problem.difficulty.slice(1)}
            </span>
          </div>

          <div className="flex items-center gap-2">
            <button
              onClick={handleRun}
              disabled={isRunning}
              className={cn(
                'flex items-center gap-2 px-4 py-2 rounded-md font-medium transition text-sm',
                isRunning
                  ? 'bg-slate-100 text-slate-400 cursor-not-allowed'
                  : 'bg-slate-100 text-slate-700 hover:bg-slate-200'
              )}
            >
              <Play className="w-4 h-4" />
              {isRunning ? 'Running...' : 'Run'}
            </button>
            <button
              onClick={handleSubmit}
              disabled={isSubmitting}
              className={cn(
                'flex items-center gap-2 px-4 py-2 rounded-md font-medium transition text-sm',
                isSubmitting
                  ? 'bg-emerald-200 text-emerald-600 cursor-not-allowed'
                  : 'bg-emerald-600 text-white hover:bg-emerald-700'
              )}
            >
              <Send className="w-4 h-4" />
              {isSubmitting ? 'Submitting...' : 'Submit'}
            </button>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <div className="flex-1 flex">
        {/* Left Panel - Problem Description */}
        <div className="w-1/2 border-r border-slate-200 overflow-hidden flex flex-col">
          {/* Tabs */}
          <div className="flex items-center border-b border-slate-200 bg-slate-50">
            <button
              onClick={() => setActiveTab('description')}
              className={cn(
                'flex items-center gap-2 px-4 py-3 border-b-2 transition text-sm',
                activeTab === 'description'
                  ? 'border-blue-600 text-blue-600'
                  : 'border-transparent text-slate-500 hover:text-slate-900'
              )}
            >
              <FileText className="w-4 h-4" />
              Description
            </button>
            <button
              onClick={() => setActiveTab('output')}
              className={cn(
                'flex items-center gap-2 px-4 py-3 border-b-2 transition text-sm',
                activeTab === 'output'
                  ? 'border-blue-600 text-blue-600'
                  : 'border-transparent text-slate-500 hover:text-slate-900'
              )}
            >
              <Terminal className="w-4 h-4" />
              Output
              {testResults && (
                testResults.status === 'accepted' 
                  ? <CheckCircle className="w-4 h-4 text-emerald-500" />
                  : <XCircle className="w-4 h-4 text-red-500" />
              )}
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
              <div className="h-full bg-white">
                {testResults ? (
                  <TestResults
                    status={testResults.status}
                    testResults={testResults.test_results}
                    passedCount={testResults.passed_count}
                    totalCount={testResults.total_count}
                  />
                ) : (
                  <div className="p-4">
                    <div className="font-mono text-sm bg-slate-50 border border-slate-200 rounded-md p-4 whitespace-pre-wrap text-slate-700">
                      {consoleOutput || 'Click "Run" to execute your code'}
                    </div>
                  </div>
                )}
              </div>
            )}
          </div>
        </div>

        {/* Right Panel - Code Editor */}
        <div className="w-1/2 flex flex-col bg-slate-900">
          <CodeEditor
            code={code}
            language={language}
            onChange={setCode}
            onReset={handleReset}
            onLanguageChange={setLanguage}
            height="calc(100vh - 60px)"
            showActions={false}
            languages={Object.keys(problem.starter_code)}
          />
        </div>
      </div>
    </div>
  )
}


'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'
import { 
  Code2, 
  Swords, 
  Clock, 
  Send,
  Trophy,
  Target
} from 'lucide-react'
import CodeEditor from '@/components/CodeEditor'
import { cn, formatTime } from '@/lib/utils'
import { battles, execution } from '@/lib/api'
import { useAuthStore, useBattleStore } from '@/store/useStore'

export default function BattleArenaPage() {
  const router = useRouter()
  const { token, user } = useAuthStore()
  const { 
    battleId, 
    problem, 
    opponent, 
    myProgress, 
    opponentProgress,
    timeRemaining,
    status,
    winner,
    code,
    setCode,
    setTimeRemaining,
    updateProgress,
    endBattle,
    reset
  } = useBattleStore()

  const [isSubmitting, setIsSubmitting] = useState(false)
  const [testResults, setTestResults] = useState<any>(null)
  const [showResults, setShowResults] = useState(false)

  // Redirect if no active battle
  useEffect(() => {
    if (!battleId || !problem) {
      router.push('/battle')
    }
  }, [battleId, problem, router])

  // Timer
  useEffect(() => {
    if (status !== 'in_progress') return

    const timer = setInterval(() => {
      setTimeRemaining(Math.max(0, timeRemaining - 1))
      
      if (timeRemaining <= 0) {
        endBattle(null) // Time's up, no winner
        setShowResults(true)
      }
    }, 1000)

    return () => clearInterval(timer)
  }, [status, timeRemaining])

  // Simulate opponent progress
  useEffect(() => {
    if (status !== 'in_progress' || !opponent) return

    const interval = setInterval(() => {
      // Random opponent progress simulation
      const newTests = Math.min(
        opponentProgress.tests_passed + (Math.random() > 0.7 ? 1 : 0),
        3
      )
      const newLines = opponentProgress.code_lines + Math.floor(Math.random() * 3)
      
      updateProgress(myProgress, {
        tests_passed: newTests,
        code_lines: newLines
      })
    }, 3000)

    return () => clearInterval(interval)
  }, [status, opponent, opponentProgress])

  const handleSubmit = async () => {
    if (isSubmitting) return
    setIsSubmitting(true)

    try {
      // Run tests
      const testCases = problem?.examples?.map((ex: any) => ({
        input: ex.input,
        expected_output: ex.output,
      })) || []

      const result = await execution.test(code, 'python', testCases)
      setTestResults(result)

      // Update my progress
      const newProgress = {
        tests_passed: result.passed_count,
        code_lines: code.split('\n').length,
        attempts: myProgress.attempts + 1
      }
      updateProgress(newProgress, opponentProgress)

      // Check for win
      if (result.status === 'accepted') {
        endBattle(user?.username || '你')
        setShowResults(true)
      }
    } catch (error) {
      console.error('Submit failed:', error)
    } finally {
      setIsSubmitting(false)
    }
  }

  const handleExit = () => {
    reset()
    router.push('/battle')
  }

  if (!problem) {
    return null
  }

  const totalTests = problem.examples?.length || 3

  return (
    <div className="min-h-screen bg-dark-900 flex flex-col">
      {/* Navigation */}
      <nav className="sticky top-0 z-50 bg-dark-900/80 backdrop-blur-xl border-b border-dark-700">
        <div className="px-4 py-3">
          <div className="flex items-center justify-between">
            {/* Left - My Progress */}
            <div className="flex items-center gap-4">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-full bg-blue-500 flex items-center justify-center">
                  <span className="font-bold">你</span>
                </div>
                <div>
                  <div className="font-semibold">{user?.username || 'Player'}</div>
                  <div className="text-sm text-green-400">
                    {myProgress.tests_passed}/{totalTests} 测试通过
                  </div>
                </div>
              </div>
              <div className="w-32 h-3 bg-dark-700 rounded-full overflow-hidden">
                <div 
                  className="h-full bg-gradient-to-r from-blue-500 to-cyan-500 transition-all duration-500"
                  style={{ width: `${(myProgress.tests_passed / totalTests) * 100}%` }}
                />
              </div>
            </div>

            {/* Center - Timer & VS */}
            <div className="flex items-center gap-6">
              <div className={cn(
                'flex items-center gap-2 px-6 py-2 rounded-xl font-mono text-2xl font-bold',
                timeRemaining < 60 ? 'bg-red-500/20 text-red-400' : 'bg-dark-700'
              )}>
                <Clock className="w-5 h-5" />
                {formatTime(timeRemaining)}
              </div>
              <div className="text-3xl font-bold text-orange-400">VS</div>
            </div>

            {/* Right - Opponent Progress */}
            <div className="flex items-center gap-4">
              <div className="w-32 h-3 bg-dark-700 rounded-full overflow-hidden">
                <div 
                  className="h-full bg-gradient-to-r from-red-500 to-orange-500 transition-all duration-500"
                  style={{ width: `${(opponentProgress.tests_passed / totalTests) * 100}%` }}
                />
              </div>
              <div className="flex items-center gap-3">
                <div>
                  <div className="font-semibold text-right">{opponent || 'Waiting...'}</div>
                  <div className="text-sm text-yellow-400 text-right">
                    {opponentProgress.tests_passed}/{totalTests} 测试通过
                  </div>
                </div>
                <div className="w-10 h-10 rounded-full bg-red-500 flex items-center justify-center">
                  <span className="font-bold">对</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </nav>

      {/* Results Modal */}
      {showResults && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80">
          <div className="bg-dark-800 rounded-2xl p-8 max-w-md w-full mx-4 border border-dark-700">
            {winner ? (
              <>
                <div className="text-center mb-6">
                  <Trophy className={cn(
                    'w-16 h-16 mx-auto mb-4',
                    winner === (user?.username || '你') ? 'text-yellow-400' : 'text-gray-400'
                  )} />
                  <h2 className="text-3xl font-bold mb-2">
                    {winner === (user?.username || '你') ? '🎉 胜利!' : '败北'}
                  </h2>
                  <p className="text-dark-400">
                    {winner === (user?.username || '你') 
                      ? '恭喜你赢得了这场对战！' 
                      : `${winner} 先完成了挑战`}
                  </p>
                </div>
                
                {winner === (user?.username || '你') && (
                  <div className="bg-green-500/10 rounded-lg p-4 mb-6 text-center">
                    <div className="text-green-400 font-bold text-2xl">+25 ELO</div>
                    <div className="text-dark-400 text-sm">积分增加</div>
                  </div>
                )}
              </>
            ) : (
              <div className="text-center mb-6">
                <Clock className="w-16 h-16 mx-auto mb-4 text-dark-400" />
                <h2 className="text-3xl font-bold mb-2">时间结束</h2>
                <p className="text-dark-400">双方都没有在规定时间内完成</p>
              </div>
            )}

            <div className="flex gap-4">
              <button
                onClick={handleExit}
                className="flex-1 px-6 py-3 bg-dark-700 rounded-lg hover:bg-dark-600 transition"
              >
                返回大厅
              </button>
              <button
                onClick={() => {
                  reset()
                  router.push('/battle')
                }}
                className="flex-1 px-6 py-3 bg-orange-500 rounded-lg hover:bg-orange-600 transition"
              >
                再来一局
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Main Content */}
      <div className="flex-1 flex">
        {/* Left - Problem */}
        <div className="w-1/3 border-r border-dark-700 overflow-y-auto p-6">
          <h2 className="text-xl font-bold mb-4">{problem.title}</h2>
          <div className="prose prose-invert prose-sm max-w-none">
            <p className="text-dark-200">{problem.description}</p>
          </div>

          {problem.examples && (
            <div className="mt-6 space-y-4">
              <h3 className="font-semibold">示例</h3>
              {problem.examples.map((ex: any, i: number) => (
                <div key={i} className="bg-dark-800 rounded-lg p-3 text-sm">
                  <div className="text-dark-400">输入：</div>
                  <code className="text-blue-400">{ex.input}</code>
                  <div className="text-dark-400 mt-2">输出：</div>
                  <code className="text-green-400">{ex.output}</code>
                </div>
              ))}
            </div>
          )}

          {/* Test Results */}
          {testResults && (
            <div className="mt-6">
              <h3 className="font-semibold mb-3">提交结果</h3>
              <div className={cn(
                'rounded-lg p-4',
                testResults.status === 'accepted' ? 'bg-green-500/10' : 'bg-red-500/10'
              )}>
                <div className={cn(
                  'font-bold mb-2',
                  testResults.status === 'accepted' ? 'text-green-400' : 'text-red-400'
                )}>
                  {testResults.status === 'accepted' ? '✓ 通过' : '✗ 未通过'}
                </div>
                <div className="text-sm text-dark-400">
                  通过 {testResults.passed_count}/{testResults.total_count} 个测试
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Right - Code Editor */}
        <div className="flex-1 flex flex-col">
          <div className="flex-1">
            <CodeEditor
              code={code}
              language="python"
              onChange={setCode}
              height="calc(100vh - 200px)"
              showActions={false}
            />
          </div>

          {/* Submit Bar */}
          <div className="p-4 border-t border-dark-700 flex items-center justify-between bg-dark-800">
            <div className="text-sm text-dark-400">
              {myProgress.attempts} 次提交 · {code.split('\n').length} 行代码
            </div>
            <button
              onClick={handleSubmit}
              disabled={isSubmitting || status === 'completed'}
              className={cn(
                'flex items-center gap-2 px-6 py-3 rounded-lg font-semibold transition',
                isSubmitting || status === 'completed'
                  ? 'bg-green-900 text-green-400 cursor-not-allowed'
                  : 'bg-green-600 text-white hover:bg-green-500'
              )}
            >
              <Send className="w-5 h-5" />
              {isSubmitting ? '提交中...' : '提交'}
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}


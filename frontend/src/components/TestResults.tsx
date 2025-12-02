'use client'

import { CheckCircle, XCircle, Clock, AlertCircle } from 'lucide-react'
import { cn, getStatusColor, getStatusText } from '@/lib/utils'

interface TestCase {
  test_case: number
  input: string
  expected_output: string
  actual_output: string
  passed: boolean
  runtime_ms?: number
  error?: string
}

interface TestResultsProps {
  status: string
  testResults: TestCase[]
  passedCount: number
  totalCount: number
  totalRuntime?: number
  aiFeeback?: string
}

export default function TestResults({
  status,
  testResults,
  passedCount,
  totalCount,
  totalRuntime,
  aiFeeback,
}: TestResultsProps) {
  const allPassed = status === 'accepted'

  return (
    <div className="h-full overflow-y-auto p-4 space-y-4">
      {/* Status Header */}
      <div className={cn(
        'flex items-center gap-3 p-4 rounded-lg',
        allPassed ? 'bg-green-500/10' : 'bg-red-500/10'
      )}>
        {allPassed ? (
          <CheckCircle className="w-8 h-8 text-green-400" />
        ) : (
          <XCircle className="w-8 h-8 text-red-400" />
        )}
        <div>
          <h3 className={cn('text-xl font-bold', getStatusColor(status))}>
            {getStatusText(status)}
          </h3>
          <p className="text-dark-400 text-sm">
            Passed {passedCount}/{totalCount} test cases
            {totalRuntime && ` · ${totalRuntime}ms`}
          </p>
        </div>
      </div>

      {/* Test Cases */}
      <div className="space-y-3">
        {testResults.map((result, i) => (
          <div
            key={i}
            className={cn(
              'rounded-lg border overflow-hidden',
              result.passed
                ? 'border-green-500/30 bg-green-500/5'
                : 'border-red-500/30 bg-red-500/5'
            )}
          >
            <div className="flex items-center justify-between px-4 py-2 bg-dark-800/50">
              <div className="flex items-center gap-2">
                {result.passed ? (
                  <CheckCircle className="w-4 h-4 text-green-400" />
                ) : (
                  <XCircle className="w-4 h-4 text-red-400" />
                )}
                <span className="font-medium">Test Case {result.test_case}</span>
              </div>
              {result.runtime_ms !== undefined && (
                <span className="text-sm text-dark-400 flex items-center gap-1">
                  <Clock className="w-3 h-3" />
                  {result.runtime_ms}ms
                </span>
              )}
            </div>

            <div className="p-4 space-y-3 text-sm">
              <div>
                <span className="text-dark-400">Input:</span>
                <pre className="mt-1 p-2 bg-dark-800 rounded font-mono text-xs overflow-x-auto">
                  {result.input}
                </pre>
              </div>

              <div>
                <span className="text-dark-400">Expected Output:</span>
                <pre className="mt-1 p-2 bg-dark-800 rounded font-mono text-xs text-green-400 overflow-x-auto">
                  {result.expected_output}
                </pre>
              </div>

              {!result.passed && (
                <div>
                  <span className="text-dark-400">Actual Output:</span>
                  <pre className="mt-1 p-2 bg-dark-800 rounded font-mono text-xs text-red-400 overflow-x-auto">
                    {result.actual_output || '(no output)'}
                  </pre>
                </div>
              )}

              {result.error && (
                <div>
                  <span className="text-red-400 flex items-center gap-1">
                    <AlertCircle className="w-4 h-4" />
                    Error:
                  </span>
                  <pre className="mt-1 p-2 bg-red-500/10 rounded font-mono text-xs text-red-400 overflow-x-auto">
                    {result.error}
                  </pre>
                </div>
              )}
            </div>
          </div>
        ))}
      </div>

      {/* AI Feedback */}
      {aiFeeback && (
        <div className="border-t border-dark-700 pt-4">
          <h4 className="font-semibold mb-2 flex items-center gap-2">
            <span className="text-purple-400">AI</span> Code Analysis
          </h4>
          <div className="bg-purple-500/10 border border-purple-500/30 rounded-lg p-4">
            <p className="text-dark-200 text-sm whitespace-pre-wrap">{aiFeeback}</p>
          </div>
        </div>
      )}
    </div>
  )
}


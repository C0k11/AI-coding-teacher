'use client'

import { useState } from 'react'
import { ChevronDown, ChevronUp, Lightbulb, Tag, BookOpen, Clock, Database } from 'lucide-react'
import { cn } from '@/lib/utils'
import type { Problem } from '@/lib/api'

interface Solution {
  approach: string
  code: string
  time_complexity: string
  space_complexity: string
  explanation: string
}

interface ProblemDescriptionProps {
  problem: Problem & { solutions?: Solution[] }
  onGetHint?: (level: number) => Promise<string[]>
  hintsUsed?: number
}

export default function ProblemDescription({
  problem,
  onGetHint,
  hintsUsed = 0,
}: ProblemDescriptionProps) {
  const [showHints, setShowHints] = useState(false)
  const [hints, setHints] = useState<string[]>([])
  const [loadingHint, setLoadingHint] = useState(false)
  const [currentHintLevel, setCurrentHintLevel] = useState(0)
  const [showSolutions, setShowSolutions] = useState(false)
  const [selectedSolution, setSelectedSolution] = useState(0)

  const handleGetHint = async () => {
    if (!onGetHint || loadingHint) return
    
    const nextLevel = currentHintLevel + 1
    if (nextLevel > 3) return
    
    setLoadingHint(true)
    try {
      const newHints = await onGetHint(nextLevel)
      setHints(newHints)
      setCurrentHintLevel(nextLevel)
      setShowHints(true)
    } catch (error) {
      console.error('Failed to get hint:', error)
    } finally {
      setLoadingHint(false)
    }
  }

  return (
    <div className="h-full overflow-y-auto p-6 space-y-6 bg-white">
      {/* Header */}
      <div>
        <div className="flex items-center gap-3 mb-2">
          <h1 className="text-xl font-bold text-slate-900">{problem.title}</h1>
          <span className={cn(
            'px-2 py-0.5 rounded text-xs font-medium',
            problem.difficulty === 'easy' ? 'bg-emerald-100 text-emerald-700' :
            problem.difficulty === 'medium' ? 'bg-amber-100 text-amber-700' : 'bg-red-100 text-red-700'
          )}>
            {problem.difficulty.charAt(0).toUpperCase() + problem.difficulty.slice(1)}
          </span>
        </div>
      </div>

      {/* Description */}
      <div className="whitespace-pre-wrap text-slate-700 leading-relaxed text-sm">
        {problem.description}
      </div>

      {/* Examples */}
      <div className="space-y-4">
        <h3 className="text-base font-semibold text-slate-900">Examples</h3>
        {problem.examples.map((example, i) => (
          <div key={i} className="bg-slate-50 rounded-md p-4 border border-slate-200">
            <div className="space-y-2">
              <div>
                <span className="text-slate-500 text-sm">Input:</span>
                <code className="block mt-1 text-sm font-mono text-blue-600">{example.input}</code>
              </div>
              <div>
                <span className="text-slate-500 text-sm">Output:</span>
                <code className="block mt-1 text-sm font-mono text-emerald-600">{example.output}</code>
              </div>
              {example.explanation && (
                <div>
                  <span className="text-slate-500 text-sm">Explanation:</span>
                  <p className="mt-1 text-sm text-slate-600">{example.explanation}</p>
                </div>
              )}
            </div>
          </div>
        ))}
      </div>

      {/* Constraints */}
      <div>
        <h3 className="text-base font-semibold text-slate-900 mb-3">Constraints</h3>
        <ul className="list-disc list-inside space-y-1 text-sm text-slate-600">
          {problem.constraints.map((constraint, i) => (
            <li key={i}>{constraint}</li>
          ))}
        </ul>
      </div>

      {/* Tags */}
      {problem.topics.length > 0 && (
        <div className="flex items-center gap-2 flex-wrap">
          <Tag className="w-4 h-4 text-slate-400" />
          {problem.topics.map((topic) => (
            <span
              key={topic}
              className="px-2 py-1 bg-slate-100 rounded text-xs text-slate-600"
            >
              {topic}
            </span>
          ))}
        </div>
      )}

      {/* Hints */}
      {onGetHint && (
        <div className="border-t border-slate-200 pt-4">
          <button
            onClick={() => setShowHints(!showHints)}
            className="flex items-center gap-2 text-amber-600 hover:text-amber-700 transition"
          >
            <Lightbulb className="w-5 h-5" />
            <span className="font-medium">Hints ({currentHintLevel}/3)</span>
            {showHints ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
          </button>

          {showHints && (
            <div className="mt-4 space-y-3">
              {hints.map((hint, i) => (
                <div key={i} className="bg-amber-50 border border-amber-200 rounded-md p-3">
                  <span className="text-amber-700 font-medium">Hint {i + 1}:</span>
                  <p className="text-slate-700 mt-1 text-sm">{hint}</p>
                </div>
              ))}
              
              {currentHintLevel < 3 && (
                <button
                  onClick={handleGetHint}
                  disabled={loadingHint}
                  className="text-sm text-amber-600 hover:text-amber-700 transition font-medium"
                >
                  {loadingHint ? 'Loading...' : 'Get Next Hint'}
                </button>
              )}
            </div>
          )}
        </div>
      )}

      {/* Solutions */}
      {problem.solutions && problem.solutions.length > 0 && (
        <div className="border-t border-slate-200 pt-4">
          <button
            onClick={() => setShowSolutions(!showSolutions)}
            className="flex items-center gap-2 text-blue-600 hover:text-blue-700 transition"
          >
            <BookOpen className="w-5 h-5" />
            <span className="font-medium">Solutions ({problem.solutions.length})</span>
            {showSolutions ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
          </button>

          {showSolutions && (
            <div className="mt-4 space-y-4">
              {/* Solution tabs */}
              {problem.solutions.length > 1 && (
                <div className="flex gap-2 flex-wrap">
                  {problem.solutions.map((sol, i) => (
                    <button
                      key={i}
                      onClick={() => setSelectedSolution(i)}
                      className={cn(
                        'px-3 py-1.5 rounded text-sm font-medium transition',
                        selectedSolution === i
                          ? 'bg-blue-600 text-white'
                          : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
                      )}
                    >
                      {sol.approach}
                    </button>
                  ))}
                </div>
              )}

              {/* Selected solution */}
              {problem.solutions[selectedSolution] && (
                <div className="space-y-4">
                  <div className="bg-blue-50 border border-blue-200 rounded-md p-4">
                    <h4 className="text-blue-800 font-semibold mb-2">
                      {problem.solutions[selectedSolution].approach}
                    </h4>
                    <p className="text-slate-700 text-sm mb-3">
                      {problem.solutions[selectedSolution].explanation}
                    </p>
                    
                    {/* Complexity */}
                    <div className="flex gap-4 text-sm mb-3">
                      <div className="flex items-center gap-1.5 text-slate-600">
                        <Clock className="w-4 h-4" />
                        <span>Time: <code className="text-blue-600">{problem.solutions[selectedSolution].time_complexity}</code></span>
                      </div>
                      <div className="flex items-center gap-1.5 text-slate-600">
                        <Database className="w-4 h-4" />
                        <span>Space: <code className="text-blue-600">{problem.solutions[selectedSolution].space_complexity}</code></span>
                      </div>
                    </div>

                    {/* Code */}
                    <div className="bg-slate-900 rounded-md p-4 overflow-x-auto">
                      <pre className="text-sm text-slate-100 font-mono whitespace-pre">
                        {problem.solutions[selectedSolution].code}
                      </pre>
                    </div>
                  </div>
                </div>
              )}
            </div>
          )}
        </div>
      )}
    </div>
  )
}


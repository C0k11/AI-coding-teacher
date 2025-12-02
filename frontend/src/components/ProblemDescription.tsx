'use client'

import { useState } from 'react'
import { ChevronDown, ChevronUp, Lightbulb, Building2, Tag, Clock, Database } from 'lucide-react'
import { cn, getDifficultyBadgeClass } from '@/lib/utils'
import type { Problem } from '@/lib/api'

interface ProblemDescriptionProps {
  problem: Problem
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
    <div className="h-full overflow-y-auto p-6 space-y-6">
      {/* Header */}
      <div>
        <div className="flex items-center gap-3 mb-2">
          <h1 className="text-2xl font-bold">{problem.title}</h1>
          <span className={cn('px-2 py-0.5 rounded text-sm', getDifficultyBadgeClass(problem.difficulty))}>
            {problem.difficulty === 'easy' ? 'Easy' : problem.difficulty === 'medium' ? 'Medium' : 'Hard'}
          </span>
        </div>
        
        {/* Stats */}
        <div className="flex items-center gap-4 text-sm text-dark-400">
          <span className="flex items-center gap-1">
            <Clock className="w-4 h-4" />
            {problem.acceptance_rate.toFixed(1)}% Acceptance Rate
          </span>
          <span className="flex items-center gap-1">
            <Database className="w-4 h-4" />
            {problem.submission_count} Submissions
          </span>
        </div>
      </div>

      {/* Description */}
      <div className="prose prose-invert prose-sm max-w-none">
        <div className="whitespace-pre-wrap text-dark-200 leading-relaxed">
          {problem.description}
        </div>
      </div>

      {/* Examples */}
      <div className="space-y-4">
        <h3 className="text-lg font-semibold">Examples</h3>
        {problem.examples.map((example, i) => (
          <div key={i} className="bg-dark-800 rounded-lg p-4 border border-dark-700">
            <div className="space-y-2">
              <div>
                <span className="text-dark-400 text-sm">Input:</span>
                <code className="block mt-1 text-sm font-mono text-blue-400">{example.input}</code>
              </div>
              <div>
                <span className="text-dark-400 text-sm">Output:</span>
                <code className="block mt-1 text-sm font-mono text-green-400">{example.output}</code>
              </div>
              {example.explanation && (
                <div>
                  <span className="text-dark-400 text-sm">Explanation:</span>
                  <p className="mt-1 text-sm text-dark-300">{example.explanation}</p>
                </div>
              )}
            </div>
          </div>
        ))}
      </div>

      {/* Constraints */}
      <div>
        <h3 className="text-lg font-semibold mb-3">Constraints</h3>
        <ul className="list-disc list-inside space-y-1 text-sm text-dark-300">
          {problem.constraints.map((constraint, i) => (
            <li key={i}>{constraint}</li>
          ))}
        </ul>
      </div>

      {/* Tags */}
      <div className="space-y-3">
        <div className="flex items-center gap-2 flex-wrap">
          <Tag className="w-4 h-4 text-dark-400" />
          {problem.topics.map((topic) => (
            <span
              key={topic}
              className="px-2 py-1 bg-dark-700 rounded text-xs text-dark-300"
            >
              {topic}
            </span>
          ))}
        </div>
        
        {problem.companies.length > 0 && (
          <div className="flex items-center gap-2 flex-wrap">
            <Building2 className="w-4 h-4 text-dark-400" />
            {problem.companies.map((company) => (
              <span
                key={company}
                className="px-2 py-1 bg-purple-500/20 text-purple-400 rounded text-xs"
              >
                {company}
              </span>
            ))}
          </div>
        )}
      </div>

      {/* Hints */}
      {onGetHint && (
        <div className="border-t border-dark-700 pt-4">
          <button
            onClick={() => setShowHints(!showHints)}
            className="flex items-center gap-2 text-yellow-400 hover:text-yellow-300 transition"
          >
            <Lightbulb className="w-5 h-5" />
            <span>Hints ({currentHintLevel}/3)</span>
            {showHints ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
          </button>

          {showHints && (
            <div className="mt-4 space-y-3">
              {hints.map((hint, i) => (
                <div key={i} className="bg-yellow-500/10 border border-yellow-500/30 rounded-lg p-3">
                  <span className="text-yellow-400 font-medium">Hint {i + 1}:</span>
                  <p className="text-dark-200 mt-1">{hint}</p>
                </div>
              ))}
              
              {currentHintLevel < 3 && (
                <button
                  onClick={handleGetHint}
                  disabled={loadingHint}
                  className="text-sm text-yellow-400 hover:text-yellow-300 transition"
                >
                  {loadingHint ? 'Loading...' : 'Get Next Hint'}
                </button>
              )}
            </div>
          )}
        </div>
      )}
    </div>
  )
}


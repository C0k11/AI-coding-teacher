'use client'

import { useState, useEffect, useCallback } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'
import { 
  Clock, 
  CheckCircle, 
  XCircle,
  Trophy,
  ChevronRight,
  Zap
} from 'lucide-react'
import { cn } from '@/lib/utils'

// Quiz Questions Data
const QUIZ_QUESTIONS = [
  // Fill in the blank questions
  {
    id: 1,
    type: 'fill_blank',
    title: 'Complete the Loop',
    code: `# Print numbers 0 to 4
for i in _____(5):
    print(i)`,
    blank: '_____',
    answer: 'range',
    hints: ['This function generates a sequence of numbers'],
    points: 10,
  },
  {
    id: 2,
    type: 'fill_blank',
    title: 'List Append',
    code: `nums = [1, 2, 3]
nums._____(4)
# nums is now [1, 2, 3, 4]`,
    blank: '_____',
    answer: 'append',
    hints: ['Method to add an element to the end of a list'],
    points: 10,
  },
  {
    id: 3,
    type: 'fill_blank',
    title: 'String Length',
    code: `text = "Hello"
length = _____(text)
# length is 5`,
    blank: '_____',
    answer: 'len',
    hints: ['Built-in function to get the length'],
    points: 10,
  },
  {
    id: 4,
    type: 'fill_blank',
    title: 'Dictionary Access',
    code: `person = {"name": "Alice", "age": 25}
name = person._____("name")
# name is "Alice"`,
    blank: '_____',
    answer: 'get',
    hints: ['Safe way to access dictionary values'],
    points: 10,
  },
  {
    id: 5,
    type: 'fill_blank',
    title: 'List Comprehension',
    code: `# Create [0, 1, 4, 9, 16]
squares = [x**2 _____ x in range(5)]`,
    blank: '_____',
    answer: 'for',
    hints: ['Keyword used in loops and comprehensions'],
    points: 10,
  },
  // Multiple choice questions
  {
    id: 6,
    type: 'multiple_choice',
    title: 'What is the output?',
    code: `x = [1, 2, 3]
y = x
y.append(4)
print(x)`,
    options: ['[1, 2, 3]', '[1, 2, 3, 4]', '[4]', 'Error'],
    answer: '[1, 2, 3, 4]',
    explanation: 'Lists are mutable and y references the same list as x',
    points: 15,
  },
  {
    id: 7,
    type: 'multiple_choice',
    title: 'What is the output?',
    code: `def foo(x=[]):
    x.append(1)
    return x

print(foo())
print(foo())`,
    options: ['[1]\\n[1]', '[1]\\n[1, 1]', '[1, 1]\\n[1, 1]', 'Error'],
    answer: '[1]\\n[1, 1]',
    explanation: 'Default mutable arguments are shared between calls',
    points: 15,
  },
  {
    id: 8,
    type: 'multiple_choice',
    title: 'What is the output?',
    code: `print(type([]) == list)`,
    options: ['True', 'False', 'list', 'Error'],
    answer: 'True',
    explanation: 'type([]) returns <class "list"> which equals list',
    points: 10,
  },
  {
    id: 9,
    type: 'multiple_choice',
    title: 'What is the output?',
    code: `nums = [1, 2, 3, 4, 5]
print(nums[1:4])`,
    options: ['[1, 2, 3, 4]', '[2, 3, 4]', '[2, 3, 4, 5]', '[1, 2, 3]'],
    answer: '[2, 3, 4]',
    explanation: 'Slicing is [start:end), end index is exclusive',
    points: 10,
  },
  {
    id: 10,
    type: 'multiple_choice',
    title: 'What is the output?',
    code: `x = 5
def change():
    x = 10
change()
print(x)`,
    options: ['5', '10', 'None', 'Error'],
    answer: '5',
    explanation: 'x inside function is a local variable, doesn\'t affect global x',
    points: 15,
  },
]

export default function QuizBattlePage() {
  const router = useRouter()
  const [currentQuestion, setCurrentQuestion] = useState(0)
  const [userAnswer, setUserAnswer] = useState('')
  const [score, setScore] = useState(0)
  const [timeRemaining, setTimeRemaining] = useState(120) // 2 minutes
  const [isFinished, setIsFinished] = useState(false)
  const [answers, setAnswers] = useState<{questionId: number, correct: boolean, userAnswer: string}[]>([])
  const [showFeedback, setShowFeedback] = useState(false)
  const [isCorrect, setIsCorrect] = useState(false)
  const [questions] = useState(() => 
    [...QUIZ_QUESTIONS].sort(() => Math.random() - 0.5).slice(0, 5)
  )

  const question = questions[currentQuestion]

  // Timer
  useEffect(() => {
    if (isFinished) return
    
    const timer = setInterval(() => {
      setTimeRemaining(prev => {
        if (prev <= 1) {
          setIsFinished(true)
          return 0
        }
        return prev - 1
      })
    }, 1000)

    return () => clearInterval(timer)
  }, [isFinished])

  const handleSubmitAnswer = useCallback(() => {
    if (!question || showFeedback) return

    const correct = question.type === 'fill_blank' 
      ? userAnswer.trim().toLowerCase() === question.answer.toLowerCase()
      : userAnswer === question.answer

    setIsCorrect(correct)
    setShowFeedback(true)

    if (correct) {
      setScore(prev => prev + question.points)
    }

    setAnswers(prev => [...prev, {
      questionId: question.id,
      correct,
      userAnswer: userAnswer
    }])

    // Auto advance after feedback
    setTimeout(() => {
      if (currentQuestion < questions.length - 1) {
        setCurrentQuestion(prev => prev + 1)
        setUserAnswer('')
        setShowFeedback(false)
      } else {
        setIsFinished(true)
      }
    }, 1500)
  }, [question, userAnswer, currentQuestion, questions.length, showFeedback])

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60)
    const secs = seconds % 60
    return `${mins}:${secs.toString().padStart(2, '0')}`
  }

  if (isFinished) {
    const correctCount = answers.filter(a => a.correct).length
    const percentage = Math.round((correctCount / questions.length) * 100)

    return (
      <div className="min-h-screen bg-slate-900 flex items-center justify-center p-6">
        <div className="bg-slate-800 rounded-2xl p-8 max-w-lg w-full border border-slate-700">
          <div className="text-center mb-8">
            <Trophy className={cn(
              'w-20 h-20 mx-auto mb-4',
              percentage >= 80 ? 'text-yellow-400' : percentage >= 50 ? 'text-slate-400' : 'text-slate-600'
            )} />
            <h1 className="text-3xl font-bold text-white mb-2">
              {percentage >= 80 ? 'Excellent!' : percentage >= 50 ? 'Good Job!' : 'Keep Practicing!'}
            </h1>
            <p className="text-slate-400">Quiz completed</p>
          </div>

          <div className="grid grid-cols-3 gap-4 mb-8">
            <div className="bg-slate-700/50 rounded-xl p-4 text-center">
              <div className="text-3xl font-bold text-white">{score}</div>
              <div className="text-sm text-slate-400">Points</div>
            </div>
            <div className="bg-slate-700/50 rounded-xl p-4 text-center">
              <div className="text-3xl font-bold text-green-400">{correctCount}/{questions.length}</div>
              <div className="text-sm text-slate-400">Correct</div>
            </div>
            <div className="bg-slate-700/50 rounded-xl p-4 text-center">
              <div className="text-3xl font-bold text-blue-400">{percentage}%</div>
              <div className="text-sm text-slate-400">Accuracy</div>
            </div>
          </div>

          {/* Answer Summary */}
          <div className="space-y-2 mb-8">
            {answers.map((ans, i) => (
              <div key={i} className={cn(
                'flex items-center gap-3 p-3 rounded-lg',
                ans.correct ? 'bg-green-500/10' : 'bg-red-500/10'
              )}>
                {ans.correct ? (
                  <CheckCircle className="w-5 h-5 text-green-400" />
                ) : (
                  <XCircle className="w-5 h-5 text-red-400" />
                )}
                <span className="text-slate-300 text-sm">Question {i + 1}</span>
              </div>
            ))}
          </div>

          <div className="flex gap-4">
            <button
              onClick={() => router.push('/battle')}
              className="flex-1 px-6 py-3 bg-slate-700 rounded-lg hover:bg-slate-600 transition text-white font-medium"
            >
              Exit
            </button>
            <button
              onClick={() => window.location.reload()}
              className="flex-1 px-6 py-3 bg-blue-600 rounded-lg hover:bg-blue-500 transition text-white font-medium"
            >
              Play Again
            </button>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-slate-900">
      {/* Header */}
      <div className="sticky top-0 z-50 bg-slate-900/90 backdrop-blur border-b border-slate-800">
        <div className="container mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <Link href="/battle" className="text-slate-400 hover:text-white transition">
                ← Back
              </Link>
              <div className="flex items-center gap-2">
                <Zap className="w-5 h-5 text-yellow-400" />
                <span className="font-bold text-white">Quick Battle</span>
              </div>
            </div>

            <div className={cn(
              'flex items-center gap-2 px-4 py-2 rounded-lg font-mono text-xl font-bold',
              timeRemaining < 30 ? 'bg-red-500/20 text-red-400' : 'bg-slate-800 text-white'
            )}>
              <Clock className="w-5 h-5" />
              {formatTime(timeRemaining)}
            </div>

            <div className="flex items-center gap-4">
              <div className="text-slate-400">
                <span className="text-white font-bold">{currentQuestion + 1}</span>/{questions.length}
              </div>
              <div className="bg-yellow-500/20 px-3 py-1 rounded-lg">
                <span className="text-yellow-400 font-bold">{score}</span>
                <span className="text-yellow-400/60 text-sm"> pts</span>
              </div>
            </div>
          </div>

          {/* Progress bar */}
          <div className="mt-4 h-1 bg-slate-800 rounded-full overflow-hidden">
            <div 
              className="h-full bg-blue-500 transition-all duration-300"
              style={{ width: `${((currentQuestion + 1) / questions.length) * 100}%` }}
            />
          </div>
        </div>
      </div>

      {/* Question */}
      <div className="container mx-auto px-6 py-12 max-w-3xl">
        <div className="mb-6">
          <span className={cn(
            'px-3 py-1 rounded-full text-sm font-medium',
            question.type === 'fill_blank' ? 'bg-purple-500/20 text-purple-400' : 'bg-blue-500/20 text-blue-400'
          )}>
            {question.type === 'fill_blank' ? 'Fill in the Blank' : 'Multiple Choice'}
          </span>
          <span className="ml-3 text-slate-500">+{question.points} pts</span>
        </div>

        <h2 className="text-2xl font-bold text-white mb-6">{question.title}</h2>

        {/* Code Block */}
        <div className="bg-slate-800 rounded-xl p-6 mb-8 border border-slate-700">
          <pre className="text-sm font-mono text-slate-100 whitespace-pre-wrap leading-relaxed">
            {question.code}
          </pre>
        </div>

        {/* Answer Input */}
        {question.type === 'fill_blank' ? (
          <div className="mb-8">
            <label className="block text-slate-400 mb-2">Your answer:</label>
            <input
              type="text"
              value={userAnswer}
              onChange={(e) => setUserAnswer(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && handleSubmitAnswer()}
              disabled={showFeedback}
              placeholder="Type the missing code..."
              className={cn(
                'w-full px-4 py-3 bg-slate-800 border rounded-lg text-white font-mono text-lg focus:outline-none focus:ring-2 transition',
                showFeedback 
                  ? isCorrect ? 'border-green-500 ring-green-500/20' : 'border-red-500 ring-red-500/20'
                  : 'border-slate-700 focus:ring-blue-500/50 focus:border-blue-500'
              )}
              autoFocus
            />
          </div>
        ) : (
          <div className="space-y-3 mb-8">
            {question.options?.map((option, i) => (
              <button
                key={i}
                onClick={() => !showFeedback && setUserAnswer(option)}
                disabled={showFeedback}
                className={cn(
                  'w-full p-4 rounded-lg border text-left transition flex items-center gap-3',
                  showFeedback
                    ? option === question.answer
                      ? 'border-green-500 bg-green-500/10'
                      : option === userAnswer
                        ? 'border-red-500 bg-red-500/10'
                        : 'border-slate-700 bg-slate-800'
                    : userAnswer === option
                      ? 'border-blue-500 bg-blue-500/10'
                      : 'border-slate-700 bg-slate-800 hover:border-slate-600'
                )}
              >
                <div className={cn(
                  'w-6 h-6 rounded-full border-2 flex items-center justify-center flex-shrink-0',
                  showFeedback
                    ? option === question.answer
                      ? 'border-green-500 bg-green-500'
                      : option === userAnswer
                        ? 'border-red-500 bg-red-500'
                        : 'border-slate-600'
                    : userAnswer === option
                      ? 'border-blue-500 bg-blue-500'
                      : 'border-slate-600'
                )}>
                  {showFeedback && option === question.answer && (
                    <CheckCircle className="w-4 h-4 text-white" />
                  )}
                  {showFeedback && option === userAnswer && option !== question.answer && (
                    <XCircle className="w-4 h-4 text-white" />
                  )}
                </div>
                <code className="text-slate-200 font-mono">{option}</code>
              </button>
            ))}
          </div>
        )}

        {/* Feedback */}
        {showFeedback && (
          <div className={cn(
            'p-4 rounded-lg mb-6',
            isCorrect ? 'bg-green-500/10 border border-green-500/30' : 'bg-red-500/10 border border-red-500/30'
          )}>
            <div className="flex items-center gap-2 mb-2">
              {isCorrect ? (
                <>
                  <CheckCircle className="w-5 h-5 text-green-400" />
                  <span className="font-bold text-green-400">Correct! +{question.points} pts</span>
                </>
              ) : (
                <>
                  <XCircle className="w-5 h-5 text-red-400" />
                  <span className="font-bold text-red-400">Incorrect</span>
                </>
              )}
            </div>
            {!isCorrect && (
              <p className="text-slate-400 text-sm">
                Correct answer: <code className="text-green-400">{question.answer}</code>
              </p>
            )}
            {question.type === 'multiple_choice' && question.explanation && (
              <p className="text-slate-400 text-sm mt-2">{question.explanation}</p>
            )}
          </div>
        )}

        {/* Submit Button */}
        {!showFeedback && (
          <button
            onClick={handleSubmitAnswer}
            disabled={!userAnswer}
            className={cn(
              'w-full flex items-center justify-center gap-2 px-6 py-4 rounded-lg font-bold text-lg transition',
              userAnswer
                ? 'bg-blue-600 hover:bg-blue-500 text-white'
                : 'bg-slate-800 text-slate-500 cursor-not-allowed'
            )}
          >
            Submit Answer
            <ChevronRight className="w-5 h-5" />
          </button>
        )}
      </div>
    </div>
  )
}

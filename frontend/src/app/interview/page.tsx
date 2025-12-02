'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'
import { motion } from 'framer-motion'
import { 
  Code2, 
  Brain, 
  Building2, 
  Clock, 
  Zap,
  Settings,
  ChevronRight,
  Sparkles
} from 'lucide-react'
import { cn } from '@/lib/utils'
import { interviews, type InterviewConfig } from '@/lib/api'
import { useAuthStore, useInterviewStore } from '@/store/useStore'

const INTERVIEW_TYPES = [
  { id: 'algorithm', name: 'Algorithm Interview', icon: Code2, description: 'Data structures and algorithms', color: 'from-blue-500 to-cyan-500' },
  { id: 'system_design', name: 'System Design', icon: Settings, description: 'Large-scale system architecture design', color: 'from-purple-500 to-pink-500' },
  { id: 'behavioral', name: 'Behavioral Interview', icon: Brain, description: 'STAR method, soft skills assessment', color: 'from-green-500 to-emerald-500' },
  { id: 'frontend', name: 'Frontend Specialized', icon: Sparkles, description: 'React/Vue, performance optimization', color: 'from-orange-500 to-red-500' },
]

const COMPANIES = [
  { id: 'google', name: 'Google', style: 'Friendly but pursue optimal solutions' },
  { id: 'meta', name: 'Meta', style: 'Focus on code simplicity and real scenarios' },
  { id: 'amazon', name: 'Amazon', style: 'Emphasize communication and leadership principles' },
  { id: 'microsoft', name: 'Microsoft', style: 'Balance technical depth and breadth' },
  { id: 'startup', name: 'Startup', style: 'Practical and efficient, solve problems quickly' },
]

const DIFFICULTIES = [
  { id: 'easy', name: 'Easy', description: 'Basic problems, suitable for beginners' },
  { id: 'medium', name: 'Medium', description: 'Standard interview difficulty' },
  { id: 'hard', name: 'Hard', description: 'Advanced problems, challenge yourself' },
]

const DURATIONS = [30, 45, 60]

export default function InterviewPage() {
  const router = useRouter()
  const { token } = useAuthStore()
  const { startInterview } = useInterviewStore()
  
  const [step, setStep] = useState(1)
  const [config, setConfig] = useState<InterviewConfig>({
    interview_type: 'algorithm',
    company: 'google',
    difficulty: 'medium',
    duration_minutes: 45,
  })
  const [isStarting, setIsStarting] = useState(false)

  const handleStart = async () => {
    setIsStarting(true)
    
    try {
      // For demo, create a mock interview session
      const mockSession = {
        interview_id: Date.now(),
        interview_type: config.interview_type,
        company: config.company,
        difficulty: config.difficulty,
        duration_minutes: config.duration_minutes,
        problem: {
          title: config.interview_type === 'algorithm' ? 'LRU Cache' : 'Design Twitter',
          description: config.interview_type === 'algorithm' 
            ? 'Please implement an LRU Cache that supports get and put operations with O(1) time complexity.'
            : 'Design a simplified version of Twitter that supports posting tweets, following users, and getting feed.'
        },
        initial_message: `Hello! I'm your interviewer today from ${config.company}. We have ${config.duration_minutes} minutes for today's interview.

Before we begin, could you briefly introduce yourself? Then we'll start with today's interview problem.`
      }

      if (token) {
        try {
          const session = await interviews.start(config, token)
          startInterview(
            session.interview_id,
            session.interview_type,
            session.company,
            session.problem,
            session.initial_message
          )
        } catch (error) {
          // Fallback to mock
          startInterview(
            mockSession.interview_id,
            mockSession.interview_type,
            mockSession.company,
            mockSession.problem,
            mockSession.initial_message
          )
        }
      } else {
        startInterview(
          mockSession.interview_id,
          mockSession.interview_type,
          mockSession.company,
          mockSession.problem,
          mockSession.initial_message
        )
      }

      router.push('/interview/session')
    } catch (error) {
      console.error('Failed to start interview:', error)
    } finally {
      setIsStarting(false)
    }
  }

  return (
    <div className="min-h-screen bg-dark-900">
      {/* Navigation */}
      <nav className="sticky top-0 z-50 bg-dark-900/80 backdrop-blur-xl border-b border-dark-700">
        <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
          <Link href="/" className="flex items-center gap-2">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-purple-500 to-pink-500 flex items-center justify-center">
              <Code2 className="w-6 h-6 text-white" />
            </div>
            <span className="text-xl font-bold">AI Coding Teacher</span>
          </Link>
          <div className="flex items-center gap-6">
            <Link href="/problems" className="text-dark-300 hover:text-white transition">Problems</Link>
            <Link href="/interview" className="text-white font-medium">Interview</Link>
            <Link href="/battle" className="text-dark-300 hover:text-white transition">Battle</Link>
            <Link href="/dashboard" className="text-dark-300 hover:text-white transition">Dashboard</Link>
          </div>
        </div>
      </nav>

      <div className="max-w-4xl mx-auto px-6 py-12">
        {/* Header */}
        <div className="text-center mb-12">
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-purple-500/20 text-purple-400 text-sm mb-4">
            <Brain className="w-4 h-4" />
            AI Interviewer Simulation
          </div>
          <h1 className="text-4xl font-bold mb-4">Ready for Your Interview?</h1>
          <p className="text-dark-400 text-lg">Select your interview type, and the AI interviewer will simulate a real interview scenario</p>
        </div>

        {/* Progress Steps */}
        <div className="flex items-center justify-center gap-4 mb-12">
          {[1, 2, 3, 4].map((s) => (
            <div key={s} className="flex items-center">
              <div className={cn(
                'w-8 h-8 rounded-full flex items-center justify-center font-medium transition',
                step >= s ? 'bg-purple-500 text-white' : 'bg-dark-700 text-dark-400'
              )}>
                {s}
              </div>
              {s < 4 && (
                <div className={cn(
                  'w-12 h-0.5 transition',
                  step > s ? 'bg-purple-500' : 'bg-dark-700'
                )} />
              )}
            </div>
          ))}
        </div>

        {/* Step 1: Interview Type */}
        {step === 1 && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
          >
            <h2 className="text-2xl font-bold mb-6 text-center">Select Interview Type</h2>
            <div className="grid grid-cols-2 gap-4">
              {INTERVIEW_TYPES.map((type) => (
                <button
                  key={type.id}
                  onClick={() => {
                    setConfig({ ...config, interview_type: type.id as any })
                    setStep(2)
                  }}
                  className={cn(
                    'p-6 rounded-xl border-2 text-left transition card-hover',
                    config.interview_type === type.id
                      ? 'border-purple-500 bg-purple-500/10'
                      : 'border-dark-700 bg-dark-800 hover:border-dark-600'
                  )}
                >
                  <div className={`w-12 h-12 rounded-lg bg-gradient-to-br ${type.color} flex items-center justify-center mb-4`}>
                    <type.icon className="w-6 h-6 text-white" />
                  </div>
                  <h3 className="text-lg font-semibold mb-1">{type.name}</h3>
                  <p className="text-dark-400 text-sm">{type.description}</p>
                </button>
              ))}
            </div>
          </motion.div>
        )}

        {/* Step 2: Company */}
        {step === 2 && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
          >
            <h2 className="text-2xl font-bold mb-6 text-center">Select Target Company</h2>
            <div className="space-y-3">
              {COMPANIES.map((company) => (
                <button
                  key={company.id}
                  onClick={() => {
                    setConfig({ ...config, company: company.id })
                    setStep(3)
                  }}
                  className={cn(
                    'w-full p-4 rounded-xl border-2 text-left transition flex items-center justify-between group',
                    config.company === company.id
                      ? 'border-purple-500 bg-purple-500/10'
                      : 'border-dark-700 bg-dark-800 hover:border-dark-600'
                  )}
                >
                  <div className="flex items-center gap-4">
                    <div className="w-12 h-12 rounded-lg bg-dark-700 flex items-center justify-center">
                      <Building2 className="w-6 h-6 text-dark-300" />
                    </div>
                    <div>
                      <h3 className="font-semibold">{company.name}</h3>
                      <p className="text-dark-400 text-sm">{company.style}</p>
                    </div>
                  </div>
                  <ChevronRight className="w-5 h-5 text-dark-500 group-hover:text-white transition" />
                </button>
              ))}
            </div>
            <button
              onClick={() => setStep(1)}
              className="mt-6 text-dark-400 hover:text-white transition"
            >
              ← Go Back
            </button>
          </motion.div>
        )}

        {/* Step 3: Difficulty */}
        {step === 3 && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
          >
            <h2 className="text-2xl font-bold mb-6 text-center">Select Difficulty</h2>
            <div className="grid grid-cols-3 gap-4">
              {DIFFICULTIES.map((diff) => (
                <button
                  key={diff.id}
                  onClick={() => {
                    setConfig({ ...config, difficulty: diff.id })
                    setStep(4)
                  }}
                  className={cn(
                    'p-6 rounded-xl border-2 text-center transition card-hover',
                    config.difficulty === diff.id
                      ? 'border-purple-500 bg-purple-500/10'
                      : 'border-dark-700 bg-dark-800 hover:border-dark-600'
                  )}
                >
                  <h3 className={cn(
                    'text-xl font-bold mb-2',
                    diff.id === 'easy' ? 'text-green-400' :
                    diff.id === 'medium' ? 'text-yellow-400' : 'text-red-400'
                  )}>
                    {diff.name}
                  </h3>
                  <p className="text-dark-400 text-sm">{diff.description}</p>
                </button>
              ))}
            </div>
            <button
              onClick={() => setStep(2)}
              className="mt-6 text-dark-400 hover:text-white transition"
            >
              ← Go Back
            </button>
          </motion.div>
        )}

        {/* Step 4: Duration & Start */}
        {step === 4 && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
          >
            <h2 className="text-2xl font-bold mb-6 text-center">Select Duration</h2>
            <div className="grid grid-cols-3 gap-4 mb-8">
              {DURATIONS.map((duration) => (
                <button
                  key={duration}
                  onClick={() => setConfig({ ...config, duration_minutes: duration })}
                  className={cn(
                    'p-6 rounded-xl border-2 text-center transition',
                    config.duration_minutes === duration
                      ? 'border-purple-500 bg-purple-500/10'
                      : 'border-dark-700 bg-dark-800 hover:border-dark-600'
                  )}
                >
                  <Clock className="w-8 h-8 mx-auto mb-2 text-dark-300" />
                  <h3 className="text-2xl font-bold">{duration}</h3>
                  <p className="text-dark-400 text-sm">minutes</p>
                </button>
              ))}
            </div>

            {/* Summary */}
            <div className="bg-dark-800 rounded-xl p-6 border border-dark-700 mb-8">
              <h3 className="font-semibold mb-4">Interview Configuration</h3>
              <div className="grid grid-cols-2 gap-4 text-sm">
                <div>
                  <span className="text-dark-400">Interview Type:</span>
                  <span className="text-white ml-2">
                    {INTERVIEW_TYPES.find(t => t.id === config.interview_type)?.name}
                  </span>
                </div>
                <div>
                  <span className="text-dark-400">Target Company:</span>
                  <span className="text-white ml-2">
                    {COMPANIES.find(c => c.id === config.company)?.name}
                  </span>
                </div>
                <div>
                  <span className="text-dark-400">Difficulty:</span>
                  <span className="text-white ml-2">
                    {DIFFICULTIES.find(d => d.id === config.difficulty)?.name}
                  </span>
                </div>
                <div>
                  <span className="text-dark-400">Duration:</span>
                  <span className="text-white ml-2">{config.duration_minutes} minutes</span>
                </div>
              </div>
            </div>

            <div className="flex items-center justify-between">
              <button
                onClick={() => setStep(3)}
                className="text-dark-400 hover:text-white transition"
              >
                ← Go Back
              </button>
              
              <button
                onClick={handleStart}
                disabled={isStarting}
                className={cn(
                  'flex items-center gap-2 px-8 py-4 rounded-xl font-semibold text-lg transition',
                  isStarting
                    ? 'bg-purple-900 text-purple-400 cursor-not-allowed'
                    : 'bg-gradient-to-r from-purple-500 to-pink-500 hover:opacity-90 glow-purple'
                )}
              >
                <Zap className="w-5 h-5" />
                {isStarting ? 'Preparing...' : 'Start Interview'}
              </button>
            </div>
          </motion.div>
        )}
      </div>
    </div>
  )
}


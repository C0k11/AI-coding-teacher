'use client'

import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import Link from 'next/link'
import { useRouter } from 'next/navigation'
import { 
  ArrowLeft, 
  Clock, 
  CheckCircle2, 
  XCircle, 
  Code2,
  Calendar,
  Filter,
  ChevronDown
} from 'lucide-react'
import { auth } from '@/lib/api'
import { useTranslations } from '@/lib/i18n'

interface Submission {
  id: number
  problem_id: number
  problem_title: string
  problem_slug: string
  problem_difficulty: string
  code: string
  language: string
  status: string
  runtime_ms?: number
  memory_kb?: number
  ai_feedback?: string
  created_at: string
}

export default function HistoryPage() {
  const router = useRouter()
  const t = useTranslations()
  const [submissions, setSubmissions] = useState<Submission[]>([])
  const [loading, setLoading] = useState(true)
  const [filter, setFilter] = useState<string>('all')
  const [showFilter, setShowFilter] = useState(false)

  useEffect(() => {
    const token = localStorage.getItem('token')
    if (!token) {
      router.push('/login')
      return
    }

    fetchSubmissions(token)
  }, [router])

  const fetchSubmissions = async (token: string) => {
    try {
      const status = filter === 'all' ? undefined : filter
      const data = await auth.getSubmissions(token, status, 100)
      setSubmissions(data.submissions || [])
    } catch (error) {
      console.error('Failed to fetch submissions:', error)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    const token = localStorage.getItem('token')
    if (token) {
      setLoading(true)
      fetchSubmissions(token)
    }
  }, [filter])

  const getDifficultyColor = (difficulty: string) => {
    switch (difficulty) {
      case 'easy':
      case 'fundamental':
        return 'text-green-500 bg-green-500/10'
      case 'medium':
        return 'text-yellow-500 bg-yellow-500/10'
      case 'hard':
        return 'text-red-500 bg-red-500/10'
      default:
        return 'text-slate-500 bg-slate-500/10'
    }
  }

  const getStatusIcon = (status: string) => {
    if (status === 'accepted') {
      return <CheckCircle2 className="w-5 h-5 text-green-500" />
    }
    return <XCircle className="w-5 h-5 text-red-500" />
  }

  const getStatusText = (status: string) => {
    switch (status) {
      case 'accepted':
        return '通过'
      case 'wrong_answer':
        return '答案错误'
      case 'time_limit':
        return '超时'
      case 'runtime_error':
        return '运行错误'
      default:
        return status
    }
  }

  const formatDate = (dateStr: string) => {
    const date = new Date(dateStr)
    return date.toLocaleDateString('zh-CN', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  }

  return (
    <div className="min-h-screen bg-slate-50">
      {/* Header */}
      <header className="bg-white border-b border-slate-200 sticky top-0 z-10">
        <div className="max-w-6xl mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center gap-4">
            <Link href="/" className="p-2 hover:bg-slate-100 rounded-lg transition">
              <ArrowLeft className="w-5 h-5 text-slate-600" />
            </Link>
            <div>
              <h1 className="text-xl font-bold text-slate-800">刷题记录</h1>
              <p className="text-sm text-slate-500">查看你的所有提交历史</p>
            </div>
          </div>
          
          {/* Filter */}
          <div className="relative">
            <button
              onClick={() => setShowFilter(!showFilter)}
              className="flex items-center gap-2 px-4 py-2 bg-slate-100 hover:bg-slate-200 rounded-lg transition"
            >
              <Filter className="w-4 h-4" />
              <span>{filter === 'all' ? '全部' : filter === 'accepted' ? '已通过' : '未通过'}</span>
              <ChevronDown className="w-4 h-4" />
            </button>
            
            {showFilter && (
              <div className="absolute right-0 mt-2 w-40 bg-white rounded-lg shadow-lg border border-slate-200 py-2 z-20">
                {[
                  { value: 'all', label: '全部' },
                  { value: 'accepted', label: '已通过' },
                  { value: 'wrong_answer', label: '未通过' }
                ].map(option => (
                  <button
                    key={option.value}
                    onClick={() => {
                      setFilter(option.value)
                      setShowFilter(false)
                    }}
                    className={`w-full px-4 py-2 text-left hover:bg-slate-50 ${
                      filter === option.value ? 'text-blue-600 bg-blue-50' : 'text-slate-700'
                    }`}
                  >
                    {option.label}
                  </button>
                ))}
              </div>
            )}
          </div>
        </div>
      </header>

      {/* Content */}
      <main className="max-w-6xl mx-auto px-4 py-8">
        {loading ? (
          <div className="flex items-center justify-center py-20">
            <div className="w-8 h-8 border-4 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
          </div>
        ) : submissions.length === 0 ? (
          <div className="text-center py-20">
            <Code2 className="w-16 h-16 text-slate-300 mx-auto mb-4" />
            <h3 className="text-xl font-semibold text-slate-600 mb-2">暂无提交记录</h3>
            <p className="text-slate-500 mb-6">开始刷题，记录你的学习进度！</p>
            <Link
              href="/problems"
              className="inline-flex items-center gap-2 px-6 py-3 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition"
            >
              去刷题
            </Link>
          </div>
        ) : (
          <div className="space-y-4">
            {submissions.map((submission, index) => (
              <motion.div
                key={submission.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.05 }}
                className="bg-white rounded-xl border border-slate-200 p-4 hover:shadow-md transition"
              >
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-4">
                    {getStatusIcon(submission.status)}
                    <div>
                      <Link 
                        href={`/problems/${submission.problem_slug}`}
                        className="font-semibold text-slate-800 hover:text-blue-600 transition"
                      >
                        {submission.problem_title}
                      </Link>
                      <div className="flex items-center gap-3 mt-1">
                        <span className={`text-xs px-2 py-0.5 rounded-full font-medium ${getDifficultyColor(submission.problem_difficulty)}`}>
                          {submission.problem_difficulty === 'easy' ? 'Fundamental' : 
                           submission.problem_difficulty === 'medium' ? 'Medium' : 'Hard'}
                        </span>
                        <span className="text-sm text-slate-500">{submission.language}</span>
                        <span className={`text-sm ${submission.status === 'accepted' ? 'text-green-600' : 'text-red-600'}`}>
                          {getStatusText(submission.status)}
                        </span>
                      </div>
                    </div>
                  </div>
                  
                  <div className="text-right">
                    <div className="flex items-center gap-4 text-sm text-slate-500">
                      {submission.runtime_ms && (
                        <span className="flex items-center gap-1">
                          <Clock className="w-4 h-4" />
                          {submission.runtime_ms}ms
                        </span>
                      )}
                      <span className="flex items-center gap-1">
                        <Calendar className="w-4 h-4" />
                        {formatDate(submission.created_at)}
                      </span>
                    </div>
                  </div>
                </div>
                
                {/* Code Preview */}
                <details className="mt-3">
                  <summary className="text-sm text-blue-600 cursor-pointer hover:text-blue-700">
                    查看代码
                  </summary>
                  <pre className="mt-2 p-3 bg-slate-900 text-slate-100 rounded-lg text-sm overflow-x-auto">
                    <code>{submission.code}</code>
                  </pre>
                  {submission.ai_feedback && (
                    <div className="mt-2 p-3 bg-blue-50 rounded-lg">
                      <p className="text-sm text-blue-800">
                        <strong>AI 反馈：</strong> {submission.ai_feedback}
                      </p>
                    </div>
                  )}
                </details>
              </motion.div>
            ))}
          </div>
        )}
      </main>
    </div>
  )
}

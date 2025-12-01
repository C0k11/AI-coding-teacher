'use client'

import { useState, useEffect } from 'react'
import Link from 'next/link'
import { motion } from 'framer-motion'
import { 
  Search, 
  Filter, 
  CheckCircle, 
  Circle,
  ChevronRight,
  Code2,
  Building2,
  Tag
} from 'lucide-react'
import { cn, getDifficultyBadgeClass } from '@/lib/utils'
import { problems as problemsApi, type ProblemListItem } from '@/lib/api'

// Sample data for demo
const SAMPLE_PROBLEMS: ProblemListItem[] = [
  { id: 1, title: 'Two Sum', slug: 'two-sum', difficulty: 'easy', topics: ['array', 'hash_table'], companies: ['google', 'amazon'], acceptance_rate: 48.2, submission_count: 15234 },
  { id: 2, title: 'Valid Parentheses', slug: 'valid-parentheses', difficulty: 'easy', topics: ['string', 'stack'], companies: ['google', 'meta'], acceptance_rate: 42.8, submission_count: 12456 },
  { id: 3, title: 'LRU Cache', slug: 'lru-cache', difficulty: 'medium', topics: ['hash_table', 'linked_list'], companies: ['google', 'amazon', 'meta'], acceptance_rate: 35.6, submission_count: 8932 },
  { id: 4, title: 'Maximum Subarray', slug: 'maximum-subarray', difficulty: 'medium', topics: ['array', 'dp'], companies: ['google', 'microsoft'], acceptance_rate: 52.1, submission_count: 18234 },
  { id: 5, title: 'Binary Tree Level Order Traversal', slug: 'binary-tree-level-order-traversal', difficulty: 'medium', topics: ['tree', 'bfs'], companies: ['google', 'meta'], acceptance_rate: 58.3, submission_count: 9876 },
]

export default function ProblemsPage() {
  const [problems, setProblems] = useState<ProblemListItem[]>(SAMPLE_PROBLEMS)
  const [loading, setLoading] = useState(false)
  const [searchQuery, setSearchQuery] = useState('')
  const [difficulty, setDifficulty] = useState<string>('')
  const [topic, setTopic] = useState<string>('')
  const [company, setCompany] = useState<string>('')

  // Fetch problems from API
  useEffect(() => {
    const fetchProblems = async () => {
      setLoading(true)
      try {
        const data = await problemsApi.list({
          difficulty: difficulty || undefined,
          topic: topic || undefined,
          company: company || undefined,
          search: searchQuery || undefined,
        })
        if (data.length > 0) {
          setProblems(data)
        }
      } catch (error) {
        console.error('Failed to fetch problems:', error)
        // Keep sample data on error
      } finally {
        setLoading(false)
      }
    }

    fetchProblems()
  }, [difficulty, topic, company, searchQuery])

  const filteredProblems = problems.filter((problem) => {
    if (searchQuery && !problem.title.toLowerCase().includes(searchQuery.toLowerCase())) {
      return false
    }
    if (difficulty && problem.difficulty !== difficulty) {
      return false
    }
    if (topic && !problem.topics.includes(topic)) {
      return false
    }
    if (company && !problem.companies.includes(company)) {
      return false
    }
    return true
  })

  const stats = {
    total: problems.length,
    easy: problems.filter(p => p.difficulty === 'easy').length,
    medium: problems.filter(p => p.difficulty === 'medium').length,
    hard: problems.filter(p => p.difficulty === 'hard').length,
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
            <Link href="/problems" className="text-white font-medium">题库</Link>
            <Link href="/interview" className="text-dark-300 hover:text-white transition">面试</Link>
            <Link href="/battle" className="text-dark-300 hover:text-white transition">对战</Link>
            <Link href="/dashboard" className="text-dark-300 hover:text-white transition">仪表盘</Link>
          </div>
        </div>
      </nav>

      <div className="max-w-7xl mx-auto px-6 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold mb-2">题库</h1>
          <p className="text-dark-400">精选算法题，AI 个性化推荐，助你高效刷题</p>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-4 gap-4 mb-8">
          <div className="bg-dark-800 rounded-xl p-4 border border-dark-700">
            <div className="text-2xl font-bold">{stats.total}</div>
            <div className="text-dark-400 text-sm">总题目</div>
          </div>
          <div className="bg-dark-800 rounded-xl p-4 border border-dark-700">
            <div className="text-2xl font-bold text-green-400">{stats.easy}</div>
            <div className="text-dark-400 text-sm">简单</div>
          </div>
          <div className="bg-dark-800 rounded-xl p-4 border border-dark-700">
            <div className="text-2xl font-bold text-yellow-400">{stats.medium}</div>
            <div className="text-dark-400 text-sm">中等</div>
          </div>
          <div className="bg-dark-800 rounded-xl p-4 border border-dark-700">
            <div className="text-2xl font-bold text-red-400">{stats.hard}</div>
            <div className="text-dark-400 text-sm">困难</div>
          </div>
        </div>

        {/* Filters */}
        <div className="flex flex-wrap items-center gap-4 mb-6">
          <div className="relative flex-1 max-w-md">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-dark-400" />
            <input
              type="text"
              placeholder="搜索题目..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full pl-10 pr-4 py-2.5 bg-dark-800 border border-dark-700 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent"
            />
          </div>

          <select
            value={difficulty}
            onChange={(e) => setDifficulty(e.target.value)}
            className="px-4 py-2.5 bg-dark-800 border border-dark-700 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
          >
            <option value="">所有难度</option>
            <option value="easy">简单</option>
            <option value="medium">中等</option>
            <option value="hard">困难</option>
          </select>

          <select
            value={topic}
            onChange={(e) => setTopic(e.target.value)}
            className="px-4 py-2.5 bg-dark-800 border border-dark-700 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
          >
            <option value="">所有主题</option>
            <option value="array">数组</option>
            <option value="string">字符串</option>
            <option value="hash_table">哈希表</option>
            <option value="linked_list">链表</option>
            <option value="tree">树</option>
            <option value="dp">动态规划</option>
            <option value="graph">图</option>
          </select>

          <select
            value={company}
            onChange={(e) => setCompany(e.target.value)}
            className="px-4 py-2.5 bg-dark-800 border border-dark-700 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
          >
            <option value="">所有公司</option>
            <option value="google">Google</option>
            <option value="meta">Meta</option>
            <option value="amazon">Amazon</option>
            <option value="microsoft">Microsoft</option>
          </select>
        </div>

        {/* Problem List */}
        <div className="bg-dark-800 rounded-xl border border-dark-700 overflow-hidden">
          {/* Header */}
          <div className="grid grid-cols-12 gap-4 px-6 py-3 bg-dark-700/50 text-sm text-dark-400 font-medium">
            <div className="col-span-1">状态</div>
            <div className="col-span-5">题目</div>
            <div className="col-span-2">难度</div>
            <div className="col-span-2">通过率</div>
            <div className="col-span-2">公司</div>
          </div>

          {/* Problems */}
          <div className="divide-y divide-dark-700">
            {loading ? (
              <div className="px-6 py-12 text-center text-dark-400">
                加载中...
              </div>
            ) : filteredProblems.length === 0 ? (
              <div className="px-6 py-12 text-center text-dark-400">
                没有找到匹配的题目
              </div>
            ) : (
              filteredProblems.map((problem, i) => (
                <motion.div
                  key={problem.id}
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: i * 0.05 }}
                >
                  <Link href={`/problems/${problem.slug}`}>
                    <div className="grid grid-cols-12 gap-4 px-6 py-4 hover:bg-dark-700/50 transition cursor-pointer group">
                      <div className="col-span-1 flex items-center">
                        <Circle className="w-5 h-5 text-dark-500" />
                      </div>
                      <div className="col-span-5 flex items-center gap-2">
                        <span className="font-medium group-hover:text-purple-400 transition">
                          {problem.id}. {problem.title}
                        </span>
                        <ChevronRight className="w-4 h-4 text-dark-500 group-hover:text-purple-400 transition opacity-0 group-hover:opacity-100" />
                      </div>
                      <div className="col-span-2 flex items-center">
                        <span className={cn('px-2 py-0.5 rounded text-xs', getDifficultyBadgeClass(problem.difficulty))}>
                          {problem.difficulty === 'easy' ? '简单' : problem.difficulty === 'medium' ? '中等' : '困难'}
                        </span>
                      </div>
                      <div className="col-span-2 flex items-center text-dark-300">
                        {problem.acceptance_rate.toFixed(1)}%
                      </div>
                      <div className="col-span-2 flex items-center gap-1">
                        {problem.companies.slice(0, 2).map((c) => (
                          <span key={c} className="px-1.5 py-0.5 bg-dark-700 rounded text-xs text-dark-400">
                            {c}
                          </span>
                        ))}
                        {problem.companies.length > 2 && (
                          <span className="text-xs text-dark-500">+{problem.companies.length - 2}</span>
                        )}
                      </div>
                    </div>
                  </Link>
                </motion.div>
              ))
            )}
          </div>
        </div>
      </div>
    </div>
  )
}


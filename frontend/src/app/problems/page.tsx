'use client'

import { useState, useEffect } from 'react'
import Link from 'next/link'
import { useRouter } from 'next/navigation'
import { Search, Circle, User, LogOut } from 'lucide-react'
import { cn } from '@/lib/utils'
import { problems as problemsApi, type ProblemListItem } from '@/lib/api'

const SAMPLE_PROBLEMS: ProblemListItem[] = [
  { id: 1, title: 'Two Sum', slug: 'two-sum', difficulty: 'easy', topics: ['array', 'hash_table'], companies: [], acceptance_rate: 48.2, submission_count: 0 },
  { id: 2, title: 'Valid Parentheses', slug: 'valid-parentheses', difficulty: 'easy', topics: ['string', 'stack'], companies: [], acceptance_rate: 42.8, submission_count: 0 },
  { id: 3, title: 'LRU Cache', slug: 'lru-cache', difficulty: 'medium', topics: ['hash_table', 'linked_list'], companies: [], acceptance_rate: 35.6, submission_count: 0 },
  { id: 4, title: 'Maximum Subarray', slug: 'maximum-subarray', difficulty: 'medium', topics: ['array', 'dp'], companies: [], acceptance_rate: 52.1, submission_count: 0 },
  { id: 5, title: 'Binary Tree Level Order Traversal', slug: 'binary-tree-level-order-traversal', difficulty: 'medium', topics: ['tree', 'bfs'], companies: [], acceptance_rate: 58.3, submission_count: 0 },
]

const navItems = [
  { href: '/', label: 'Home' },
  { href: '/problems', label: 'Problems' },
  { href: '/battle', label: 'Battle' },
]

export default function ProblemsPage() {
  const router = useRouter()
  const [problems, setProblems] = useState<ProblemListItem[]>(SAMPLE_PROBLEMS)
  const [loading, setLoading] = useState(false)
  const [searchQuery, setSearchQuery] = useState('')
  const [difficulty, setDifficulty] = useState<string>('')
  const [user, setUser] = useState<{ name: string } | null>(null)

  useEffect(() => {
    const savedUser = localStorage.getItem('user')
    if (savedUser) {
      try { setUser(JSON.parse(savedUser)) } catch {}
    }
  }, [])

  const handleLogout = () => {
    localStorage.removeItem('token')
    localStorage.removeItem('user')
    setUser(null)
    router.refresh()
  }

  useEffect(() => {
    const fetchProblems = async () => {
      setLoading(true)
      try {
        const data = await problemsApi.list({ difficulty: difficulty || undefined, search: searchQuery || undefined })
        if (data.length > 0) setProblems(data)
      } catch (error) {
        console.error('Failed to fetch problems:', error)
      } finally {
        setLoading(false)
      }
    }
    fetchProblems()
  }, [difficulty, searchQuery])

  const filteredProblems = problems.filter((problem) => {
    if (searchQuery && !problem.title.toLowerCase().includes(searchQuery.toLowerCase())) return false
    if (difficulty && problem.difficulty !== difficulty) return false
    return true
  })

  return (
    <div className="min-h-screen bg-white">
      {/* Navigation */}
      <header className="fixed top-0 left-0 right-0 z-50 bg-white border-b border-slate-200">
        <div className="container mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <Link href="/" className="text-xl font-bold">
              <span className="text-slate-900">Cok</span>
              <span className="text-blue-600">11</span>
            </Link>
            <div className="flex items-center gap-6">
              {navItems.map((item) => (
                <Link key={item.href} href={item.href} className={cn(
                  "font-medium transition-colors",
                  item.href === '/problems' ? "text-slate-900" : "text-slate-600 hover:text-slate-900"
                )}>
                  {item.label}
                </Link>
              ))}
            </div>
            <div className="flex items-center gap-4">
              {user ? (
                <div className="flex items-center gap-3">
                  <span className="text-slate-700 font-medium flex items-center gap-2">
                    <User className="w-4 h-4" /> {user.name}
                  </span>
                  <button onClick={handleLogout} className="text-slate-500 hover:text-slate-700">
                    <LogOut className="w-4 h-4" />
                  </button>
                </div>
              ) : (
                <Link href="/login" className="px-4 py-2 bg-slate-900 text-white rounded-md font-medium hover:bg-slate-800">
                  Sign in
                </Link>
              )}
            </div>
          </div>
        </div>
      </header>

      <div className="container mx-auto px-6 pt-24 pb-12">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-2xl font-bold text-slate-900 mb-1">Problems</h1>
          <p className="text-slate-500">Practice algorithm problems to improve your coding skills</p>
        </div>

        {/* Filters */}
        <div className="flex items-center gap-4 mb-6">
          <div className="relative flex-1 max-w-sm">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
            <input
              type="text"
              placeholder="Search problems..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full pl-10 pr-4 py-2 border border-slate-200 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
          <select
            value={difficulty}
            onChange={(e) => setDifficulty(e.target.value)}
            className="px-3 py-2 border border-slate-200 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="">All Difficulty</option>
            <option value="easy">Easy</option>
            <option value="medium">Medium</option>
            <option value="hard">Hard</option>
          </select>
        </div>

        {/* Problem List */}
        <div className="border border-slate-200 rounded-md overflow-hidden">
          <table className="w-full">
            <thead className="bg-slate-50 border-b border-slate-200">
              <tr className="text-left text-sm text-slate-500">
                <th className="px-4 py-3 w-12">Status</th>
                <th className="px-4 py-3">Title</th>
                <th className="px-4 py-3 w-24">Difficulty</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {loading ? (
                <tr><td colSpan={3} className="px-4 py-8 text-center text-slate-400">Loading...</td></tr>
              ) : filteredProblems.length === 0 ? (
                <tr><td colSpan={3} className="px-4 py-8 text-center text-slate-400">No problems found</td></tr>
              ) : (
                filteredProblems.map((problem) => (
                  <tr key={problem.id} className="hover:bg-slate-50">
                    <td className="px-4 py-3">
                      <Circle className="w-4 h-4 text-slate-300" />
                    </td>
                    <td className="px-4 py-3">
                      <Link href={`/problems/${problem.slug}`} className="text-slate-900 hover:text-blue-600 font-medium">
                        {problem.id}. {problem.title}
                      </Link>
                    </td>
                    <td className="px-4 py-3">
                      <span className={cn(
                        'px-2 py-0.5 rounded text-xs font-medium',
                        problem.difficulty === 'easy' ? 'bg-emerald-100 text-emerald-700' :
                        problem.difficulty === 'medium' ? 'bg-amber-100 text-amber-700' : 'bg-red-100 text-red-700'
                      )}>
                        {problem.difficulty.charAt(0).toUpperCase() + problem.difficulty.slice(1)}
                      </span>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}


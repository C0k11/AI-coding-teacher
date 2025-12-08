'use client'

import { useState, useCallback, useEffect } from 'react'
import Link from 'next/link'
import { useRouter } from 'next/navigation'
import { motion } from 'framer-motion'
import ReactFlow, {
  Node,
  Edge,
  Background,
  Controls,
  MiniMap,
  useNodesState,
  useEdgesState,
} from 'reactflow'
import 'reactflow/dist/style.css'
import {
  Swords,
  Trophy,
  Target,
  Flame,
  BookOpen,
  User,
  LogOut,
  History,
  Code2
} from 'lucide-react'
import { cn } from '@/lib/utils'
import { useAuthStore } from '@/store/useStore'
import { useTranslations } from '@/lib/i18n'
import LanguageSwitcher from '@/components/LanguageSwitcher'
import { auth } from '@/lib/api'


// Knowledge Graph Data
const initialNodes: Node[] = [
  { id: 'array', position: { x: 250, y: 0 }, data: { label: 'Array', mastery: 0.8 }, type: 'custom' },
  { id: 'string', position: { x: 450, y: 0 }, data: { label: 'String', mastery: 0.7 }, type: 'custom' },
  { id: 'hash_table', position: { x: 350, y: 100 }, data: { label: 'Hash Table', mastery: 0.75 }, type: 'custom' },
  { id: 'two_pointers', position: { x: 150, y: 150 }, data: { label: 'Two Pointers', mastery: 0.65 }, type: 'custom' },
  { id: 'sliding_window', position: { x: 50, y: 250 }, data: { label: 'Sliding Window', mastery: 0.5 }, type: 'custom' },
  { id: 'linked_list', position: { x: 550, y: 150 }, data: { label: 'Linked List', mastery: 0.6 }, type: 'custom' },
  { id: 'stack', position: { x: 450, y: 200 }, data: { label: 'Stack', mastery: 0.7 }, type: 'custom' },
  { id: 'queue', position: { x: 250, y: 200 }, data: { label: 'Queue', mastery: 0.55 }, type: 'custom' },
  { id: 'tree', position: { x: 450, y: 300 }, data: { label: 'Tree', mastery: 0.5 }, type: 'custom' },
  { id: 'binary_tree', position: { x: 350, y: 380 }, data: { label: 'Binary Tree', mastery: 0.45 }, type: 'custom' },
  { id: 'bfs', position: { x: 200, y: 350 }, data: { label: 'BFS', mastery: 0.4 }, type: 'custom' },
  { id: 'dfs', position: { x: 500, y: 380 }, data: { label: 'DFS', mastery: 0.35 }, type: 'custom' },
  { id: 'graph', position: { x: 350, y: 480 }, data: { label: 'Graph', mastery: 0.25 }, type: 'custom' },
  { id: 'dp', position: { x: 150, y: 480 }, data: { label: 'DP', mastery: 0.2 }, type: 'custom' },
  { id: 'backtracking', position: { x: 550, y: 480 }, data: { label: 'Backtracking', mastery: 0.3 }, type: 'custom' },
]

const initialEdges: Edge[] = [
  { id: 'e1', source: 'array', target: 'hash_table', type: 'smoothstep', animated: true },
  { id: 'e2', source: 'array', target: 'two_pointers', type: 'smoothstep' },
  { id: 'e3', source: 'two_pointers', target: 'sliding_window', type: 'smoothstep' },
  { id: 'e4', source: 'array', target: 'stack', type: 'smoothstep' },
  { id: 'e5', source: 'array', target: 'queue', type: 'smoothstep' },
  { id: 'e6', source: 'linked_list', target: 'tree', type: 'smoothstep' },
  { id: 'e7', source: 'tree', target: 'binary_tree', type: 'smoothstep' },
  { id: 'e8', source: 'queue', target: 'bfs', type: 'smoothstep' },
  { id: 'e9', source: 'stack', target: 'dfs', type: 'smoothstep' },
  { id: 'e10', source: 'tree', target: 'graph', type: 'smoothstep' },
  { id: 'e11', source: 'bfs', target: 'graph', type: 'smoothstep' },
  { id: 'e12', source: 'dfs', target: 'graph', type: 'smoothstep' },
  { id: 'e13', source: 'dfs', target: 'backtracking', type: 'smoothstep' },
  { id: 'e14', source: 'backtracking', target: 'dp', type: 'smoothstep' },
]

// Custom Node Component
function CustomNode({ data }: { data: { label: string; mastery: number } }) {
  const getMasteryColor = (mastery: number) => {
    if (mastery >= 0.7) return 'bg-emerald-500'
    if (mastery >= 0.4) return 'bg-amber-500'
    return 'bg-red-500'
  }

  return (
    <div className={cn(
      'px-4 py-2 rounded-md border bg-white shadow-sm',
      data.mastery >= 0.7 ? 'border-emerald-300' :
      data.mastery >= 0.4 ? 'border-amber-300' : 'border-red-300'
    )}>
      <div className="text-sm font-medium text-slate-900">{data.label}</div>
      <div className="flex items-center gap-2 mt-1">
        <div className="flex-1 h-1.5 bg-slate-100 rounded-full overflow-hidden">
          <div
            className={`h-full ${getMasteryColor(data.mastery)}`}
            style={{ width: `${data.mastery * 100}%` }}
          />
        </div>
        <span className="text-xs text-slate-500">{Math.round(data.mastery * 100)}%</span>
      </div>
    </div>
  )
}

const nodeTypes = { custom: CustomNode }

const DEFAULT_STATS = {
  problems_solved: 0,
  battles_won: 0,
  current_streak: 0,
  elo_rating: 1200,
}


export default function DashboardPage() {
  const router = useRouter()
  const t = useTranslations()
  const { user: authUser } = useAuthStore()
  const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes)
  const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges)
  const [selectedNode, setSelectedNode] = useState<string | null>(null)
  const [user, setUser] = useState<{ name: string } | null>(null)
  const [stats, setStats] = useState(DEFAULT_STATS)

  const navItems = [
    { href: '/', label: t.nav.home },
    { href: '/problems', label: t.nav.problems },
    { href: '/battle', label: t.nav.battle },
    { href: '/dashboard', label: t.nav.dashboard },
  ]

  useEffect(() => {
    const savedUser = localStorage.getItem('user')
    if (savedUser) {
      try {
        setUser(JSON.parse(savedUser))
      } catch {}
    }
    
    // Fetch latest stats from server
    const token = localStorage.getItem('token')
    if (token) {
      auth.getStats(token).then(data => {
        setStats({
          problems_solved: data.problems_solved || 0,
          battles_won: data.battles_won || 0,
          current_streak: data.current_streak || 0,
          elo_rating: data.elo_rating || 1200,
        })
      }).catch(console.error)
    }
  }, [])

  const handleLogout = () => {
    localStorage.removeItem('token')
    localStorage.removeItem('user')
    setUser(null)
    router.push('/')
  }

  const onNodeClick = useCallback((event: React.MouseEvent, node: Node) => {
    setSelectedNode(node.id)
  }, [])

  return (
    <div className="min-h-screen bg-slate-50">
      {/* Navigation */}
      <header className="fixed top-0 left-0 right-0 z-50 bg-white border-b border-slate-200">
        <div className="container mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <Link href="/" className="flex items-center">
              <span className="text-xl font-bold tracking-tight">
                <span className="text-slate-900">Cok</span>
                <span className="text-blue-600">11</span>
              </span>
            </Link>

            <div className="hidden md:flex items-center gap-6">
              {navItems.map((item) => (
                <Link
                  key={item.href}
                  href={item.href}
                  className={cn(
                    "font-medium transition-colors",
                    item.href === '/dashboard' ? "text-slate-900" : "text-slate-600 hover:text-slate-900"
                  )}
                >
                  {item.label}
                </Link>
              ))}
            </div>

            <div className="hidden md:flex items-center gap-4">
              <LanguageSwitcher />
              {user ? (
                <div className="flex items-center gap-4">
                  <div className="flex items-center gap-2 text-slate-700">
                    <User className="w-4 h-4" />
                    <span className="font-medium">{user.name}</span>
                  </div>
                  <button onClick={handleLogout} className="text-slate-500 hover:text-slate-700">
                    <LogOut className="w-4 h-4" />
                  </button>
                </div>
              ) : (
                <Link href="/login" className="px-4 py-2 text-white bg-slate-900 hover:bg-slate-800 rounded-md font-medium">
                  {t.nav.signIn}
                </Link>
              )}
            </div>
          </div>
        </div>
      </header>

      <div className="container mx-auto px-6 pt-28 pb-12">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-slate-900 mb-2">
            {t.dashboard.welcome}, {user?.name || t.common.developer}
          </h1>
          <p className="text-slate-500">{t.dashboard.subtitle}</p>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
          <div className="bg-white rounded-md p-4 border border-slate-200">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-md bg-emerald-50 flex items-center justify-center">
                <Target className="w-5 h-5 text-emerald-600" />
              </div>
              <div>
                <div className="text-2xl font-bold text-slate-900">{stats.problems_solved}</div>
                <div className="text-xs text-slate-500">{t.dashboard.problemsSolved}</div>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-md p-4 border border-slate-200">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-md bg-blue-50 flex items-center justify-center">
                <Swords className="w-5 h-5 text-blue-600" />
              </div>
              <div>
                <div className="text-2xl font-bold text-slate-900">{stats.battles_won}</div>
                <div className="text-xs text-slate-500">{t.dashboard.battlesWon}</div>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-md p-4 border border-slate-200">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-md bg-orange-50 flex items-center justify-center">
                <Flame className="w-5 h-5 text-orange-600" />
              </div>
              <div>
                <div className="text-2xl font-bold text-slate-900">{stats.current_streak}</div>
                <div className="text-xs text-slate-500">{t.dashboard.dayStreak}</div>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-md p-4 border border-slate-200">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-md bg-amber-50 flex items-center justify-center">
                <Trophy className="w-5 h-5 text-amber-600" />
              </div>
              <div>
                <div className="text-2xl font-bold text-slate-900">{stats.elo_rating}</div>
                <div className="text-xs text-slate-500">{t.dashboard.eloRating}</div>
              </div>
            </div>
          </div>
        </div>

        <div className="grid md:grid-cols-3 gap-6">
          {/* Knowledge Graph */}
          <div className="md:col-span-2">
            <div className="bg-white rounded-md border border-slate-200 overflow-hidden">
              <div className="px-6 py-4 border-b border-slate-100 flex items-center justify-between">
                <h2 className="text-lg font-semibold text-slate-900 flex items-center gap-2">
                  <BookOpen className="w-5 h-5 text-blue-600" />
                  {t.dashboard.knowledgeGraph}
                </h2>
                <span className="text-sm text-slate-500">{t.dashboard.clickForDetails}</span>
              </div>
              <div style={{ height: 500 }}>
                <ReactFlow
                  nodes={nodes}
                  edges={edges}
                  onNodesChange={onNodesChange}
                  onEdgesChange={onEdgesChange}
                  onNodeClick={onNodeClick}
                  nodeTypes={nodeTypes}
                  fitView
                  attributionPosition="bottom-left"
                >
                  <Background color="#e2e8f0" gap={20} />
                  <Controls />
                  <MiniMap 
                    nodeColor={(node) => {
                      const mastery = node.data?.mastery || 0
                      if (mastery >= 0.7) return '#10b981'
                      if (mastery >= 0.4) return '#f59e0b'
                      return '#ef4444'
                    }}
                  />
                </ReactFlow>
              </div>
            </div>
          </div>

          {/* Right Sidebar */}
          <div className="space-y-6">
            {/* Quick Actions */}
            <div className="bg-white rounded-md border border-slate-200 p-4">
              <h3 className="font-semibold text-slate-900 mb-4">{t.dashboard.quickActions}</h3>
              <div className="space-y-3">
                <Link
                  href="/problems"
                  className="flex items-center gap-3 p-3 bg-slate-50 rounded-md hover:bg-slate-100 transition"
                >
                  <BookOpen className="w-5 h-5 text-blue-600" />
                  <span className="font-medium text-slate-900">{t.dashboard.practiceProblems}</span>
                </Link>
                <Link
                  href="/battle"
                  className="flex items-center gap-3 p-3 bg-slate-50 rounded-md hover:bg-slate-100 transition"
                >
                  <Swords className="w-5 h-5 text-blue-600" />
                  <span className="font-medium text-slate-900">{t.dashboard.codeBattle}</span>
                </Link>
                <Link
                  href="/history"
                  className="flex items-center gap-3 p-3 bg-slate-50 rounded-md hover:bg-slate-100 transition"
                >
                  <History className="w-5 h-5 text-emerald-600" />
                  <span className="font-medium text-slate-900">{t.dashboard.submissionHistory}</span>
                </Link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}


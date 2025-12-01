'use client'

import { useState, useCallback } from 'react'
import Link from 'next/link'
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
  Code2,
  Brain,
  Swords,
  Trophy,
  Target,
  TrendingUp,
  Calendar,
  Flame,
  BookOpen,
  ChevronRight,
  Star
} from 'lucide-react'
import { cn, getDifficultyBadgeClass } from '@/lib/utils'
import { useAuthStore } from '@/store/useStore'

// Knowledge Graph Data
const initialNodes: Node[] = [
  { id: 'array', position: { x: 250, y: 0 }, data: { label: '数组', mastery: 0.8 }, type: 'custom' },
  { id: 'string', position: { x: 450, y: 0 }, data: { label: '字符串', mastery: 0.7 }, type: 'custom' },
  { id: 'hash_table', position: { x: 350, y: 100 }, data: { label: '哈希表', mastery: 0.75 }, type: 'custom' },
  { id: 'two_pointers', position: { x: 150, y: 150 }, data: { label: '双指针', mastery: 0.65 }, type: 'custom' },
  { id: 'sliding_window', position: { x: 50, y: 250 }, data: { label: '滑动窗口', mastery: 0.5 }, type: 'custom' },
  { id: 'linked_list', position: { x: 550, y: 150 }, data: { label: '链表', mastery: 0.6 }, type: 'custom' },
  { id: 'stack', position: { x: 450, y: 200 }, data: { label: '栈', mastery: 0.7 }, type: 'custom' },
  { id: 'queue', position: { x: 250, y: 200 }, data: { label: '队列', mastery: 0.55 }, type: 'custom' },
  { id: 'tree', position: { x: 450, y: 300 }, data: { label: '树', mastery: 0.5 }, type: 'custom' },
  { id: 'binary_tree', position: { x: 350, y: 380 }, data: { label: '二叉树', mastery: 0.45 }, type: 'custom' },
  { id: 'bfs', position: { x: 200, y: 350 }, data: { label: 'BFS', mastery: 0.4 }, type: 'custom' },
  { id: 'dfs', position: { x: 500, y: 380 }, data: { label: 'DFS', mastery: 0.35 }, type: 'custom' },
  { id: 'graph', position: { x: 350, y: 480 }, data: { label: '图', mastery: 0.25 }, type: 'custom' },
  { id: 'dp', position: { x: 150, y: 480 }, data: { label: '动态规划', mastery: 0.2 }, type: 'custom' },
  { id: 'backtracking', position: { x: 550, y: 480 }, data: { label: '回溯', mastery: 0.3 }, type: 'custom' },
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
    if (mastery >= 0.7) return 'from-green-500 to-emerald-500'
    if (mastery >= 0.4) return 'from-yellow-500 to-orange-500'
    return 'from-red-500 to-pink-500'
  }

  return (
    <div className={cn(
      'px-4 py-2 rounded-lg border-2 bg-dark-800 shadow-lg',
      data.mastery >= 0.7 ? 'border-green-500/50' :
      data.mastery >= 0.4 ? 'border-yellow-500/50' : 'border-red-500/50'
    )}>
      <div className="text-sm font-medium text-white">{data.label}</div>
      <div className="flex items-center gap-2 mt-1">
        <div className="flex-1 h-1.5 bg-dark-600 rounded-full overflow-hidden">
          <div
            className={`h-full bg-gradient-to-r ${getMasteryColor(data.mastery)}`}
            style={{ width: `${data.mastery * 100}%` }}
          />
        </div>
        <span className="text-xs text-dark-400">{Math.round(data.mastery * 100)}%</span>
      </div>
    </div>
  )
}

const nodeTypes = { custom: CustomNode }

// Mock Data
const MOCK_STATS = {
  problems_solved: 47,
  total_problems: 100,
  interviews_completed: 8,
  battles_won: 12,
  current_streak: 5,
  elo_rating: 1450,
}

const MOCK_RECENT_ACTIVITY = [
  { type: 'problem', title: 'Two Sum', result: 'accepted', time: '2小时前' },
  { type: 'interview', title: 'Google 算法面试', result: '7.5/10', time: '昨天' },
  { type: 'battle', title: '对战 @CodeMaster', result: 'win', time: '2天前' },
  { type: 'problem', title: 'LRU Cache', result: 'accepted', time: '3天前' },
]

const MOCK_RECOMMENDED = [
  { id: 1, title: 'Maximum Subarray', difficulty: 'medium', reason: '巩固动态规划' },
  { id: 2, title: 'Binary Tree Traversal', difficulty: 'easy', reason: '加强树结构' },
  { id: 3, title: 'Graph BFS', difficulty: 'medium', reason: '探索图算法' },
]

export default function DashboardPage() {
  const { user } = useAuthStore()
  const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes)
  const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges)
  const [selectedNode, setSelectedNode] = useState<string | null>(null)

  const onNodeClick = useCallback((event: React.MouseEvent, node: Node) => {
    setSelectedNode(node.id)
  }, [])

  const stats = user ? {
    problems_solved: user.problems_solved,
    interviews_completed: user.interviews_completed,
    battles_won: user.battles_won,
    current_streak: user.current_streak,
    elo_rating: user.elo_rating,
  } : MOCK_STATS

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
            <Link href="/problems" className="text-dark-300 hover:text-white transition">题库</Link>
            <Link href="/interview" className="text-dark-300 hover:text-white transition">面试</Link>
            <Link href="/battle" className="text-dark-300 hover:text-white transition">对战</Link>
            <Link href="/dashboard" className="text-white font-medium">仪表盘</Link>
          </div>
        </div>
      </nav>

      <div className="max-w-7xl mx-auto px-6 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold mb-2">
            你好，{user?.username || '学习者'} 👋
          </h1>
          <p className="text-dark-400">继续保持学习，你正在变得更强！</p>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-2 md:grid-cols-5 gap-4 mb-8">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="bg-dark-800 rounded-xl p-4 border border-dark-700"
          >
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-lg bg-green-500/20 flex items-center justify-center">
                <Target className="w-5 h-5 text-green-400" />
              </div>
              <div>
                <div className="text-2xl font-bold">{stats.problems_solved}</div>
                <div className="text-xs text-dark-400">已解决题目</div>
              </div>
            </div>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
            className="bg-dark-800 rounded-xl p-4 border border-dark-700"
          >
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-lg bg-purple-500/20 flex items-center justify-center">
                <Brain className="w-5 h-5 text-purple-400" />
              </div>
              <div>
                <div className="text-2xl font-bold">{stats.interviews_completed}</div>
                <div className="text-xs text-dark-400">模拟面试</div>
              </div>
            </div>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
            className="bg-dark-800 rounded-xl p-4 border border-dark-700"
          >
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-lg bg-orange-500/20 flex items-center justify-center">
                <Swords className="w-5 h-5 text-orange-400" />
              </div>
              <div>
                <div className="text-2xl font-bold">{stats.battles_won}</div>
                <div className="text-xs text-dark-400">对战胜利</div>
              </div>
            </div>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
            className="bg-dark-800 rounded-xl p-4 border border-dark-700"
          >
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-lg bg-red-500/20 flex items-center justify-center">
                <Flame className="w-5 h-5 text-red-400" />
              </div>
              <div>
                <div className="text-2xl font-bold">{stats.current_streak}</div>
                <div className="text-xs text-dark-400">连续天数</div>
              </div>
            </div>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4 }}
            className="bg-dark-800 rounded-xl p-4 border border-dark-700"
          >
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-lg bg-yellow-500/20 flex items-center justify-center">
                <Trophy className="w-5 h-5 text-yellow-400" />
              </div>
              <div>
                <div className="text-2xl font-bold">{stats.elo_rating}</div>
                <div className="text-xs text-dark-400">ELO 积分</div>
              </div>
            </div>
          </motion.div>
        </div>

        <div className="grid md:grid-cols-3 gap-6">
          {/* Knowledge Graph */}
          <div className="md:col-span-2">
            <div className="bg-dark-800 rounded-xl border border-dark-700 overflow-hidden">
              <div className="px-6 py-4 border-b border-dark-700 flex items-center justify-between">
                <h2 className="text-lg font-semibold flex items-center gap-2">
                  <BookOpen className="w-5 h-5 text-purple-400" />
                  知识图谱
                </h2>
                <span className="text-sm text-dark-400">点击节点查看详情</span>
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
                  <Background color="#30363d" gap={20} />
                  <Controls className="bg-dark-700 border-dark-600" />
                  <MiniMap 
                    nodeColor={(node) => {
                      const mastery = node.data?.mastery || 0
                      if (mastery >= 0.7) return '#22c55e'
                      if (mastery >= 0.4) return '#eab308'
                      return '#ef4444'
                    }}
                    className="bg-dark-800 border-dark-700"
                  />
                </ReactFlow>
              </div>
            </div>
          </div>

          {/* Right Sidebar */}
          <div className="space-y-6">
            {/* Recommended Problems */}
            <div className="bg-dark-800 rounded-xl border border-dark-700">
              <div className="px-4 py-3 border-b border-dark-700 flex items-center justify-between">
                <h3 className="font-semibold flex items-center gap-2">
                  <Star className="w-4 h-4 text-yellow-400" />
                  推荐练习
                </h3>
                <Link href="/problems" className="text-sm text-purple-400 hover:text-purple-300">
                  查看全部
                </Link>
              </div>
              <div className="divide-y divide-dark-700">
                {MOCK_RECOMMENDED.map((problem) => (
                  <Link
                    key={problem.id}
                    href={`/problems/${problem.title.toLowerCase().replace(/ /g, '-')}`}
                    className="block px-4 py-3 hover:bg-dark-700/50 transition"
                  >
                    <div className="flex items-center justify-between mb-1">
                      <span className="font-medium">{problem.title}</span>
                      <span className={cn(
                        'px-2 py-0.5 rounded text-xs',
                        getDifficultyBadgeClass(problem.difficulty)
                      )}>
                        {problem.difficulty}
                      </span>
                    </div>
                    <div className="text-xs text-dark-400">{problem.reason}</div>
                  </Link>
                ))}
              </div>
            </div>

            {/* Recent Activity */}
            <div className="bg-dark-800 rounded-xl border border-dark-700">
              <div className="px-4 py-3 border-b border-dark-700">
                <h3 className="font-semibold flex items-center gap-2">
                  <TrendingUp className="w-4 h-4 text-green-400" />
                  最近活动
                </h3>
              </div>
              <div className="divide-y divide-dark-700">
                {MOCK_RECENT_ACTIVITY.map((activity, i) => (
                  <div key={i} className="px-4 py-3 flex items-center gap-3">
                    <div className={cn(
                      'w-8 h-8 rounded-lg flex items-center justify-center',
                      activity.type === 'problem' ? 'bg-green-500/20' :
                      activity.type === 'interview' ? 'bg-purple-500/20' : 'bg-orange-500/20'
                    )}>
                      {activity.type === 'problem' ? <Code2 className="w-4 h-4 text-green-400" /> :
                       activity.type === 'interview' ? <Brain className="w-4 h-4 text-purple-400" /> :
                       <Swords className="w-4 h-4 text-orange-400" />}
                    </div>
                    <div className="flex-1 min-w-0">
                      <div className="font-medium text-sm truncate">{activity.title}</div>
                      <div className="text-xs text-dark-400">{activity.time}</div>
                    </div>
                    <span className={cn(
                      'text-xs px-2 py-0.5 rounded',
                      activity.result === 'accepted' || activity.result === 'win'
                        ? 'bg-green-500/20 text-green-400'
                        : 'bg-purple-500/20 text-purple-400'
                    )}>
                      {activity.result}
                    </span>
                  </div>
                ))}
              </div>
            </div>

            {/* Quick Actions */}
            <div className="grid grid-cols-2 gap-3">
              <Link
                href="/interview"
                className="p-4 bg-purple-500/10 border border-purple-500/30 rounded-xl hover:bg-purple-500/20 transition text-center"
              >
                <Brain className="w-6 h-6 mx-auto mb-2 text-purple-400" />
                <span className="text-sm font-medium">开始面试</span>
              </Link>
              <Link
                href="/battle"
                className="p-4 bg-orange-500/10 border border-orange-500/30 rounded-xl hover:bg-orange-500/20 transition text-center"
              >
                <Swords className="w-6 h-6 mx-auto mb-2 text-orange-400" />
                <span className="text-sm font-medium">快速对战</span>
              </Link>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}


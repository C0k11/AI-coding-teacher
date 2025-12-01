'use client'

import { motion } from 'framer-motion'
import Link from 'next/link'
import { 
  Code2, 
  Brain, 
  Swords, 
  GitBranch, 
  Trophy,
  Zap,
  Users,
  Target
} from 'lucide-react'

const features = [
  {
    icon: Brain,
    title: 'AI 面试官模拟',
    description: '真实模拟 Google、Meta、Amazon 等大厂技术面试，获得即时反馈和评分报告',
    color: 'from-purple-500 to-pink-500',
    href: '/interview'
  },
  {
    icon: Code2,
    title: '智能题库系统',
    description: '500+ 精选算法题，AI 个性化推荐，渐进式提示，多语言支持',
    color: 'from-blue-500 to-cyan-500',
    href: '/problems'
  },
  {
    icon: Swords,
    title: '代码对战',
    description: '实时 1v1 对战，全球排行榜，锦标赛模式，让刷题更有趣',
    color: 'from-orange-500 to-red-500',
    href: '/battle'
  },
  {
    icon: GitBranch,
    title: '知识图谱',
    description: '可视化学习路径，追踪掌握程度，智能推荐下一步学习内容',
    color: 'from-green-500 to-emerald-500',
    href: '/dashboard'
  }
]

const stats = [
  { label: '题目数量', value: '500+' },
  { label: '模拟面试', value: '1000+' },
  { label: '活跃用户', value: '10K+' },
  { label: '代码对战', value: '50K+' }
]

export default function Home() {
  return (
    <main className="min-h-screen">
      {/* Navigation */}
      <nav className="fixed top-0 w-full z-50 bg-dark-900/80 backdrop-blur-xl border-b border-dark-700">
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
            <Link href="/dashboard" className="text-dark-300 hover:text-white transition">仪表盘</Link>
            <Link 
              href="/login" 
              className="px-4 py-2 rounded-lg bg-gradient-to-r from-purple-500 to-pink-500 hover:opacity-90 transition font-medium"
            >
              登录
            </Link>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="pt-32 pb-20 px-6 relative overflow-hidden">
        {/* Background effects */}
        <div className="absolute inset-0 overflow-hidden">
          <div className="absolute -top-40 -right-40 w-96 h-96 bg-purple-500/20 rounded-full blur-3xl" />
          <div className="absolute top-40 -left-40 w-96 h-96 bg-pink-500/20 rounded-full blur-3xl" />
          <div className="absolute bottom-0 left-1/2 w-96 h-96 bg-blue-500/10 rounded-full blur-3xl" />
        </div>

        <div className="max-w-7xl mx-auto relative">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            className="text-center"
          >
            <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-dark-700/50 border border-dark-600 mb-6">
              <span className="pulse-dot" />
              <span className="text-sm text-dark-300">AI 驱动的新一代编程学习平台</span>
            </div>
            
            <h1 className="text-5xl md:text-7xl font-bold mb-6 leading-tight">
              用 <span className="gradient-text">AI</span> 征服
              <br />
              技术面试
            </h1>
            
            <p className="text-xl text-dark-300 max-w-2xl mx-auto mb-10">
              不只是刷题，是完整的学习系统。AI 个性化指导，
              真实面试模拟，项目驱动学习，社交对战。
            </p>

            <div className="flex items-center justify-center gap-4">
              <Link 
                href="/interview"
                className="px-8 py-4 rounded-xl bg-gradient-to-r from-purple-500 to-pink-500 hover:opacity-90 transition font-semibold text-lg flex items-center gap-2 glow-purple"
              >
                <Brain className="w-5 h-5" />
                开始模拟面试
              </Link>
              <Link 
                href="/problems"
                className="px-8 py-4 rounded-xl bg-dark-700 hover:bg-dark-600 transition font-semibold text-lg border border-dark-600"
              >
                浏览题库
              </Link>
            </div>
          </motion.div>

          {/* Stats */}
          <motion.div 
            initial={{ opacity: 0, y: 40 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.3 }}
            className="grid grid-cols-2 md:grid-cols-4 gap-6 mt-20"
          >
            {stats.map((stat, i) => (
              <div 
                key={stat.label}
                className="text-center p-6 rounded-2xl bg-dark-800/50 border border-dark-700"
              >
                <div className="text-3xl font-bold gradient-text mb-1">{stat.value}</div>
                <div className="text-dark-400">{stat.label}</div>
              </div>
            ))}
          </motion.div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 px-6">
        <div className="max-w-7xl mx-auto">
          <motion.div
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-4xl font-bold mb-4">核心功能</h2>
            <p className="text-dark-300 text-lg">全方位提升你的编程能力和面试表现</p>
          </motion.div>

          <div className="grid md:grid-cols-2 gap-6">
            {features.map((feature, i) => (
              <motion.div
                key={feature.title}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: i * 0.1 }}
              >
                <Link href={feature.href}>
                  <div className="group p-8 rounded-2xl bg-dark-800/50 border border-dark-700 hover:border-dark-500 transition card-hover h-full">
                    <div className={`w-14 h-14 rounded-xl bg-gradient-to-br ${feature.color} flex items-center justify-center mb-6 group-hover:scale-110 transition`}>
                      <feature.icon className="w-7 h-7 text-white" />
                    </div>
                    <h3 className="text-2xl font-bold mb-3">{feature.title}</h3>
                    <p className="text-dark-300">{feature.description}</p>
                  </div>
                </Link>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Interview Preview Section */}
      <section className="py-20 px-6 bg-dark-800/30">
        <div className="max-w-7xl mx-auto">
          <div className="grid md:grid-cols-2 gap-12 items-center">
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true }}
            >
              <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-purple-500/20 text-purple-400 text-sm mb-4">
                <Zap className="w-4 h-4" />
                最受欢迎
              </div>
              <h2 className="text-4xl font-bold mb-4">AI 面试官模拟</h2>
              <p className="text-dark-300 text-lg mb-6">
                完整模拟真实技术面试流程，包括行为面试、算法面试、系统设计和前端专项。
                AI 面试官会根据你选择的目标公司调整风格。
              </p>
              <ul className="space-y-3 mb-8">
                {[
                  '支持 Google、Meta、Amazon 等公司风格',
                  '实时代码编辑和执行',
                  '语音对话支持',
                  '详细评分报告和改进建议'
                ].map((item, i) => (
                  <li key={i} className="flex items-center gap-3 text-dark-200">
                    <div className="w-5 h-5 rounded-full bg-green-500/20 flex items-center justify-center">
                      <Target className="w-3 h-3 text-green-400" />
                    </div>
                    {item}
                  </li>
                ))}
              </ul>
              <Link 
                href="/interview"
                className="inline-flex items-center gap-2 px-6 py-3 rounded-lg bg-purple-500 hover:bg-purple-600 transition font-medium"
              >
                开始面试
                <Zap className="w-4 h-4" />
              </Link>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, x: 20 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true }}
              className="relative"
            >
              {/* Mock Interview UI */}
              <div className="rounded-2xl bg-dark-800 border border-dark-700 overflow-hidden shadow-2xl">
                <div className="px-4 py-3 bg-dark-700 border-b border-dark-600 flex items-center gap-2">
                  <div className="w-3 h-3 rounded-full bg-red-500" />
                  <div className="w-3 h-3 rounded-full bg-yellow-500" />
                  <div className="w-3 h-3 rounded-full bg-green-500" />
                  <span className="ml-2 text-sm text-dark-400">AI Interview - Google</span>
                </div>
                <div className="p-6">
                  <div className="flex items-start gap-4 mb-6">
                    <div className="w-10 h-10 rounded-full bg-gradient-to-br from-blue-500 to-cyan-500 flex items-center justify-center flex-shrink-0">
                      <Brain className="w-5 h-5 text-white" />
                    </div>
                    <div className="bg-dark-700 rounded-lg rounded-tl-none p-4 max-w-md">
                      <p className="text-sm text-dark-200">
                        你好！我是今天的面试官。请实现一个 LRU Cache，需要支持 get 和 put 操作，时间复杂度都是 O(1)。
                      </p>
                    </div>
                  </div>
                  <div className="bg-dark-900 rounded-lg p-4 font-mono text-sm">
                    <pre className="text-green-400">
{`class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = {}
        # ...`}
                    </pre>
                  </div>
                </div>
              </div>
            </motion.div>
          </div>
        </div>
      </section>

      {/* Battle Section */}
      <section className="py-20 px-6">
        <div className="max-w-7xl mx-auto">
          <div className="grid md:grid-cols-2 gap-12 items-center">
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true }}
              className="order-2 md:order-1"
            >
              {/* Mock Battle UI */}
              <div className="rounded-2xl bg-dark-800 border border-dark-700 overflow-hidden shadow-2xl">
                <div className="px-6 py-4 bg-dark-700 border-b border-dark-600">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-3">
                      <div className="w-10 h-10 rounded-full bg-blue-500 flex items-center justify-center">
                        <span className="font-bold">你</span>
                      </div>
                      <div>
                        <div className="font-semibold">Player1</div>
                        <div className="text-sm text-green-400">85% 进度</div>
                      </div>
                    </div>
                    <div className="text-2xl font-bold text-orange-400">VS</div>
                    <div className="flex items-center gap-3">
                      <div>
                        <div className="font-semibold text-right">Opponent</div>
                        <div className="text-sm text-yellow-400 text-right">60% 进度</div>
                      </div>
                      <div className="w-10 h-10 rounded-full bg-red-500 flex items-center justify-center">
                        <span className="font-bold">对</span>
                      </div>
                    </div>
                  </div>
                </div>
                <div className="p-6">
                  <div className="text-center mb-4">
                    <div className="text-4xl font-mono font-bold text-white">12:34</div>
                    <div className="text-dark-400">剩余时间</div>
                  </div>
                  <div className="grid grid-cols-2 gap-4">
                    <div className="h-3 bg-dark-600 rounded-full overflow-hidden">
                      <div className="h-full bg-gradient-to-r from-blue-500 to-cyan-500" style={{width: '85%'}} />
                    </div>
                    <div className="h-3 bg-dark-600 rounded-full overflow-hidden">
                      <div className="h-full bg-gradient-to-r from-red-500 to-orange-500" style={{width: '60%'}} />
                    </div>
                  </div>
                </div>
              </div>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, x: 20 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true }}
              className="order-1 md:order-2"
            >
              <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-orange-500/20 text-orange-400 text-sm mb-4">
                <Swords className="w-4 h-4" />
                超有趣
              </div>
              <h2 className="text-4xl font-bold mb-4">代码对战</h2>
              <p className="text-dark-300 text-lg mb-6">
                实时 1v1 对战，与全球选手一较高下。相同题目，看谁先完成。
                支持快速匹配、好友挑战和锦标赛模式。
              </p>
              <ul className="space-y-3 mb-8">
                {[
                  '实时对战，毫秒级状态同步',
                  'ELO 评分系统，公平匹配',
                  '全球排行榜',
                  '每日竞技场，赢取奖励'
                ].map((item, i) => (
                  <li key={i} className="flex items-center gap-3 text-dark-200">
                    <div className="w-5 h-5 rounded-full bg-orange-500/20 flex items-center justify-center">
                      <Trophy className="w-3 h-3 text-orange-400" />
                    </div>
                    {item}
                  </li>
                ))}
              </ul>
              <Link 
                href="/battle"
                className="inline-flex items-center gap-2 px-6 py-3 rounded-lg bg-orange-500 hover:bg-orange-600 transition font-medium"
              >
                开始对战
                <Swords className="w-4 h-4" />
              </Link>
            </motion.div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 px-6">
        <div className="max-w-4xl mx-auto text-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="p-12 rounded-3xl bg-gradient-to-br from-purple-500/20 to-pink-500/20 border border-purple-500/30"
          >
            <h2 className="text-4xl font-bold mb-4">准备好征服面试了吗？</h2>
            <p className="text-dark-300 text-lg mb-8">
              立即注册，开始你的 AI 编程学习之旅
            </p>
            <div className="flex items-center justify-center gap-4">
              <Link 
                href="/register"
                className="px-8 py-4 rounded-xl bg-white text-dark-900 hover:bg-dark-100 transition font-semibold text-lg"
              >
                免费注册
              </Link>
              <Link 
                href="/problems"
                className="px-8 py-4 rounded-xl bg-dark-700 hover:bg-dark-600 transition font-semibold text-lg border border-dark-600"
              >
                先看看题库
              </Link>
            </div>
          </motion.div>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-12 px-6 border-t border-dark-700">
        <div className="max-w-7xl mx-auto">
          <div className="flex flex-col md:flex-row items-center justify-between gap-6">
            <div className="flex items-center gap-2">
              <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-purple-500 to-pink-500 flex items-center justify-center">
                <Code2 className="w-5 h-5 text-white" />
              </div>
              <span className="font-bold">AI Coding Teacher</span>
            </div>
            <div className="flex items-center gap-8 text-dark-400">
              <Link href="/about" className="hover:text-white transition">关于</Link>
              <Link href="/docs" className="hover:text-white transition">文档</Link>
              <Link href="/privacy" className="hover:text-white transition">隐私</Link>
              <Link href="/terms" className="hover:text-white transition">条款</Link>
            </div>
            <div className="text-dark-400 text-sm">
              © 2024 AI Coding Teacher. All rights reserved.
            </div>
          </div>
        </div>
      </footer>
    </main>
  )
}


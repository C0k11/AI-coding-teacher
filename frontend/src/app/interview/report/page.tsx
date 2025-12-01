'use client'

import { useRouter } from 'next/navigation'
import Link from 'next/link'
import { motion } from 'framer-motion'
import {
  Code2,
  Brain,
  Star,
  CheckCircle,
  AlertCircle,
  ArrowRight,
  BarChart3,
  Clock,
  Target,
  TrendingUp
} from 'lucide-react'
import { cn } from '@/lib/utils'

// Mock report data
const MOCK_REPORT = {
  overall_score: 7.5,
  dimension_scores: {
    problem_understanding: 8,
    algorithm_design: 7,
    code_implementation: 7,
    communication: 8,
    optimization: 6
  },
  time_analysis: {
    understanding: 5,
    designing: 10,
    coding: 25,
    testing: 5
  },
  strengths: [
    '主动澄清问题要求',
    '沟通思路清晰',
    '代码风格良好',
    '考虑了基本边缘情况'
  ],
  improvements: [
    '时间分配可以更合理',
    '优化意识可以加强',
    '可以更主动讨论复杂度',
    '测试覆盖可以更全面'
  ],
  suggestions: [
    '多练习动态规划类题目',
    '加强时间复杂度分析能力',
    '练习口头表达算法思路',
    '学习更多优化技巧'
  ],
  recommended_topics: ['dp', 'graph', 'binary_search']
}

const DIMENSION_LABELS: Record<string, string> = {
  problem_understanding: '问题理解',
  algorithm_design: '算法设计',
  code_implementation: '代码实现',
  communication: '沟通能力',
  optimization: '优化意识'
}

export default function InterviewReportPage() {
  const router = useRouter()
  const report = MOCK_REPORT

  const getScoreColor = (score: number) => {
    if (score >= 8) return 'text-green-400'
    if (score >= 6) return 'text-yellow-400'
    return 'text-red-400'
  }

  const getScoreLabel = (score: number) => {
    if (score >= 9) return '优秀'
    if (score >= 7) return '良好'
    if (score >= 5) return '一般'
    return '需改进'
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
        </div>
      </nav>

      <div className="max-w-4xl mx-auto px-6 py-12">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-12"
        >
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-purple-500/20 text-purple-400 text-sm mb-4">
            <BarChart3 className="w-4 h-4" />
            面试报告
          </div>
          <h1 className="text-4xl font-bold mb-4">面试完成！</h1>
          <p className="text-dark-400">以下是你的详细评估报告</p>
        </motion.div>

        {/* Overall Score */}
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.2 }}
          className="bg-gradient-to-br from-purple-500/20 to-pink-500/20 rounded-2xl p-8 border border-purple-500/30 mb-8 text-center"
        >
          <div className="text-6xl font-bold mb-2">
            <span className={getScoreColor(report.overall_score)}>
              {report.overall_score}
            </span>
            <span className="text-2xl text-dark-400">/10</span>
          </div>
          <div className="text-xl text-dark-300">
            总体评分：{getScoreLabel(report.overall_score)}
          </div>
        </motion.div>

        {/* Dimension Scores */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="bg-dark-800 rounded-xl border border-dark-700 p-6 mb-8"
        >
          <h2 className="text-lg font-semibold mb-6 flex items-center gap-2">
            <Target className="w-5 h-5 text-purple-400" />
            各维度评分
          </h2>
          <div className="space-y-4">
            {Object.entries(report.dimension_scores).map(([key, score]) => (
              <div key={key} className="flex items-center gap-4">
                <div className="w-24 text-sm text-dark-300">
                  {DIMENSION_LABELS[key] || key}
                </div>
                <div className="flex-1 h-3 bg-dark-700 rounded-full overflow-hidden">
                  <motion.div
                    initial={{ width: 0 }}
                    animate={{ width: `${score * 10}%` }}
                    transition={{ delay: 0.5, duration: 0.8 }}
                    className={cn(
                      'h-full rounded-full',
                      score >= 8 ? 'bg-green-500' :
                      score >= 6 ? 'bg-yellow-500' : 'bg-red-500'
                    )}
                  />
                </div>
                <div className={cn('w-12 text-right font-bold', getScoreColor(score))}>
                  {score}/10
                </div>
              </div>
            ))}
          </div>
        </motion.div>

        {/* Time Analysis */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
          className="bg-dark-800 rounded-xl border border-dark-700 p-6 mb-8"
        >
          <h2 className="text-lg font-semibold mb-6 flex items-center gap-2">
            <Clock className="w-5 h-5 text-blue-400" />
            时间分配分析
          </h2>
          <div className="grid grid-cols-4 gap-4">
            {Object.entries(report.time_analysis).map(([phase, minutes]) => (
              <div key={phase} className="text-center">
                <div className="text-3xl font-bold text-blue-400 mb-1">{minutes}</div>
                <div className="text-sm text-dark-400">
                  {phase === 'understanding' ? '理解问题' :
                   phase === 'designing' ? '设计算法' :
                   phase === 'coding' ? '编码实现' : '测试优化'}
                </div>
                <div className="text-xs text-dark-500">分钟</div>
              </div>
            ))}
          </div>
        </motion.div>

        {/* Strengths & Improvements */}
        <div className="grid md:grid-cols-2 gap-6 mb-8">
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.5 }}
            className="bg-dark-800 rounded-xl border border-dark-700 p-6"
          >
            <h2 className="text-lg font-semibold mb-4 flex items-center gap-2">
              <CheckCircle className="w-5 h-5 text-green-400" />
              做得好的方面
            </h2>
            <ul className="space-y-3">
              {report.strengths.map((item, i) => (
                <li key={i} className="flex items-start gap-2">
                  <Star className="w-4 h-4 text-green-400 mt-0.5 flex-shrink-0" />
                  <span className="text-dark-200">{item}</span>
                </li>
              ))}
            </ul>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.5 }}
            className="bg-dark-800 rounded-xl border border-dark-700 p-6"
          >
            <h2 className="text-lg font-semibold mb-4 flex items-center gap-2">
              <AlertCircle className="w-5 h-5 text-yellow-400" />
              需要改进
            </h2>
            <ul className="space-y-3">
              {report.improvements.map((item, i) => (
                <li key={i} className="flex items-start gap-2">
                  <ArrowRight className="w-4 h-4 text-yellow-400 mt-0.5 flex-shrink-0" />
                  <span className="text-dark-200">{item}</span>
                </li>
              ))}
            </ul>
          </motion.div>
        </div>

        {/* AI Suggestions */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.6 }}
          className="bg-gradient-to-br from-blue-500/10 to-cyan-500/10 rounded-xl border border-blue-500/30 p-6 mb-8"
        >
          <h2 className="text-lg font-semibold mb-4 flex items-center gap-2">
            <TrendingUp className="w-5 h-5 text-blue-400" />
            AI 改进建议
          </h2>
          <ul className="space-y-3">
            {report.suggestions.map((suggestion, i) => (
              <li key={i} className="flex items-start gap-3">
                <span className="w-6 h-6 rounded-full bg-blue-500/20 flex items-center justify-center text-sm text-blue-400 flex-shrink-0">
                  {i + 1}
                </span>
                <span className="text-dark-200">{suggestion}</span>
              </li>
            ))}
          </ul>
        </motion.div>

        {/* Recommended Topics */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.7 }}
          className="bg-dark-800 rounded-xl border border-dark-700 p-6 mb-8"
        >
          <h2 className="text-lg font-semibold mb-4">推荐练习主题</h2>
          <div className="flex flex-wrap gap-2">
            {report.recommended_topics.map((topic) => (
              <Link
                key={topic}
                href={`/problems?topic=${topic}`}
                className="px-4 py-2 bg-purple-500/20 text-purple-400 rounded-lg hover:bg-purple-500/30 transition"
              >
                {topic === 'dp' ? '动态规划' :
                 topic === 'graph' ? '图算法' :
                 topic === 'binary_search' ? '二分查找' : topic}
              </Link>
            ))}
          </div>
        </motion.div>

        {/* Actions */}
        <div className="flex items-center justify-center gap-4">
          <Link
            href="/interview"
            className="px-6 py-3 bg-dark-700 rounded-xl hover:bg-dark-600 transition font-medium"
          >
            再来一次
          </Link>
          <Link
            href="/problems"
            className="px-6 py-3 bg-purple-500 rounded-xl hover:bg-purple-600 transition font-medium flex items-center gap-2"
          >
            开始练习
            <ArrowRight className="w-4 h-4" />
          </Link>
        </div>
      </div>
    </div>
  )
}


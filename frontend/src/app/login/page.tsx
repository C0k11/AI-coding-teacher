'use client'

import { useState } from 'react'
import { motion } from 'framer-motion'
import Link from 'next/link'
import { useRouter } from 'next/navigation'
import { 
  Code2, 
  Mail, 
  Lock, 
  ArrowRight, 
  Eye, 
  EyeOff, 
  User,
  BookOpen,
  Swords,
  Trophy,
  GitBranch
} from 'lucide-react'

export default function LoginPage() {
  const router = useRouter()
  const [isLogin, setIsLogin] = useState(true)
  const [showPassword, setShowPassword] = useState(false)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  
  const [formData, setFormData] = useState({
    email: '',
    username: '',
    password: '',
    confirmPassword: ''
  })

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    setLoading(true)

    try {
      if (!isLogin && formData.password !== formData.confirmPassword) {
        setError('Passwords do not match')
        setLoading(false)
        return
      }

      if (!isLogin && formData.password.length < 6) {
        setError('Password must be at least 6 characters')
        setLoading(false)
        return
      }

      const endpoint = isLogin ? '/api/users/login/json' : '/api/users/register'
      const body = isLogin 
        ? { email: formData.email, password: formData.password }
        : { email: formData.email, username: formData.username, password: formData.password }

      const res = await fetch(`http://localhost:8000${endpoint}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body)
      })

      if (!res.ok) {
        const data = await res.json()
        throw new Error(data.detail || 'Operation failed')
      }

      const data = await res.json()
      
      if (data.access_token) {
        localStorage.setItem('token', data.access_token)
        localStorage.setItem('user', JSON.stringify(data.user))
        router.push('/')
      }
    } catch (err: any) {
      setError(err.message || 'Failed to fetch')
    } finally {
      setLoading(false)
    }
  }

  const features = [
    { icon: BookOpen, text: '500+ Algorithm Problems' },
    { icon: Swords, text: 'Real-time Code Battles' },
    { icon: Trophy, text: 'ELO Ranking System' },
    { icon: GitBranch, text: 'Learning Path Tracking' },
  ]

  return (
    <div className="min-h-screen flex">
      {/* Left side - Form */}
      <div className="flex-1 flex items-center justify-center p-8 bg-white">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="w-full max-w-md"
        >
          {/* Logo - Cok11 Brand */}
          <Link href="/" className="flex items-center mb-8">
            <span className="text-2xl font-bold tracking-tight">
              <span className="text-slate-800">Cok</span>
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-500 to-indigo-500">11</span>
            </span>
          </Link>

          {/* Title */}
          <h1 className="text-3xl font-bold mb-2 text-slate-800">
            {isLogin ? 'Welcome back' : 'Create account'}
          </h1>
          <p className="text-slate-500 mb-8">
            {isLogin ? 'Sign in to continue your learning journey' : 'Register to start your coding journey'}
          </p>

          {error && (
            <div className="mb-4 p-3 rounded-xl bg-red-50 border border-red-200 text-red-600 text-sm">
              {error}
            </div>
          )}

          {/* Form */}
          <form onSubmit={handleSubmit} className="space-y-4">
            {!isLogin && (
              <motion.div
                initial={{ opacity: 0, height: 0 }}
                animate={{ opacity: 1, height: 'auto' }}
              >
                <label className="block text-sm font-medium text-slate-700 mb-2">Username</label>
                <div className="relative">
                  <User className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
                  <input
                    type="text"
                    value={formData.username}
                    onChange={(e) => setFormData({ ...formData, username: e.target.value })}
                    className="input-primary pl-12"
                    placeholder="Enter username"
                    required={!isLogin}
                  />
                </div>
              </motion.div>
            )}

            <div>
              <label className="block text-sm font-medium text-slate-700 mb-2">Email</label>
              <div className="relative">
                <Mail className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
                <input
                  type="email"
                  value={formData.email}
                  onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                  className="input-primary pl-12"
                  placeholder="your@email.com"
                  required
                />
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-slate-700 mb-2">Password</label>
              <div className="relative">
                <Lock className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
                <input
                  type={showPassword ? 'text' : 'password'}
                  value={formData.password}
                  onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                  className="input-primary pl-12 pr-12"
                  placeholder="Enter password"
                  required
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-4 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600"
                >
                  {showPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
                </button>
              </div>
            </div>

            {!isLogin && (
              <motion.div
                initial={{ opacity: 0, height: 0 }}
                animate={{ opacity: 1, height: 'auto' }}
              >
                <label className="block text-sm font-medium text-slate-700 mb-2">Confirm Password</label>
                <div className="relative">
                  <Lock className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
                  <input
                    type={showPassword ? 'text' : 'password'}
                    value={formData.confirmPassword}
                    onChange={(e) => setFormData({ ...formData, confirmPassword: e.target.value })}
                    className="input-primary pl-12"
                    placeholder="Re-enter password"
                    required={!isLogin}
                  />
                </div>
              </motion.div>
            )}

            <button
              type="submit"
              disabled={loading}
              className="w-full py-3 px-4 rounded-xl bg-gradient-to-r from-blue-500 to-indigo-600 text-white font-semibold hover:opacity-90 transition disabled:opacity-50 flex items-center justify-center gap-2 shadow-lg shadow-blue-500/25"
            >
              {loading ? (
                <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
              ) : (
                <>
                  {isLogin ? 'Sign In' : 'Sign Up'}
                  <ArrowRight className="w-5 h-5" />
                </>
              )}
            </button>
          </form>

          {/* Toggle */}
          <p className="mt-8 text-center text-slate-600">
            {isLogin ? "Don't have an account?" : 'Already have an account?'}
            <button
              onClick={() => {
                setIsLogin(!isLogin)
                setError('')
                setFormData({ email: '', password: '', username: '', confirmPassword: '' })
              }}
              className="ml-2 text-blue-600 hover:text-blue-700 font-semibold"
            >
              {isLogin ? 'Sign Up' : 'Sign In'}
            </button>
          </p>
        </motion.div>
      </div>

      {/* Right side - Feature showcase */}
      <div className="hidden lg:flex flex-1 bg-gradient-to-br from-blue-500 via-blue-600 to-indigo-600 items-center justify-center p-12 relative overflow-hidden">
        {/* Background decorations */}
        <div className="absolute inset-0">
          <div className="absolute top-20 left-20 w-64 h-64 bg-white/10 rounded-full blur-3xl" />
          <div className="absolute bottom-20 right-20 w-96 h-96 bg-indigo-400/20 rounded-full blur-3xl" />
        </div>
        
        <div className="relative z-10 text-white text-center max-w-lg">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
          >
            <h2 className="text-4xl font-bold mb-6 leading-tight">
              Level up your
              <br />
              coding skills with AI
            </h2>
            <p className="text-xl text-white/80 mb-12">
              Algorithm problems, code battles, learning path tracking - all running locally
            </p>
          </motion.div>

          {/* Features */}
          <motion.div 
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4 }}
            className="space-y-4"
          >
            {features.map((feature, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.5 + index * 0.1 }}
                className="flex items-center gap-4 text-left bg-white/10 backdrop-blur-sm rounded-xl px-6 py-4"
              >
                <div className="w-10 h-10 rounded-lg bg-white/20 flex items-center justify-center">
                  <feature.icon className="w-5 h-5" />
                </div>
                <span className="font-medium">{feature.text}</span>
              </motion.div>
            ))}
          </motion.div>
        </div>
      </div>
    </div>
  )
}

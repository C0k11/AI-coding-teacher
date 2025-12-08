'use client'

import { useState, useEffect, useCallback } from 'react'
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
import { useTranslations } from '@/lib/i18n'
import LanguageSwitcher from '@/components/LanguageSwitcher'
import { auth } from '@/lib/api'

// Google OAuth Client ID - 在 .env.local 中配置
const GOOGLE_CLIENT_ID = process.env.NEXT_PUBLIC_GOOGLE_CLIENT_ID || ''

declare global {
  interface Window {
    google?: {
      accounts: {
        id: {
          initialize: (config: any) => void
          renderButton: (element: HTMLElement, config: any) => void
          prompt: () => void
        }
      }
    }
  }
}

export default function LoginPage() {
  const router = useRouter()
  const t = useTranslations()
  const [isLogin, setIsLogin] = useState(true)
  const [showPassword, setShowPassword] = useState(false)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [googleReady, setGoogleReady] = useState(false)
  
  const [formData, setFormData] = useState({
    email: '',
    username: '',
    password: '',
    confirmPassword: ''
  })

  // Google OAuth 回调处理
  const handleGoogleCallback = useCallback(async (response: any) => {
    setLoading(true)
    setError('')
    try {
      const result = await auth.googleAuth(response.credential)
      if (result.access_token) {
        localStorage.setItem('token', result.access_token)
        localStorage.setItem('user', JSON.stringify(result.user))
        router.push('/')
      }
    } catch (err: any) {
      setError(err.message || 'Google 登录失败')
    } finally {
      setLoading(false)
    }
  }, [router])

  // 初始化 Google OAuth
  useEffect(() => {
    if (!GOOGLE_CLIENT_ID) return
    
    const initGoogle = () => {
      if (window.google?.accounts?.id) {
        window.google.accounts.id.initialize({
          client_id: GOOGLE_CLIENT_ID,
          callback: handleGoogleCallback,
        })
        
        const buttonDiv = document.getElementById('google-signin-button')
        if (buttonDiv) {
          window.google.accounts.id.renderButton(buttonDiv, {
            theme: 'outline',
            size: 'large',
            width: 280,
            text: 'continue_with',
          })
          setGoogleReady(true)
        }
      }
    }
    
    // 尝试初始化，如果脚本还没加载完成就等待
    if (window.google?.accounts?.id) {
      initGoogle()
    } else {
      // 等待 Google 脚本加载
      const checkGoogle = setInterval(() => {
        if (window.google?.accounts?.id) {
          clearInterval(checkGoogle)
          initGoogle()
        }
      }, 100)
      
      // 5秒后停止检查
      setTimeout(() => clearInterval(checkGoogle), 5000)
    }
  }, [handleGoogleCallback])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    setLoading(true)

    try {
      if (!isLogin && formData.password !== formData.confirmPassword) {
        setError(t.login.passwordsNoMatch)
        setLoading(false)
        return
      }

      if (!isLogin && formData.password.length < 6) {
        setError(t.login.passwordTooShort)
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
    { icon: BookOpen, text: t.login.features.problems },
    { icon: Swords, text: t.login.features.battles },
    { icon: Trophy, text: t.login.features.ranking },
    { icon: GitBranch, text: t.login.features.learning },
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
          <div className="flex items-center justify-between mb-8">
            <Link href="/" className="flex items-center">
              <span className="text-2xl font-bold tracking-tight">
                <span className="text-slate-800">Cok</span>
                <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-500 to-indigo-500">11</span>
              </span>
            </Link>
            <LanguageSwitcher />
          </div>

          {/* Title */}
          <h1 className="text-3xl font-bold mb-2 text-slate-800">
            {isLogin ? t.login.welcomeBack : t.login.createAccount}
          </h1>
          <p className="text-slate-500 mb-8">
            {isLogin ? t.login.signInSubtitle : t.login.signUpSubtitle}
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
                <label className="block text-sm font-medium text-slate-700 mb-2">{t.login.username}</label>
                <div className="relative">
                  <User className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
                  <input
                    type="text"
                    value={formData.username}
                    onChange={(e) => setFormData({ ...formData, username: e.target.value })}
                    className="input-primary pl-12"
                    placeholder={t.login.enterUsername}
                    required={!isLogin}
                  />
                </div>
              </motion.div>
            )}

            <div>
              <label className="block text-sm font-medium text-slate-700 mb-2">{t.login.email}</label>
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
              <label className="block text-sm font-medium text-slate-700 mb-2">{t.login.password}</label>
              <div className="relative">
                <Lock className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
                <input
                  type={showPassword ? 'text' : 'password'}
                  value={formData.password}
                  onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                  className="input-primary pl-12 pr-12"
                  placeholder={t.login.enterPassword}
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
                <label className="block text-sm font-medium text-slate-700 mb-2">{t.login.confirmPassword}</label>
                <div className="relative">
                  <Lock className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
                  <input
                    type={showPassword ? 'text' : 'password'}
                    value={formData.confirmPassword}
                    onChange={(e) => setFormData({ ...formData, confirmPassword: e.target.value })}
                    className="input-primary pl-12"
                    placeholder={t.login.reEnterPassword}
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
                  {isLogin ? t.login.signInBtn : t.login.signUpBtn}
                  <ArrowRight className="w-5 h-5" />
                </>
              )}
            </button>
          </form>

          {/* Divider */}
          <div className="my-6 flex items-center">
            <div className="flex-1 border-t border-slate-200"></div>
            <span className="px-4 text-sm text-slate-400">或</span>
            <div className="flex-1 border-t border-slate-200"></div>
          </div>

          {/* Google Login Button */}
          {GOOGLE_CLIENT_ID ? (
            <>
              {!googleReady && (
                <div className="w-full flex justify-center min-h-[44px]">
                  <div className="flex items-center gap-2 text-slate-400">
                    <div className="w-4 h-4 border-2 border-slate-300 border-t-blue-500 rounded-full animate-spin"></div>
                    加载中...
                  </div>
                </div>
              )}
              <div 
                id="google-signin-button" 
                className="w-full flex justify-center"
                style={{ display: googleReady ? 'flex' : 'none' }}
              ></div>
            </>
          ) : (
            <button
              type="button"
              disabled
              className="w-full py-3 px-4 rounded-xl border border-slate-200 text-slate-400 font-medium flex items-center justify-center gap-3 cursor-not-allowed"
            >
              <svg className="w-5 h-5" viewBox="0 0 24 24">
                <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
                <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
                <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
                <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
              </svg>
              Google 登录 (需配置)
            </button>
          )}

          {/* Toggle */}
          <p className="mt-8 text-center text-slate-600">
            {isLogin ? t.login.noAccount : t.login.hasAccount}
            <button
              onClick={() => {
                setIsLogin(!isLogin)
                setError('')
                setFormData({ email: '', password: '', username: '', confirmPassword: '' })
              }}
              className="ml-2 text-blue-600 hover:text-blue-700 font-semibold"
            >
              {isLogin ? t.login.signUpBtn : t.login.signInBtn}
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
              {t.login.sidebar.title}
            </h2>
            <p className="text-xl text-white/80 mb-12">
              {t.login.sidebar.subtitle}
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

'use client'

import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import Link from 'next/link'
import { useRouter } from 'next/navigation'
import { 
  Code2, 
  Swords, 
  GitBranch, 
  BookOpen,
  Target,
  ArrowRight,
  Home as HomeIcon,
  BarChart3,
  User,
  LogOut
} from 'lucide-react'
import { useTranslations } from '@/lib/i18n'
import LanguageSwitcher from '@/components/LanguageSwitcher'

export default function Home() {
  const router = useRouter()
  const [user, setUser] = useState<{ name: string } | null>(null)
  const t = useTranslations()

  const features = [
    {
      icon: BookOpen,
      title: t.home.features.problemLibrary.title,
      description: t.home.features.problemLibrary.description,
      color: 'primary',
    },
    {
      icon: Code2,
      title: t.home.features.aiAnalysis.title,
      description: t.home.features.aiAnalysis.description,
      color: 'accent',
    },
    {
      icon: Swords,
      title: t.home.features.realtimeBattle.title,
      description: t.home.features.realtimeBattle.description,
      color: 'success',
    },
    {
      icon: GitBranch,
      title: t.home.features.learningPath.title,
      description: t.home.features.learningPath.description,
      color: 'primary',
    }
  ]

  const stats = [
    { label: t.home.stats.problems, value: '500+' },
    { label: t.home.stats.languages, value: '7+' },
    { label: t.home.stats.battles, value: '50K+' },
  ]

  const navItems = [
    { href: '/', label: t.nav.home, icon: HomeIcon },
    { href: '/problems', label: t.nav.problems, icon: BookOpen },
    { href: '/battle', label: t.nav.battle, icon: Swords },
    { href: '/dashboard', label: t.nav.dashboard, icon: BarChart3 },
  ]

  useEffect(() => {
    const savedUser = localStorage.getItem('user')
    if (savedUser) {
      try {
        setUser(JSON.parse(savedUser))
      } catch {}
    }
  }, [])

  const handleLogout = () => {
    localStorage.removeItem('token')
    localStorage.removeItem('user')
    setUser(null)
    router.refresh()
  }

  return (
    <div className="min-h-screen bg-white">
      {/* Navigation */}
      <header className="fixed top-0 left-0 right-0 z-50 bg-white border-b border-slate-200">
        <div className="container mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            {/* Logo - Cok11 Brand */}
            <Link href="/" className="flex items-center">
              <span className="text-xl font-bold tracking-tight">
                <span className="text-slate-900">Cok</span>
                <span className="text-blue-600">11</span>
              </span>
            </Link>

            {/* Desktop Navigation */}
            <div className="hidden md:flex items-center gap-6">
              {navItems.map((item) => (
                <Link
                  key={item.href}
                  href={item.href}
                  className="text-slate-600 hover:text-slate-900 font-medium transition-colors"
                >
                  {item.label}
                </Link>
              ))}
            </div>

            {/* Right side - User or Login */}
            <div className="hidden md:flex items-center gap-4">
              <LanguageSwitcher />
              {user ? (
                <div className="flex items-center gap-4">
                  <div className="flex items-center gap-2 text-slate-700">
                    <User className="w-4 h-4" />
                    <span className="font-medium">{user.name}</span>
                  </div>
                  <button
                    onClick={handleLogout}
                    className="flex items-center gap-1 text-slate-500 hover:text-slate-700 transition-colors"
                  >
                    <LogOut className="w-4 h-4" />
                  </button>
                </div>
              ) : (
                <Link
                  href="/login"
                  className="px-4 py-2 text-white bg-slate-900 hover:bg-slate-800 rounded-md font-medium transition-colors"
                >
                  {t.nav.signIn}
                </Link>
              )}
            </div>
          </div>
        </div>
      </header>

      {/* Hero Section - GitHub style */}
      <section className="pt-32 pb-20 bg-slate-50 border-b border-slate-200">
        <div className="container mx-auto px-6">
          <div className="max-w-4xl mx-auto text-center">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5 }}
            >
              <h1 className="text-4xl md:text-6xl font-bold mb-6 text-slate-900 leading-tight">
                {t.home.heroTitle}
                <br />
                <span className="text-blue-600">{t.home.heroTitleHighlight}</span>
              </h1>
            
              <p className="text-xl text-slate-600 max-w-2xl mx-auto mb-10">
                {t.home.heroSubtitle}
              </p>

              <div className="flex items-center justify-center gap-4">
                <Link 
                  href="/problems"
                  className="px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-md transition-colors"
                >
                  {t.home.getStarted}
                </Link>
                <Link 
                  href="/battle"
                  className="px-6 py-3 bg-white hover:bg-slate-50 border border-slate-300 text-slate-700 font-medium rounded-md transition-colors"
                >
                  {t.home.codeBattle}
                </Link>
              </div>
            </motion.div>

            {/* Stats */}
            <motion.div 
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: 0.2 }}
              className="flex justify-center gap-12 mt-16"
            >
              {stats.map((stat) => (
                <div key={stat.label} className="text-center">
                  <div className="text-3xl font-bold text-slate-900">{stat.value}</div>
                  <div className="text-sm text-slate-500">{stat.label}</div>
                </div>
              ))}
            </motion.div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-24 bg-white">
        <div className="max-w-7xl mx-auto px-6">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <span className="text-blue-600 font-semibold text-sm uppercase tracking-wider">{t.home.features.title}</span>
            <h2 className="text-4xl md:text-5xl font-bold mt-4 mb-6 text-slate-900">{t.home.features.subtitle}</h2>
            <p className="text-xl text-slate-600 max-w-2xl mx-auto">
              {t.home.features.description}
            </p>
          </motion.div>

          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
            {features.map((feature, i) => (
              <motion.div
                key={feature.title}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: i * 0.1 }}
                className="modern-card p-8 text-center group"
              >
                <div className={`
                  w-16 h-16 mx-auto mb-6 rounded-2xl flex items-center justify-center
                  transition-all duration-300 group-hover:scale-110
                  ${feature.color === 'primary' ? 'bg-blue-100 text-blue-600' : ''}
                  ${feature.color === 'accent' ? 'bg-indigo-100 text-indigo-600' : ''}
                  ${feature.color === 'success' ? 'bg-emerald-100 text-emerald-600' : ''}
                `}>
                  <feature.icon className="w-8 h-8" />
                </div>
                <h3 className="text-xl font-bold mb-3 text-slate-800">{feature.title}</h3>
                <p className="text-slate-600">{feature.description}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Battle Section */}
      <section className="py-24 bg-gradient-to-b from-slate-50 to-white">
        <div className="max-w-7xl mx-auto px-6">
          <div className="grid md:grid-cols-2 gap-12 items-center">
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true }}
            >
              <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-orange-100 text-orange-600 text-sm font-medium mb-4">
                <Swords className="w-4 h-4" />
                {t.home.battleSection.badge}
              </div>
              <h2 className="text-4xl font-bold mb-4 text-slate-900">{t.home.battleSection.title}</h2>
              <p className="text-slate-600 text-lg mb-6">
                {t.home.battleSection.description}
              </p>
              <ul className="space-y-3 mb-8">
                {t.home.battleSection.features.map((item, i) => (
                  <li key={i} className="flex items-center gap-3 text-slate-700">
                    <div className="w-5 h-5 rounded-full bg-green-100 flex items-center justify-center">
                      <Target className="w-3 h-3 text-green-600" />
                    </div>
                    {item}
                  </li>
                ))}
              </ul>
              <Link 
                href="/battle"
                className="inline-flex items-center gap-2 px-6 py-3 rounded-xl bg-orange-500 hover:bg-orange-600 text-white transition font-medium"
              >
                {t.home.battleSection.startBattle}
                <Swords className="w-4 h-4" />
              </Link>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, x: 20 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true }}
              className="relative"
            >
              <div className="rounded-2xl bg-white border border-slate-200 overflow-hidden shadow-xl">
                <div className="px-6 py-4 bg-slate-50 border-b border-slate-200">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-3">
                      <div className="w-10 h-10 rounded-full bg-blue-500 flex items-center justify-center text-white font-bold">P1</div>
                      <div>
                        <div className="font-semibold text-slate-800">Player1</div>
                        <div className="text-sm text-green-600">85% {t.home.battleSection.progress}</div>
                      </div>
                    </div>
                    <div className="text-2xl font-bold text-orange-500">VS</div>
                    <div className="flex items-center gap-3">
                      <div>
                        <div className="font-semibold text-slate-800 text-right">Player2</div>
                        <div className="text-sm text-yellow-600 text-right">60% {t.home.battleSection.progress}</div>
                      </div>
                      <div className="w-10 h-10 rounded-full bg-red-500 flex items-center justify-center text-white font-bold">P2</div>
                    </div>
                  </div>
                </div>
                <div className="p-6">
                  <div className="text-center mb-4">
                    <div className="text-4xl font-mono font-bold text-slate-800">12:34</div>
                    <div className="text-slate-500">{t.home.battleSection.timeRemaining}</div>
                  </div>
                  <div className="grid grid-cols-2 gap-4">
                    <div className="h-3 bg-slate-200 rounded-full overflow-hidden">
                      <div className="h-full bg-gradient-to-r from-blue-500 to-cyan-500 rounded-full" style={{width: '85%'}} />
                    </div>
                    <div className="h-3 bg-slate-200 rounded-full overflow-hidden">
                      <div className="h-full bg-gradient-to-r from-red-500 to-orange-500 rounded-full" style={{width: '60%'}} />
                    </div>
                  </div>
                </div>
              </div>
            </motion.div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-24 bg-gradient-to-r from-blue-600 via-blue-500 to-indigo-600 relative overflow-hidden">
        <div className="absolute top-0 left-0 w-96 h-96 bg-white/10 rounded-full blur-3xl" />
        <div className="absolute bottom-0 right-0 w-96 h-96 bg-indigo-400/20 rounded-full blur-3xl" />
        
        <div className="max-w-4xl mx-auto px-6 text-center relative z-10">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
          >
            <h2 className="text-4xl md:text-5xl font-bold mb-6 text-white">{t.home.cta.title}</h2>
            <p className="text-xl text-white/80 mb-10 max-w-2xl mx-auto">
              {t.home.cta.subtitle}
            </p>
            <div className="flex items-center justify-center gap-4">
              <Link 
                href="/login"
                className="inline-flex items-center gap-2 px-8 py-4 bg-white text-blue-600 font-semibold rounded-xl shadow-lg hover:shadow-xl transition-all duration-300 hover:-translate-y-1"
              >
                {t.home.cta.getStartedFree}
                <ArrowRight className="w-5 h-5" />
              </Link>
              <Link 
                href="/problems"
                className="px-8 py-4 rounded-xl bg-white/10 hover:bg-white/20 transition font-semibold text-lg text-white border border-white/20"
              >
                {t.home.cta.browseProblems}
              </Link>
            </div>
          </motion.div>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-12 px-6 bg-white border-t border-slate-200">
        <div className="max-w-7xl mx-auto">
          <div className="flex flex-col md:flex-row items-center justify-between gap-6">
            <div className="flex items-center gap-2">
              <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-blue-500 to-indigo-600 flex items-center justify-center">
                <Code2 className="w-5 h-5 text-white" />
              </div>
              <span className="font-bold text-slate-800">AI Coding Teacher</span>
            </div>
            <div className="flex items-center gap-8 text-slate-500">
              <Link href="/about" className="hover:text-slate-900 transition">{t.home.footer.about}</Link>
              <Link href="/docs" className="hover:text-slate-900 transition">{t.home.footer.docs}</Link>
              <Link href="/privacy" className="hover:text-slate-900 transition">{t.home.footer.privacy}</Link>
            </div>
            <div className="text-slate-400 text-sm">
              2024 AI Coding Teacher
            </div>
          </div>
        </div>
      </footer>
    </div>
  )
}


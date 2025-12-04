'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'
import { motion } from 'framer-motion'
import { 
  Swords, 
  Users, 
  Trophy, 
  Clock,
  Target,
  ChevronRight,
  User,
  LogOut
} from 'lucide-react'
import { cn } from '@/lib/utils'
import { battles } from '@/lib/api'
import { useAuthStore, useBattleStore } from '@/store/useStore'

const BATTLE_MODES = [
  { 
    id: 'quick_match', 
    name: 'Quick Match', 
    description: 'Match with opponents of similar skill level',
  },
  { 
    id: 'friend_challenge', 
    name: 'Friend Challenge', 
    description: 'Challenge a friend to a 1v1 battle',
  },
  { 
    id: 'tournament', 
    name: 'Tournament', 
    description: 'Join weekly tournaments and compete for ranking',
  },
]


const navItems = [
  { href: '/', label: 'Home' },
  { href: '/problems', label: 'Problems' },
  { href: '/battle', label: 'Battle' },
  { href: '/dashboard', label: 'Dashboard' },
]

export default function BattlePage() {
  const router = useRouter()
  const { token, user: authUser } = useAuthStore()
  const { startBattle } = useBattleStore()
  
  const [selectedMode, setSelectedMode] = useState('quick_match')
  const [friendUsername, setFriendUsername] = useState('')
  const [isSearching, setIsSearching] = useState(false)
  const [user, setUser] = useState<{ name: string } | null>(null)

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

  const handleStartBattle = async () => {
    setIsSearching(true)

    try {
      const mockBattle = {
        battle_id: Date.now(),
        problem: {
          id: 1,
          title: 'Two Sum',
          slug: 'two-sum',
          difficulty: 'easy',
          description: 'Given an array of integers nums and an integer target...',
          examples: [{ input: 'nums = [2,7,11,15], target = 9', output: '[0,1]' }],
          starter_code: {
            python: 'class Solution:\n    def twoSum(self, nums: list[int], target: int) -> list[int]:\n        pass'
          }
        },
        mode: selectedMode,
        status: 'waiting',
        opponent: selectedMode === 'quick_match' ? 'Opponent' : null,
        time_limit_seconds: 900
      }

      if (token) {
        try {
          const battle = await battles.create(
            selectedMode,
            selectedMode === 'friend_challenge' ? friendUsername : undefined,
            token
          )
          startBattle(battle.battle_id, battle.problem, battle.opponent || null, battle.time_limit_seconds)
        } catch (error) {
          startBattle(mockBattle.battle_id, mockBattle.problem, mockBattle.opponent, mockBattle.time_limit_seconds)
        }
      } else {
        startBattle(mockBattle.battle_id, mockBattle.problem, 'AI Opponent', mockBattle.time_limit_seconds)
      }

      router.push('/battle/arena')
    } catch (error) {
      console.error('Failed to start battle:', error)
    } finally {
      setIsSearching(false)
    }
  }

  return (
    <div className="min-h-screen bg-white">
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
                    item.href === '/battle' ? "text-slate-900" : "text-slate-600 hover:text-slate-900"
                  )}
                >
                  {item.label}
                </Link>
              ))}
            </div>

            <div className="hidden md:flex items-center gap-4">
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
                  Sign in
                </Link>
              )}
            </div>
          </div>
        </div>
      </header>

      <div className="container mx-auto px-6 pt-28 pb-12">
        {/* Header */}
        <div className="mb-12">
          <h1 className="text-3xl font-bold text-slate-900 mb-2">Code Battle</h1>
          <p className="text-slate-500">Compete with players worldwide on the same problem</p>
        </div>

        <div className="max-w-2xl">
          {/* Battle Modes */}
          <div className="space-y-6">
            <h2 className="text-lg font-semibold text-slate-900">Select Battle Mode</h2>
            
            <div className="space-y-3">
              {BATTLE_MODES.map((mode) => (
                <button
                  key={mode.id}
                  onClick={() => setSelectedMode(mode.id)}
                  className={cn(
                    'w-full p-4 rounded-md border text-left transition flex items-center gap-4',
                    selectedMode === mode.id
                      ? 'border-blue-500 bg-blue-50'
                      : 'border-slate-200 bg-white hover:border-slate-300'
                  )}
                >
                  <div className="flex-1">
                    <h3 className="font-medium text-slate-900">{mode.name}</h3>
                    <p className="text-slate-500 text-sm">{mode.description}</p>
                  </div>
                  <ChevronRight className={cn(
                    'w-5 h-5',
                    selectedMode === mode.id ? 'text-blue-500' : 'text-slate-300'
                  )} />
                </button>
              ))}
            </div>

            {/* Friend Challenge Input */}
            {selectedMode === 'friend_challenge' && (
              <div className="bg-slate-50 rounded-md p-4 border border-slate-200">
                <label className="block text-sm text-slate-600 mb-2">Friend Username</label>
                <input
                  type="text"
                  value={friendUsername}
                  onChange={(e) => setFriendUsername(e.target.value)}
                  placeholder="Enter friend's username"
                  className="input-primary"
                />
              </div>
            )}

            {/* Start Button */}
            <button
              onClick={handleStartBattle}
              disabled={isSearching || (selectedMode === 'friend_challenge' && !friendUsername)}
              className={cn(
                'w-full flex items-center justify-center gap-2 px-6 py-3 rounded-md font-medium transition',
                isSearching
                  ? 'bg-slate-100 text-slate-400 cursor-not-allowed'
                  : 'bg-blue-600 hover:bg-blue-700 text-white'
              )}
            >
              <Swords className="w-5 h-5" />
              {isSearching ? 'Matching...' : 'Start Battle'}
            </button>

            {/* Battle Info */}
            <div className="grid grid-cols-3 gap-4">
              <div className="bg-white rounded-md p-4 border border-slate-200 text-center">
                <Clock className="w-5 h-5 mx-auto mb-2 text-slate-400" />
                <div className="text-lg font-bold text-slate-900">15:00</div>
                <div className="text-xs text-slate-500">Time Limit</div>
              </div>
              <div className="bg-white rounded-md p-4 border border-slate-200 text-center">
                <Target className="w-5 h-5 mx-auto mb-2 text-slate-400" />
                <div className="text-lg font-bold text-slate-900">1v1</div>
                <div className="text-xs text-slate-500">Battle Mode</div>
              </div>
              <div className="bg-white rounded-md p-4 border border-slate-200 text-center">
                <Trophy className="w-5 h-5 mx-auto mb-2 text-slate-400" />
                <div className="text-lg font-bold text-slate-900">+25</div>
                <div className="text-xs text-slate-500">Win Points</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}


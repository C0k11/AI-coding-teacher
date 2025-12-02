'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'
import { motion } from 'framer-motion'
import { 
  Code2, 
  Swords, 
  Users, 
  Trophy, 
  Clock,
  Zap,
  Target,
  ChevronRight
} from 'lucide-react'
import { cn } from '@/lib/utils'
import { battles } from '@/lib/api'
import { useAuthStore, useBattleStore } from '@/store/useStore'

const BATTLE_MODES = [
  { 
    id: 'quick_match', 
    name: 'Quick Match', 
    icon: Zap, 
    description: 'Match with opponents of similar skill level',
    color: 'from-orange-500 to-red-500'
  },
  { 
    id: 'friend_challenge', 
    name: 'Friend Challenge', 
    icon: Users, 
    description: 'Challenge a friend to a 1v1 battle',
    color: 'from-blue-500 to-cyan-500'
  },
  { 
    id: 'tournament', 
    name: 'Tournament', 
    icon: Trophy, 
    description: 'Join weekly tournaments and compete for ranking',
    color: 'from-yellow-500 to-orange-500'
  },
]

// Mock leaderboard data
const MOCK_LEADERBOARD = [
  { rank: 1, username: 'CodeMaster', elo_rating: 2450, battles_won: 156 },
  { rank: 2, username: 'AlgoNinja', elo_rating: 2380, battles_won: 142 },
  { rank: 3, username: 'ByteWarrior', elo_rating: 2320, battles_won: 138 },
  { rank: 4, username: 'DataHero', elo_rating: 2280, battles_won: 125 },
  { rank: 5, username: 'LogicKing', elo_rating: 2245, battles_won: 118 },
]

export default function BattlePage() {
  const router = useRouter()
  const { token, user } = useAuthStore()
  const { startBattle } = useBattleStore()
  
  const [selectedMode, setSelectedMode] = useState('quick_match')
  const [friendUsername, setFriendUsername] = useState('')
  const [isSearching, setIsSearching] = useState(false)

  const handleStartBattle = async () => {
    setIsSearching(true)

    try {
      // Mock battle creation for demo
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
          // Fallback to mock
          startBattle(mockBattle.battle_id, mockBattle.problem, mockBattle.opponent, mockBattle.time_limit_seconds)
        }
      } else {
        // Demo mode
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
            <Link href="/problems" className="text-dark-300 hover:text-white transition">Problems</Link>
            <Link href="/interview" className="text-dark-300 hover:text-white transition">Interview</Link>
            <Link href="/battle" className="text-white font-medium">Battle</Link>
            <Link href="/dashboard" className="text-dark-300 hover:text-white transition">Dashboard</Link>
          </div>
        </div>
      </nav>

      <div className="max-w-6xl mx-auto px-6 py-12">
        {/* Header */}
        <div className="text-center mb-12">
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-orange-500/20 text-orange-400 text-sm mb-4">
            <Swords className="w-4 h-4" />
            Code Battle
          </div>
          <h1 className="text-4xl font-bold mb-4">Real-time 1v1 Battle</h1>
          <p className="text-dark-400 text-lg">Compete with players worldwide on the same problem, see who finishes first</p>
        </div>

        <div className="grid md:grid-cols-3 gap-8">
          {/* Left - Battle Modes */}
          <div className="md:col-span-2 space-y-6">
            <h2 className="text-xl font-bold">Select Battle Mode</h2>
            
            <div className="space-y-4">
              {BATTLE_MODES.map((mode) => (
                <motion.button
                  key={mode.id}
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                  onClick={() => setSelectedMode(mode.id)}
                  className={cn(
                    'w-full p-6 rounded-xl border-2 text-left transition flex items-center gap-4',
                    selectedMode === mode.id
                      ? 'border-orange-500 bg-orange-500/10'
                      : 'border-dark-700 bg-dark-800 hover:border-dark-600'
                  )}
                >
                  <div className={`w-14 h-14 rounded-xl bg-gradient-to-br ${mode.color} flex items-center justify-center`}>
                    <mode.icon className="w-7 h-7 text-white" />
                  </div>
                  <div className="flex-1">
                    <h3 className="text-lg font-semibold">{mode.name}</h3>
                    <p className="text-dark-400 text-sm">{mode.description}</p>
                  </div>
                  <ChevronRight className={cn(
                    'w-5 h-5 transition',
                    selectedMode === mode.id ? 'text-orange-400' : 'text-dark-500'
                  )} />
                </motion.button>
              ))}
            </div>

            {/* Friend Challenge Input */}
            {selectedMode === 'friend_challenge' && (
              <motion.div
                initial={{ opacity: 0, height: 0 }}
                animate={{ opacity: 1, height: 'auto' }}
                className="bg-dark-800 rounded-xl p-6 border border-dark-700"
              >
                <label className="block text-sm text-dark-400 mb-2">Friend Username</label>
                <input
                  type="text"
                  value={friendUsername}
                  onChange={(e) => setFriendUsername(e.target.value)}
                  placeholder="Enter friend's username"
                  className="w-full px-4 py-3 bg-dark-700 border border-dark-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500"
                />
              </motion.div>
            )}

            {/* Start Button */}
            <button
              onClick={handleStartBattle}
              disabled={isSearching || (selectedMode === 'friend_challenge' && !friendUsername)}
              className={cn(
                'w-full flex items-center justify-center gap-2 px-8 py-4 rounded-xl font-semibold text-lg transition',
                isSearching
                  ? 'bg-orange-900 text-orange-400 cursor-not-allowed'
                  : 'bg-gradient-to-r from-orange-500 to-red-500 hover:opacity-90 glow-orange'
              )}
            >
              <Swords className="w-5 h-5" />
              {isSearching ? 'Matching...' : 'Start Battle'}
            </button>

            {/* Battle Info */}
            <div className="grid grid-cols-3 gap-4">
              <div className="bg-dark-800 rounded-xl p-4 border border-dark-700 text-center">
                <Clock className="w-6 h-6 mx-auto mb-2 text-dark-400" />
                <div className="text-lg font-bold">15:00</div>
                <div className="text-xs text-dark-400">Time Limit</div>
              </div>
              <div className="bg-dark-800 rounded-xl p-4 border border-dark-700 text-center">
                <Target className="w-6 h-6 mx-auto mb-2 text-dark-400" />
                <div className="text-lg font-bold">1v1</div>
                <div className="text-xs text-dark-400">Battle Mode</div>
              </div>
              <div className="bg-dark-800 rounded-xl p-4 border border-dark-700 text-center">
                <Trophy className="w-6 h-6 mx-auto mb-2 text-dark-400" />
                <div className="text-lg font-bold">+25</div>
                <div className="text-xs text-dark-400">Win Points</div>
              </div>
            </div>
          </div>

          {/* Right - Leaderboard */}
          <div className="space-y-6">
            <h2 className="text-xl font-bold flex items-center gap-2">
              <Trophy className="w-5 h-5 text-yellow-400" />
              Leaderboard
            </h2>

            <div className="bg-dark-800 rounded-xl border border-dark-700 overflow-hidden">
              {MOCK_LEADERBOARD.map((player, i) => (
                <div
                  key={player.rank}
                  className={cn(
                    'flex items-center gap-3 px-4 py-3',
                    i < MOCK_LEADERBOARD.length - 1 && 'border-b border-dark-700'
                  )}
                >
                  <div className={cn(
                    'w-8 h-8 rounded-full flex items-center justify-center font-bold text-sm',
                    player.rank === 1 ? 'bg-yellow-500 text-black' :
                    player.rank === 2 ? 'bg-gray-300 text-black' :
                    player.rank === 3 ? 'bg-orange-600 text-white' :
                    'bg-dark-700 text-dark-400'
                  )}>
                    {player.rank}
                  </div>
                  <div className="flex-1">
                    <div className="font-medium">{player.username}</div>
                    <div className="text-xs text-dark-400">{player.battles_won} Wins</div>
                  </div>
                  <div className="text-right">
                    <div className="font-mono font-bold text-orange-400">{player.elo_rating}</div>
                    <div className="text-xs text-dark-400">ELO</div>
                  </div>
                </div>
              ))}
            </div>

            {/* User Stats */}
            {user && (
              <div className="bg-gradient-to-br from-orange-500/20 to-red-500/20 rounded-xl p-4 border border-orange-500/30">
                <div className="text-sm text-dark-400 mb-1">Your Rank</div>
                <div className="flex items-center justify-between">
                  <span className="text-2xl font-bold">#{user.elo_rating > 2000 ? '125' : '500+'}</span>
                  <span className="text-orange-400 font-mono">{user.elo_rating} ELO</span>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}


import { create } from 'zustand'
import { persist } from 'zustand/middleware'
import type { User } from '@/lib/api'

interface AuthState {
  token: string | null
  user: User | null
  setAuth: (token: string, user: User) => void
  logout: () => void
  updateUser: (user: Partial<User>) => void
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      token: null,
      user: null,
      setAuth: (token, user) => set({ token, user }),
      logout: () => set({ token: null, user: null }),
      updateUser: (updates) =>
        set((state) => ({
          user: state.user ? { ...state.user, ...updates } : null,
        })),
    }),
    {
      name: 'auth-storage',
    }
  )
)

interface InterviewState {
  interviewId: number | null
  interviewType: string | null
  company: string | null
  problem: { title: string; description: string } | null
  messages: Array<{ role: string; content: string; timestamp: string }>
  code: string
  isActive: boolean
  startInterview: (id: number, type: string, company: string, problem: any, initialMessage: string) => void
  addMessage: (role: string, content: string) => void
  setCode: (code: string) => void
  endInterview: () => void
}

export const useInterviewStore = create<InterviewState>((set) => ({
  interviewId: null,
  interviewType: null,
  company: null,
  problem: null,
  messages: [],
  code: '',
  isActive: false,
  startInterview: (id, type, company, problem, initialMessage) =>
    set({
      interviewId: id,
      interviewType: type,
      company,
      problem,
      messages: [{ role: 'assistant', content: initialMessage, timestamp: new Date().toISOString() }],
      code: '',
      isActive: true,
    }),
  addMessage: (role, content) =>
    set((state) => ({
      messages: [...state.messages, { role, content, timestamp: new Date().toISOString() }],
    })),
  setCode: (code) => set({ code }),
  endInterview: () =>
    set({
      interviewId: null,
      interviewType: null,
      company: null,
      problem: null,
      messages: [],
      code: '',
      isActive: false,
    }),
}))

interface BattleState {
  battleId: number | null
  problem: any | null
  opponent: string | null
  myProgress: { tests_passed: number; code_lines: number; attempts: number }
  opponentProgress: { tests_passed: number; code_lines: number }
  timeRemaining: number
  status: 'idle' | 'waiting' | 'in_progress' | 'completed'
  winner: string | null
  code: string
  startBattle: (id: number, problem: any, opponent: string | null, timeLimit: number) => void
  updateProgress: (my: any, opponent: any) => void
  setTimeRemaining: (time: number) => void
  setCode: (code: string) => void
  endBattle: (winner: string | null) => void
  reset: () => void
}

export const useBattleStore = create<BattleState>((set) => ({
  battleId: null,
  problem: null,
  opponent: null,
  myProgress: { tests_passed: 0, code_lines: 0, attempts: 0 },
  opponentProgress: { tests_passed: 0, code_lines: 0 },
  timeRemaining: 0,
  status: 'idle',
  winner: null,
  code: '',
  startBattle: (id, problem, opponent, timeLimit) =>
    set({
      battleId: id,
      problem,
      opponent,
      timeRemaining: timeLimit,
      status: opponent ? 'in_progress' : 'waiting',
      myProgress: { tests_passed: 0, code_lines: 0, attempts: 0 },
      opponentProgress: { tests_passed: 0, code_lines: 0 },
      winner: null,
      code: problem?.starter_code?.python || '',
    }),
  updateProgress: (my, opponent) =>
    set({
      myProgress: my,
      opponentProgress: opponent,
    }),
  setTimeRemaining: (time) => set({ timeRemaining: time }),
  setCode: (code) => set({ code }),
  endBattle: (winner) => set({ status: 'completed', winner }),
  reset: () =>
    set({
      battleId: null,
      problem: null,
      opponent: null,
      myProgress: { tests_passed: 0, code_lines: 0, attempts: 0 },
      opponentProgress: { tests_passed: 0, code_lines: 0 },
      timeRemaining: 0,
      status: 'idle',
      winner: null,
      code: '',
    }),
}))

interface UIState {
  sidebarOpen: boolean
  theme: 'dark' | 'light'
  editorFontSize: number
  toggleSidebar: () => void
  setTheme: (theme: 'dark' | 'light') => void
  setEditorFontSize: (size: number) => void
}

export const useUIStore = create<UIState>()(
  persist(
    (set) => ({
      sidebarOpen: true,
      theme: 'dark',
      editorFontSize: 14,
      toggleSidebar: () => set((state) => ({ sidebarOpen: !state.sidebarOpen })),
      setTheme: (theme) => set({ theme }),
      setEditorFontSize: (size) => set({ editorFontSize: size }),
    }),
    {
      name: 'ui-storage',
    }
  )
)


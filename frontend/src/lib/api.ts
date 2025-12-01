/**
 * API Client for AI Coding Teacher
 */

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api'

interface FetchOptions extends RequestInit {
  token?: string
}

async function fetchAPI<T>(endpoint: string, options: FetchOptions = {}): Promise<T> {
  const { token, ...fetchOptions } = options
  
  const headers: HeadersInit = {
    'Content-Type': 'application/json',
    ...options.headers,
  }
  
  if (token) {
    headers['Authorization'] = `Bearer ${token}`
  }
  
  const response = await fetch(`${API_BASE}${endpoint}`, {
    ...fetchOptions,
    headers,
  })
  
  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'An error occurred' }))
    throw new Error(error.detail || `HTTP error! status: ${response.status}`)
  }
  
  return response.json()
}

// ============== Auth ==============

export interface User {
  id: number
  email: string
  username: string
  avatar_url?: string
  skill_level: string
  knowledge_state: Record<string, number>
  elo_rating: number
  problems_solved: number
  interviews_completed: number
  battles_won: number
  current_streak: number
}

export interface LoginResponse {
  access_token: string
  token_type: string
}

export const auth = {
  login: (email: string, password: string) =>
    fetchAPI<LoginResponse>('/users/login', {
      method: 'POST',
      body: new URLSearchParams({ username: email, password }).toString(),
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    }),
  
  register: (email: string, username: string, password: string) =>
    fetchAPI<User>('/users/register', {
      method: 'POST',
      body: JSON.stringify({ email, username, password }),
    }),
  
  getMe: (token: string) =>
    fetchAPI<User>('/users/me', { token }),
  
  getStats: (token: string) =>
    fetchAPI<any>('/users/me/stats', { token }),
}

// ============== Problems ==============

export interface Problem {
  id: number
  title: string
  slug: string
  description: string
  difficulty: 'easy' | 'medium' | 'hard'
  examples: Array<{ input: string; output: string; explanation?: string }>
  constraints: string[]
  starter_code: Record<string, string>
  topics: string[]
  companies: string[]
  patterns: string[]
  hints: string[]
  acceptance_rate: number
  submission_count: number
}

export interface ProblemListItem {
  id: number
  title: string
  slug: string
  difficulty: string
  topics: string[]
  companies: string[]
  acceptance_rate: number
  submission_count: number
}

export interface Submission {
  id: number
  problem_id: number
  code: string
  language: string
  status: string
  runtime_ms?: number
  memory_kb?: number
  test_results: any[]
  ai_feedback?: string
  created_at: string
}

export const problems = {
  list: (params?: { difficulty?: string; topic?: string; company?: string; search?: string }) => {
    const searchParams = new URLSearchParams()
    if (params?.difficulty) searchParams.set('difficulty', params.difficulty)
    if (params?.topic) searchParams.set('topic', params.topic)
    if (params?.company) searchParams.set('company', params.company)
    if (params?.search) searchParams.set('search', params.search)
    const query = searchParams.toString()
    return fetchAPI<ProblemListItem[]>(`/problems${query ? `?${query}` : ''}`)
  },
  
  get: (slug: string) =>
    fetchAPI<Problem>(`/problems/${slug}`),
  
  getHints: (slug: string, level: number = 1) =>
    fetchAPI<{ hints: string[] }>(`/problems/${slug}/hints?hint_level=${level}`),
  
  getSolutions: (slug: string, token: string) =>
    fetchAPI<{ solutions: any[]; time_complexity: string; space_complexity: string }>(
      `/problems/${slug}/solutions`,
      { token }
    ),
  
  submit: (slug: string, code: string, language: string, token: string) =>
    fetchAPI<Submission>(`/problems/${slug}/submit`, {
      method: 'POST',
      body: JSON.stringify({ problem_id: 0, code, language }),
      token,
    }),
  
  getSubmissions: (slug: string, token: string) =>
    fetchAPI<Submission[]>(`/problems/${slug}/submissions`, { token }),
  
  getRecommended: (token: string, limit: number = 5) =>
    fetchAPI<Array<{ problem: ProblemListItem; reason: string }>>(
      `/problems/recommended?limit=${limit}`,
      { token }
    ),
  
  getTopics: () =>
    fetchAPI<string[]>('/problems/topics'),
  
  getCompanies: () =>
    fetchAPI<string[]>('/problems/companies'),
}

// ============== Code Execution ==============

export interface ExecutionResult {
  success: boolean
  output: string
  error?: string
}

export interface TestResult {
  status: string
  test_results: Array<{
    test_case: number
    input: string
    expected_output: string
    actual_output: string
    passed: boolean
    runtime_ms?: number
    error?: string
  }>
  passed_count: number
  total_count: number
}

export const execution = {
  run: (code: string, language: string, stdin: string = '') =>
    fetchAPI<ExecutionResult>('/execute/run', {
      method: 'POST',
      body: JSON.stringify({ code, language, stdin }),
    }),
  
  test: (code: string, language: string, testCases: Array<{ input: string; expected_output: string }>) =>
    fetchAPI<TestResult>('/execute/test', {
      method: 'POST',
      body: JSON.stringify({ code, language, test_cases: testCases }),
    }),
  
  getLanguages: () =>
    fetchAPI<{ languages: Array<{ id: string; name: string; version: string }> }>('/execute/languages'),
}

// ============== Interviews ==============

export interface InterviewConfig {
  interview_type: 'algorithm' | 'system_design' | 'behavioral' | 'frontend'
  company: string
  difficulty: string
  duration_minutes: number
}

export interface InterviewSession {
  interview_id: number
  interview_type: string
  company: string
  difficulty: string
  duration_minutes: number
  problem: { title: string; description: string }
  initial_message: string
}

export interface InterviewMessage {
  response: string
  timestamp: string
}

export interface InterviewReport {
  interview_id: number
  report: {
    overall_score: number
    dimension_scores: Record<string, number>
    strengths: string[]
    improvements: string[]
    suggestions: string[]
    recommended_topics: string[]
  }
}

export const interviews = {
  start: (config: InterviewConfig, token: string) =>
    fetchAPI<InterviewSession>('/interviews/start', {
      method: 'POST',
      body: JSON.stringify(config),
      token,
    }),
  
  sendMessage: (interviewId: number, message: string, code?: string, token?: string) =>
    fetchAPI<InterviewMessage>(`/interviews/${interviewId}/message`, {
      method: 'POST',
      body: JSON.stringify({ interview_id: interviewId, message, code }),
      token,
    }),
  
  end: (interviewId: number, finalCode: string, token: string) =>
    fetchAPI<InterviewReport>(`/interviews/${interviewId}/end`, {
      method: 'POST',
      body: JSON.stringify({ final_code: finalCode }),
      token,
    }),
  
  get: (interviewId: number, token: string) =>
    fetchAPI<any>(`/interviews/${interviewId}`, { token }),
  
  list: (token: string, status?: string) => {
    const query = status ? `?status=${status}` : ''
    return fetchAPI<any[]>(`/interviews${query}`, { token })
  },
}

// ============== Battles ==============

export interface BattleSession {
  battle_id: number
  problem: ProblemListItem & { description?: string; examples?: any[]; starter_code?: Record<string, string> }
  mode: string
  status: string
  opponent?: string
  time_limit_seconds: number
}

export interface BattleStatus {
  id: number
  problem: any
  player1: { username: string; progress: any }
  player2?: { username: string; progress: any }
  mode: string
  status: string
  time_remaining_seconds: number
  winner?: string
}

export interface BattleSubmitResult {
  passed: boolean
  tests_passed: number
  total_tests: number
  score: number
  is_winner: boolean
  test_results: any[]
}

export const battles = {
  create: (mode: string, friendUsername?: string, token?: string) =>
    fetchAPI<BattleSession>('/battles/create', {
      method: 'POST',
      body: JSON.stringify({ mode, friend_username: friendUsername }),
      token,
    }),
  
  join: (battleId: number, token: string) =>
    fetchAPI<BattleSession>(`/battles/${battleId}/join`, {
      method: 'POST',
      token,
    }),
  
  get: (battleId: number, token: string) =>
    fetchAPI<BattleStatus>(`/battles/${battleId}`, { token }),
  
  submit: (battleId: number, code: string, language: string, token: string) =>
    fetchAPI<BattleSubmitResult>(`/battles/${battleId}/submit`, {
      method: 'POST',
      body: JSON.stringify({ code, language }),
      token,
    }),
  
  list: (token: string, status?: string) => {
    const query = status ? `?status=${status}` : ''
    return fetchAPI<any[]>(`/battles${query}`, { token })
  },
  
  getQueueStatus: (token: string) =>
    fetchAPI<{ queue_length: number; estimated_wait_seconds: number }>(
      '/battles/matchmaking/queue',
      { token }
    ),
}

// ============== Leaderboard ==============

export const leaderboard = {
  get: (limit: number = 100) =>
    fetchAPI<Array<{
      rank: number
      username: string
      avatar_url?: string
      elo_rating: number
      problems_solved: number
      battles_won: number
    }>>(`/users/leaderboard?limit=${limit}`),
}


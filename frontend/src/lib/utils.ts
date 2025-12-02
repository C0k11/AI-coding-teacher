import { clsx, type ClassValue } from 'clsx'
import { twMerge } from 'tailwind-merge'

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

export function formatTime(seconds: number): string {
  const mins = Math.floor(seconds / 60)
  const secs = seconds % 60
  return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`
}

export function formatDate(date: string | Date): string {
  return new Date(date).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  })
}

export function formatDateTime(date: string | Date): string {
  return new Date(date).toLocaleString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  })
}

export function getDifficultyColor(difficulty: string): string {
  switch (difficulty.toLowerCase()) {
    case 'easy':
      return 'text-green-400'
    case 'medium':
      return 'text-yellow-400'
    case 'hard':
      return 'text-red-400'
    default:
      return 'text-gray-400'
  }
}

export function getDifficultyBadgeClass(difficulty: string): string {
  switch (difficulty.toLowerCase()) {
    case 'easy':
      return 'badge-easy'
    case 'medium':
      return 'badge-medium'
    case 'hard':
      return 'badge-hard'
    default:
      return 'bg-gray-500/20 text-gray-400'
  }
}

export function getStatusColor(status: string): string {
  switch (status.toLowerCase()) {
    case 'accepted':
      return 'text-green-400'
    case 'wrong_answer':
      return 'text-red-400'
    case 'time_limit_exceeded':
      return 'text-yellow-400'
    case 'runtime_error':
      return 'text-orange-400'
    case 'compile_error':
      return 'text-red-400'
    default:
      return 'text-gray-400'
  }
}

export function getStatusText(status: string): string {
  switch (status.toLowerCase()) {
    case 'accepted':
      return 'Accepted'
    case 'wrong_answer':
      return 'Wrong Answer'
    case 'time_limit_exceeded':
      return 'Time Limit Exceeded'
    case 'runtime_error':
      return 'Runtime Error'
    case 'compile_error':
      return 'Compile Error'
    default:
      return status
  }
}

export function truncateText(text: string, maxLength: number): string {
  if (text.length <= maxLength) return text
  return text.slice(0, maxLength) + '...'
}

export function debounce<T extends (...args: any[]) => any>(
  func: T,
  wait: number
): (...args: Parameters<T>) => void {
  let timeout: NodeJS.Timeout | null = null
  
  return (...args: Parameters<T>) => {
    if (timeout) clearTimeout(timeout)
    timeout = setTimeout(() => func(...args), wait)
  }
}

export function throttle<T extends (...args: any[]) => any>(
  func: T,
  limit: number
): (...args: Parameters<T>) => void {
  let inThrottle: boolean = false
  
  return (...args: Parameters<T>) => {
    if (!inThrottle) {
      func(...args)
      inThrottle = true
      setTimeout(() => (inThrottle = false), limit)
    }
  }
}

// Language mapping for Monaco Editor
export function getMonacoLanguage(language: string): string {
  const mapping: Record<string, string> = {
    python: 'python',
    python3: 'python',
    javascript: 'javascript',
    typescript: 'typescript',
    java: 'java',
    cpp: 'cpp',
    'c++': 'cpp',
    go: 'go',
    rust: 'rust',
  }
  return mapping[language.toLowerCase()] || 'plaintext'
}

// Calculate ELO rating change
export function calculateEloChange(
  playerRating: number,
  opponentRating: number,
  won: boolean,
  kFactor: number = 32
): number {
  const expectedScore = 1 / (1 + Math.pow(10, (opponentRating - playerRating) / 400))
  const actualScore = won ? 1 : 0
  return Math.round(kFactor * (actualScore - expectedScore))
}

// Generate avatar placeholder
export function getAvatarUrl(username: string): string {
  return `https://api.dicebear.com/7.x/identicon/svg?seed=${encodeURIComponent(username)}`
}

// Local storage helpers with SSR safety
export const storage = {
  get: (key: string): string | null => {
    if (typeof window === 'undefined') return null
    return localStorage.getItem(key)
  },
  set: (key: string, value: string): void => {
    if (typeof window === 'undefined') return
    localStorage.setItem(key, value)
  },
  remove: (key: string): void => {
    if (typeof window === 'undefined') return
    localStorage.removeItem(key)
  },
}


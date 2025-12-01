'use client'

import { useState, useEffect, useRef } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'
import { 
  Code2, 
  Brain, 
  Send, 
  Clock, 
  Mic, 
  MicOff,
  StopCircle,
  Play
} from 'lucide-react'
import CodeEditor from '@/components/CodeEditor'
import { cn, formatTime } from '@/lib/utils'
import { interviews } from '@/lib/api'
import { useAuthStore, useInterviewStore } from '@/store/useStore'

export default function InterviewSessionPage() {
  const router = useRouter()
  const { token } = useAuthStore()
  const { 
    interviewId, 
    interviewType, 
    company, 
    problem, 
    messages, 
    code, 
    isActive,
    addMessage, 
    setCode, 
    endInterview 
  } = useInterviewStore()

  const [inputMessage, setInputMessage] = useState('')
  const [isSending, setIsSending] = useState(false)
  const [timeRemaining, setTimeRemaining] = useState(45 * 60) // 45 minutes
  const [isRecording, setIsRecording] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  // Redirect if no active interview
  useEffect(() => {
    if (!isActive || !interviewId) {
      router.push('/interview')
    }
  }, [isActive, interviewId, router])

  // Timer
  useEffect(() => {
    const timer = setInterval(() => {
      setTimeRemaining((prev) => {
        if (prev <= 0) {
          handleEndInterview()
          return 0
        }
        return prev - 1
      })
    }, 1000)

    return () => clearInterval(timer)
  }, [])

  // Scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  const handleSendMessage = async () => {
    if (!inputMessage.trim() || isSending) return

    const userMessage = inputMessage.trim()
    setInputMessage('')
    setIsSending(true)

    // Add user message
    addMessage('user', userMessage)

    try {
      // Get AI response
      if (token && interviewId) {
        try {
          const response = await interviews.sendMessage(interviewId, userMessage, code, token)
          addMessage('assistant', response.response)
        } catch (error) {
          // Fallback to mock response
          setTimeout(() => {
            const mockResponse = getMockResponse(userMessage, code)
            addMessage('assistant', mockResponse)
          }, 1000)
        }
      } else {
        // Mock response for demo
        setTimeout(() => {
          const mockResponse = getMockResponse(userMessage, code)
          addMessage('assistant', mockResponse)
        }, 1000)
      }
    } catch (error) {
      console.error('Failed to send message:', error)
      addMessage('assistant', '抱歉，出现了一些问题。请重试。')
    } finally {
      setIsSending(false)
    }
  }

  const getMockResponse = (message: string, currentCode: string): string => {
    // Simple mock responses based on message content
    if (message.includes('你好') || message.includes('介绍')) {
      return '很高兴认识你！让我们开始今天的面试吧。你能先说说你对这道题的初步想法吗？'
    }
    if (currentCode && currentCode.length > 100) {
      return '我看到你已经开始写代码了。能解释一下你的思路吗？这个方法的时间复杂度是多少？'
    }
    if (message.includes('提示') || message.includes('帮助')) {
      return '提示：你可以考虑使用哈希表来优化查找时间。想想如何用空间换时间。'
    }
    return '好的，继续说下去。你能更详细地解释一下这个思路吗？考虑一下边缘情况。'
  }

  const handleEndInterview = async () => {
    try {
      if (token && interviewId) {
        const report = await interviews.end(interviewId, code, token)
        console.log('Interview report:', report)
      }
    } catch (error) {
      console.error('Failed to end interview:', error)
    }
    
    endInterview()
    router.push('/interview/report')
  }

  const toggleRecording = () => {
    setIsRecording(!isRecording)
    // TODO: Implement speech recognition
  }

  if (!isActive) {
    return null
  }

  return (
    <div className="min-h-screen bg-dark-900 flex flex-col">
      {/* Navigation */}
      <nav className="sticky top-0 z-50 bg-dark-900/80 backdrop-blur-xl border-b border-dark-700">
        <div className="px-4 py-3 flex items-center justify-between">
          <div className="flex items-center gap-4">
            <Link href="/" className="flex items-center gap-2">
              <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-purple-500 to-pink-500 flex items-center justify-center">
                <Code2 className="w-5 h-5 text-white" />
              </div>
            </Link>
            <div className="flex items-center gap-2">
              <span className="font-semibold">AI 面试 - {company}</span>
              <span className="px-2 py-0.5 bg-purple-500/20 text-purple-400 rounded text-sm">
                {interviewType}
              </span>
            </div>
          </div>

          <div className="flex items-center gap-4">
            {/* Timer */}
            <div className={cn(
              'flex items-center gap-2 px-4 py-2 rounded-lg font-mono',
              timeRemaining < 300 ? 'bg-red-500/20 text-red-400' : 'bg-dark-700'
            )}>
              <Clock className="w-4 h-4" />
              {formatTime(timeRemaining)}
            </div>

            <button
              onClick={handleEndInterview}
              className="flex items-center gap-2 px-4 py-2 bg-red-500/20 text-red-400 rounded-lg hover:bg-red-500/30 transition"
            >
              <StopCircle className="w-4 h-4" />
              结束面试
            </button>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <div className="flex-1 flex">
        {/* Left Panel - Code Editor */}
        <div className="w-1/2 border-r border-dark-700 flex flex-col">
          <div className="px-4 py-2 bg-dark-800 border-b border-dark-700">
            <h3 className="font-medium">代码编辑器</h3>
          </div>
          <div className="flex-1">
            <CodeEditor
              code={code}
              language="python"
              onChange={setCode}
              height="calc(100vh - 180px)"
              showActions={false}
            />
          </div>
        </div>

        {/* Right Panel - Chat */}
        <div className="w-1/2 flex flex-col">
          {/* Problem Description */}
          {problem && (
            <div className="px-4 py-3 bg-dark-800 border-b border-dark-700">
              <h3 className="font-semibold">{problem.title}</h3>
              <p className="text-dark-400 text-sm mt-1">{problem.description}</p>
            </div>
          )}

          {/* Messages */}
          <div className="flex-1 overflow-y-auto p-4 space-y-4">
            {messages.map((msg, i) => (
              <div
                key={i}
                className={cn(
                  'flex gap-3',
                  msg.role === 'user' ? 'flex-row-reverse' : ''
                )}
              >
                <div className={cn(
                  'w-10 h-10 rounded-full flex items-center justify-center flex-shrink-0',
                  msg.role === 'user'
                    ? 'bg-blue-500'
                    : 'bg-gradient-to-br from-purple-500 to-pink-500'
                )}>
                  {msg.role === 'user' ? (
                    <span className="font-bold">你</span>
                  ) : (
                    <Brain className="w-5 h-5 text-white" />
                  )}
                </div>
                <div className={cn(
                  'max-w-[80%] rounded-2xl px-4 py-3',
                  msg.role === 'user'
                    ? 'bg-blue-500 rounded-tr-none'
                    : 'bg-dark-700 rounded-tl-none'
                )}>
                  <p className="text-sm whitespace-pre-wrap">{msg.content}</p>
                  <span className="text-xs text-dark-400 mt-1 block">
                    {new Date(msg.timestamp).toLocaleTimeString()}
                  </span>
                </div>
              </div>
            ))}
            
            {isSending && (
              <div className="flex gap-3">
                <div className="w-10 h-10 rounded-full bg-gradient-to-br from-purple-500 to-pink-500 flex items-center justify-center">
                  <Brain className="w-5 h-5 text-white" />
                </div>
                <div className="bg-dark-700 rounded-2xl rounded-tl-none px-4 py-3">
                  <div className="flex gap-1">
                    <span className="w-2 h-2 bg-dark-400 rounded-full animate-bounce" />
                    <span className="w-2 h-2 bg-dark-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }} />
                    <span className="w-2 h-2 bg-dark-400 rounded-full animate-bounce" style={{ animationDelay: '0.4s' }} />
                  </div>
                </div>
              </div>
            )}
            
            <div ref={messagesEndRef} />
          </div>

          {/* Input */}
          <div className="p-4 border-t border-dark-700">
            <div className="flex items-end gap-2">
              <button
                onClick={toggleRecording}
                className={cn(
                  'p-3 rounded-lg transition',
                  isRecording
                    ? 'bg-red-500 text-white'
                    : 'bg-dark-700 text-dark-300 hover:text-white'
                )}
              >
                {isRecording ? <MicOff className="w-5 h-5" /> : <Mic className="w-5 h-5" />}
              </button>
              
              <div className="flex-1 relative">
                <textarea
                  value={inputMessage}
                  onChange={(e) => setInputMessage(e.target.value)}
                  onKeyDown={(e) => {
                    if (e.key === 'Enter' && !e.shiftKey) {
                      e.preventDefault()
                      handleSendMessage()
                    }
                  }}
                  placeholder="输入你的回答... (按 Enter 发送)"
                  rows={2}
                  className="w-full px-4 py-3 bg-dark-800 border border-dark-700 rounded-lg resize-none focus:outline-none focus:ring-2 focus:ring-purple-500"
                />
              </div>
              
              <button
                onClick={handleSendMessage}
                disabled={!inputMessage.trim() || isSending}
                className={cn(
                  'p-3 rounded-lg transition',
                  inputMessage.trim() && !isSending
                    ? 'bg-purple-500 text-white hover:bg-purple-600'
                    : 'bg-dark-700 text-dark-500 cursor-not-allowed'
                )}
              >
                <Send className="w-5 h-5" />
              </button>
            </div>
            
            <p className="text-xs text-dark-500 mt-2">
              提示：你可以边说边写代码，面试官会观察你的代码
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}


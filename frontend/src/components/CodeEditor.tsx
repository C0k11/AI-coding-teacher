'use client'

import { useRef, useEffect, useState } from 'react'
import Editor, { OnMount, OnChange } from '@monaco-editor/react'
import { Play, Send, RotateCcw, Settings } from 'lucide-react'
import { cn, getMonacoLanguage } from '@/lib/utils'
import { useUIStore } from '@/store/useStore'

interface CodeEditorProps {
  code: string
  language: string
  onChange: (code: string) => void
  onRun?: () => void
  onSubmit?: () => void
  onReset?: () => void
  readOnly?: boolean
  height?: string
  showActions?: boolean
  isRunning?: boolean
  isSubmitting?: boolean
  languages?: string[]
  onLanguageChange?: (language: string) => void
}

export default function CodeEditor({
  code,
  language,
  onChange,
  onRun,
  onSubmit,
  onReset,
  readOnly = false,
  height = '500px',
  showActions = true,
  isRunning = false,
  isSubmitting = false,
  languages = ['python', 'javascript', 'java', 'cpp'],
  onLanguageChange,
}: CodeEditorProps) {
  const editorRef = useRef<any>(null)
  const { editorFontSize } = useUIStore()
  const [mounted, setMounted] = useState(false)

  useEffect(() => {
    setMounted(true)
  }, [])

  const handleEditorDidMount: OnMount = (editor, monaco) => {
    editorRef.current = editor

    // Define custom dark theme
    monaco.editor.defineTheme('ai-coding-dark', {
      base: 'vs-dark',
      inherit: true,
      rules: [
        { token: 'comment', foreground: '6e7681', fontStyle: 'italic' },
        { token: 'keyword', foreground: 'ff7b72' },
        { token: 'string', foreground: 'a5d6ff' },
        { token: 'number', foreground: '79c0ff' },
        { token: 'function', foreground: 'd2a8ff' },
        { token: 'variable', foreground: 'ffa657' },
        { token: 'type', foreground: '7ee787' },
      ],
      colors: {
        'editor.background': '#0d1117',
        'editor.foreground': '#c9d1d9',
        'editor.lineHighlightBackground': '#161b22',
        'editor.selectionBackground': '#264f78',
        'editorCursor.foreground': '#c9d1d9',
        'editorLineNumber.foreground': '#484f58',
        'editorLineNumber.activeForeground': '#c9d1d9',
      },
    })

    monaco.editor.setTheme('ai-coding-dark')

    // Keyboard shortcuts
    editor.addCommand(monaco.KeyMod.CtrlCmd | monaco.KeyCode.Enter, () => {
      onRun?.()
    })

    editor.addCommand(monaco.KeyMod.CtrlCmd | monaco.KeyMod.Shift | monaco.KeyCode.Enter, () => {
      onSubmit?.()
    })
  }

  const handleChange: OnChange = (value) => {
    onChange(value || '')
  }

  if (!mounted) {
    return (
      <div 
        className="bg-dark-900 rounded-lg border border-dark-700 flex items-center justify-center"
        style={{ height }}
      >
        <div className="animate-pulse text-dark-400">加载编辑器...</div>
      </div>
    )
  }

  return (
    <div className="flex flex-col rounded-lg border border-dark-700 overflow-hidden bg-dark-900">
      {/* Toolbar */}
      {showActions && (
        <div className="flex items-center justify-between px-4 py-2 bg-dark-800 border-b border-dark-700">
          <div className="flex items-center gap-2">
            <select
              value={language}
              onChange={(e) => onLanguageChange?.(e.target.value)}
              className="px-3 py-1.5 bg-dark-700 border border-dark-600 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-purple-500"
            >
              {languages.map((lang) => (
                <option key={lang} value={lang}>
                  {lang.charAt(0).toUpperCase() + lang.slice(1)}
                </option>
              ))}
            </select>
          </div>

          <div className="flex items-center gap-2">
            {onReset && (
              <button
                onClick={onReset}
                className="p-2 text-dark-400 hover:text-white hover:bg-dark-700 rounded-lg transition"
                title="重置代码"
              >
                <RotateCcw className="w-4 h-4" />
              </button>
            )}

            {onRun && (
              <button
                onClick={onRun}
                disabled={isRunning}
                className={cn(
                  'flex items-center gap-2 px-4 py-1.5 rounded-lg font-medium text-sm transition',
                  isRunning
                    ? 'bg-dark-600 text-dark-400 cursor-not-allowed'
                    : 'bg-dark-700 text-white hover:bg-dark-600'
                )}
              >
                <Play className="w-4 h-4" />
                {isRunning ? '运行中...' : '运行'}
              </button>
            )}

            {onSubmit && (
              <button
                onClick={onSubmit}
                disabled={isSubmitting}
                className={cn(
                  'flex items-center gap-2 px-4 py-1.5 rounded-lg font-medium text-sm transition',
                  isSubmitting
                    ? 'bg-green-900 text-green-400 cursor-not-allowed'
                    : 'bg-green-600 text-white hover:bg-green-500'
                )}
              >
                <Send className="w-4 h-4" />
                {isSubmitting ? '提交中...' : '提交'}
              </button>
            )}
          </div>
        </div>
      )}

      {/* Editor */}
      <Editor
        height={height}
        language={getMonacoLanguage(language)}
        value={code}
        onChange={handleChange}
        onMount={handleEditorDidMount}
        options={{
          readOnly,
          fontSize: editorFontSize,
          fontFamily: "'JetBrains Mono', 'Fira Code', monospace",
          fontLigatures: true,
          minimap: { enabled: false },
          scrollBeyondLastLine: false,
          automaticLayout: true,
          tabSize: 4,
          wordWrap: 'on',
          lineNumbers: 'on',
          renderLineHighlight: 'all',
          cursorBlinking: 'smooth',
          smoothScrolling: true,
          padding: { top: 16, bottom: 16 },
        }}
        theme="vs-dark"
      />
    </div>
  )
}


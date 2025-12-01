import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'AI Coding Teacher - 智能编程导师',
  description: 'AI驱动的编程学习平台，包含面试模拟、代码对战、个性化学习',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="zh">
      <body className="font-sans antialiased bg-dark-900 text-dark-100">
        {children}
      </body>
    </html>
  )
}


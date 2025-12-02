import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'AI Coding Teacher - Intelligent Programming Tutor',
  description: 'AI-powered programming learning platform with interview simulation, code battles, and personalized learning',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
      <html lang="en">
      <body className="font-sans antialiased bg-dark-900 text-dark-100">
        {children}
      </body>
    </html>
  )
}


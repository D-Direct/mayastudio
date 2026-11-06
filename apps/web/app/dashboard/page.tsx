'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import type { User } from '@supabase/supabase-js'
import { supabase } from '@/lib/supabase'

export default function DashboardPage() {
  const [user, setUser] = useState<User | null>(null)
  const [loading, setLoading] = useState(true)
  const router = useRouter()

  useEffect(() => {
    const getUser = async () => {
      const { data: { user } } = await supabase.auth.getUser()

      if (!user) {
        router.push('/login')
        return
      }

      setUser(user)
      setLoading(false)
    }

    getUser()
  }, [supabase, router])

  const handleSignOut = async () => {
    await supabase.auth.signOut()
    router.push('/')
  }

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex justify-between items-center">
          <div className="flex items-center gap-2">
            <span className="text-2xl">🎬</span>
            <h1 className="text-xl font-bold text-gray-900">MayaStudio AI</h1>
          </div>
          <div className="flex items-center gap-4">
            <div className="text-right">
              <p className="text-sm text-gray-600">{user?.email}</p>
              <p className="text-xs text-gray-500">100 credits remaining</p>
            </div>
            <button
              onClick={handleSignOut}
              className="px-4 py-2 text-sm text-gray-600 hover:text-gray-900"
            >
              Sign Out
            </button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Welcome Banner */}
        <div className="bg-gradient-to-r from-blue-600 to-indigo-600 rounded-lg p-8 text-white mb-8">
          <h2 className="text-3xl font-bold mb-2">Welcome to MayaStudio AI!</h2>
          <p className="text-blue-100 mb-4">
            Your AI-powered video creation studio is ready. Start creating amazing content!
          </p>
          <button className="px-6 py-3 bg-white text-blue-600 rounded-lg font-medium hover:bg-blue-50 transition">
            + Create New Project
          </button>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center justify-between mb-2">
              <h3 className="text-sm font-medium text-gray-600">Total Projects</h3>
              <span className="text-2xl">📁</span>
            </div>
            <p className="text-3xl font-bold text-gray-900">0</p>
            <p className="text-sm text-gray-500 mt-1">No projects yet</p>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center justify-between mb-2">
              <h3 className="text-sm font-medium text-gray-600">Videos Rendered</h3>
              <span className="text-2xl">🎥</span>
            </div>
            <p className="text-3xl font-bold text-gray-900">0</p>
            <p className="text-sm text-gray-500 mt-1">Ready to create your first</p>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center justify-between mb-2">
              <h3 className="text-sm font-medium text-gray-600">Google Drive</h3>
              <span className="text-2xl">☁️</span>
            </div>
            <p className="text-sm font-medium text-green-600">Connected</p>
            <p className="text-sm text-gray-500 mt-1">Files saved to your drive</p>
          </div>
        </div>

        {/* Recent Projects */}
        <div className="bg-white rounded-lg shadow">
          <div className="p-6 border-b border-gray-200">
            <h3 className="text-lg font-semibold text-gray-900">Recent Projects</h3>
          </div>
          <div className="p-12 text-center">
            <div className="text-6xl mb-4">📽️</div>
            <h4 className="text-lg font-medium text-gray-900 mb-2">No projects yet</h4>
            <p className="text-gray-600 mb-6">
              Create your first project to start making amazing videos with AI
            </p>
            <button className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition">
              Create Your First Project
            </button>
          </div>
        </div>

        {/* Quick Start Guide */}
        <div className="mt-8 bg-blue-50 border border-blue-200 rounded-lg p-6">
          <h3 className="font-semibold text-blue-900 mb-4">🚀 Quick Start Guide</h3>
          <ol className="space-y-3 text-sm text-blue-800">
            <li className="flex gap-3">
              <span className="font-bold">1.</span>
              <span>Create a new project and give it a name</span>
            </li>
            <li className="flex gap-3">
              <span className="font-bold">2.</span>
              <span>Write your script or paste existing dialogue</span>
            </li>
            <li className="flex gap-3">
              <span className="font-bold">3.</span>
              <span>Assign voices to characters using AI voice synthesis</span>
            </li>
            <li className="flex gap-3">
              <span className="font-bold">4.</span>
              <span>Upload or select background images/videos</span>
            </li>
            <li className="flex gap-3">
              <span className="font-bold">5.</span>
              <span>Click render and let AI create your video!</span>
            </li>
          </ol>
        </div>
      </main>
    </div>
  )
}

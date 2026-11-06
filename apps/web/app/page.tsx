export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-24">
      <div className="text-center">
        <h1 className="text-6xl font-bold mb-4">
          🎬 MayaStudio AI
        </h1>
        <p className="text-xl text-gray-600 mb-8">
          Multi-Speaker AI Voice & Video Studio for YouTube Shorts & Series
        </p>
        <p className="text-sm text-gray-500 mb-4">
          Create engaging video content with AI-powered voice synthesis
        </p>
        <div className="flex gap-4 justify-center">
          <a
            href="/login"
            className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition"
          >
            Get Started
          </a>
          <a
            href="https://github.com/D-Direct/mayastudio"
            target="_blank"
            rel="noopener noreferrer"
            className="px-6 py-3 border border-gray-300 rounded-lg hover:border-gray-400 transition"
          >
            View on GitHub
          </a>
        </div>
        <div className="mt-12 grid grid-cols-1 md:grid-cols-3 gap-6 text-left">
          <div className="p-6 border rounded-lg">
            <h3 className="font-bold mb-2">🎤 AI Voice Synthesis</h3>
            <p className="text-sm text-gray-600">
              Multi-speaker voice design and cloning with Google Cloud TTS
            </p>
          </div>
          <div className="p-6 border rounded-lg">
            <h3 className="font-bold mb-2">✏️ Smart Editor</h3>
            <p className="text-sm text-gray-600">
              Line-by-line dialogue editor with instant regeneration
            </p>
          </div>
          <div className="p-6 border rounded-lg">
            <h3 className="font-bold mb-2">🎬 Auto Assembly</h3>
            <p className="text-sm text-gray-600">
              Automated video stitching with subtitles and effects
            </p>
          </div>
        </div>
      </div>
    </main>
  )
}

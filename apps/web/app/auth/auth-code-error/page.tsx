export default function AuthCodeError() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-red-50 to-orange-100">
      <div className="max-w-md w-full mx-4">
        <div className="bg-white rounded-2xl shadow-xl p-8">
          <div className="text-center mb-8">
            <div className="text-6xl mb-4">⚠️</div>
            <h1 className="text-3xl font-bold text-gray-900 mb-2">Authentication Error</h1>
            <p className="text-gray-600">
              We encountered an issue while signing you in with Google.
            </p>
          </div>

          <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-6">
            <h3 className="text-sm font-semibold text-red-900 mb-2">What happened?</h3>
            <p className="text-sm text-red-700">
              The authentication code could not be exchanged. This usually happens when:
            </p>
            <ul className="mt-2 space-y-1 text-sm text-red-700 list-disc list-inside">
              <li>The authentication process took too long</li>
              <li>The page was refreshed during sign-in</li>
              <li>The authentication code was already used</li>
            </ul>
          </div>

          <div className="space-y-3">
            <a
              href="/login"
              className="block w-full px-6 py-3 bg-blue-600 text-white text-center rounded-lg hover:bg-blue-700 transition font-medium"
            >
              Try Again
            </a>
            <a
              href="/"
              className="block w-full px-6 py-3 border-2 border-gray-300 text-gray-700 text-center rounded-lg hover:border-gray-400 transition font-medium"
            >
              Back to Home
            </a>
          </div>

          <div className="mt-6 pt-6 border-t border-gray-200">
            <p className="text-xs text-gray-500 text-center">
              If this problem persists, please contact support or try signing in again later.
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}

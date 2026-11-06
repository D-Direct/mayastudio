import { createClient } from '@/lib/supabase/server'
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

export async function GET(request: NextRequest) {
  const requestUrl = new URL(request.url)
  const { searchParams, origin } = requestUrl

  // Log all parameters for debugging
  console.log('Auth callback URL:', requestUrl.toString())
  console.log('Search params:', Object.fromEntries(searchParams.entries()))
  console.log('All search param keys:', Array.from(searchParams.keys()))
  console.log('Hash:', requestUrl.hash)
  console.log('Pathname:', requestUrl.pathname)

  // Check for error first
  const error_description = searchParams.get('error_description')
  if (error_description) {
    console.error('OAuth error in URL:', error_description)
    return NextResponse.redirect(`${origin}/auth/auth-code-error?error=${encodeURIComponent(error_description)}`)
  }

  const code = searchParams.get('code')
  const next = searchParams.get('next') ?? '/dashboard'

  console.log('Code parameter:', code ? 'present' : 'missing')

  if (code) {
    const supabase = await createClient()
    const { data, error } = await supabase.auth.exchangeCodeForSession(code)

    if (error) {
      console.error('Auth callback error:', error)
      return NextResponse.redirect(`${origin}/auth/auth-code-error?error=${encodeURIComponent(error.message)}`)
    }

    if (data.session) {
      const forwardedHost = request.headers.get('x-forwarded-host')
      const isLocalEnv = process.env.NODE_ENV === 'development'

      if (isLocalEnv) {
        return NextResponse.redirect(`${origin}${next}`)
      } else if (forwardedHost) {
        return NextResponse.redirect(`https://${forwardedHost}${next}`)
      } else {
        return NextResponse.redirect(`${origin}${next}`)
      }
    }
  }

  // No code parameter or no session
  return NextResponse.redirect(`${origin}/auth/auth-code-error?error=No authorization code provided`)
}

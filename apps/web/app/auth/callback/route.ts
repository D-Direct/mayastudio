import { createClient } from '@supabase/supabase-js'
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'
import { cookies } from 'next/headers'

export async function GET(request: NextRequest) {
  const requestUrl = new URL(request.url)
  const code = requestUrl.searchParams.get('code')

  if (code) {
    // Create a Supabase client for server-side use
    const supabase = createClient(
      process.env.NEXT_PUBLIC_SUPABASE_URL!,
      process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
      {
        auth: {
          flowType: 'pkce',
        },
      }
    )

    const { data, error } = await supabase.auth.exchangeCodeForSession(code)

    if (error) {
      console.error('Auth callback error:', error)
      return NextResponse.redirect(`${requestUrl.origin}/login?error=${error.message}`)
    }

    // Set the session in cookies
    if (data.session) {
      const response = NextResponse.redirect(`${requestUrl.origin}/dashboard`)

      // Set auth cookies
      response.cookies.set('sb-access-token', data.session.access_token, {
        path: '/',
        sameSite: 'lax',
        secure: true,
        httpOnly: true,
      })

      response.cookies.set('sb-refresh-token', data.session.refresh_token, {
        path: '/',
        sameSite: 'lax',
        secure: true,
        httpOnly: true,
      })

      return response
    }
  }

  // Redirect to dashboard after successful login
  return NextResponse.redirect(`${requestUrl.origin}/dashboard`)
}

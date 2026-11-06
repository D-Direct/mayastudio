# OAuth Authentication Flow

## Overview

MayaStudio AI uses Google OAuth for authentication via Supabase, implemented using the official `@supabase/ssr` package for Next.js 14 App Router. This document explains the complete authentication architecture and flow.

## Architecture

### Three Client Factories

The authentication system uses three separate Supabase client factories for different contexts:

1. **Browser Client** (`lib/supabase/client.ts`)
   - Used in Client Components
   - Runs in the browser
   - Reads session from cookies
   - Created with `createBrowserClient` from `@supabase/ssr`

2. **Server Client** (`lib/supabase/server.ts`)
   - Used in Server Components and Route Handlers
   - Runs on the server
   - Manages session cookies
   - Created with `createServerClient` from `@supabase/ssr`

3. **Middleware Client** (`lib/supabase/middleware.ts`)
   - Used in Next.js middleware
   - Refreshes sessions on every request
   - Updates session cookies
   - Created with `createServerClient` from `@supabase/ssr`

## Complete OAuth Flow

### Step-by-Step Process

```
┌─────────────────────────────────────────────────────────────────────────┐
│ 1. User visits login page                                              │
│    https://mayastudio-two.vercel.app/login                             │
└─────────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ 2. User clicks "Continue with Google" button                           │
│    - Client Component (app/login/page.tsx)                             │
│    - Uses Browser Client (lib/supabase/client.ts)                      │
│    - Calls: supabase.auth.signInWithOAuth()                            │
└─────────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ 3. Redirect to Google OAuth Consent Screen                             │
│    - User selects Google account                                       │
│    - User grants permissions:                                          │
│      • Email, Profile (OpenID)                                         │
│      • Google Drive (drive.file scope)                                 │
│    - Parameters:                                                       │
│      • access_type: offline                                            │
│      • prompt: consent                                                 │
│      • redirectTo: /auth/callback                                      │
└─────────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ 4. Google redirects to Supabase with authorization code                │
│    https://owlnunxiwpyxilsdqldn.supabase.co/auth/v1/callback           │
│    - Supabase validates the code with Google                           │
│    - Supabase creates/updates user record                              │
│    - Supabase generates session tokens                                 │
└─────────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ 5. Supabase redirects to callback route with code                      │
│    https://mayastudio-two.vercel.app/auth/callback?code=XXX            │
│    - Route Handler (app/auth/callback/route.ts)                        │
│    - Uses Server Client (lib/supabase/server.ts)                       │
│    - Calls: supabase.auth.exchangeCodeForSession(code)                 │
│    - Server client sets httpOnly cookies:                              │
│      • Session cookies managed by Supabase                             │
│      • Secure, httpOnly, sameSite=lax                                  │
└─────────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ 6. Redirect to dashboard                                               │
│    NextResponse.redirect('/dashboard')                                 │
└─────────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ 7. Middleware intercepts request                                       │
│    - Middleware (middleware.ts)                                        │
│    - Uses Middleware Client (lib/supabase/middleware.ts)               │
│    - Calls: supabase.auth.getUser()                                    │
│    - Refreshes session if needed                                       │
│    - Updates session cookies                                           │
│    - Allows request to proceed                                         │
└─────────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ 8. Dashboard page loads                                                │
│    - Client Component (app/dashboard/page.tsx)                         │
│    - Uses Browser Client (lib/supabase/client.ts)                      │
│    - Calls: supabase.auth.getUser()                                    │
│    - Reads session from cookies                                        │
│    - Displays user dashboard                                           │
│    - ✅ User is authenticated!                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

## Key Files

### 1. Browser Client (`apps/web/lib/supabase/client.ts`)

```typescript
import { createBrowserClient } from '@supabase/ssr'

export function createClient() {
  return createBrowserClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
  )
}
```

**Usage:**
- Client Components (marked with `'use client'`)
- Login page, Dashboard page
- Any component that runs in the browser

### 2. Server Client (`apps/web/lib/supabase/server.ts`)

```typescript
import { createServerClient } from '@supabase/ssr'
import { cookies } from 'next/headers'

export async function createClient() {
  const cookieStore = await cookies()

  return createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        getAll() {
          return cookieStore.getAll()
        },
        setAll(cookiesToSet) {
          try {
            cookiesToSet.forEach(({ name, value, options }) =>
              cookieStore.set(name, value, options)
            )
          } catch {
            // The `setAll` method was called from a Server Component.
            // This can be ignored if you have middleware refreshing
            // user sessions.
          }
        },
      },
    }
  )
}
```

**Usage:**
- Server Components
- Route Handlers (like `/auth/callback`)
- API routes
- Server Actions

### 3. Middleware Client (`apps/web/lib/supabase/middleware.ts`)

```typescript
import { createServerClient } from '@supabase/ssr'
import { NextResponse, type NextRequest } from 'next/server'

export async function updateSession(request: NextRequest) {
  let supabaseResponse = NextResponse.next({
    request,
  })

  const supabase = createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        getAll() {
          return request.cookies.getAll()
        },
        setAll(cookiesToSet) {
          cookiesToSet.forEach(({ name, value, options }) =>
            request.cookies.set(name, value)
          )
          supabaseResponse = NextResponse.next({
            request,
          })
          cookiesToSet.forEach(({ name, value, options }) =>
            supabaseResponse.cookies.set(name, value, options)
          )
        },
      },
    }
  )

  const {
    data: { user },
  } = await supabase.auth.getUser()

  if (
    !user &&
    !request.nextUrl.pathname.startsWith('/login') &&
    !request.nextUrl.pathname.startsWith('/auth')
  ) {
    const url = request.nextUrl.clone()
    url.pathname = '/login'
    return NextResponse.redirect(url)
  }

  return supabaseResponse
}
```

**Usage:**
- Next.js middleware
- Automatically runs on every request
- Refreshes sessions
- Protects routes

### 4. Middleware (`apps/web/middleware.ts`)

```typescript
import { type NextRequest } from 'next/server'
import { updateSession } from '@/lib/supabase/middleware'

export async function middleware(request: NextRequest) {
  return await updateSession(request)
}

export const config = {
  matcher: [
    '/((?!_next/static|_next/image|favicon.ico|.*\\.(?:svg|png|jpg|jpeg|gif|webp)$).*)',
  ],
}
```

### 5. OAuth Callback (`apps/web/app/auth/callback/route.ts`)

```typescript
import { createClient } from '@/lib/supabase/server'
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

export async function GET(request: NextRequest) {
  const { searchParams, origin } = new URL(request.url)
  const code = searchParams.get('code')
  const next = searchParams.get('next') ?? '/dashboard'

  if (code) {
    const supabase = await createClient()
    const { error } = await supabase.auth.exchangeCodeForSession(code)
    if (!error) {
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

  return NextResponse.redirect(`${origin}/auth/auth-code-error`)
}
```

## Environment Variables

### Required Variables

```bash
# Supabase Configuration
NEXT_PUBLIC_SUPABASE_URL=https://owlnunxiwpyxilsdqldn.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJ...

# App Configuration
NEXT_PUBLIC_APP_URL=https://mayastudio-two.vercel.app

# Google OAuth Client ID (configured in Supabase)
NEXT_PUBLIC_GOOGLE_CLIENT_ID=868230822105-231st56v3ik4kg2r4209rj15bl38q52.apps.googleusercontent.com
```

### Vercel Configuration

All `NEXT_PUBLIC_*` variables must be set as **Config** type (not Secret) in Vercel, as they need to be available at build time and in the client.

## Supabase Configuration

### 1. Authentication Settings

**URL Configuration:**
- Site URL: `https://mayastudio-two.vercel.app`
- Redirect URLs:
  - `https://mayastudio-two.vercel.app/**` (wildcard for all routes)

### 2. Google OAuth Provider

**Enabled Scopes:**
- `openid` - Basic authentication
- `email` - User email
- `profile` - User profile info
- `https://www.googleapis.com/auth/drive.file` - Google Drive access (files created by app only)

**OAuth Client Configuration:**
- Client ID: Set in Supabase Auth Providers → Google
- Client Secret: Set in Supabase Auth Providers → Google
- Authorized redirect URIs in Google Cloud:
  - `https://owlnunxiwpyxilsdqldn.supabase.co/auth/v1/callback`

### 3. Test Users

For testing (OAuth app in testing mode):
- arathnayaka@gmail.com
- anuradha.rathnayaka@gmail.com

## Session Management

### Cookie Storage

Sessions are stored in secure httpOnly cookies managed by Supabase:
- Cookie name prefix: `sb-`
- Secure: Yes (HTTPS only)
- HttpOnly: Yes (not accessible via JavaScript)
- SameSite: Lax
- Path: `/`

### Session Refresh

The middleware automatically refreshes sessions:
- Runs on every request
- Checks session validity
- Refreshes access token if needed
- Updates cookies with new tokens

### Session Expiry

- Access tokens expire after 1 hour
- Refresh tokens are used to get new access tokens
- Middleware handles refresh automatically
- Users stay logged in as long as refresh token is valid

## Security Considerations

### PKCE Flow

The OAuth flow uses PKCE (Proof Key for Code Exchange):
- More secure than implicit flow
- No tokens in URL fragments
- Authorization code exchanged server-side
- Reduces risk of token interception

### Cookie Security

- HttpOnly cookies prevent XSS attacks
- Secure flag requires HTTPS
- SameSite=Lax prevents CSRF attacks
- Cookies only sent to same origin

### Route Protection

Middleware protects all routes except:
- `/login` - Login page
- `/auth/*` - Auth callback routes
- `/_next/*` - Next.js internal routes
- Static files (images, CSS, etc.)

Unauthenticated users are redirected to `/login`

## Troubleshooting

### Common Issues

1. **Login Loop (redirects back to login)**
   - Check middleware is running
   - Verify cookies are being set
   - Check Supabase Site URL matches production URL
   - Ensure all clients are using `@supabase/ssr` package

2. **"Multiple GoTrueClient instances" warning**
   - Don't create Supabase clients directly
   - Always use the client factory functions
   - Don't create singleton clients in global scope

3. **Session not persisting**
   - Verify middleware is properly configured
   - Check cookie settings in browser
   - Ensure HTTPS in production
   - Check Supabase redirect URLs

4. **OAuth redirect to localhost**
   - Remove localhost from Supabase redirect URLs
   - Use `NEXT_PUBLIC_APP_URL` environment variable
   - Check Google OAuth redirect URIs

### Debugging

Enable debug logging by checking browser console for:
- Supabase auth state changes
- Cookie values (non-httpOnly only)
- Network requests to Supabase auth endpoints
- Middleware execution logs

## References

- [Supabase SSR Documentation](https://supabase.com/docs/guides/auth/server-side/nextjs)
- [Next.js Middleware](https://nextjs.org/docs/app/building-your-application/routing/middleware)
- [Google OAuth 2.0](https://developers.google.com/identity/protocols/oauth2)
- [@supabase/ssr Package](https://www.npmjs.com/package/@supabase/ssr)

## Migration Notes

### From @supabase/supabase-js to @supabase/ssr

If migrating from direct `@supabase/supabase-js` usage:

1. Install `@supabase/ssr`:
   ```bash
   npm install @supabase/ssr
   ```

2. Create the three client factories (client.ts, server.ts, middleware.ts)

3. Add middleware.ts to project root

4. Update all Supabase client usage:
   - Client Components: Use `createClient()` from `lib/supabase/client.ts`
   - Server Components/Routes: Use `createClient()` from `lib/supabase/server.ts`
   - Middleware: Use `updateSession()` from `lib/supabase/middleware.ts`

5. Remove any direct `createClient()` calls from `@supabase/supabase-js`

6. Remove singleton client patterns

7. Test authentication flow end-to-end

## Last Updated

2025-01-07 - Initial documentation after implementing proper SSR authentication

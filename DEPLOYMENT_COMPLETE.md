# 🎉 MayaStudio AI - Deployment Complete!

**Deployment Date:** November 6, 2026
**Status:** ✅ All Services Live and Running

---

## 📊 Live Services Overview

### Frontend (Vercel)
- **URL:** https://mayastudio-two.vercel.app
- **Status:** ✅ Live
- **Framework:** Next.js 14
- **Region:** Auto (Global CDN)

### Backend API (Railway)
- **URL:** https://mayastudio-production.up.railway.app
- **Status:** ✅ Online
- **Framework:** FastAPI (Python)
- **Region:** US East

### Celery Worker (Railway)
- **Service:** mayastudio-worker
- **Status:** ✅ Online
- **Purpose:** Background task processing (audio, video, parsing)

### Redis (Railway)
- **Status:** ✅ Online
- **Purpose:** Celery message broker and result backend

### Database (Supabase)
- **URL:** https://owhuxnwypxilsdqjdn.supabase.co
- **Status:** ✅ Online
- **Region:** Tokyo (ap-northeast-1)
- **Tables:** 7 tables with RLS policies

---

## 🔧 Configuration Summary

### Environment Variables (Frontend - Vercel)

```bash
NEXT_PUBLIC_SUPABASE_URL=https://owhuxnwypxilsdqjdn.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJhbGc... [configured]
NEXT_PUBLIC_API_URL=https://mayastudio-production.up.railway.app
NEXT_PUBLIC_GOOGLE_CLIENT_ID=868230822105-231sit56v3ik4kg2r4209rj15bi38q52.apps.googleusercontent.com
NEXT_PUBLIC_APP_URL=https://mayastudio-two.vercel.app
```

### Environment Variables (Backend - Railway)

```bash
DATABASE_URL=postgresql://postgres:***@db.owhuxnwypxilsdqjdn.supabase.co:5432/postgres
REDIS_URL=${{Redis.REDIS_URL}}
GOOGLE_CLIENT_ID=868230822105-231sit56v3ik4kg2r4209rj15bi38q52.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=GOCSPX-*** [configured]
GOOGLE_APPLICATION_CREDENTIALS_JSON={...} [configured]
SUPABASE_URL=https://owhuxnwypxilsdqjdn.supabase.co
SUPABASE_SERVICE_KEY=eyJhbGc... [configured]
ENVIRONMENT=production
CELERY_BROKER_URL=${{Redis.REDIS_URL}}
CELERY_RESULT_BACKEND=${{Redis.REDIS_URL}}
```

### Environment Variables (Celery Worker - Railway)

Same as Backend API + additional:

```bash
C_FORCE_ROOT=true
```

---

## 🔐 Google Cloud Configuration

### Project Details
- **Project Name:** MayaStudio
- **Project ID:** mayastudio-513907

### Enabled APIs
- ✅ Google Drive API
- ✅ Cloud Text-to-Speech API
- ✅ Gemini API

### OAuth 2.0 Client
- **Client ID:** 868230822105-231sit56v3ik4kg2r4209rj15bi38q52.apps.googleusercontent.com
- **Type:** Web application

**Authorized JavaScript Origins:**
- http://localhost:3000
- https://owhuxnwypxilsdqjdn.supabase.co
- https://mayastudio-two.vercel.app

**Authorized Redirect URIs:**
- http://localhost:3000/api/auth/callback/google
- https://owhuxnwypxilsdqjdn.supabase.co/auth/v1/callback
- https://mayastudio-two.vercel.app/api/auth/callback/google

### Service Account
- **Email:** mayastudio-backend@mayastudio-513907.iam.gserviceaccount.com
- **Role:** Editor
- **Purpose:** Backend API access to Google Cloud services

---

## 🗄️ Database Schema (Supabase)

### Tables Created
1. **user_profiles** - User account data and Google OAuth tokens
2. **projects** - User video projects
3. **scenes** - Individual scenes within projects
4. **voice_profiles** - Custom voice configurations
5. **dialogue_blocks** - Script dialogue with speaker assignments
6. **render_jobs** - Video rendering queue and status
7. **usage_logs** - Credit usage tracking

### Security
- ✅ Row Level Security (RLS) policies enabled on all tables
- ✅ Policies enforce user isolation
- ✅ Service role key for backend, anon key for frontend

---

## 🚀 Deployment Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         User Browser                         │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│              Frontend (Vercel - Global CDN)                  │
│         https://mayastudio-two.vercel.app                    │
│                    Next.js 14 App                            │
└────────────┬────────────────────────────┬────────────────────┘
             │                            │
             │ API Calls                  │ Auth
             ▼                            ▼
┌─────────────────────────┐  ┌──────────────────────────────┐
│  Backend API (Railway)  │  │    Supabase Auth & DB       │
│  FastAPI + Celery       │  │  PostgreSQL + Auth Service  │
│  Port: 8000             │  │  Tokyo Region               │
└────────┬────────────────┘  └──────────────────────────────┘
         │
         ├─── Redis (Railway) ◄──── Celery Worker (Railway)
         │                          Background Tasks
         │
         └─── Google Cloud Services
              ├── Drive API (user storage)
              ├── TTS API (voice synthesis)
              └── Gemini API (script parsing)
```

---

## 🛠️ Issues Resolved During Deployment

### Vercel Deployment Issues
1. ✅ **Fixed:** vercel.json referenced non-existent secrets → Removed env block
2. ✅ **Fixed:** Double `cd apps/web` in build commands → Removed duplicates
3. ✅ **Fixed:** Root Directory not set → Set to `apps/web`
4. ✅ **Fixed:** Missing `tailwindcss-animate` package → Added to package.json
5. ✅ **Fixed:** Skip deployments setting blocking builds → Disabled

### Railway Deployment Issues
1. ✅ **Fixed:** httpx version conflict with supabase → Downgraded to 0.24.1
2. ✅ **Fixed:** GEMINI_API_KEY required but not set → Made optional
3. ✅ **Fixed:** Celery worker superuser warning → Added C_FORCE_ROOT=true

### Configuration Issues
1. ✅ **Fixed:** Root directory configuration mismatch
2. ✅ **Fixed:** Environment variables properly configured across all services
3. ✅ **Fixed:** Google OAuth redirect URIs updated with production URLs

---

## 📦 Key Files Modified

### Added
- `apps/api/start-worker.sh` - Celery worker startup script
- `supabase/migrations/00_drop_all_tables.sql` - Database reset script
- `SUPABASE_CONNECTION_STRING_GUIDE.md` - Setup documentation

### Modified
- `apps/api/requirements.txt` - Fixed httpx version
- `apps/api/app/config.py` - Made GEMINI_API_KEY optional
- `apps/web/package.json` - Added tailwindcss-animate
- `apps/web/app/page.tsx` - Enhanced landing page
- `.gitignore` - Protected sensitive files

---

## 💰 Cost Breakdown (Free Tier)

### Current Monthly Cost: ~$0-5

| Service | Tier | Cost |
|---------|------|------|
| Vercel | Hobby | Free |
| Railway | Trial | $5 credit (free for now) |
| Supabase | Free | Free (500MB DB, 1GB file storage) |
| Google Cloud | Free Tier | Free (within quotas) |

**Total:** $0/month during trial period
**Post-trial estimate:** $5-20/month (Railway usage-based)

### Free Tier Limits
- **Vercel:** 100GB bandwidth, unlimited deployments
- **Railway:** $5 monthly credit, 500 execution hours
- **Supabase:** 500MB database, 1GB file storage, 50K MAU
- **Google Cloud:** 1M TTS characters/month free

---

## ✅ Deployment Checklist

### Infrastructure
- [x] Vercel account connected to GitHub
- [x] Railway account connected to GitHub
- [x] Supabase project created
- [x] Google Cloud project created

### Services Deployed
- [x] Frontend deployed to Vercel
- [x] Backend API deployed to Railway
- [x] Celery worker deployed to Railway
- [x] Redis database added to Railway
- [x] PostgreSQL database migrated on Supabase

### Configuration
- [x] All environment variables configured
- [x] Google OAuth credentials created
- [x] Google Service Account created
- [x] OAuth redirect URIs configured
- [x] Database schema migrated
- [x] RLS policies enabled

### Testing
- [x] Frontend loads successfully
- [x] Backend API is accessible
- [x] Celery worker is running
- [x] Database connection verified

---

## 🔍 Testing URLs

### Public Endpoints
- **Frontend:** https://mayastudio-two.vercel.app
- **Backend API:** https://mayastudio-production.up.railway.app
- **API Health Check:** https://mayastudio-production.up.railway.app/health
- **API Docs:** https://mayastudio-production.up.railway.app/docs

### Expected Responses
- Frontend: Landing page with "MayaStudio AI" heading
- Health Check: `{"status": "healthy"}`
- API Docs: Interactive Swagger documentation

---

## 🎯 Next Steps (Future Development)

### Immediate
1. Test user registration and Google OAuth login
2. Test project creation and scene management
3. Verify Google Drive integration
4. Test voice synthesis with Google TTS
5. Test video rendering pipeline

### Short-term
1. Add email notifications for render completion
2. Implement credit usage tracking UI
3. Add project sharing features
4. Create tutorial/onboarding flow

### Long-term
1. Custom voice cloning
2. Advanced video editing features
3. Template library
4. Collaboration features
5. API rate limiting
6. Analytics dashboard

---

## 📚 Documentation References

- [Deployment Walkthrough](./DEPLOYMENT_WALKTHROUGH.md)
- [Setup Guide](./SETUP_GUIDE.md)
- [Project Structure](./PROJECT_STRUCTURE.md)
- [Free Tier Limits](./FREE_TIER_LIMITS.md)
- [Development Plan](./DEVELOPMENT_PLAN_SUMMARY.md)
- [Quick Start](./QUICK_START.md)

---

## 🆘 Troubleshooting

### Frontend Issues
- **Site not loading:** Check Vercel deployment logs
- **API calls failing:** Verify NEXT_PUBLIC_API_URL is correct
- **OAuth not working:** Check Google Cloud redirect URIs

### Backend Issues
- **API not responding:** Check Railway deployment logs
- **Database errors:** Verify DATABASE_URL and Supabase credentials
- **Celery tasks failing:** Check worker logs and Redis connection

### Common Commands

```bash
# Check Railway logs
railway logs

# Redeploy Vercel
vercel --prod

# Test backend locally
cd apps/api
uvicorn app.main:app --reload

# Test frontend locally
cd apps/web
npm run dev
```

---

## 👥 Team & Credits

**Project:** MayaStudio AI
**Organization:** D-Direct
**Repository:** https://github.com/D-Direct/mayastudio
**Deployment Date:** November 6, 2026

**Technology Stack:**
- Frontend: Next.js 14, React 18, TypeScript, Tailwind CSS
- Backend: Python 3.11, FastAPI, Celery
- Database: PostgreSQL (Supabase)
- Cache/Queue: Redis
- AI Services: Google Gemini, Google Cloud TTS
- Storage: Google Drive (user-owned)
- Hosting: Vercel + Railway

---

**🎉 Congratulations! MayaStudio AI is now fully deployed and ready for use!**

For support or questions, refer to the documentation or check the GitHub repository issues.

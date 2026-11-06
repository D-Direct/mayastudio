# MayaStudio AI - Deployment Checklist

Use this checklist to ensure proper setup of all services.

## ✅ Pre-Deployment Setup

### 1. Accounts Created
- [ ] GitHub account
- [ ] Vercel account (sign up with GitHub)
- [ ] Railway account (sign up with GitHub)
- [ ] Supabase account
- [ ] Google Cloud Platform account

### 2. Repository Setup
- [ ] GitHub repository created
- [ ] Local repository cloned
- [ ] `.gitignore` file in place
- [ ] Initial commit pushed

## ✅ Supabase Configuration

### Database Setup
- [ ] Supabase project created (free tier)
- [ ] Project name: `mayastudio-dev`
- [ ] Database password saved securely
- [ ] Region selected (closest to you)

### Credentials Collected
- [ ] Project URL copied
- [ ] `anon/public` key copied
- [ ] `service_role` key copied (for backend only)

### Database Schema
- [ ] SQL Editor opened
- [ ] Migration file `20240101_initial_schema.sql` executed
- [ ] Tables created successfully:
  - [ ] `user_profiles`
  - [ ] `projects`
  - [ ] `scenes`
  - [ ] `voice_profiles`
  - [ ] `dialogue_blocks`
- [ ] Row Level Security (RLS) policies active
- [ ] Indexes created

### Storage Setup
- [ ] Storage bucket created (if not using Google Drive exclusively)
- [ ] Storage policies configured
- [ ] Public access configured for thumbnails (optional)

### Authentication
- [ ] Email provider enabled (or)
- [ ] Google OAuth provider configured
- [ ] Redirect URLs added

## ✅ Google Cloud Platform Setup

### Project Setup
- [ ] GCP project created: "MayaStudio Dev"
- [ ] Billing enabled (won't be charged on free tier)
- [ ] Project ID noted

### APIs Enabled
- [ ] Google Drive API enabled
- [ ] Generative Language API (Gemini) enabled
- [ ] Cloud Text-to-Speech API enabled

### OAuth 2.0 Client
- [ ] OAuth consent screen configured
  - [ ] App name: "MayaStudio AI"
  - [ ] Support email added
  - [ ] Scopes added: `https://www.googleapis.com/auth/drive.file`
- [ ] OAuth Client ID created (Web application)
- [ ] Authorized JavaScript origins added:
  - [ ] `http://localhost:3000`
  - [ ] `https://YOUR-APP.vercel.app`
- [ ] Authorized redirect URIs added:
  - [ ] `http://localhost:3000/api/auth/callback/google`
  - [ ] `https://YOUR-APP.vercel.app/api/auth/callback/google`
- [ ] Client ID copied
- [ ] Client Secret copied

### API Keys
- [ ] API key created for Gemini
- [ ] API key restricted to required APIs
- [ ] API key copied and saved

### Service Account
- [ ] Service account created: `mayastudio-backend`
- [ ] Service account role assigned
- [ ] JSON key downloaded
- [ ] JSON key content copied (for Railway env var)

### Budget Alerts (Recommended)
- [ ] Budget alert set ($10/month threshold)
- [ ] Email notifications configured

## ✅ Railway Configuration

### Project Setup
- [ ] Railway project created: "MayaStudio Backend"
- [ ] GitHub repository connected

### Redis Service
- [ ] Redis database added
- [ ] Connection URL copied from "Connect" tab
- [ ] Redis URL format: `redis://default:PASSWORD@host:port`

### FastAPI Service
- [ ] New service created from GitHub repo
- [ ] Root directory set: `apps/api`
- [ ] Dockerfile detected
- [ ] Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- [ ] Environment variables added (see below)
- [ ] Service deployed successfully
- [ ] Public domain generated
- [ ] Service URL copied

### Celery Worker Service
- [ ] New service created (same GitHub repo)
- [ ] Root directory set: `apps/api`
- [ ] Start command: `celery -A app.worker worker --loglevel=info`
- [ ] Same environment variables as API service
- [ ] Worker started successfully

### Environment Variables (Railway)
```env
# Database
DATABASE_URL=postgresql://postgres:PASSWORD@db.xxx.supabase.co:5432/postgres

# Redis
REDIS_URL=redis://default:PASSWORD@red-xxx.railway.app:6379

# Google OAuth
GOOGLE_CLIENT_ID=xxx.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=GOCSPX-xxx

# Google AI
GEMINI_API_KEY=AIzaSyXxx

# Google Service Account (paste entire JSON as one line)
GOOGLE_APPLICATION_CREDENTIALS_JSON={"type":"service_account",...}

# Supabase
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_SERVICE_KEY=eyJxxx...

# App Config
FRONTEND_URL=https://mayastudio.vercel.app
ENVIRONMENT=development

# Celery
CELERY_BROKER_URL=redis://default:PASSWORD@red-xxx.railway.app:6379
CELERY_RESULT_BACKEND=redis://default:PASSWORD@red-xxx.railway.app:6379
```

- [ ] All environment variables added
- [ ] Variables saved
- [ ] Services redeployed

### Monitoring
- [ ] Usage dashboard checked
- [ ] $5 monthly credit visible
- [ ] Usage alerts configured (optional)

## ✅ Vercel Configuration

### Project Setup
- [ ] Vercel project created
- [ ] GitHub repository imported
- [ ] Framework detected: Next.js
- [ ] Root directory set: `apps/web`
- [ ] Build settings auto-detected

### Environment Variables (Vercel)
```env
NEXT_PUBLIC_SUPABASE_URL=https://xxx.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJxxx...
NEXT_PUBLIC_API_URL=https://mayastudio-api.up.railway.app
NEXT_PUBLIC_GOOGLE_CLIENT_ID=xxx.apps.googleusercontent.com
NEXT_PUBLIC_APP_URL=https://mayastudio.vercel.app
```

- [ ] All environment variables added
- [ ] Variables saved for all environments (Production, Preview, Development)

### Deployment
- [ ] Initial deployment triggered
- [ ] Build successful
- [ ] Deployment URL generated
- [ ] Production domain assigned
- [ ] Custom domain configured (optional)

### Post-Deployment
- [ ] Site accessible at production URL
- [ ] No console errors
- [ ] API connection working
- [ ] Authentication flow tested

### Google OAuth Update
- [ ] Vercel production URL copied
- [ ] Added to Google Cloud Console:
  - [ ] Authorized JavaScript origins
  - [ ] Authorized redirect URIs

## ✅ Local Development Setup

### Frontend Setup
```bash
cd apps/web
npm install
```
- [ ] Dependencies installed
- [ ] `.env.local` created with environment variables
- [ ] Development server starts: `npm run dev`
- [ ] Site loads at http://localhost:3000

### Backend Setup
```bash
cd apps/api
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```
- [ ] Virtual environment created
- [ ] Dependencies installed
- [ ] `.env` file created with environment variables
- [ ] `credentials.json` saved in `apps/api/`
- [ ] Server starts: `uvicorn app.main:app --reload`
- [ ] API accessible at http://localhost:8000
- [ ] Swagger docs load at http://localhost:8000/docs

### Worker Setup (Optional for local dev)
```bash
cd apps/api
celery -A app.worker worker --loglevel=info
```
- [ ] Celery worker starts
- [ ] Connects to Redis
- [ ] No errors in logs

## ✅ Integration Testing

### Authentication
- [ ] User can sign up
- [ ] User can log in
- [ ] Google OAuth flow works
- [ ] User session persists
- [ ] User can log out

### Google Drive Integration
- [ ] "Connect Google Drive" button works
- [ ] OAuth consent screen appears
- [ ] Permissions requested correctly
- [ ] Drive connection successful
- [ ] MayaStudio folder created in user's Drive

### API Communication
- [ ] Frontend can call backend API
- [ ] CORS configured correctly
- [ ] Authentication headers sent
- [ ] API responses received

### Database
- [ ] User profile created on signup
- [ ] Projects can be created
- [ ] Data persists correctly
- [ ] RLS policies working (users see only their data)

## ✅ Monitoring & Alerts

### Vercel
- [ ] Analytics enabled
- [ ] Build notifications configured
- [ ] Error tracking setup (Sentry - optional)

### Railway
- [ ] Deployment notifications enabled
- [ ] Service health checked
- [ ] Logs accessible

### Supabase
- [ ] Database usage monitored
- [ ] Storage usage monitored
- [ ] API requests tracked

### Google Cloud
- [ ] Budget alerts active
- [ ] API quota alerts configured
- [ ] Billing reports reviewed

## ✅ Security Checklist

### Secrets Management
- [ ] No secrets committed to Git
- [ ] `.env` files in `.gitignore`
- [ ] Service account JSON not in repo
- [ ] API keys rotated if exposed

### API Security
- [ ] CORS properly configured
- [ ] Rate limiting implemented (optional for MVP)
- [ ] Input validation on all endpoints
- [ ] SQL injection protection (using ORM)

### Authentication
- [ ] JWT tokens expire properly
- [ ] Refresh token rotation working
- [ ] Password hashing enabled (if using email auth)
- [ ] OAuth scopes minimal (drive.file only)

### Database
- [ ] RLS policies enforced
- [ ] Service role key only in backend
- [ ] Database backups enabled

## ✅ Performance Optimization

### Frontend
- [ ] Images optimized (Next.js Image component)
- [ ] Code splitting enabled
- [ ] Static pages cached
- [ ] Bundle size checked (<1MB initial)

### Backend
- [ ] Database queries optimized
- [ ] Indexes on foreign keys
- [ ] Connection pooling configured
- [ ] Response caching for static data

### Media
- [ ] Audio files compressed
- [ ] Video files optimized (H.264)
- [ ] CDN configured for static assets

## ✅ Documentation

- [ ] README.md complete
- [ ] SETUP_GUIDE.md reviewed
- [ ] API documentation generated (Swagger)
- [ ] Environment variables documented
- [ ] Deployment process documented

## ✅ Final Checks

- [ ] All services running (green status)
- [ ] No errors in logs
- [ ] Test user can complete full workflow:
  1. [ ] Sign up
  2. [ ] Connect Google Drive
  3. [ ] Create project
  4. [ ] Upload/parse script
  5. [ ] Generate audio (test with small sample)
  6. [ ] Export video (test with minimal scene)
- [ ] Costs within budget:
  - [ ] Railway usage < $5/month
  - [ ] Google Cloud < $10/month
  - [ ] Vercel within free tier
  - [ ] Supabase within free tier

## 🚀 Production Readiness (Optional)

Only complete if going to production:

- [ ] Custom domain configured
- [ ] SSL certificate verified
- [ ] Privacy policy page added
- [ ] Terms of service page added
- [ ] Error tracking (Sentry) integrated
- [ ] Analytics (Posthog/Mixpanel) added
- [ ] Uptime monitoring (UptimeRobot)
- [ ] Backup strategy implemented
- [ ] Disaster recovery plan documented

---

## Notes & Issues

Document any issues encountered during setup:

```
Date: ___________
Issue: ___________
Resolution: ___________
```

---

**Setup completed by:** ________________
**Date:** ________________
**Time taken:** ________________

# MayaStudio AI - Quick Start Guide

Get MayaStudio running in under 30 minutes!

## 🎯 What You'll Build

A free-tier deployment of MayaStudio AI with:
- ✅ Frontend on Vercel
- ✅ Backend on Railway
- ✅ Database on Supabase
- ✅ Google Drive storage integration

**Total cost: $5-10/month** (mostly Google API usage)

---

## ⚡ Quick Setup (30 minutes)

### Step 1: Clone & Setup Accounts (10 min)

```bash
# 1. Create accounts (sign up with GitHub for speed)
# - Vercel: https://vercel.com
# - Railway: https://railway.app
# - Supabase: https://supabase.com
# - Google Cloud: https://console.cloud.google.com

# 2. Clone repository
git clone https://github.com/YOUR_USERNAME/mayastudio-ai.git
cd mayastudio-ai
```

### Step 2: Supabase Setup (5 min)

```bash
# 1. Create Supabase project
#    - Go to https://supabase.com/dashboard
#    - Click "New project"
#    - Name: mayastudio-dev
#    - Generate strong password
#    - Select closest region
#    - Wait 2 minutes for creation

# 2. Run database migration
#    - Go to SQL Editor
#    - Copy content from supabase/migrations/20240101_initial_schema.sql
#    - Run the SQL
#    - Verify tables created (Projects, Scenes, etc.)

# 3. Copy credentials
#    - Settings → API
#    - Copy Project URL
#    - Copy anon/public key
#    - Copy service_role key
```

### Step 3: Google Cloud Setup (10 min)

```bash
# 1. Create GCP project
#    - Go to https://console.cloud.google.com
#    - Create new project: "MayaStudio Dev"
#    - Enable billing (required but won't be charged on free tier)

# 2. Enable APIs (APIs & Services → Library)
#    - Google Drive API
#    - Generative Language API (Gemini)
#    - Cloud Text-to-Speech API

# 3. Create OAuth credentials
#    - APIs & Services → Credentials
#    - Configure OAuth consent screen
#    - Create OAuth Client ID (Web application)
#    - Add authorized origins:
#      * http://localhost:3000
#      * https://YOUR-APP.vercel.app (add after Vercel deploy)
#    - Add redirect URIs:
#      * http://localhost:3000/api/auth/callback/google
#      * https://YOUR-APP.vercel.app/api/auth/callback/google
#    - Copy Client ID and Secret

# 4. Create API key
#    - Create Credentials → API key
#    - Copy API key (for Gemini)

# 5. Create service account
#    - IAM & Admin → Service Accounts
#    - Create service account
#    - Download JSON key file
```

### Step 4: Railway Setup (3 min)

```bash
# 1. Create Railway project
#    - Go to https://railway.app
#    - New Project → Deploy from GitHub repo
#    - Connect your repository

# 2. Add Redis
#    - New → Database → Redis
#    - Note connection URL

# 3. Add API service
#    - New → GitHub Repo
#    - Root directory: apps/api
#    - It will auto-detect Dockerfile

# 4. Add environment variables (copy from template below)

# 5. Add Celery worker service
#    - New → GitHub Repo (same repo)
#    - Root directory: apps/api
#    - Override start command:
#      celery -A app.worker worker --loglevel=info
```

### Step 5: Vercel Setup (2 min)

```bash
# 1. Deploy to Vercel
#    - Go to https://vercel.com
#    - New Project → Import from GitHub
#    - Root directory: apps/web
#    - Add environment variables (template below)
#    - Deploy!

# 2. Copy deployment URL
#    - Copy your Vercel URL (e.g., https://mayastudio.vercel.app)

# 3. Update Google OAuth
#    - Go back to Google Cloud Console
#    - Add Vercel URL to authorized origins and redirect URIs
```

---

## 📋 Environment Variables Templates

### Vercel (Frontend)

```env
NEXT_PUBLIC_SUPABASE_URL=https://xxxxx.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJhbGc...
NEXT_PUBLIC_API_URL=https://mayastudio-production.up.railway.app
NEXT_PUBLIC_GOOGLE_CLIENT_ID=xxxxx.apps.googleusercontent.com
NEXT_PUBLIC_APP_URL=https://mayastudio.vercel.app
```

### Railway (Backend API + Worker)

```env
# Database
DATABASE_URL=postgresql://postgres:PASSWORD@db.xxxxx.supabase.co:5432/postgres

# Redis (from Railway Redis service)
REDIS_URL=redis://default:PASSWORD@redis.railway.internal:6379

# Google OAuth
GOOGLE_CLIENT_ID=xxxxx.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=GOCSPX-xxxxx

# Google AI
GEMINI_API_KEY=AIzaSyxxxxx

# Google Service Account (paste entire JSON content)
GOOGLE_APPLICATION_CREDENTIALS_JSON={"type":"service_account","project_id":"..."}

# Supabase
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_SERVICE_KEY=eyJhbGc...

# App Config
FRONTEND_URL=https://mayastudio.vercel.app
ENVIRONMENT=production

# Celery
CELERY_BROKER_URL=redis://default:PASSWORD@redis.railway.internal:6379
CELERY_RESULT_BACKEND=redis://default:PASSWORD@redis.railway.internal:6379
```

---

## 🧪 Local Development

### Prerequisites

```bash
# Install dependencies
node -v  # Should be 18+
python --version  # Should be 3.11+
```

### Run Locally

```bash
# Terminal 1: Frontend
cd apps/web
npm install
cp .env.example .env.local
# Edit .env.local with your credentials
npm run dev
# → http://localhost:3000

# Terminal 2: Backend
cd apps/api
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your credentials
# Save credentials.json from Google Cloud
uvicorn app.main:app --reload
# → http://localhost:8000

# Terminal 3: Worker (optional)
cd apps/api
source venv/bin/activate
celery -A app.worker worker --loglevel=info
```

---

## ✅ Verification Checklist

After setup, verify everything works:

### Frontend
- [ ] Site loads at Vercel URL
- [ ] No console errors (F12 → Console)
- [ ] Can navigate to login page

### Backend
- [ ] API accessible at Railway URL
- [ ] Swagger docs load: `https://your-api.railway.app/docs`
- [ ] Health check works: `https://your-api.railway.app/health`

### Database
- [ ] Can connect to Supabase
- [ ] Tables exist (check Supabase Table Editor)
- [ ] RLS policies active

### Integration
- [ ] User can sign up
- [ ] Google OAuth flow works
- [ ] Can create a project
- [ ] Data persists in database

---

## 🚀 Next Steps

Now that everything is running:

### 1. Build Core Features

```bash
# Follow the development roadmap:
# 1. Implement script parsing (Gemini API)
# 2. Add voice profile management
# 3. Build dialogue editor UI
# 4. Integrate TTS audio generation
# 5. Add video assembly pipeline
```

### 2. Read the Docs

- [Project Structure](./PROJECT_STRUCTURE.md) - Code organization
- [Setup Guide](./SETUP_GUIDE.md) - Detailed instructions
- [Free Tier Limits](./FREE_TIER_LIMITS.md) - Cost optimization
- [Deployment Checklist](./DEPLOYMENT_CHECKLIST.md) - Complete checklist

### 3. Monitor Usage

```bash
# Check weekly:
- Vercel: https://vercel.com/dashboard/usage
- Railway: https://railway.app/project/usage
- Supabase: https://supabase.com/dashboard/project/_/reports
- Google Cloud: https://console.cloud.google.com/billing
```

---

## 🆘 Common Issues

### Issue: Vercel build fails

```bash
# Solution:
# 1. Check build logs in Vercel dashboard
# 2. Verify package.json has correct dependencies
# 3. Ensure environment variables are set
# 4. Try deploying from local:
npm install -g vercel
cd apps/web
vercel
```

### Issue: Railway service won't start

```bash
# Solution:
# 1. Check Railway logs
# 2. Verify Dockerfile exists in apps/api
# 3. Check environment variables are set
# 4. Test locally first:
docker build -t mayastudio-api apps/api
docker run -p 8000:8000 mayastudio-api
```

### Issue: Database connection fails

```bash
# Solution:
# 1. Verify DATABASE_URL format:
#    postgresql://postgres:PASSWORD@HOST:5432/postgres
# 2. Check Supabase project is not paused
# 3. Test connection from Railway:
#    Railway → Service → Shell
#    psql $DATABASE_URL
```

### Issue: Google OAuth not working

```bash
# Solution:
# 1. Verify redirect URIs in Google Console exactly match
# 2. Check client ID in frontend env vars
# 3. Ensure APIs are enabled in Google Cloud
# 4. Clear browser cache and try again
```

---

## 💡 Pro Tips

### Tip 1: Use Railway CLI for faster development

```bash
# Install Railway CLI
npm i -g @railway/cli

# Link your project
railway link

# Run commands in Railway environment
railway run python manage.py migrate

# View logs
railway logs

# Open shell
railway shell
```

### Tip 2: Use Supabase CLI

```bash
# Install Supabase CLI
npm i -g supabase

# Link project
supabase link --project-ref YOUR_PROJECT_REF

# Pull remote schema
supabase db pull

# Create migration
supabase migration new add_new_field

# Push changes
supabase db push
```

### Tip 3: Monitor costs proactively

```bash
# Set up budget alerts in Google Cloud
# Set up usage alerts in Railway
# Check dashboards every Monday morning
```

---

## 📞 Get Help

- 📖 [Full Setup Guide](./SETUP_GUIDE.md)
- 🐛 [GitHub Issues](https://github.com/YOUR_USERNAME/mayastudio-ai/issues)
- 💬 [Discussions](https://github.com/YOUR_USERNAME/mayastudio-ai/discussions)

---

**Ready to build? Let's go! 🚀**

```bash
git clone https://github.com/YOUR_USERNAME/mayastudio-ai.git
cd mayastudio-ai
# Follow steps above
```

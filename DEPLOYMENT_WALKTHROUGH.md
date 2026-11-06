# MayaStudio AI - Deployment Walkthrough

**Status:** Accounts Created ✅
**Next:** Configure Services & Deploy

---

## 🎯 Overview

We'll configure services in this order:
1. **Supabase** - Run database migration (10 min)
2. **Google Cloud** - Enable APIs & create credentials (15 min)
3. **Railway** - Deploy backend (5 min)
4. **Vercel** - Deploy frontend (5 min)

**Total time:** ~35 minutes

---

## 1️⃣ Supabase Configuration (10 min)

### Step 1.1: Create New Project

1. Go to https://supabase.com/dashboard
2. Click **"New project"**
3. Fill in details:
   - **Name:** `mayastudio-dev`
   - **Database Password:** Generate a strong password (save it!)
   - **Region:** Choose closest to you (e.g., `Singapore (Southeast Asia)`)
   - **Pricing Plan:** Free
4. Click **"Create new project"**
5. Wait ~2 minutes for project creation

### Step 1.2: Get Your Credentials

1. Once created, go to **Settings** → **API**
2. Copy and save these values:

```
Project URL:          https://xxxxx.supabase.co
anon/public key:      eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
service_role key:     eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9... (different from anon)
```

3. Go to **Settings** → **Database** → **Connection String**
4. Copy the **URI** format:

```
postgresql://postgres:[YOUR-PASSWORD]@db.xxxxx.supabase.co:5432/postgres
```

Replace `[YOUR-PASSWORD]` with the database password you created.

### Step 1.3: Run Database Migration

1. In Supabase Dashboard, go to **SQL Editor**
2. Click **"New query"**
3. Open your local file: `supabase/migrations/20241106_initial_schema.sql`
4. Copy the ENTIRE contents and paste into SQL Editor
5. Click **"Run"** (or press Ctrl+Enter)
6. You should see: **"Success. No rows returned"**

### Step 1.4: Verify Tables Created

1. Go to **Table Editor** (left sidebar)
2. You should see these tables:
   - ✅ `user_profiles`
   - ✅ `projects`
   - ✅ `scenes`
   - ✅ `voice_profiles`
   - ✅ `dialogue_blocks`
   - ✅ `render_jobs`
   - ✅ `usage_logs`

### Step 1.5: Configure Authentication (Optional for now)

1. Go to **Authentication** → **Providers**
2. Enable **Google** provider:
   - Toggle ON
   - Leave Client ID and Secret empty for now (we'll add after Google Cloud setup)

**✅ Supabase Done!** Save your credentials for later.

---

## 2️⃣ Google Cloud Platform Configuration (15 min)

### Step 2.1: Create Project

1. Go to https://console.cloud.google.com
2. Click project dropdown (top left)
3. Click **"New Project"**
4. **Project name:** `MayaStudio Dev`
5. Click **"Create"**
6. Wait ~30 seconds, then select your new project

### Step 2.2: Enable Billing

1. Go to **Billing** (left menu or search)
2. Click **"Link a billing account"**
3. Follow prompts to add credit card
   - ⚠️ You won't be charged with free tier usage
   - Set up billing alerts recommended

### Step 2.3: Enable Required APIs

1. Go to **APIs & Services** → **Library**
2. Search and enable each of these:

#### API 1: Google Drive API
- Search: "Google Drive API"
- Click it → Click **"Enable"**

#### API 2: Generative Language API (Gemini)
- Search: "Generative Language API"
- Click it → Click **"Enable"**

#### API 3: Cloud Text-to-Speech API
- Search: "Cloud Text-to-Speech API"
- Click it → Click **"Enable"**

### Step 2.4: Configure OAuth Consent Screen

1. Go to **APIs & Services** → **OAuth consent screen**
2. **User Type:** External → Click **"Create"**
3. Fill in required fields:
   - **App name:** MayaStudio AI
   - **User support email:** your email
   - **Developer contact:** your email
4. Click **"Save and Continue"**
5. **Scopes:** Click **"Add or Remove Scopes"**
   - Search for: `https://www.googleapis.com/auth/drive.file`
   - Check the box
   - Click **"Update"** → **"Save and Continue"**
6. **Test users:** Add your Gmail address → **"Save and Continue"**
7. Click **"Back to Dashboard"**

### Step 2.5: Create OAuth 2.0 Client ID

1. Go to **APIs & Services** → **Credentials**
2. Click **"Create Credentials"** → **"OAuth client ID"**
3. **Application type:** Web application
4. **Name:** MayaStudio Web Client
5. **Authorized JavaScript origins:**
   - Click **"Add URI"**
   - Add: `http://localhost:3000`
   - Click **"Add URI"** again
   - Add: `https://mayastudio.vercel.app` (or your Vercel URL - we'll update this later)
6. **Authorized redirect URIs:**
   - Click **"Add URI"**
   - Add: `http://localhost:3000/api/auth/callback/google`
   - Click **"Add URI"** again
   - Add: `https://mayastudio.vercel.app/api/auth/callback/google`
7. Click **"Create"**

8. **Save these credentials:**

```
Client ID:        xxxxx.apps.googleusercontent.com
Client Secret:    GOCSPX-xxxxx
```

### Step 2.6: Create API Key (for Gemini)

1. Still in **Credentials**, click **"Create Credentials"** → **"API key"**
2. Copy the API key: `AIzaSyXxx...`
3. Click **"Restrict Key"** (recommended)
4. **Name:** MayaStudio Backend Key
5. **API restrictions:**
   - Select **"Restrict key"**
   - Check:
     - ✅ Cloud Text-to-Speech API
     - ✅ Generative Language API
6. Click **"Save"**

**Save your API key:** `AIzaSyXxx...`

### Step 2.7: Create Service Account

1. Go to **IAM & Admin** → **Service Accounts**
2. Click **"Create Service Account"**
3. **Service account name:** `mayastudio-backend`
4. **Service account ID:** (auto-filled)
5. Click **"Create and Continue"**
6. **Role:** Select **"Project" → "Editor"**
7. Click **"Continue"** → **"Done"**

8. Find your new service account in the list
9. Click the **email address** of the service account
10. Go to **Keys** tab
11. Click **"Add Key"** → **"Create new key"**
12. **Key type:** JSON
13. Click **"Create"**
14. JSON file downloads automatically - **Save this file!**

### Step 2.8: Set Up Budget Alerts (Recommended)

1. Go to **Billing** → **Budgets & alerts**
2. Click **"Create Budget"**
3. **Name:** MayaStudio Monthly Budget
4. **Budget amount:** $20
5. **Threshold rules:** 50%, 90%, 100%
6. Add your email for alerts
7. Click **"Finish"**

**✅ Google Cloud Done!** You now have:
- ✅ Client ID & Secret
- ✅ API Key
- ✅ Service Account JSON file

---

## 3️⃣ Railway Deployment (5 min)

### Step 3.1: Create New Project

1. Go to https://railway.app/dashboard
2. Click **"New Project"**
3. Select **"Deploy from GitHub repo"**
4. Select your repository: `D-Direct/mayastudio`
5. Click **"Deploy Now"**

Railway will create a project, but we need to configure services properly.

### Step 3.2: Add Redis Service

1. In your project, click **"New"** → **"Database"** → **"Add Redis"**
2. Redis will be created automatically
3. Click on Redis service → **"Connect"** tab
4. Copy the **Redis URL**: `redis://default:xxxxx@redis.railway.internal:6379`

### Step 3.3: Configure FastAPI Service

1. Click **"New"** → **"GitHub Repo"**
2. Select `D-Direct/mayastudio`
3. Click on the new service
4. Go to **Settings**:
   - **Service Name:** `mayastudio-api`
   - **Root Directory:** `apps/api`
   - **Start Command:** Leave empty (uses Dockerfile)
5. Click **"Variables"** tab
6. Click **"Raw Editor"**
7. Paste the following (replace with YOUR actual values):

```bash
# Database (from Supabase)
DATABASE_URL=postgresql://postgres:YOUR_SUPABASE_PASSWORD@db.xxxxx.supabase.co:5432/postgres

# Redis (from Railway Redis service)
REDIS_URL=redis://default:xxxxx@redis.railway.internal:6379

# Google OAuth (from Google Cloud)
GOOGLE_CLIENT_ID=xxxxx.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=GOCSPX-xxxxx

# Google AI (from Google Cloud)
GEMINI_API_KEY=AIzaSyXxx

# Google Service Account (paste JSON content as single line)
GOOGLE_APPLICATION_CREDENTIALS_JSON={"type":"service_account","project_id":"mayastudio-dev","private_key_id":"...","private_key":"-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n","client_email":"mayastudio-backend@...","client_id":"...","auth_uri":"https://accounts.google.com/o/oauth2/auth","token_uri":"https://oauth2.googleapis.com/token","auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs","client_x509_cert_url":"..."}

# Supabase (from Supabase)
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_SERVICE_KEY=eyJhbGc... (the service_role key, not anon)

# App Config
FRONTEND_URL=https://mayastudio.vercel.app
ENVIRONMENT=production

# Celery
CELERY_BROKER_URL=redis://default:xxxxx@redis.railway.internal:6379
CELERY_RESULT_BACKEND=redis://default:xxxxx@redis.railway.internal:6379
```

8. Click **"Save Variables"**
9. Service will automatically redeploy

### Step 3.4: Add Celery Worker Service

1. Click **"New"** → **"GitHub Repo"**
2. Select `D-Direct/mayastudio` again
3. Click on the new service
4. Go to **Settings**:
   - **Service Name:** `mayastudio-worker`
   - **Root Directory:** `apps/api`
   - **Start Command:** `celery -A app.worker worker --loglevel=info`
5. Click **"Variables"** tab
6. Paste the SAME environment variables as the API service
7. Save and redeploy

### Step 3.5: Get API URL

1. Click on `mayastudio-api` service
2. Go to **Settings** → **Networking**
3. Click **"Generate Domain"**
4. Copy the URL: `https://mayastudio-api-production.up.railway.app`

**✅ Railway Done!** Your backend is deployed!

---

## 4️⃣ Vercel Deployment (5 min)

### Step 4.1: Import Project

1. Go to https://vercel.com/dashboard
2. Click **"Add New..."** → **"Project"**
3. Click **"Import"** next to `D-Direct/mayastudio`
4. Configure:
   - **Framework Preset:** Next.js (auto-detected)
   - **Root Directory:** `apps/web`
   - **Build Command:** (leave default)
   - **Output Directory:** (leave default)

### Step 4.2: Add Environment Variables

1. Expand **"Environment Variables"**
2. Add each variable for **Production**, **Preview**, and **Development**:

```bash
NEXT_PUBLIC_SUPABASE_URL=https://xxxxx.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJhbGc... (anon key from Supabase)
NEXT_PUBLIC_API_URL=https://mayastudio-api-production.up.railway.app
NEXT_PUBLIC_GOOGLE_CLIENT_ID=xxxxx.apps.googleusercontent.com
NEXT_PUBLIC_APP_URL=https://mayastudio.vercel.app
```

3. Click **"Deploy"**
4. Wait ~2 minutes for build

### Step 4.3: Get Vercel URL

1. After deployment, copy your URL: `https://mayastudio.vercel.app` (or similar)
2. You can add a custom domain later in **Settings** → **Domains**

### Step 4.4: Update Google Cloud OAuth URLs

1. Go back to Google Cloud Console
2. **APIs & Services** → **Credentials**
3. Click your OAuth Client ID
4. Update **Authorized JavaScript origins:**
   - Replace or add your Vercel URL: `https://mayastudio.vercel.app`
5. Update **Authorized redirect URIs:**
   - Replace or add: `https://mayastudio.vercel.app/api/auth/callback/google`
6. Click **"Save"**

### Step 4.5: Update Supabase Google Auth (Optional)

1. Go to Supabase Dashboard
2. **Authentication** → **Providers** → **Google**
3. Add your Google Client ID and Secret
4. **Redirect URL:** `https://xxxxx.supabase.co/auth/v1/callback`
5. Click **"Save"**

**✅ Vercel Done!** Your frontend is deployed!

---

## 5️⃣ Verification & Testing (5 min)

### Test Backend API

1. Open: `https://mayastudio-api-production.up.railway.app/health`
2. You should see:
   ```json
   {
     "status": "healthy",
     "app": "MayaStudio AI",
     "version": "1.0.0",
     "environment": "production"
   }
   ```

### Test API Documentation

1. Open: `https://mayastudio-api-production.up.railway.app/docs`
2. You should see Swagger API documentation
3. Try the `/health` endpoint

### Test Frontend

1. Open: `https://mayastudio.vercel.app`
2. You should see the landing page
3. Check browser console for errors (F12 → Console)

### Test Database Connection

1. Railway → `mayastudio-api` → **Deployments** → **View Logs**
2. Look for startup logs - should see "Starting MayaStudio AI..."
3. No database connection errors

---

## ✅ Deployment Complete!

### Your Live URLs

```
Frontend:  https://mayastudio.vercel.app
Backend:   https://mayastudio-api-production.up.railway.app
API Docs:  https://mayastudio-api-production.up.railway.app/docs
Database:  Supabase (7 tables created)
```

### Credentials Summary

Save these somewhere safe (password manager recommended):

```
=== SUPABASE ===
Project URL: https://xxxxx.supabase.co
Anon Key: eyJhbGc...
Service Role Key: eyJhbGc...
Database URL: postgresql://postgres:...

=== GOOGLE CLOUD ===
Client ID: xxxxx.apps.googleusercontent.com
Client Secret: GOCSPX-xxxxx
API Key: AIzaSyXxx
Service Account JSON: (file saved locally)

=== RAILWAY ===
API URL: https://mayastudio-api-production.up.railway.app
Redis URL: redis://default:xxxxx@...

=== VERCEL ===
Frontend URL: https://mayastudio.vercel.app
```

---

## 🎯 Next Steps

Now that everything is deployed, you can start implementing features!

### Week 2-3: Backend Implementation

1. **Implement Google OAuth** in `apps/api/app/api/routes/auth.py`
2. **Implement Google Drive service** in `apps/api/app/services/drive.py`
3. **Implement Gemini parsing** in `apps/api/app/services/gemini.py`
4. **Implement TTS** in `apps/api/app/services/tts.py`

### Week 3-4: Frontend Implementation

1. **Create login page** in `apps/web/app/login/page.tsx`
2. **Create dashboard** in `apps/web/app/dashboard/page.tsx`
3. **Build project management UI**
4. **Build dialogue editor**

---

## 📊 Monitoring

### Check Service Health

**Railway:**
- Dashboard → Usage (monitor $5 credit)
- Each service → Deployments → View Logs

**Vercel:**
- Dashboard → Analytics
- Monitor bandwidth (100GB/month limit)

**Supabase:**
- Dashboard → Reports
- Monitor database size (500MB limit)

**Google Cloud:**
- Billing → Budgets & alerts
- Monitor API usage

---

## 🆘 Troubleshooting

### Backend won't start (Railway)
- Check **Logs** for errors
- Verify all environment variables are set
- Check DATABASE_URL format is correct

### Frontend build fails (Vercel)
- Check build logs
- Verify `apps/web/package.json` exists
- Check environment variables

### Database connection fails
- Verify DATABASE_URL in Railway
- Check Supabase project is not paused
- Test connection from Railway logs

### API returns 404
- Verify Railway domain is generated
- Check NEXT_PUBLIC_API_URL in Vercel
- Test backend health endpoint directly

---

**Deployment walkthrough complete! 🎉**

**Ready to start coding?** Follow [DEVELOPMENT_PLAN_SUMMARY.md](./DEVELOPMENT_PLAN_SUMMARY.md)

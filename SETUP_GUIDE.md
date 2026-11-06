# MayaStudio AI - Setup Guide (Free Tier Development)

## Prerequisites

- Node.js 18+ installed
- Python 3.11+ installed
- Git installed
- GitHub account
- Google Cloud account (free tier)

## Step-by-Step Setup

### 1. Create GitHub Repository

```bash
# Create new repo on GitHub.com
# Then clone locally
git clone https://github.com/YOUR_USERNAME/mayastudio-ai.git
cd mayastudio-ai
```

### 2. Set Up Supabase (Free Tier)

1. Go to [supabase.com](https://supabase.com)
2. Click "Start your project"
3. Create organization (free)
4. Create new project:
   - Name: `mayastudio-dev`
   - Database Password: (generate strong password)
   - Region: Choose closest to you
   - Pricing Plan: **Free**

5. Wait for project to be created (~2 minutes)

6. Get your credentials:
   - Go to Project Settings → API
   - Copy:
     - `Project URL` (NEXT_PUBLIC_SUPABASE_URL)
     - `anon/public key` (NEXT_PUBLIC_SUPABASE_ANON_KEY)
     - `service_role key` (SUPABASE_SERVICE_KEY - backend only)

7. Create database schema:
   - Go to SQL Editor
   - Run the migration files from `supabase/migrations/`

### 3. Set Up Google Cloud (Free Tier)

#### A. Create Google Cloud Project

1. Go to [console.cloud.google.com](https://console.cloud.google.com)
2. Create new project: "MayaStudio Dev"
3. Enable billing (won't be charged on free tier)

#### B. Enable APIs

```bash
# Enable required APIs:
1. Google Drive API
2. Google AI API (Gemini)
3. Cloud Text-to-Speech API
```

In console:
- Go to "APIs & Services" → "Library"
- Search and enable each API above

#### C. Create OAuth 2.0 Credentials

1. Go to "APIs & Services" → "Credentials"
2. Click "Create Credentials" → "OAuth client ID"
3. Configure consent screen:
   - User Type: External
   - App name: MayaStudio AI
   - Support email: your email
   - Scopes: Add `https://www.googleapis.com/auth/drive.file`
4. Create OAuth Client ID:
   - Application type: Web application
   - Authorized JavaScript origins:
     - `http://localhost:3000`
     - `https://YOUR-APP.vercel.app` (add later)
   - Authorized redirect URIs:
     - `http://localhost:3000/api/auth/callback/google`
     - `https://YOUR-APP.vercel.app/api/auth/callback/google`
5. Copy Client ID and Client Secret

#### D. Create API Key (for Gemini)

1. Go to "APIs & Services" → "Credentials"
2. Click "Create Credentials" → "API key"
3. Copy API key
4. Restrict key (recommended):
   - API restrictions → Select APIs:
     - Cloud Text-to-Speech API
     - Generative Language API

#### E. Create Service Account (for backend)

1. Go to "IAM & Admin" → "Service Accounts"
2. Create service account:
   - Name: `mayastudio-backend`
   - Role: "Service Account User"
3. Create key:
   - Key type: JSON
   - Download JSON file (save as `credentials.json`)

### 4. Set Up Railway (Free Tier)

1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub
3. Create new project: "MayaStudio Backend"
4. Add services:

#### Service 1: PostgreSQL (Optional - using Supabase instead)
- Skip this, we're using Supabase

#### Service 2: Redis
1. Click "New Service" → "Database" → "Redis"
2. Note: Railway Redis is included in free tier
3. Copy connection URL from "Connect" tab

#### Service 3: FastAPI Backend
1. Click "New Service" → "GitHub Repo"
2. Connect your GitHub repo
3. Configure:
   - Root Directory: `apps/api`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
4. Add environment variables (see below)

#### Service 4: Celery Worker
1. Click "New Service" → "GitHub Repo" (same repo)
2. Configure:
   - Root Directory: `apps/api`
   - Start Command: `celery -A app.worker worker --loglevel=info`
3. Add same environment variables as API

### 5. Set Up Vercel (Free Tier)

1. Go to [vercel.com](https://vercel.com)
2. Sign up with GitHub
3. Click "Add New..." → "Project"
4. Import your GitHub repo
5. Configure:
   - Framework Preset: Next.js
   - Root Directory: `apps/web`
   - Build Command: (auto-detected)
   - Output Directory: (auto-detected)
6. Add environment variables (see below)
7. Deploy

### 6. Configure Environment Variables

#### Vercel (Frontend)

```env
NEXT_PUBLIC_SUPABASE_URL=https://xxx.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJxxx...
NEXT_PUBLIC_API_URL=https://mayastudio-api.up.railway.app
NEXT_PUBLIC_GOOGLE_CLIENT_ID=xxx.apps.googleusercontent.com
NEXT_PUBLIC_APP_URL=https://mayastudio.vercel.app
```

#### Railway API Service

```env
DATABASE_URL=postgresql://postgres:[PASSWORD]@db.xxx.supabase.co:5432/postgres
REDIS_URL=redis://default:[PASSWORD]@red-xxx.railway.app:6379
GOOGLE_CLIENT_ID=xxx.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=GOCSPX-xxx
GEMINI_API_KEY=AIzaSyXxx
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_SERVICE_KEY=eyJxxx...
FRONTEND_URL=https://mayastudio.vercel.app
ENVIRONMENT=development
CELERY_BROKER_URL=redis://default:[PASSWORD]@red-xxx.railway.app:6379
CELERY_RESULT_BACKEND=redis://default:[PASSWORD]@red-xxx.railway.app:6379
```

Add `credentials.json` content:
1. In Railway, go to service → Variables
2. Click "RAW Editor"
3. Add:
```env
GOOGLE_APPLICATION_CREDENTIALS_JSON={"type": "service_account", ...}
```

#### Railway Worker Service
- Use same environment variables as API service

### 7. Initialize Project Locally

```bash
cd mayastudio-ai

# Create project structure
mkdir -p apps/web apps/api supabase/migrations docs

# Frontend setup
cd apps/web
npm create next-app@latest . --typescript --tailwind --app --src-dir --import-alias "@/*"
npm install @supabase/supabase-js @tanstack/react-query zustand axios
npm install -D @types/node

# Backend setup
cd ../api
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install fastapi uvicorn[standard] sqlalchemy psycopg2-binary redis celery
pip install google-cloud-texttospeech google-generativeai google-api-python-client
pip install python-multipart aiofiles pydantic-settings
pip freeze > requirements.txt

# Create Dockerfile
cat > Dockerfile << 'EOF'
FROM python:3.11-slim

WORKDIR /app

# Install FFmpeg
RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
EOF
```

### 8. Create Database Schema

Create `supabase/migrations/20240101_initial_schema.sql`:

```sql
-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Users table (extends Supabase auth.users)
CREATE TABLE public.user_profiles (
  id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
  email TEXT UNIQUE NOT NULL,
  full_name TEXT,
  google_access_token TEXT,
  google_refresh_token TEXT,
  google_token_expires_at TIMESTAMPTZ,
  drive_root_folder_id TEXT,
  storage_preference TEXT DEFAULT 'google_drive',
  credits_balance INTEGER DEFAULT 100,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Projects table
CREATE TABLE public.projects (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES public.user_profiles(id) ON DELETE CASCADE,
  title TEXT NOT NULL,
  description TEXT,
  aspect_ratio TEXT DEFAULT '9:16' CHECK (aspect_ratio IN ('9:16', '16:9')),
  drive_folder_id TEXT,
  status TEXT DEFAULT 'draft' CHECK (status IN ('draft', 'in_progress', 'completed')),
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Scenes table
CREATE TABLE public.scenes (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  project_id UUID REFERENCES public.projects(id) ON DELETE CASCADE,
  scene_number INTEGER NOT NULL,
  heading TEXT NOT NULL,
  description TEXT,
  drive_folder_id TEXT,
  background_video_drive_id TEXT,
  background_video_url TEXT,
  export_drive_id TEXT,
  export_drive_link TEXT,
  order_index INTEGER NOT NULL,
  status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'processing', 'completed', 'failed')),
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(project_id, scene_number)
);

-- Voice profiles table
CREATE TABLE public.voice_profiles (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES public.user_profiles(id) ON DELETE CASCADE,
  character_name TEXT NOT NULL,
  voice_id TEXT NOT NULL,
  voice_type TEXT CHECK (voice_type IN ('designed', 'cloned')),
  voice_description TEXT,
  sample_audio_url TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Dialogue blocks table
CREATE TABLE public.dialogue_blocks (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  scene_id UUID REFERENCES public.scenes(id) ON DELETE CASCADE,
  actor_name TEXT NOT NULL,
  voice_id TEXT NOT NULL,
  emotion_tone TEXT NOT NULL,
  sinhala_text TEXT NOT NULL,
  english_translation TEXT,
  audio_drive_id TEXT,
  audio_url TEXT,
  audio_cache_url TEXT,
  cache_expires_at TIMESTAMPTZ,
  duration_seconds NUMERIC(5,2),
  status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'generated', 'modified', 'failed')),
  order_index INTEGER NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes for performance
CREATE INDEX idx_projects_user_id ON public.projects(user_id);
CREATE INDEX idx_scenes_project_id ON public.scenes(project_id);
CREATE INDEX idx_dialogue_blocks_scene_id ON public.dialogue_blocks(scene_id);
CREATE INDEX idx_voice_profiles_user_id ON public.voice_profiles(user_id);

-- Row Level Security (RLS)
ALTER TABLE public.user_profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.projects ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.scenes ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.dialogue_blocks ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.voice_profiles ENABLE ROW LEVEL SECURITY;

-- RLS Policies
-- Users can only see their own profile
CREATE POLICY "Users can view own profile" ON public.user_profiles
  FOR SELECT USING (auth.uid() = id);
CREATE POLICY "Users can update own profile" ON public.user_profiles
  FOR UPDATE USING (auth.uid() = id);

-- Users can only see their own projects
CREATE POLICY "Users can view own projects" ON public.projects
  FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can insert own projects" ON public.projects
  FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "Users can update own projects" ON public.projects
  FOR UPDATE USING (auth.uid() = user_id);
CREATE POLICY "Users can delete own projects" ON public.projects
  FOR DELETE USING (auth.uid() = user_id);

-- Similar policies for scenes (through projects)
CREATE POLICY "Users can view own scenes" ON public.scenes
  FOR SELECT USING (
    EXISTS (
      SELECT 1 FROM public.projects
      WHERE projects.id = scenes.project_id
      AND projects.user_id = auth.uid()
    )
  );

CREATE POLICY "Users can modify own scenes" ON public.scenes
  FOR ALL USING (
    EXISTS (
      SELECT 1 FROM public.projects
      WHERE projects.id = scenes.project_id
      AND projects.user_id = auth.uid()
    )
  );

-- Similar policies for dialogue blocks
CREATE POLICY "Users can view own dialogue blocks" ON public.dialogue_blocks
  FOR SELECT USING (
    EXISTS (
      SELECT 1 FROM public.scenes
      JOIN public.projects ON projects.id = scenes.project_id
      WHERE scenes.id = dialogue_blocks.scene_id
      AND projects.user_id = auth.uid()
    )
  );

CREATE POLICY "Users can modify own dialogue blocks" ON public.dialogue_blocks
  FOR ALL USING (
    EXISTS (
      SELECT 1 FROM public.scenes
      JOIN public.projects ON projects.id = scenes.project_id
      WHERE scenes.id = dialogue_blocks.scene_id
      AND projects.user_id = auth.uid()
    )
  );

-- Voice profiles policies
CREATE POLICY "Users can view own voice profiles" ON public.voice_profiles
  FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can manage own voice profiles" ON public.voice_profiles
  FOR ALL USING (auth.uid() = user_id);
```

Run in Supabase SQL Editor.

### 9. Test Local Development

```bash
# Terminal 1: Backend
cd apps/api
source venv/bin/activate
uvicorn app.main:app --reload

# Terminal 2: Frontend
cd apps/web
npm run dev

# Terminal 3: Celery Worker (optional for testing)
cd apps/api
celery -A app.worker worker --loglevel=info
```

Visit: http://localhost:3000

### 10. Deploy

```bash
# Commit and push
git add .
git commit -m "Initial MayaStudio setup"
git push origin main

# Vercel and Railway will auto-deploy!
```

## Monitoring Free Tier Usage

### Vercel
- Dashboard → Your Project → Analytics
- Watch bandwidth usage (100GB/month limit)

### Railway
- Dashboard → Project → Usage
- Watch $5 credit consumption
- Set up usage alerts

### Supabase
- Dashboard → Reports
- Watch database size (500MB limit)
- Watch storage (1GB limit)

## Troubleshooting

### Railway service won't start
- Check logs in Railway dashboard
- Verify environment variables are set
- Ensure Dockerfile is correct

### Vercel build fails
- Check build logs
- Verify `package.json` dependencies
- Check Next.js version compatibility

### Database connection fails
- Verify DATABASE_URL format
- Check Supabase project is not paused
- Verify connection pooling settings

### Google OAuth not working
- Verify redirect URIs in Google Console
- Check client ID/secret are correct
- Ensure APIs are enabled

## Next Steps

1. ✅ All services deployed
2. Test user registration flow
3. Test Google Drive OAuth
4. Implement first feature: Script parsing
5. Set up monitoring and error tracking (Sentry free tier)

## Support Resources

- Vercel Docs: https://vercel.com/docs
- Railway Docs: https://docs.railway.app
- Supabase Docs: https://supabase.com/docs
- Next.js Docs: https://nextjs.org/docs
- FastAPI Docs: https://fastapi.tiangolo.com

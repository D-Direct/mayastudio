# MayaStudio AI - Project Structure (Vercel + Railway)

## Repository Structure

```
mayastudio-ai/
├── .github/
│   └── workflows/
│       ├── deploy-vercel.yml          # Auto-deploy frontend
│       └── deploy-railway.yml         # Auto-deploy backend
├── apps/
│   ├── web/                           # Next.js Frontend (Vercel)
│   │   ├── app/
│   │   │   ├── (auth)/
│   │   │   │   ├── login/
│   │   │   │   └── signup/
│   │   │   ├── (dashboard)/
│   │   │   │   ├── projects/
│   │   │   │   ├── scenes/
│   │   │   │   └── settings/
│   │   │   ├── api/                   # Vercel API Routes (light)
│   │   │   │   ├── auth/
│   │   │   │   └── webhooks/
│   │   │   ├── layout.tsx
│   │   │   └── page.tsx
│   │   ├── components/
│   │   │   ├── ui/                    # Shadcn components
│   │   │   ├── audio/
│   │   │   │   ├── WaveformPlayer.tsx
│   │   │   │   └── AudioControls.tsx
│   │   │   ├── editor/
│   │   │   │   ├── DialogueBlock.tsx
│   │   │   │   ├── SceneDrawer.tsx
│   │   │   │   └── PreviewPanel.tsx
│   │   │   └── projects/
│   │   │       ├── ProjectCard.tsx
│   │   │       └── SceneCard.tsx
│   │   ├── lib/
│   │   │   ├── api-client.ts          # Axios/Fetch wrapper
│   │   │   ├── supabase.ts            # Supabase client
│   │   │   ├── google-drive.ts        # Drive API client
│   │   │   └── store/                 # Zustand stores
│   │   │       ├── project-store.ts
│   │   │       ├── audio-store.ts
│   │   │       └── ui-store.ts
│   │   ├── hooks/
│   │   │   ├── useProjects.ts
│   │   │   ├── useScenes.ts
│   │   │   ├── useDialogueBlocks.ts
│   │   │   └── useGoogleDrive.ts
│   │   ├── public/
│   │   ├── .env.local.example
│   │   ├── next.config.js
│   │   ├── package.json
│   │   ├── tailwind.config.ts
│   │   └── tsconfig.json
│   │
│   └── api/                           # Python FastAPI Backend (Railway)
│       ├── app/
│       │   ├── main.py                # FastAPI app entry
│       │   ├── config.py              # Settings & env vars
│       │   ├── database.py            # SQLAlchemy setup
│       │   ├── worker.py              # Celery app
│       │   ├── api/
│       │   │   ├── routes/
│       │   │   │   ├── auth.py
│       │   │   │   ├── projects.py
│       │   │   │   ├── scenes.py
│       │   │   │   ├── dialogue.py
│       │   │   │   ├── voices.py
│       │   │   │   ├── parsing.py     # Script parsing
│       │   │   │   └── render.py      # Video rendering
│       │   │   └── deps.py            # Dependencies
│       │   ├── services/
│       │   │   ├── gemini.py          # Google Gemini API
│       │   │   ├── tts.py             # Google Cloud TTS
│       │   │   ├── drive.py           # Google Drive operations
│       │   │   ├── ffmpeg.py          # Video processing
│       │   │   └── audio.py           # Audio manipulation
│       │   ├── tasks/
│       │   │   ├── audio_generation.py   # Celery tasks
│       │   │   ├── video_rendering.py
│       │   │   └── script_parsing.py
│       │   ├── models/
│       │   │   ├── user.py
│       │   │   ├── project.py
│       │   │   ├── scene.py
│       │   │   ├── dialogue_block.py
│       │   │   └── voice_profile.py
│       │   ├── schemas/
│       │   │   ├── project.py         # Pydantic models
│       │   │   ├── scene.py
│       │   │   └── dialogue.py
│       │   └── utils/
│       │       ├── auth.py
│       │       ├── storage.py
│       │       └── validators.py
│       ├── tests/
│       ├── requirements.txt
│       ├── Dockerfile
│       ├── railway.json               # Railway config
│       └── .env.example
│
├── packages/                          # Shared packages (optional)
│   ├── types/                         # Shared TypeScript types
│   ├── ui/                            # Shared UI components
│   └── config/                        # Shared configs
│
├── supabase/
│   ├── migrations/
│   │   ├── 20240101_initial_schema.sql
│   │   ├── 20240102_google_drive_fields.sql
│   │   └── 20240103_voice_profiles.sql
│   ├── seed.sql
│   └── config.toml
│
├── docs/
│   ├── setup.md
│   ├── deployment.md
│   ├── api-reference.md
│   └── architecture.md
│
├── .gitignore
├── README.md
├── package.json                       # Root package.json (for monorepo)
└── turbo.json                         # Turborepo config (optional)
```

## Environment Variables

### Frontend (Vercel) - `.env.local`
```env
# Supabase
NEXT_PUBLIC_SUPABASE_URL=https://xxx.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJxxx...

# Backend API
NEXT_PUBLIC_API_URL=https://mayastudio-api.up.railway.app

# Google OAuth
NEXT_PUBLIC_GOOGLE_CLIENT_ID=xxx.apps.googleusercontent.com

# App Config
NEXT_PUBLIC_APP_URL=https://mayastudio.vercel.app
```

### Backend (Railway) - `.env`
```env
# Database
DATABASE_URL=postgresql://postgres:xxx@db.xxx.supabase.co:5432/postgres

# Redis
REDIS_URL=redis://default:xxx@red-xxx.railway.app:6379

# Google Cloud
GOOGLE_APPLICATION_CREDENTIALS=/app/credentials.json
GOOGLE_CLIENT_ID=xxx.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=GOCSPX-xxx
GEMINI_API_KEY=AIzaSyXxx

# Supabase (for storage)
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_SERVICE_KEY=eyJxxx...

# App Config
FRONTEND_URL=https://mayastudio.vercel.app
ENVIRONMENT=development

# Celery
CELERY_BROKER_URL=redis://default:xxx@red-xxx.railway.app:6379
CELERY_RESULT_BACKEND=redis://default:xxx@red-xxx.railway.app:6379
```

## Service Responsibilities

| Service | Handles |
|---------|---------|
| **Vercel (Frontend)** | UI, auth pages, static content, light API routes |
| **Railway (API)** | Heavy API logic, Gemini/TTS integration, job queuing |
| **Railway (Worker)** | Celery tasks, FFmpeg processing, long-running jobs |
| **Railway (Redis)** | Task queue, caching, rate limiting |
| **Supabase (DB)** | PostgreSQL database, metadata storage |
| **Supabase (Auth)** | User authentication (optional, can use Google OAuth) |
| **Google Drive** | User's media file storage |

## Deployment Flow

```
Developer pushes to GitHub
         ↓
    ┌────┴────┐
    ▼         ▼
 Vercel    Railway
(Frontend) (Backend)
    │         │
    └────┬────┘
         ▼
    Production
```

## Cost Monitoring

### Free Tier Limits to Watch:

**Vercel:**
- ✓ Bandwidth: 100GB/month
- ✓ Build time: 6000 minutes/month
- ✓ Serverless function executions: 100GB-hrs

**Railway:**
- ✓ Monthly credit: $5 (~500 hours)
- ✓ Usage dashboard: railway.app/project/usage

**Supabase:**
- ✓ Database size: 500MB
- ✓ File storage: 1GB
- ✓ Bandwidth: 2GB
- ✓ Pauses after 7 days inactivity (dev projects)

## Upgrade Path

When you outgrow free tiers:

1. **Railway**: $5/month → Pay-as-you-go (~$10-20/mo for light usage)
2. **Supabase**: Free → Pro ($25/mo) for 8GB DB + 100GB storage
3. **Vercel**: Free → Pro ($20/mo) for better performance
4. **Google Cloud**: Pay-per-use (set budget alerts)

**Total**: ~$55-65/month for production-ready setup

# MayaStudio AI - Technology Stack

**Last Updated:** 2025-01-07
**Status:** Production-Ready Infrastructure

---

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE                          │
│              Browser (Desktop & Mobile Responsive)              │
└────────────────────────────┬────────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────────┐
│                    FRONTEND APPLICATION                         │
│         Next.js 14 (React) + TypeScript + Tailwind CSS          │
│                  Deployed on Vercel (Edge Network)              │
│              https://mayastudio-two.vercel.app                  │
└──────────────┬──────────────────────────┬──────────────────────┘
               │                          │
               │ REST API                 │ Real-time Updates
               │ (JSON)                   │ (Future: WebSockets)
               │                          │
┌──────────────▼──────────────────────────▼──────────────────────┐
│                     BACKEND API LAYER                           │
│              FastAPI (Python) + Celery Worker                   │
│              Deployed on Railway (Docker Containers)            │
│         https://mayastudio-production.up.railway.app            │
└───┬──────────┬──────────────┬──────────────┬──────────────┬────┘
    │          │              │              │              │
    │ Gemini   │ TTS          │ Drive        │ FFmpeg       │ Queue
    │ API      │ API          │ API          │ Processing   │ Tasks
    │          │              │              │              │
┌───▼──────────▼──────────────▼──────────────▼──────────────▼────┐
│                   EXTERNAL SERVICES LAYER                       │
├─────────────────┬───────────────────┬───────────────────────────┤
│ Google AI       │ Google Cloud      │ Infrastructure            │
│ - Gemini API    │ - Cloud TTS       │ - Supabase (Database)     │
│   (Parsing)     │   (Audio Gen)     │ - Railway Redis (Queue)   │
│                 │ - Drive API       │ - Vercel (CDN)            │
│                 │   (Storage)       │                           │
└─────────────────┴───────────────────┴───────────────────────────┘
```

---

## 🎨 Frontend Stack

### **Core Framework**
| Technology | Version | Purpose | Status |
|------------|---------|---------|--------|
| **Next.js** | 14.0.3 | React framework with App Router | ✅ Deployed |
| **React** | 18.2.0 | UI component library | ✅ Active |
| **TypeScript** | 5.3.2 | Type safety & IDE support | ✅ Active |

### **Styling & UI Components**
| Technology | Version | Purpose | Status |
|------------|---------|---------|--------|
| **Tailwind CSS** | 3.3.5 | Utility-first CSS framework | ✅ Active |
| **Tailwind Animate** | 1.0.7 | Animation utilities | ✅ Active |
| **Lucide React** | 0.292.0 | Icon library | ✅ Active |
| **clsx** | 2.0.0 | Conditional className utility | ✅ Active |
| **tailwind-merge** | 2.1.0 | Merge Tailwind classes | ✅ Active |
| **class-variance-authority** | 0.7.0 | Component variants | ✅ Active |

**Planned:**
- Shadcn UI components (Week 3-4)

### **State Management**
| Technology | Version | Purpose | Status |
|------------|---------|---------|--------|
| **Zustand** | 4.4.6 | Global state management | ✅ Installed, not used yet |
| **React Query** | 5.8.4 | Server state & caching | ✅ Installed, not used yet |

### **Authentication & Data**
| Technology | Version | Purpose | Status |
|------------|---------|---------|--------|
| **@supabase/ssr** | 0.12.7 | Server-side rendering auth | ✅ Active |
| **@supabase/supabase-js** | 2.38.4 | Supabase client SDK | ✅ Active |
| **axios** | 1.6.2 | HTTP client for API calls | ✅ Installed |

### **Media Processing (Frontend)**
| Technology | Version | Purpose | Status |
|------------|---------|---------|--------|
| **wavesurfer.js** | 7.4.4 | Audio waveform visualization | ✅ Installed, not integrated |

### **Build Tools**
| Technology | Version | Purpose |
|------------|---------|---------|
| **PostCSS** | 8.4.31 | CSS processing |
| **Autoprefixer** | 10.4.16 | CSS vendor prefixes |
| **ESLint** | 8.54.0 | Code linting |

---

## ⚙️ Backend Stack

### **Core Framework**
| Technology | Version | Purpose | Status |
|------------|---------|---------|--------|
| **FastAPI** | 0.104.1 | Modern Python API framework | ✅ Deployed |
| **Uvicorn** | 0.24.0 | ASGI server | ✅ Active |
| **Python** | 3.11+ | Programming language | ✅ Active |

### **Database & ORM**
| Technology | Version | Purpose | Status |
|------------|---------|---------|--------|
| **SQLAlchemy** | 2.0.23 | SQL ORM | ✅ Installed |
| **Alembic** | 1.12.1 | Database migrations | ✅ Installed |
| **asyncpg** | 0.29.0 | Async PostgreSQL driver | ✅ Installed |
| **psycopg2-binary** | 2.9.9 | PostgreSQL adapter | ✅ Installed |

### **Task Queue & Caching**
| Technology | Version | Purpose | Status |
|------------|---------|---------|--------|
| **Celery** | 5.3.4 | Distributed task queue | ✅ Deployed |
| **Redis** | 5.0.1 | Message broker & cache | ✅ Deployed on Railway |

### **Google Cloud APIs**
| Technology | Version | Purpose | Status |
|------------|---------|---------|--------|
| **google-generativeai** | 0.3.1 | Gemini AI API | ✅ Installed, not integrated |
| **google-cloud-texttospeech** | 2.15.0 | Text-to-Speech API | ✅ Installed, not integrated |
| **google-cloud-storage** | 2.13.0 | Cloud Storage | ✅ Installed, not integrated |
| **google-api-python-client** | 2.108.0 | Google Drive API | ✅ Installed, not integrated |
| **google-auth-oauthlib** | 1.1.0 | OAuth 2.0 authentication | ✅ Active |
| **google-auth-httplib2** | 0.1.1 | HTTP auth library | ✅ Active |

### **Media Processing (Backend)**
| Technology | Version | Purpose | Status |
|------------|---------|---------|--------|
| **ffmpeg-python** | 0.2.0 | Python wrapper for FFmpeg | ✅ Installed, not integrated |
| **FFmpeg** | Latest | Video/audio processing | ⚠️ Needs installation on Railway |

### **Utilities & Config**
| Technology | Version | Purpose | Status |
|------------|---------|---------|--------|
| **Pydantic** | 2.5.0 | Data validation | ✅ Active |
| **pydantic-settings** | 2.1.0 | Settings management | ✅ Active |
| **python-dotenv** | 1.0.0 | Environment variables | ✅ Active |
| **httpx** | 0.24.1 | Async HTTP client | ✅ Installed |
| **requests** | 2.31.0 | HTTP library | ✅ Installed |
| **aiofiles** | 23.2.1 | Async file operations | ✅ Installed |

### **Security**
| Technology | Version | Purpose | Status |
|------------|---------|---------|--------|
| **python-jose** | 3.3.0 | JWT tokens | ✅ Installed |
| **passlib** | 1.7.4 | Password hashing | ✅ Installed |

### **Testing & Quality**
| Technology | Version | Purpose | Status |
|------------|---------|---------|--------|
| **pytest** | 7.4.3 | Testing framework | ✅ Installed, no tests yet |
| **pytest-asyncio** | 0.21.1 | Async test support | ✅ Installed |
| **black** | 23.11.0 | Code formatter | ✅ Installed |
| **flake8** | 6.1.0 | Style checker | ✅ Installed |

---

## 🗄️ Database & Storage

### **Primary Database**
| Service | Technology | Purpose | Status |
|---------|------------|---------|--------|
| **Supabase** | PostgreSQL 15+ | Relational database | ✅ Active |
| - | pgvector extension | Vector embeddings (future) | ⚠️ Not enabled |
| - | Row Level Security | Authorization | ✅ Configured |

**Database Schema:**
```
✅ user_profiles        -- User data + OAuth tokens
✅ projects             -- Project metadata
✅ scenes               -- Scene details with ordering
✅ voice_profiles       -- Character voice mappings
✅ dialogue_blocks      -- Dialogue with audio & status
✅ render_jobs          -- Video rendering job queue
✅ usage_logs           -- API usage tracking
```

### **File Storage**
| Service | Purpose | Status |
|---------|---------|--------|
| **Supabase Storage** | Audio files (MP3) | ✅ Available, not used |
| **Google Drive API** | User file storage | ✅ OAuth granted, not integrated |
| **Vercel Blob** | Temporary uploads (optional) | ⚠️ Not configured |

---

## ☁️ Cloud Infrastructure & Deployment

### **Hosting Platforms**

#### **Frontend Hosting**
```
Platform:    Vercel
Tier:        Free (Hobby Plan)
Region:      Global Edge Network
URL:         https://mayastudio-two.vercel.app
Features:    - Auto-deploy from GitHub
             - Edge functions
             - CDN caching
             - Analytics
Status:      ✅ Production Ready
```

#### **Backend Hosting**
```
Platform:    Railway
Tier:        Free ($5 credits/month)
Region:      US West (configurable)
Services:    1. API Service (FastAPI)
             2. Worker Service (Celery)
             3. Redis Database
URL:         https://mayastudio-production.up.railway.app
Deployment:  Docker containers
Status:      ✅ Production Ready
```

#### **Database Hosting**
```
Platform:    Supabase
Tier:        Free
Region:      ap-northeast-1 (Tokyo)
Project ID:  owlnunxiwpyxilsdqldn
Database:    PostgreSQL 15
Features:    - 500 MB database
             - 1 GB file storage
             - Unlimited API requests
             - Row Level Security
Status:      ✅ Production Ready
```

### **Deployment Configuration**

#### **Vercel (Frontend)**
```json
{
  "buildCommand": "npm run build",
  "outputDirectory": ".next",
  "installCommand": "npm install",
  "framework": "nextjs",
  "regions": ["all"]
}
```

#### **Railway (Backend)**
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## 🔌 External APIs & Services

### **AI & Machine Learning**
| Service | API | Purpose | Status |
|---------|-----|---------|--------|
| **Google AI Studio** | Gemini 1.5 Pro | Script parsing, context analysis | ✅ API key configured |
| **Google Cloud TTS** | Text-to-Speech | Audio synthesis (Sinhala support) | ✅ Credentials configured |

**Gemini API Capabilities:**
- Multi-turn conversations
- JSON output mode
- Function calling
- Vision (future: image analysis)

**TTS Voice Options:**
- Standard voices (free)
- WaveNet voices (premium)
- Neural2 voices (premium)
- Custom voice models (enterprise)

### **Google Cloud Services**
| Service | Purpose | Status |
|---------|---------|--------|
| **Google Drive API** | User file storage | ✅ OAuth scope granted |
| **Cloud Storage** | Backend file storage | ⚠️ Not configured |
| **Cloud Functions** | Serverless tasks (optional) | ❌ Not planned |

### **Authentication**
| Service | Method | Status |
|---------|--------|--------|
| **Google OAuth 2.0** | Sign in with Google | ✅ Active |
| - | Drive file scope | ✅ Granted |
| - | Email scope | ✅ Granted |
| - | Profile scope | ✅ Granted |

### **Future Integrations (Planned)**
| Service | Purpose | Timeline |
|---------|---------|----------|
| **Stripe** | Payment processing | Week 7-8 |
| **SendGrid** | Transactional emails | Week 6 |
| **Sentry** | Error tracking | Week 5 |
| **Google Analytics** | Usage analytics | Week 6 |

---

## 🛠️ Development Tools

### **Version Control**
```
Git:         2.x
Repository:  https://github.com/D-Direct/mayastudio
Branch:      master (main)
CI/CD:       Vercel (frontend) + Railway (backend)
             Auto-deploy on git push
```

### **Package Managers**
```
Frontend:    npm (Node.js)
Backend:     pip (Python)
Monorepo:    npm workspaces
```

### **Local Development**
```bash
# Frontend
cd apps/web
npm install
npm run dev          # http://localhost:3000

# Backend
cd apps/api
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload  # http://localhost:8000

# Celery Worker
celery -A app.worker worker --loglevel=info

# Redis (local)
redis-server
```

### **Environment Variables**

#### Frontend (.env.local)
```bash
NEXT_PUBLIC_SUPABASE_URL=https://owlnunxiwpyxilsdqldn.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJ...
NEXT_PUBLIC_APP_URL=https://mayastudio-two.vercel.app
NEXT_PUBLIC_API_URL=https://mayastudio-production.up.railway.app
```

#### Backend (.env)
```bash
SUPABASE_URL=https://owlnunxiwpyxilsdqldn.supabase.co
SUPABASE_SERVICE_KEY=eyJ...
DATABASE_URL=postgresql://...
REDIS_URL=redis://...
GEMINI_API_KEY=...
GOOGLE_APPLICATION_CREDENTIALS=./service-account.json
```

---

## 📦 File Structure

```
mayastudio/
├── apps/
│   ├── web/                    # Next.js Frontend
│   │   ├── app/               # Next.js App Router pages
│   │   ├── components/        # React components
│   │   ├── lib/               # Utilities & clients
│   │   │   └── supabase/      # Supabase SSR clients
│   │   ├── public/            # Static assets
│   │   └── package.json
│   │
│   └── api/                    # FastAPI Backend
│       ├── app/
│       │   ├── main.py        # FastAPI app
│       │   ├── config.py      # Configuration
│       │   ├── worker.py      # Celery worker
│       │   ├── api/routes/    # API endpoints
│       │   └── tasks/         # Celery tasks
│       ├── Dockerfile
│       └── requirements.txt
│
├── supabase/
│   └── migrations/            # Database migrations
│
├── docs/                      # Documentation
│   ├── OAUTH_FLOW.md
│   ├── CURRENT_STATUS.md
│   └── REQUIREMENTS_VS_PROGRESS.md
│
└── package.json               # Monorepo config
```

---

## 🔒 Security Stack

### **Authentication & Authorization**
- ✅ Google OAuth 2.0 (PKCE flow)
- ✅ Supabase Auth (JWT tokens)
- ✅ HTTP-only secure cookies
- ✅ Row Level Security (RLS) on database
- ✅ Middleware route protection

### **API Security**
- ⚠️ Rate limiting (not implemented yet)
- ⚠️ CORS configuration (needs review)
- ✅ Environment variable protection
- ✅ Service account key management
- ⚠️ API key rotation (needs setup)

### **Data Protection**
- ✅ PostgreSQL encryption at rest
- ✅ TLS/HTTPS for all connections
- ✅ Secrets stored in environment variables
- ⚠️ PII data encryption (needs review)

---

## 📊 Performance & Monitoring

### **Current Monitoring**
| Tool | Purpose | Status |
|------|---------|--------|
| Vercel Analytics | Frontend performance | ✅ Enabled |
| Railway Metrics | Backend CPU/memory | ✅ Enabled |
| Supabase Dashboard | Database queries | ✅ Enabled |

### **Planned Monitoring**
| Tool | Purpose | Timeline |
|------|---------|----------|
| Sentry | Error tracking | Week 5 |
| LogRocket | Session replay | Week 6 |
| Google Analytics | User behavior | Week 6 |

### **Performance Targets**
- Page load: < 3s (First Contentful Paint)
- API response: < 500ms (p95)
- Video render: < 2min for 1min video
- Audio generation: < 10s per block

---

## 🌐 Browser & Device Support

### **Browser Compatibility**
```
✅ Chrome 90+
✅ Firefox 88+
✅ Safari 14+
✅ Edge 90+
⚠️ Mobile Safari (needs testing)
⚠️ Chrome Android (needs testing)
```

### **Device Support**
```
✅ Desktop (1920x1080+)
⚠️ Tablet (768x1024) - needs responsive work
⚠️ Mobile (375x667) - needs responsive work
```

---

## 🔄 Version Control & Releases

### **Current Version**
```
Version:     0.1.0 (Alpha)
Status:      Infrastructure Complete
Progress:    15% (Authentication + Deployment)
Last Deploy: 2025-01-07
```

### **Git Workflow**
```
Branch:      master
Strategy:    Trunk-based development
CI/CD:       Auto-deploy on push
Tags:        Semantic versioning (v0.1.0)
```

---

## 📚 Technology Decision Rationale

### **Why Next.js 14?**
- ✅ Server & client components (optimal performance)
- ✅ Built-in API routes (optional backend)
- ✅ Excellent Vercel integration
- ✅ TypeScript first-class support
- ✅ Image optimization out of the box

### **Why FastAPI?**
- ✅ Modern async Python framework
- ✅ Automatic OpenAPI docs
- ✅ Excellent performance (comparable to Node.js)
- ✅ Great integration with ML/AI libraries
- ✅ Native Pydantic validation

### **Why Supabase?**
- ✅ PostgreSQL (proven, reliable)
- ✅ Built-in authentication
- ✅ Row Level Security
- ✅ Real-time subscriptions (future)
- ✅ Free tier generous for MVP

### **Why Railway?**
- ✅ Simple Docker deployment
- ✅ Built-in Redis & PostgreSQL
- ✅ Auto-scaling
- ✅ Generous free tier
- ✅ Great developer experience

### **Why Celery + Redis?**
- ✅ Battle-tested task queue
- ✅ Perfect for long-running tasks (video rendering)
- ✅ Retry logic built-in
- ✅ Works great with FastAPI
- ✅ Easy monitoring

---

## 🚀 Upgrade Path

### **When to Upgrade Services**

**Vercel (Frontend):**
```
Free Tier:     Good for 0-1,000 users
Pro ($20/mo):  Upgrade at 1,000+ users or need analytics
```

**Railway (Backend):**
```
Free Tier:     Good for development/testing
Hobby ($5/mo): Upgrade immediately after launch
Pro ($20/mo):  Upgrade at 100+ concurrent users
```

**Supabase:**
```
Free Tier:     Good for 0-10,000 users
Pro ($25/mo):  Upgrade at 10,000+ users or need more storage
```

---

## ✅ Tech Stack Summary

**Frontend:** Next.js 14 + React + TypeScript + Tailwind CSS
**Backend:** FastAPI + Python + Celery + Redis
**Database:** Supabase (PostgreSQL)
**AI/ML:** Google Gemini + Google Cloud TTS
**Media:** FFmpeg + wavesurfer.js
**Auth:** Google OAuth 2.0 + Supabase Auth
**Hosting:** Vercel (frontend) + Railway (backend)
**Storage:** Google Drive API + Supabase Storage

**Total Stack Components:** 40+ technologies
**Status:** Production-ready infrastructure, features pending
**Next Focus:** Build features using existing stack

---

**Last Updated:** 2025-01-07
**Maintained By:** Development Team
**Questions?** See [CURRENT_STATUS.md](./CURRENT_STATUS.md) for progress

# MayaStudio AI

> Multi-Speaker AI Voice & Video Studio for YouTube Shorts & Series

Create professional multi-character vertical mini-dramas, animated shorts, and YouTube series with AI-powered voice synthesis and automated video production.

## ✨ Features

- 🎭 **Multi-Speaker Script Parsing** - AI-powered screenplay analysis using Google Gemini
- 🎤 **Voice Design & Cloning** - Create unique character voices or clone existing ones
- 🎵 **High-Fidelity Audio Synthesis** - Google Cloud TTS with Sinhala language support
- ✏️ **Granular Line Editor** - Edit and regenerate individual dialogue lines
- 🎬 **Automated Video Assembly** - FFmpeg-powered video stitching with subtitles
- 📱 **Multi-Format Export** - Support for 9:16 (Shorts) and 16:9 (Full Episodes)
- 💾 **Google Drive Integration** - Store your projects in your own Google Drive (zero storage costs!)

## 🏗️ Architecture

### Tech Stack

**Frontend (Vercel)**
- Next.js 14 (App Router, TypeScript)
- Tailwind CSS + Shadcn UI
- Zustand (State Management)
- Wavesurfer.js (Audio Visualization)
- React Query

**Backend (Railway)**
- Python FastAPI
- Celery + Redis (Background Jobs)
- FFmpeg (Video Processing)
- Google Gemini API
- Google Cloud TTS

**Database & Storage**
- Supabase (PostgreSQL + Auth)
- Google Drive (User Storage - BYOS)
- Cloudflare R2 (Optional CDN)

## 🚀 Quick Start

### 📖 Complete Documentation

**→ See [INDEX.md](./INDEX.md) for full documentation navigation**

**Quick Links:**
- 🎯 [Quick Start (30 min)](./QUICK_START.md) - Fastest way to get running
- 📋 [Setup Guide](./SETUP_GUIDE.md) - Detailed instructions
- ✅ [Deployment Checklist](./DEPLOYMENT_CHECKLIST.md) - Step-by-step deployment
- 💰 [Free Tier Limits](./FREE_TIER_LIMITS.md) - Cost optimization
- 📊 [Development Plan](./DEVELOPMENT_PLAN_SUMMARY.md) - Complete roadmap

### Prerequisites

- Node.js 18+
- Python 3.11+
- Google Cloud account (free tier)
- Supabase account (free tier)
- Railway account (free tier)

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/mayastudio-ai.git
   cd mayastudio-ai
   ```

2. **Follow the detailed setup guide**

   See [SETUP_GUIDE.md](./SETUP_GUIDE.md) for complete step-by-step instructions.

3. **Install dependencies**
   ```bash
   # Frontend
   cd apps/web
   npm install

   # Backend
   cd apps/api
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

4. **Configure environment variables**

   Copy `.env.example` files and fill in your credentials.

5. **Run locally**
   ```bash
   # Frontend (Terminal 1)
   cd apps/web
   npm run dev

   # Backend (Terminal 2)
   cd apps/api
   uvicorn app.main:app --reload

   # Worker (Terminal 3)
   cd apps/api
   celery -A app.worker worker --loglevel=info
   ```

## 📖 Documentation

- [Setup Guide](./SETUP_GUIDE.md) - Complete setup instructions
- [Project Structure](./PROJECT_STRUCTURE.md) - Code organization
- [API Reference](./docs/api-reference.md) - Backend API documentation
- [Architecture](./docs/architecture.md) - System design details

## 💰 Pricing & Free Tier

This project is designed to run **completely free** during development:

| Service | Free Tier | Cost |
|---------|-----------|------|
| Vercel | 100GB bandwidth, unlimited deploys | **$0** |
| Railway | $5/month credit (~500 hours) | **$0** |
| Supabase | 500MB DB, 1GB storage | **$0** |
| Google Drive | 15GB per user | **$0** |
| Google Cloud | Pay-per-use (small amounts) | **~$5-10** |

**Total**: **$5-10/month** for development and testing!

See [PROJECT_STRUCTURE.md](./PROJECT_STRUCTURE.md) for upgrade paths.

## 🗺️ Roadmap

### Phase 1: Foundation ✅
- [x] Project setup
- [x] Database schema
- [x] Authentication
- [ ] Google Drive integration

### Phase 2: Core Features (In Progress)
- [ ] Script parsing with Gemini
- [ ] Voice profile management
- [ ] Audio synthesis
- [ ] Dialogue editor UI

### Phase 3: Video Production
- [ ] FFmpeg pipeline
- [ ] Subtitle generation
- [ ] Video export
- [ ] Preview system

### Phase 4: Advanced Features
- [ ] Batch processing
- [ ] Voice library
- [ ] Team collaboration
- [ ] Analytics dashboard

## 🤝 Contributing

Contributions are welcome! Please read our [Contributing Guide](./CONTRIBUTING.md) first.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.

## 🙏 Acknowledgments

- Google Cloud for AI/ML APIs
- Vercel for hosting
- Railway for backend infrastructure
- Supabase for database & auth
- FFmpeg for video processing

## 📧 Support

- 📖 [Documentation](./docs/)
- 🐛 [Issue Tracker](https://github.com/YOUR_USERNAME/mayastudio-ai/issues)
- 💬 [Discussions](https://github.com/YOUR_USERNAME/mayastudio-ai/discussions)

---

Built with ❤️ for content creators worldwide

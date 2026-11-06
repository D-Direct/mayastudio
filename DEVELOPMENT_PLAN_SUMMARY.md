# MayaStudio AI - Development Plan Summary

## 📋 Executive Summary

**Project:** MayaStudio AI - Multi-Speaker AI Voice & Video Studio for YouTube Shorts & Series

**Goal:** Build a SaaS platform that automates the creation of multi-character video content using AI voice synthesis and automated video assembly.

**Target Cost:** $5-20/month during development (free tier optimization)

**Timeline:** 8-9 weeks to MVP

---

## 🏗️ Architecture Decision

### Selected Stack: **Vercel + Railway (Free Tier)**

| Component | Service | Reason | Cost |
|-----------|---------|--------|------|
| Frontend | Vercel | Perfect for Next.js, free tier generous | $0 |
| Backend | Railway | Docker support, Redis included, easy setup | $0-5 |
| Database | Supabase | Managed PostgreSQL, Auth, Storage | $0 |
| Storage | Google Drive | User's own storage (BYOS strategy) | $0 |
| APIs | Google Cloud | Gemini + TTS, pay-per-use | $5-15 |

**Total: $5-20/month** during development

### Why Not Other Options?

- ❌ **Hetzner VPS:** No free tier, requires $13/mo minimum
- ❌ **Firebase:** 3-5x more expensive, FFmpeg limitations, cold starts
- ❌ **All-cloud (AWS/GCP):** Overkill for MVP, $100-300/mo
- ✅ **Vercel + Railway:** Best balance of free tier + features

---

## 💡 Key Innovation: Google Drive Integration

### "Bring Your Own Storage" (BYOS) Strategy

Instead of paying for user storage, integrate Google Drive:

**Benefits:**
- ✅ Zero storage costs (users use their 15GB free Drive)
- ✅ Unlimited scalability
- ✅ Users own their data
- ✅ Familiar interface
- ✅ Built-in backup

**How it works:**
1. User signs in with Google OAuth
2. App creates `/MayaStudio/` folder in their Drive
3. All source files and exports stored in their Drive
4. Backend downloads temporarily for processing
5. Results uploaded back to their Drive
6. Temp files deleted

**Cost savings:** $1,500-2,300/month at 1000 users!

---

## 🎯 Technical Architecture

### Data Flow

```
┌─────────────────────────────────────────────────────────────┐
│                    USER'S GOOGLE DRIVE                      │
│        (Source videos, audio blocks, exports)               │
└──────────────────────┬──────────────────────────────────────┘
                       │ Google Drive API
┌──────────────────────▼──────────────────────────────────────┐
│                 RAILWAY BACKEND (FastAPI)                   │
│  - Downloads files temporarily for processing               │
│  - Runs FFmpeg video assembly                               │
│  - Generates audio with Google TTS                          │
│  - Uploads results back to Drive                            │
│  - Deletes temp files                                       │
└──────────────────────┬──────────────────────────────────────┘
                       │ REST API
┌──────────────────────▼──────────────────────────────────────┐
│               VERCEL FRONTEND (Next.js)                     │
│  - User interface for editing                               │
│  - Audio waveform visualization                             │
│  - Scene management dashboard                               │
│  - Real-time preview                                        │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│            SUPABASE (PostgreSQL + Auth)                     │
│  - User profiles & preferences                              │
│  - Project metadata                                         │
│  - Scene structure                                          │
│  - Dialogue text & settings                                 │
│  - Google Drive file IDs (pointers only)                    │
└─────────────────────────────────────────────────────────────┘
```

---

## 📂 Project Structure

```
mayastudio-ai/
├── apps/
│   ├── web/                    # Next.js frontend (Vercel)
│   │   ├── app/                # App router pages
│   │   ├── components/         # UI components
│   │   ├── lib/                # Utilities & clients
│   │   └── hooks/              # React hooks
│   │
│   └── api/                    # Python backend (Railway)
│       ├── app/
│       │   ├── main.py         # FastAPI entry
│       │   ├── worker.py       # Celery tasks
│       │   ├── api/routes/     # API endpoints
│       │   ├── services/       # Business logic
│       │   ├── models/         # Database models
│       │   └── tasks/          # Background jobs
│       └── Dockerfile
│
├── supabase/
│   └── migrations/             # Database schema
│
├── docs/
└── Configuration files (.gitignore, README, etc.)
```

---

## 🗄️ Database Schema

### Core Tables

**user_profiles**
- User info, Google OAuth tokens
- Drive folder ID
- Credit balance

**projects**
- Project metadata
- Drive folder mapping
- Aspect ratio settings

**scenes**
- Scene details
- Video asset references (Drive IDs)
- Export status

**dialogue_blocks**
- Dialogue text (Sinhala + English)
- Audio file reference (Drive ID)
- Voice profile mapping
- Generation status

**voice_profiles**
- Character name
- Voice ID (from Google API)
- Voice type (designed/cloned)

---

## ⚡ Development Phases

### Phase 1: Foundation (Week 1) ✅ DOCUMENTED
- ✅ Project structure created
- ✅ Setup guides written
- ✅ Configuration files created
- ✅ Deployment checklist prepared
- 🔄 Next: Initialize codebase

### Phase 2: Backend Core (Weeks 2-3)
**Tasks:**
1. Set up FastAPI project structure
2. Integrate Supabase database
3. Implement Google OAuth flow
4. Build Google Drive service
5. Create Gemini script parser
6. Integrate Google TTS
7. Set up Celery worker queue
8. Build FFmpeg video processor

### Phase 3: Frontend Core (Weeks 3-4)
**Tasks:**
1. Initialize Next.js with Shadcn UI
2. Build authentication pages
3. Create project dashboard
4. Build scene overview page
5. Implement dialogue editor
6. Add audio player (Wavesurfer.js)
7. Create voice profile manager
8. Build preview panel

### Phase 4: Integration (Weeks 4-5)
**Tasks:**
1. Connect frontend to backend API
2. Implement React Query hooks
3. Set up Zustand state management
4. Add WebSocket for real-time updates
5. Build Google Drive file picker
6. Implement upload/download flows
7. Add error handling
8. Create loading states

### Phase 5: Video Production (Weeks 5-6)
**Tasks:**
1. Build FFmpeg pipeline
2. Implement subtitle generation
3. Create video export queue
4. Add progress tracking
5. Build preview system
6. Optimize video rendering
7. Add export formats (9:16, 16:9)

### Phase 6: Polish (Weeks 6-7)
**Tasks:**
1. Implement credit/billing system
2. Add usage analytics
3. Build settings pages
4. Create onboarding flow
5. Add keyboard shortcuts
6. Optimize performance
7. Mobile responsiveness

### Phase 7: Testing (Week 7-8)
**Tasks:**
1. Unit tests (backend)
2. Component tests (frontend)
3. Integration tests
4. E2E tests (Playwright)
5. Load testing
6. Security audit
7. Bug fixes

### Phase 8: Launch (Week 8-9)
**Tasks:**
1. Production deployment
2. Domain setup
3. Monitoring setup
4. Documentation finalization
5. Beta user testing
6. Performance tuning
7. Launch! 🚀

---

## 📊 Free Tier Limits

### Critical Limits to Monitor

| Service | Limit | Estimated Usage | Status |
|---------|-------|-----------------|--------|
| Vercel Bandwidth | 100GB/mo | ~10-20GB | ✅ Safe |
| Railway Credit | $5/mo | ~$0.50-2 | ✅ Safe |
| Supabase DB | 500MB | ~50-100MB | ✅ Safe |
| Supabase Storage | 1GB | ~100MB | ✅ Safe |
| Google TTS | 4M chars/mo free | ~75-150K | ✅ Safe |
| Gemini API | Pay-per-use | ~$1-5/mo | ✅ Safe |

**Monitoring Plan:**
- Check dashboards weekly
- Set up alerts at 80% thresholds
- Optimize before upgrading

---

## 💰 Cost Projections

### Development Phase (0-10 users)
- Vercel: $0
- Railway: $0-2
- Supabase: $0
- Google Cloud: $5-10
- **Total: $5-12/month**

### Beta Phase (10-100 users)
- Vercel: $0-20
- Railway: $15-20
- Supabase: $25
- Google Cloud: $10-30
- **Total: $50-95/month**

### Launch Phase (100-1000 users)
- Vercel: $20
- Railway: $50-100
- Supabase: $25-50
- Google Cloud: $50-200
- **Total: $145-370/month**

### Scale Phase (1000+ users)
- Consider migrating to VPS or AWS/GCP
- **Estimated: $300-1000/month**

---

## 🎯 Success Metrics

### MVP Goals (Week 8)
- [ ] User can sign up with Google
- [ ] User can upload screenplay script
- [ ] Script parsed into structured dialogue
- [ ] User can assign voices to characters
- [ ] Audio generated for all dialogue blocks
- [ ] User can edit and regenerate individual lines
- [ ] Final video exported to user's Google Drive
- [ ] End-to-end workflow complete in <10 minutes

### Performance Targets
- Page load: <2 seconds
- API response: <500ms
- Audio generation: <5 seconds per block
- Video export: <2 minutes for 1-minute scene
- Database queries: <100ms

### Quality Targets
- Zero data loss
- 99% uptime (dev environment)
- <1% error rate
- Mobile responsive
- Accessible (WCAG AA)

---

## 🚨 Risk Mitigation

### Technical Risks

**Risk:** Google API costs exceed budget
**Mitigation:**
- Implement aggressive caching
- Set hard budget limits ($50/mo)
- Monitor daily usage

**Risk:** Railway free tier exhausted
**Mitigation:**
- Optimize worker efficiency
- Implement service sleep
- Upgrade to pay-as-you-go ($10/mo) if needed

**Risk:** FFmpeg processing too slow
**Mitigation:**
- Optimize video encoding settings
- Implement job prioritization
- Add processing progress indicators

**Risk:** User's Drive quota full
**Mitigation:**
- Check quota before operations
- Prompt user to upgrade Drive storage
- Offer server storage as paid option

### Business Risks

**Risk:** Users don't want to connect Google Drive
**Mitigation:**
- Offer both options (Drive or server)
- Clearly explain benefits
- Make it optional, not required

**Risk:** Too expensive to scale
**Mitigation:**
- Design for cost efficiency from day 1
- Monitor unit economics
- Plan migration to cheaper infrastructure

---

## 📚 Documentation Status

### Completed ✅
- [x] Project specification review
- [x] Architecture decision
- [x] Hosting strategy analysis
- [x] Project structure design
- [x] Setup guide
- [x] Deployment checklist
- [x] Free tier limits guide
- [x] Quick start guide
- [x] Development plan summary

### To Create 🔄
- [ ] API documentation (auto-generated from FastAPI)
- [ ] Component storybook
- [ ] User guide
- [ ] Contributing guide
- [ ] Code style guide

---

## 🎬 Next Actions

### Immediate Next Steps (This Week)

1. **Initialize Repository**
   ```bash
   git init
   git add .
   git commit -m "Initial project setup"
   git remote add origin https://github.com/YOUR_USERNAME/mayastudio-ai.git
   git push -u origin main
   ```

2. **Set Up Services**
   - Create Supabase project
   - Create Google Cloud project
   - Enable required APIs
   - Create OAuth credentials

3. **Deploy Infrastructure**
   - Connect Railway to GitHub
   - Connect Vercel to GitHub
   - Configure environment variables
   - Test deployments

4. **Start Development**
   - Create FastAPI skeleton
   - Create Next.js skeleton
   - Test local development
   - Commit initial code

### Week 2 Focus

1. **Backend Foundation**
   - Database models
   - Supabase integration
   - Google OAuth
   - Basic API endpoints

2. **Frontend Foundation**
   - Authentication pages
   - Dashboard layout
   - Component library setup
   - State management

---

## ✅ Success Criteria

### Week 1 (Setup) ✅
- [x] Architecture decided
- [x] Documentation complete
- [ ] Accounts created
- [ ] Repository initialized
- [ ] Services deployed (empty)

### Week 4 (Core Features)
- [ ] User authentication working
- [ ] Google Drive integration working
- [ ] Script parsing functional
- [ ] Audio generation working

### Week 8 (MVP)
- [ ] End-to-end workflow complete
- [ ] All core features working
- [ ] Tests passing
- [ ] Documentation updated
- [ ] Ready for beta users

---

## 📞 Support & Resources

### Official Documentation
- [Vercel Docs](https://vercel.com/docs)
- [Railway Docs](https://docs.railway.app)
- [Supabase Docs](https://supabase.com/docs)
- [Next.js Docs](https://nextjs.org/docs)
- [FastAPI Docs](https://fastapi.tiangolo.com)

### Google Cloud
- [Google Drive API](https://developers.google.com/drive)
- [Gemini API](https://ai.google.dev/docs)
- [Cloud TTS](https://cloud.google.com/text-to-speech/docs)

### Community
- [GitHub Discussions](https://github.com/YOUR_USERNAME/mayastudio-ai/discussions)
- [Issue Tracker](https://github.com/YOUR_USERNAME/mayastudio-ai/issues)

---

**Document Version:** 1.0
**Last Updated:** 2024-11-06
**Next Review:** Weekly (every Monday)

---

## 🎉 Summary

We've designed a **cost-effective, scalable architecture** for MayaStudio AI using:

✅ **Free tier services** (Vercel + Railway + Supabase)
✅ **Smart storage strategy** (User's Google Drive = $0 cost)
✅ **Modern tech stack** (Next.js + FastAPI + Celery)
✅ **Clear development roadmap** (8 weeks to MVP)
✅ **Comprehensive documentation** (Setup to deployment)

**Ready to start building? Let's go! 🚀**

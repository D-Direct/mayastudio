# MayaStudio AI - Requirements vs Progress Summary

**Last Updated:** 2025-01-07

---

## 📋 Original Requirements (From Spec)

### **Product Vision**
MayaStudio AI is a SaaS platform for creating multi-character vertical mini-dramas, animated shorts, and YouTube series by:
1. Parsing multi-speaker screenplays into structured JSON using Gemini AI
2. Managing persistent character voice profiles
3. Synthesizing dialogue audio via Google Cloud TTS
4. Providing line-by-line audio-text editor for retakes
5. Managing episode/scene structures
6. Assembling audio + video into finished videos (9:16 or 16:9)

### **Core User Workflows (Required)**

#### Workflow 1: Project & Scene Management
- Create projects with multiple scenes
- Scene overview dashboard showing all scenes
- Drag-and-drop scene reordering
- Scene completion status tracking (e.g., "🟢 12/12 Generated")
- Import screenplay scripts (PDF/TXT)
- Navigate between scenes easily

#### Workflow 2: Character Voice Management
- Assign voice profiles to characters
- **Voice Design:** Create voices from text prompts (e.g., "deep male voice, 30s, formal tone")
- **Voice Cloning:** Upload reference audio to clone voices
- Persistent voice mapping (Character → voice_id)
- Pre-production voice setup before rendering

#### Workflow 3: Script Parsing
- Upload/paste raw screenplay text (Sinhala dialogue + English stage directions)
- Gemini AI converts unstructured text → validated JSON
- Extract:
  - Actor names
  - Dialogue text (Sinhala)
  - Emotion/tone context
  - Scene headings
  - Stage directions

#### Workflow 4: Dialogue Editor (Line-by-Line)
- Visual dialogue block cards
- Each block shows:
  - Actor dropdown
  - Tone/emotion selector
  - Text editor (Sinhala support)
  - Audio waveform visualization
  - Generation status (🟢 Generated / 🟡 Modified / ⏳ Pending)
- Actions per block:
  - Play audio
  - Edit text/tone
  - Re-generate audio (individual blocks)
  - Delete block
- Status tracking:
  - 'pending' → user clicks generate
  - 'generated' → audio ready
  - 'modified' → text changed, needs re-gen
  - 'failed' → error occurred

#### Workflow 5: Video Assembly & Export
- Preview panel showing visual asset + subtitles
- Master audio timeline visualization (waveform)
- Background video/B-roll selection
- Aspect ratio selection (9:16 Shorts / 16:9 Series)
- "Stitch & Export Final MP4" button
- FFmpeg-powered video rendering
- Burn-in Sinhala subtitles
- Download final video

#### Workflow 6: Background Processing
- Async job queue (Celery + Redis)
- Handle long-running tasks:
  - Batch audio generation
  - Video rendering
  - Script parsing
- Progress tracking
- No UI timeouts

---

## 🗓️ Planned Development Approach (8-Week Plan)

### **Phase 1: Infrastructure (Week 1)** ✅
- [x] Set up Next.js 14 frontend
- [x] Set up FastAPI backend
- [x] Set up Supabase database
- [x] Deploy to Vercel + Railway
- [x] Configure Celery + Redis
- [x] Implement authentication
- [x] Create database schema

### **Phase 2: Backend Services (Weeks 2-3)** ⏳
- [ ] Integrate Google Gemini API (script parsing)
- [ ] Integrate Google Cloud TTS (audio generation)
- [ ] Integrate Google Drive API (file storage)
- [ ] Implement voice profile management
- [ ] Build FFmpeg video processing pipeline
- [ ] Create Celery background tasks

### **Phase 3: Frontend UI (Weeks 3-4)** ⏳
- [ ] Build Scene Overview Dashboard
- [ ] Create Dialogue Editor workspace
- [ ] Implement audio player (wavesurfer.js)
- [ ] Build voice selection UI
- [ ] Create video preview panel
- [ ] Add drag-and-drop functionality

### **Phase 4: Integration (Weeks 4-5)** ⏳
- [ ] Connect frontend to backend APIs
- [ ] Implement real-time status updates
- [ ] Add file upload/download
- [ ] Integrate payment system (Stripe)
- [ ] Build credit tracking system

### **Phase 5: Polish & Testing (Weeks 6-8)** ⏳
- [ ] UI/UX refinement
- [ ] Performance optimization
- [ ] Bug fixes
- [ ] User testing
- [ ] Documentation
- [ ] Launch preparation

---

## 📊 Current Progress (As of January 7, 2025)

### ✅ **COMPLETED** (Infrastructure - Week 1)

#### Authentication & User Management
- ✅ Google OAuth login flow (working end-to-end)
- ✅ Session management with cookies
- ✅ Protected routes via middleware
- ✅ User profile creation in database
- ✅ OAuth scopes for Google Drive access

#### Infrastructure Deployment
- ✅ Frontend: Vercel (https://mayastudio-two.vercel.app)
- ✅ Backend API: Railway (https://mayastudio-production.up.railway.app)
- ✅ Celery Worker: Railway (running)
- ✅ Redis: Railway (running)
- ✅ Database: Supabase (with complete schema)

#### Database Schema Created
```sql
✅ user_profiles        -- User data + OAuth tokens
✅ projects             -- Project metadata
✅ scenes               -- Scene details with ordering
✅ voice_profiles       -- Character voice mappings
✅ dialogue_blocks      -- Dialogue with audio & status
✅ render_jobs          -- Video rendering job queue
✅ usage_logs           -- API usage tracking
```

#### Pages Created (Basic UI)
- ✅ Landing page (`/`)
- ✅ Login page (`/login`)
- ✅ Dashboard page (`/dashboard`)
- ✅ Auth callback (`/auth/callback`)
- ✅ Error page (`/auth/auth-code-error`)

#### Backend API Structure
- ✅ All routes defined (7 route files)
- ✅ FastAPI application setup
- ✅ Celery worker configured
- ✅ Docker deployment ready

---

### ⏳ **IN PROGRESS / NOT STARTED**

#### Backend Services (0% Implemented)
- ❌ **Gemini API Integration** - Script parsing not implemented
- ❌ **Google Cloud TTS** - Audio generation not connected
- ❌ **Google Drive API** - File storage not integrated
- ❌ **FFmpeg Pipeline** - Video assembly not built
- ❌ **Celery Tasks** - No background tasks processing
- ❌ **Voice Profile Management** - No voice creation/cloning
- ❌ **Database Operations** - CRUD operations are placeholders

#### Frontend Functionality (0% Implemented)
- ❌ **Project CRUD** - Can't create/edit/delete projects
- ❌ **Scene Management** - No scene overview dashboard
- ❌ **Script Input** - No text editor for scripts
- ❌ **Script Parsing UI** - No Gemini parsing interface
- ❌ **Voice Selection** - No voice profile UI
- ❌ **Dialogue Editor** - Block cards not functional
- ❌ **Audio Player** - No wavesurfer.js integration
- ❌ **Video Preview** - No preview panel
- ❌ **Export Functionality** - Can't render/download videos

#### Features Not Started
- ❌ Scene drag-and-drop reordering
- ❌ Line-by-line audio regeneration
- ❌ Status tracking (pending/generated/modified)
- ❌ Batch operations
- ❌ Real-time progress updates
- ❌ File upload handling
- ❌ Credit system / billing
- ❌ Stripe integration

---

## 🎯 Feature-by-Feature Comparison

| Feature | Required | Planned | Current Status | Priority |
|---------|----------|---------|----------------|----------|
| **Authentication** | ✅ Yes | Week 1 | ✅ **DONE** | Critical |
| **Project CRUD** | ✅ Yes | Week 2 | ❌ Not started | **High** |
| **Scene Management** | ✅ Yes | Week 2 | ❌ Not started | **High** |
| **Script Upload** | ✅ Yes | Week 2 | ❌ Not started | **High** |
| **Gemini Parsing** | ✅ Yes | Week 2 | ❌ Not started | **High** |
| **Voice Profiles** | ✅ Yes | Week 3 | ❌ Not started | Medium |
| **Voice Design** | ✅ Yes | Week 3 | ❌ Not started | Medium |
| **Voice Cloning** | ⚠️ Optional | Week 4 | ❌ Not started | Low |
| **Dialogue Editor** | ✅ Yes | Week 3 | ❌ Not started | **High** |
| **TTS Audio Gen** | ✅ Yes | Week 3 | ❌ Not started | **High** |
| **Audio Player** | ✅ Yes | Week 3 | ❌ Not started | Medium |
| **Line Re-generate** | ✅ Yes | Week 3 | ❌ Not started | Medium |
| **Status Tracking** | ✅ Yes | Week 3 | ❌ Not started | Medium |
| **Video Preview** | ✅ Yes | Week 4 | ❌ Not started | Medium |
| **FFmpeg Render** | ✅ Yes | Week 5 | ❌ Not started | Medium |
| **Subtitle Burn-in** | ✅ Yes | Week 5 | ❌ Not started | Low |
| **Video Export** | ✅ Yes | Week 5 | ❌ Not started | Medium |
| **Google Drive** | ⚠️ Optional | Week 4 | ❌ Not started | Low |
| **Drag-Drop Scenes** | ⚠️ Optional | Week 6 | ❌ Not started | Low |
| **Stripe Billing** | ⚠️ Optional | Week 7 | ❌ Not started | Low |
| **Credit System** | ⚠️ Optional | Week 7 | ❌ Not started | Low |

---

## 📈 Overall Progress Metrics

### By Phase
```
Phase 1: Infrastructure       ████████████████████ 100% ✅
Phase 2: Backend Services     ██░░░░░░░░░░░░░░░░░░   5% ⏳
Phase 3: Frontend UI          ██░░░░░░░░░░░░░░░░░░  10% ⏳
Phase 4: Integration          ░░░░░░░░░░░░░░░░░░░░   0% ❌
Phase 5: Polish & Testing     ░░░░░░░░░░░░░░░░░░░░   0% ❌
```

### By Component
```
Authentication:        100% ✅ COMPLETE
Deployment:           100% ✅ COMPLETE
Database:             100% ✅ COMPLETE
API Structure:         20% ⏳ (routes defined, no logic)
Frontend Pages:        15% ⏳ (layouts only, no functionality)
AI Integrations:        0% ❌ NOT STARTED
Media Processing:       0% ❌ NOT STARTED
User Features:          0% ❌ NOT STARTED
```

### Overall Project Completion
```
Total Progress:  ████░░░░░░░░░░░░░░░░  15%
```

**Status:** Infrastructure complete, ready to build features

---

## 🎯 Recommended MVP Scope (Simplified First Version)

To get a working product faster, here's a simplified MVP that covers the **core value proposition**:

### ✅ **MVP Must-Have Features**

1. **Project Management (Basic)**
   - Create project with title
   - List all projects
   - Open/delete projects
   - NO scene reordering yet

2. **Script Input (Simple)**
   - Paste raw script text
   - Save to database
   - NO PDF upload initially

3. **Gemini Parsing**
   - Send script to Gemini API
   - Parse into structured JSON
   - Extract: actor, dialogue, tone
   - Display results

4. **Voice Selection (Simple)**
   - Pre-defined voice list (no custom creation yet)
   - Assign voice to character
   - Save mapping

5. **TTS Audio Generation**
   - Generate audio for each dialogue block
   - Show progress indicator
   - Save audio files
   - Mark blocks as "generated"

6. **Basic Dialogue List**
   - Show all dialogue blocks
   - Play audio button
   - Edit text capability
   - Re-generate button (per block)

7. **Video Assembly (Simple)**
   - Single background image (no video yet)
   - Stitch audio timeline
   - Add Sinhala subtitles
   - Export as MP4

8. **Download**
   - Download final video
   - Save to Google Drive (optional)

### ❌ **MVP Can Wait (Later Versions)**

- ❌ Voice design/cloning (use pre-made voices)
- ❌ Advanced scene management
- ❌ Drag-and-drop reordering
- ❌ Real-time waveform visualization
- ❌ Video preview panel
- ❌ Batch operations
- ❌ Stripe billing
- ❌ Credit system
- ❌ Collaboration features

---

## 🚀 Next Steps (Priority Order)

### **Sprint 1: Foundation (Week 2)** - Project & Script Management

**Goal:** Users can create projects and input scripts

1. ✅ Build Project CRUD UI
   - Create project form (modal)
   - Project list/grid display
   - Edit/delete project
   - Connect to backend API

2. ✅ Build Script Input Interface
   - Text editor component (Sinhala support)
   - Save script to database
   - Load existing script
   - Character count/validation

3. ✅ Implement Backend Project API
   - POST /api/projects (create)
   - GET /api/projects (list)
   - GET /api/projects/:id (get one)
   - PUT /api/projects/:id (update)
   - DELETE /api/projects/:id (delete)

**Deliverable:** Users can create projects and write/save scripts

---

### **Sprint 2: AI Parsing (Week 3)** - Gemini Integration

**Goal:** Scripts automatically parse into structured dialogue

1. ✅ Integrate Gemini API (Backend)
   - Set up Gemini SDK
   - Create parsing prompt
   - Handle API responses
   - Error handling

2. ✅ Build Parsing UI (Frontend)
   - "Parse Script" button
   - Loading state
   - Display parsed results
   - Error messages

3. ✅ Save Parsed Data
   - Store scenes in database
   - Store dialogue blocks
   - Link to voice profiles

**Deliverable:** Raw scripts become structured dialogue blocks

---

### **Sprint 3: Voice & Audio (Week 4)** - TTS Integration

**Goal:** Generate audio for all dialogue blocks

1. ✅ Voice Profile Management
   - List available voices (Google TTS)
   - Assign voice to character
   - Save voice mappings

2. ✅ Integrate Google Cloud TTS
   - Set up TTS API
   - Generate audio for single block
   - Save MP3 files
   - Update block status

3. ✅ Audio Playback UI
   - Audio player component
   - Play/pause controls
   - Loading states
   - "Generate Audio" button

**Deliverable:** Users hear AI-generated dialogue

---

### **Sprint 4: Video Assembly (Week 5)** - FFmpeg Integration

**Goal:** Create downloadable videos

1. ✅ FFmpeg Pipeline (Backend)
   - Install FFmpeg
   - Stitch audio timeline
   - Add background image
   - Burn-in subtitles
   - Export MP4

2. ✅ Celery Async Tasks
   - Create rendering task
   - Progress tracking
   - Error handling
   - File storage

3. ✅ Export UI (Frontend)
   - "Render Video" button
   - Progress indicator
   - Download button
   - Error handling

**Deliverable:** Users download finished videos

---

## 📝 Summary

### **Where We Are:**
- ✅ Infrastructure: 100% complete
- ✅ Authentication: Working
- ✅ Deployments: All live
- ⏳ Features: 0% implemented

### **What's Next:**
- Build Project CRUD (Sprint 1)
- Add Script Input (Sprint 1)
- Integrate Gemini (Sprint 2)
- Add TTS Audio (Sprint 3)
- Build Video Export (Sprint 4)

### **Timeline Estimate:**
- **MVP (Core Features):** 4-6 weeks
- **Polished Product:** 8-10 weeks
- **Full Spec:** 12-16 weeks

### **Current Focus:**
Start with **Project CRUD** → foundation for everything else

---

**Status:** Ready to start building features! 🚀
**Next Action:** Implement Project Management (Create/List/Edit/Delete)

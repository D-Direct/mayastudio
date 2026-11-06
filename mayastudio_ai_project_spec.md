# MayaStudio AI — Multi-Speaker AI Voice & Video Studio for YouTube Shorts & Series

## Software Architecture & Development Specification V1.1

## 1. Executive Summary & Vision

**MayaStudio AI** is a specialized SaaS application designed for creators, filmmakers, and content producers making multi-character vertical mini-dramas, animated shorts, and YouTube series (such as adapted Sinhala screenplays).

The platform automates the process of:

1. Parsing raw multi-speaker screenplays into structured JSON data using LLM reasoning.

2. Managing persistent character voice profiles (Voice Design & Instant Voice Cloning).

3. Synthesizing high-fidelity, contextual dialogue audio blocks via Google Gemini TTS / Speech APIs.

4. Providing a granular, stateful line-by-line audio-text editor for fast retakes and modifications.

5. Managing episode structures through a dedicated **Scene Navigation & Dashboard Architecture**.

6. Programmatically assembling and stitching audio chunks with visual media assets into finished 1–3 minute video blocks (YouTube Shorts 9:16 or Series 16:9).

## 2. System Architecture & Tech Stack

```
 ┌─────────────────────────────────────────────────────────────────────────┐
 │                            FRONTEND LAYER                               │
 │   Next.js 14+ (React/TS) + Tailwind CSS + Shadcn UI + Wavesurfer.js     │
 └────────────────────────────────────┬────────────────────────────────────┘
                                      │ REST / WebSockets / React Query
 ┌────────────────────────────────────▼────────────────────────────────────┐
 │                            BACKEND LAYER                                │
 │   Python (FastAPI) + Celery/Redis Queue + FFmpeg Stitching Engine       │
 └──────────┬─────────────────────────┬──────────────────────────┬─────────┘
            │                         │                          │
 ┌──────────▼──────────┐   ┌──────────▼──────────┐    ┌──────────▼──────────┐
 │ Google Gemini API   │   │  Google Cloud TTS   │    │ Database & Auth     │
 │ (Script Parsing &   │   │  / Voices API       │    │ Supabase (Postgres) │
 │ Tone Context)       │   │ (Audio Synthesizer) │    │ & Stripe Payments   │
 └─────────────────────┘   └─────────────────────┘    └─────────────────────┘

```

* **Frontend:** Next.js 14+ (App Router, TypeScript), Tailwind CSS, Shadcn UI components, Zustand (State Management), `wavesurfer.js` (Audio visualization).

* **Backend API:** Python (FastAPI) for AI SDK integration, streaming audio endpoints, and media pipeline control.

* **Background Worker Queue:** Redis + Celery (Handles asynchronous FFmpeg rendering jobs and multi-file batch audio processing without UI timeouts).

* **Media Processing:** `ffmpeg-python` for video cropping (9:16 / 16:9), burn-in Sinhala subtitles, and audio timeline stitching.

* **AI & Speech Services:**

  * Google AI Studio / Gemini API (Script parsing, performance directions, tone reasoning).

  * Google Gemini Voices API / Google Cloud TTS (Native Sinhala script rendering, voice cloning, and audio output).

* **Database & Storage:** Supabase (PostgreSQL for project/scene relational data, S3 Object Storage for `.mp3` chunks and exported `.mp4` renders).

* **Auth & Billing:** Supabase Auth + Stripe (Subscription tiers & token credit allocation).

## 3. Core Functional Workflows

### 3.1. Episode & Scene Management Architecture

The app uses a 2-level scene hierarchy:

1. **Scene Overview Page (`/projects/:id/scenes`):** A dashboard displaying all scene cards in sequence. Users can drag-and-drop to reorder scenes, view completion status (`🟢 12/12 Generated`), or upload raw scripts for automated parsing.

2. **In-Editor Scene Switcher:** A left-hand collapsible drawer inside the Dialogue Editor allowing instant switching between scenes without leaving the workspace.

### 3.2. Cast & Voice Management (Pre-Production)

Before rendering scenes, users assign or design persistent voice profiles for each character:

* **Voice Design (Prompt-based):** Natural language prompts (e.g., *"A smooth, deep male voice in his 30s with a sharp, formal tone"*) sent to Google API (`POST /v1beta/voices`) return a persistent `voice_id`.

* **Voice Cloning (Replication):** Uploading a short reference audio file of a native speaker yields a cloned `voice_id`.

* **Mapping:** Each project character (e.g., `AKEN`, `AMAYA`) maps to a unique `voice_id` saved in the database.

### 3.3. Script Parsing Engine

Users upload or paste raw script text (e.g., Sinhala dialogue with English stage directions). Gemini converts unstructured screenplay text into a validated JSON array of dialogue objects.

### 3.4. Granular Line-by-Line Synthesis & Re-generation State Machine

Each dialogue card operates independently:

```
[ User Edits Text / Tone ] ──► Status changes to 'MODIFIED' (Yellow)
                                              │
                                   [ User Clicks Re-Generate ]
                                              │
                                   [ API POST /api/generate-block ]
                                              │
                                 Synthesizes new audio block
                                              │
                               Overwrites target block_id.mp3 file
                                              │
                              Status changes to 'GENERATED' (Green)

```

## 4. UI/UX Screens & Component Architecture

### 4.1. Screen 1: Scene Overview Dashboard (`/projects/:id/scenes`)

```
┌──────────────────────────────────────────────────────────────────────────────┐
│ [Logo] MayaStudio AI  | Project: Episode 1: The First Impression | 💎 450 Cr │
├──────────────────────────────────────────────────────────────────────────────┤
│ [ + Add New Scene ]   [ 📄 Import Screenplay Script (PDF/TXT) ]             │
│                                                                              │
│ ┌────────────────────────┐  ┌────────────────────────┐  ┌──────────────────┐ │
│ │ Scene 01               │  │ Scene 02               │  │ Scene 03         │ │
│ │ INT. COLOMBO STUDIO    │  │ EXT. ROAD - NIGHT      │  │ INT. HOME - DAY  │ │
│ │ [ Video Thumbnail ]    │  │ [ Video Thumbnail ]    │  │ [ Thumbnail ]    │ │
│ │ 12 lines • 0:42s       │  │ 8 lines • 0:28s        │  │ 15 lines • 0:55s │ │
│ │ Status: 🟢 12/12 Done  │  │ Status: 🟡 4/8 Modified│  │ Status: ⏳ Draft │ │
│ │ [ Open Editor ]        │  │ [ Open Editor ]        │  │ [ Open Editor ]  │ │
│ └────────────────────────┘  └────────────────────────┘  └──────────────────┘ │
└──────────────────────────────────────────────────────────────────────────────┘

```

### 4.2. Screen 2: Dialogue Editor & Workspace (`/projects/:id/scenes/:sceneId`)

```
┌─────────────────────────────────────────┬────────────────────────────────────┐
│ SCRIPT & DIALOGUE EDITOR                │ PREVIEW & TIMELINE ASSEMBLY        │
├─────────────────────────────────────────┼────────────────────────────────────┤
│ [<] Episode 1 ▾ | Scene 01: Studio      │ ┌────────────────────────────────┐ │
│                                         │ │                                │ │
│ [Block #01]                             │ │   Visual Asset Preview Frame   │ │
│ Actor: [ Amaya ▾ ] Tone: [ Calm ▾ ]     │ │   (9:16 Shorts Video + Sub)    │ │
│ ┌─────────────────────────────────────┐ │ │                                │ │
│ │ "මේක Aken ගේ අලුත් song එකට..."      │ │ └────────────────────────────────┘ │
│ └─────────────────────────────────────┘ │ ▶ Play Scene  [■ Stop]   Length: 28s │
│ Status: 🟢 Generated (04.2s)            │ ────────────────────────────────── │
│ [ ▶ Play ] [ 🔄 Re-Generate ] [ 🗑️ ]   │ Master Audio Waveform Track:       │
│                                         │ ▃▄▆█▇▅▃▂      ▂▃▄▅▆▇█▇▆▅▃          │
│ [Block #02]                             │ ────────────────────────────────── │
│ Actor: [ Aken ▾ ] Tone: [ Sharp ▾ ]     │ Background Video / B-Roll Clip:    │
│ ┌─────────────────────────────────────┐ │ [ studio_bg_clip.mp4           ▾ ] │
│ │ "මම කොතනද ඉන්නේ?"                   │ │                                    │
│ └─────────────────────────────────────┘ │                                    │
│ Status: 🟡 Modified (Unsaved changes)   │                                    │
│ [ ▶ Play Prev ] [ ✨ Re-Generate ]      │ [ 🎬 Stitch & Export Final MP4 ]   │
└─────────────────────────┴────────────────────────────────────┘

```

## 5. Database Schema (Supabase / Postgres)

```
-- Projects Table
CREATE TABLE projects (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES auth.users(id),
  title TEXT NOT NULL,
  aspect_ratio TEXT DEFAULT '9:16',
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Scenes Table
CREATE TABLE scenes (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  project_id UUID REFERENCES projects(id) ON DELETE CASCADE,
  scene_number INT NOT NULL,
  heading TEXT NOT NULL,
  b_roll_url TEXT,
  order_index INT NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Dialogue Blocks Table
CREATE TABLE dialogue_blocks (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  scene_id UUID REFERENCES scenes(id) ON DELETE CASCADE,
  actor_name TEXT NOT NULL,
  voice_id TEXT NOT NULL,
  emotion_tone TEXT NOT NULL,
  sinhala_text TEXT NOT NULL,
  audio_url TEXT,
  duration_seconds NUMERIC(4,2),
  status TEXT CHECK (status IN ('pending', 'generated', 'modified', 'failed')),
  order_index INT NOT NULL
);

```

## 6. Implementation Roadmap

1. **Phase 1: Proof-of-Concept Pilot Script (Days 1–3)**

   * Implement Gemini API script parsing script in Python (FastAPI).

   * Generate static voice blocks for Scene 1 using Google Gemini Speech API.

   * Verify native Sinhala phonetic rendering and tone modulation quality.

2. **Phase 2: Core SaaS Web Backend & Database (Days 4–10)**

   * Set up Next.js frontend with Shadcn UI components.

   * Build Supabase schema for Users, Projects, Scenes, and Dialogue Blocks.

   * Integrate block-level edit/re-generate state logic and scene navigation drawer.

3. **Phase 3: FFmpeg Worker & SaaS Billing (Days 11–18)**

   * Build Redis/Celery queue to merge dialogue `.mp3` files with video background assets using FFmpeg.

   * Integrate Stripe subscriptions and credit balance enforcement.

   * Test export pipelines for 9:16 (Shorts) and 16:9 (Full YouTube episodes).
-- MayaStudio AI - Initial Database Schema
-- Version: 1.0
-- Created: 2024-11-06

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ============================================================================
-- USER PROFILES TABLE
-- Extends Supabase auth.users with additional fields
-- ============================================================================
CREATE TABLE public.user_profiles (
  id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
  email TEXT UNIQUE NOT NULL,
  full_name TEXT,
  avatar_url TEXT,

  -- Google Drive Integration
  google_access_token TEXT,
  google_refresh_token TEXT,
  google_token_expires_at TIMESTAMPTZ,
  drive_root_folder_id TEXT,

  -- Storage & Billing
  storage_preference TEXT DEFAULT 'google_drive' CHECK (storage_preference IN ('google_drive', 'server', 'hybrid')),
  credits_balance INTEGER DEFAULT 100,
  subscription_tier TEXT DEFAULT 'free' CHECK (subscription_tier IN ('free', 'pro', 'business')),

  -- Metadata
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================================================
-- PROJECTS TABLE
-- Top-level container for video projects
-- ============================================================================
CREATE TABLE public.projects (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID NOT NULL REFERENCES public.user_profiles(id) ON DELETE CASCADE,

  -- Project Details
  title TEXT NOT NULL,
  description TEXT,
  aspect_ratio TEXT DEFAULT '9:16' CHECK (aspect_ratio IN ('9:16', '16:9')),

  -- Google Drive Integration
  drive_folder_id TEXT,

  -- Status & Metadata
  status TEXT DEFAULT 'draft' CHECK (status IN ('draft', 'in_progress', 'completed', 'archived')),
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================================================
-- SCENES TABLE
-- Individual scenes within a project
-- ============================================================================
CREATE TABLE public.scenes (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  project_id UUID NOT NULL REFERENCES public.projects(id) ON DELETE CASCADE,

  -- Scene Details
  scene_number INTEGER NOT NULL,
  heading TEXT NOT NULL,
  description TEXT,

  -- Google Drive References
  drive_folder_id TEXT,
  background_video_drive_id TEXT,
  background_video_url TEXT,
  export_drive_id TEXT,
  export_drive_link TEXT,

  -- Ordering & Status
  order_index INTEGER NOT NULL,
  status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'processing', 'completed', 'failed')),

  -- Metadata
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),

  -- Constraints
  UNIQUE(project_id, scene_number)
);

-- ============================================================================
-- VOICE PROFILES TABLE
-- Character voice profiles (designed or cloned)
-- ============================================================================
CREATE TABLE public.voice_profiles (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID NOT NULL REFERENCES public.user_profiles(id) ON DELETE CASCADE,

  -- Voice Details
  character_name TEXT NOT NULL,
  voice_id TEXT NOT NULL, -- Google Cloud TTS voice ID
  voice_type TEXT CHECK (voice_type IN ('designed', 'cloned', 'preset')),
  voice_description TEXT,

  -- Voice Settings
  gender TEXT CHECK (gender IN ('male', 'female', 'neutral')),
  age_range TEXT,
  language_code TEXT DEFAULT 'si-LK', -- Sinhala

  -- Sample Audio
  sample_audio_url TEXT,
  sample_audio_drive_id TEXT,

  -- Metadata
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================================================
-- DIALOGUE BLOCKS TABLE
-- Individual dialogue lines with audio
-- ============================================================================
CREATE TABLE public.dialogue_blocks (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  scene_id UUID NOT NULL REFERENCES public.scenes(id) ON DELETE CASCADE,

  -- Actor & Voice
  actor_name TEXT NOT NULL,
  voice_id TEXT NOT NULL, -- References voice_profiles or direct Google voice ID
  emotion_tone TEXT NOT NULL,

  -- Dialogue Content
  sinhala_text TEXT NOT NULL,
  english_translation TEXT,

  -- Audio Files
  audio_drive_id TEXT,
  audio_url TEXT,
  audio_cache_url TEXT, -- Temporary cached URL on server
  cache_expires_at TIMESTAMPTZ,

  -- Audio Metadata
  duration_seconds NUMERIC(5,2),

  -- Generation Status
  status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'generated', 'modified', 'failed')),
  error_message TEXT,

  -- Ordering
  order_index INTEGER NOT NULL,

  -- Metadata
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================================================
-- RENDER JOBS TABLE
-- Track video rendering jobs
-- ============================================================================
CREATE TABLE public.render_jobs (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  scene_id UUID NOT NULL REFERENCES public.scenes(id) ON DELETE CASCADE,
  user_id UUID NOT NULL REFERENCES public.user_profiles(id) ON DELETE CASCADE,

  -- Job Details
  job_type TEXT DEFAULT 'video_export' CHECK (job_type IN ('video_export', 'audio_generation', 'script_parsing')),
  status TEXT DEFAULT 'queued' CHECK (status IN ('queued', 'processing', 'completed', 'failed')),

  -- Progress Tracking
  progress_percentage INTEGER DEFAULT 0 CHECK (progress_percentage >= 0 AND progress_percentage <= 100),
  current_step TEXT,

  -- Results
  output_drive_id TEXT,
  output_url TEXT,
  error_message TEXT,

  -- Performance Metrics
  started_at TIMESTAMPTZ,
  completed_at TIMESTAMPTZ,
  processing_duration_seconds INTEGER,

  -- Metadata
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================================================
-- USAGE LOGS TABLE
-- Track API usage for billing
-- ============================================================================
CREATE TABLE public.usage_logs (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID NOT NULL REFERENCES public.user_profiles(id) ON DELETE CASCADE,

  -- Usage Details
  action_type TEXT NOT NULL CHECK (action_type IN ('tts_generation', 'script_parsing', 'video_render', 'voice_clone')),
  credits_used INTEGER NOT NULL,

  -- Context
  project_id UUID REFERENCES public.projects(id) ON DELETE SET NULL,
  scene_id UUID REFERENCES public.scenes(id) ON DELETE SET NULL,

  -- Metadata
  metadata JSONB, -- Additional context (e.g., character count, duration)
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================================================
-- INDEXES
-- Optimize common queries
-- ============================================================================

-- User Profiles
CREATE INDEX idx_user_profiles_email ON public.user_profiles(email);

-- Projects
CREATE INDEX idx_projects_user_id ON public.projects(user_id);
CREATE INDEX idx_projects_status ON public.projects(status);
CREATE INDEX idx_projects_created_at ON public.projects(created_at DESC);

-- Scenes
CREATE INDEX idx_scenes_project_id ON public.scenes(project_id);
CREATE INDEX idx_scenes_status ON public.scenes(status);
CREATE INDEX idx_scenes_order_index ON public.scenes(project_id, order_index);

-- Voice Profiles
CREATE INDEX idx_voice_profiles_user_id ON public.voice_profiles(user_id);
CREATE INDEX idx_voice_profiles_character_name ON public.voice_profiles(character_name);

-- Dialogue Blocks
CREATE INDEX idx_dialogue_blocks_scene_id ON public.dialogue_blocks(scene_id);
CREATE INDEX idx_dialogue_blocks_status ON public.dialogue_blocks(status);
CREATE INDEX idx_dialogue_blocks_order_index ON public.dialogue_blocks(scene_id, order_index);

-- Render Jobs
CREATE INDEX idx_render_jobs_user_id ON public.render_jobs(user_id);
CREATE INDEX idx_render_jobs_scene_id ON public.render_jobs(scene_id);
CREATE INDEX idx_render_jobs_status ON public.render_jobs(status);
CREATE INDEX idx_render_jobs_created_at ON public.render_jobs(created_at DESC);

-- Usage Logs
CREATE INDEX idx_usage_logs_user_id ON public.usage_logs(user_id);
CREATE INDEX idx_usage_logs_created_at ON public.usage_logs(created_at DESC);

-- ============================================================================
-- ROW LEVEL SECURITY (RLS)
-- Enable RLS on all tables
-- ============================================================================

ALTER TABLE public.user_profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.projects ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.scenes ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.voice_profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.dialogue_blocks ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.render_jobs ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.usage_logs ENABLE ROW LEVEL SECURITY;

-- ============================================================================
-- RLS POLICIES - USER PROFILES
-- ============================================================================

CREATE POLICY "Users can view own profile"
  ON public.user_profiles FOR SELECT
  USING (auth.uid() = id);

CREATE POLICY "Users can update own profile"
  ON public.user_profiles FOR UPDATE
  USING (auth.uid() = id);

CREATE POLICY "Users can insert own profile"
  ON public.user_profiles FOR INSERT
  WITH CHECK (auth.uid() = id);

-- ============================================================================
-- RLS POLICIES - PROJECTS
-- ============================================================================

CREATE POLICY "Users can view own projects"
  ON public.projects FOR SELECT
  USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own projects"
  ON public.projects FOR INSERT
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own projects"
  ON public.projects FOR UPDATE
  USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own projects"
  ON public.projects FOR DELETE
  USING (auth.uid() = user_id);

-- ============================================================================
-- RLS POLICIES - SCENES
-- ============================================================================

CREATE POLICY "Users can view own scenes"
  ON public.scenes FOR SELECT
  USING (
    EXISTS (
      SELECT 1 FROM public.projects
      WHERE projects.id = scenes.project_id
      AND projects.user_id = auth.uid()
    )
  );

CREATE POLICY "Users can insert own scenes"
  ON public.scenes FOR INSERT
  WITH CHECK (
    EXISTS (
      SELECT 1 FROM public.projects
      WHERE projects.id = scenes.project_id
      AND projects.user_id = auth.uid()
    )
  );

CREATE POLICY "Users can update own scenes"
  ON public.scenes FOR UPDATE
  USING (
    EXISTS (
      SELECT 1 FROM public.projects
      WHERE projects.id = scenes.project_id
      AND projects.user_id = auth.uid()
    )
  );

CREATE POLICY "Users can delete own scenes"
  ON public.scenes FOR DELETE
  USING (
    EXISTS (
      SELECT 1 FROM public.projects
      WHERE projects.id = scenes.project_id
      AND projects.user_id = auth.uid()
    )
  );

-- ============================================================================
-- RLS POLICIES - VOICE PROFILES
-- ============================================================================

CREATE POLICY "Users can view own voice profiles"
  ON public.voice_profiles FOR SELECT
  USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own voice profiles"
  ON public.voice_profiles FOR INSERT
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own voice profiles"
  ON public.voice_profiles FOR UPDATE
  USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own voice profiles"
  ON public.voice_profiles FOR DELETE
  USING (auth.uid() = user_id);

-- ============================================================================
-- RLS POLICIES - DIALOGUE BLOCKS
-- ============================================================================

CREATE POLICY "Users can view own dialogue blocks"
  ON public.dialogue_blocks FOR SELECT
  USING (
    EXISTS (
      SELECT 1 FROM public.scenes
      JOIN public.projects ON projects.id = scenes.project_id
      WHERE scenes.id = dialogue_blocks.scene_id
      AND projects.user_id = auth.uid()
    )
  );

CREATE POLICY "Users can insert own dialogue blocks"
  ON public.dialogue_blocks FOR INSERT
  WITH CHECK (
    EXISTS (
      SELECT 1 FROM public.scenes
      JOIN public.projects ON projects.id = scenes.project_id
      WHERE scenes.id = dialogue_blocks.scene_id
      AND projects.user_id = auth.uid()
    )
  );

CREATE POLICY "Users can update own dialogue blocks"
  ON public.dialogue_blocks FOR UPDATE
  USING (
    EXISTS (
      SELECT 1 FROM public.scenes
      JOIN public.projects ON projects.id = scenes.project_id
      WHERE scenes.id = dialogue_blocks.scene_id
      AND projects.user_id = auth.uid()
    )
  );

CREATE POLICY "Users can delete own dialogue blocks"
  ON public.dialogue_blocks FOR DELETE
  USING (
    EXISTS (
      SELECT 1 FROM public.scenes
      JOIN public.projects ON projects.id = scenes.project_id
      WHERE scenes.id = dialogue_blocks.scene_id
      AND projects.user_id = auth.uid()
    )
  );

-- ============================================================================
-- RLS POLICIES - RENDER JOBS
-- ============================================================================

CREATE POLICY "Users can view own render jobs"
  ON public.render_jobs FOR SELECT
  USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own render jobs"
  ON public.render_jobs FOR INSERT
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own render jobs"
  ON public.render_jobs FOR UPDATE
  USING (auth.uid() = user_id);

-- ============================================================================
-- RLS POLICIES - USAGE LOGS
-- ============================================================================

CREATE POLICY "Users can view own usage logs"
  ON public.usage_logs FOR SELECT
  USING (auth.uid() = user_id);

CREATE POLICY "System can insert usage logs"
  ON public.usage_logs FOR INSERT
  WITH CHECK (true); -- Backend service role can insert

-- ============================================================================
-- FUNCTIONS & TRIGGERS
-- Auto-update updated_at timestamp
-- ============================================================================

CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Apply trigger to all tables with updated_at
CREATE TRIGGER update_user_profiles_updated_at BEFORE UPDATE ON public.user_profiles
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_projects_updated_at BEFORE UPDATE ON public.projects
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_scenes_updated_at BEFORE UPDATE ON public.scenes
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_voice_profiles_updated_at BEFORE UPDATE ON public.voice_profiles
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_dialogue_blocks_updated_at BEFORE UPDATE ON public.dialogue_blocks
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_render_jobs_updated_at BEFORE UPDATE ON public.render_jobs
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ============================================================================
-- INITIAL DATA (Optional)
-- ============================================================================

-- You can add seed data here if needed
-- Example: INSERT INTO public.voice_profiles (character_name, voice_id, ...) VALUES (...);

-- ============================================================================
-- COMMENTS
-- Document tables and columns
-- ============================================================================

COMMENT ON TABLE public.user_profiles IS 'User profile information extending Supabase auth.users';
COMMENT ON TABLE public.projects IS 'Top-level container for video projects';
COMMENT ON TABLE public.scenes IS 'Individual scenes within a project';
COMMENT ON TABLE public.voice_profiles IS 'Character voice profiles for TTS';
COMMENT ON TABLE public.dialogue_blocks IS 'Individual dialogue lines with audio';
COMMENT ON TABLE public.render_jobs IS 'Video rendering job queue and status';
COMMENT ON TABLE public.usage_logs IS 'API usage tracking for billing';

-- End of migration

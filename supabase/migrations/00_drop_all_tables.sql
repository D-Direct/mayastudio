-- Drop All Existing Tables
-- Run this FIRST if you need to reset the database

-- Drop all tables in the correct order (respecting foreign key dependencies)
DROP TABLE IF EXISTS public.usage_logs CASCADE;
DROP TABLE IF EXISTS public.render_jobs CASCADE;
DROP TABLE IF EXISTS public.dialogue_blocks CASCADE;
DROP TABLE IF EXISTS public.voice_profiles CASCADE;
DROP TABLE IF EXISTS public.scenes CASCADE;
DROP TABLE IF EXISTS public.projects CASCADE;
DROP TABLE IF EXISTS public.user_profiles CASCADE;

-- Drop the update trigger function if it exists
DROP FUNCTION IF EXISTS update_updated_at_column() CASCADE;

-- Success message
SELECT 'All tables dropped successfully!' as message;

# How to Get Supabase Connection String

## Method 1: From Project Settings → Database

1. **Click the gear icon (⚙️)** at the bottom left sidebar
2. You'll see "Project Settings"
3. Click **"Database"** in the left menu (under CONFIGURATION)
4. Scroll down to **"Connection String"** section
5. You'll see different formats:
   - **URI** - This is what you need! `postgresql://postgres:[YOUR-PASSWORD]@db.xxxxx.supabase.co:5432/postgres`
   - Connection pooling
   - Direct connection

## Method 2: From Project Settings → API

1. Click the gear icon (⚙️) at the bottom left
2. Click **"API"** in the left menu
3. Copy these values:

### Project URL
```
https://xxxxx.supabase.co
```

### API Keys
- **anon/public key**: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...` (for frontend)
- **service_role key**: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...` (for backend - keep secret!)

## What You Need for MayaStudio:

### For Backend (Railway):

```bash
# Database connection string
DATABASE_URL=postgresql://postgres:[YOUR-PASSWORD]@db.xxxxx.supabase.co:5432/postgres

# Supabase credentials
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_SERVICE_KEY=eyJhbGc... (service_role key - NOT anon key!)
```

### For Frontend (Vercel):

```bash
# Supabase credentials
NEXT_PUBLIC_SUPABASE_URL=https://xxxxx.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJhbGc... (anon/public key)
```

## Quick Navigation in Supabase Dashboard:

```
Bottom Left Sidebar Icons:
├── 🏠 Home
├── 📊 Table Editor
├── 🔐 Authentication
├── 📦 Storage
├── 📡 Database
├── 🔧 SQL Editor
├── 📈 Logs
└── ⚙️  Project Settings  ← Click here!
    ├── General
    ├── Database          ← Connection string here!
    ├── API              ← API keys here!
    └── Billing
```

## Copy This Template:

Once you have your credentials, save them:

```
Project URL:          https://owhuxnwypxilsdqjdn.supabase.co
Anon Key:            eyJ_____
Service Role Key:    eyJ_____ (different from anon)
Database Password:   [The password you created when making the project]
Database URL:        postgresql://postgres:[PASSWORD]@db.owhuxnwypxilsdqjdn.supabase.co:5432/postgres
```

## 🔍 Can't Find It?

If you're still having trouble:

1. Make sure you're in the **MayaStudio** project (check top of page)
2. The database password is the one you created when setting up the project
3. If you forgot it, you can reset it from Settings → Database → "Reset database password"

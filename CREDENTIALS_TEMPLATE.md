# MayaStudio AI - Credentials Tracker

Use this template to track all your credentials. **Keep this file private!**

⚠️ **This file is in .gitignore** - it won't be committed to Git.

---

## 📋 Supabase

**Project Name:** mayastudio-dev

```
Project URL:          https://_____.supabase.co
Anon Key:            eyJ_____
Service Role Key:    eyJ_____ (DIFFERENT from anon - keep secret!)
Database Password:   _____
Database URL:        postgresql://postgres:_____@db._____.supabase.co:5432/postgres
```

**Dashboard:** https://supabase.com/dashboard/project/_____

---

## 🔐 Google Cloud Platform

**Project Name:** MayaStudio Dev
**Project ID:** mayastudio-dev-_____

### OAuth 2.0 Client

```
Client ID:           _____.apps.googleusercontent.com
Client Secret:       GOCSPX-_____
```

### API Key (Gemini)

```
API Key:             AIzaSy_____
```

### Service Account

```
Email:               mayastudio-backend@_____.iam.gserviceaccount.com
JSON File Location:  /path/to/credentials.json
```

**Console:** https://console.cloud.google.com

---

## 🚂 Railway

**Project Name:** MayaStudio Backend

### Services

```
API Service URL:     https://mayastudio-api-production.up.railway.app
Worker Service:      (no public URL)
Redis URL:           redis://default:_____@redis.railway.internal:6379
```

**Dashboard:** https://railway.app/project/_____

---

## ▲ Vercel

**Project Name:** mayastudio

```
Frontend URL:        https://mayastudio.vercel.app
Alternative URLs:    https://mayastudio-_____.vercel.app
```

**Dashboard:** https://vercel.com/___/mayastudio

---

## 🔗 Complete Environment Variables

### Backend (.env for Railway)

```bash
# Database
DATABASE_URL=postgresql://postgres:_____@db._____.supabase.co:5432/postgres

# Redis
REDIS_URL=redis://default:_____@redis.railway.internal:6379

# Google OAuth
GOOGLE_CLIENT_ID=_____.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=GOCSPX-_____

# Google AI
GEMINI_API_KEY=AIzaSy_____

# Google Service Account (paste entire JSON as one line)
GOOGLE_APPLICATION_CREDENTIALS_JSON={"type":"service_account",...}

# Supabase
SUPABASE_URL=https://_____.supabase.co
SUPABASE_SERVICE_KEY=eyJ_____

# App Config
FRONTEND_URL=https://mayastudio.vercel.app
ENVIRONMENT=production

# Celery
CELERY_BROKER_URL=redis://default:_____@redis.railway.internal:6379
CELERY_RESULT_BACKEND=redis://default:_____@redis.railway.internal:6379
```

### Frontend (.env.local for Vercel)

```bash
NEXT_PUBLIC_SUPABASE_URL=https://_____.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJ_____
NEXT_PUBLIC_API_URL=https://mayastudio-api-production.up.railway.app
NEXT_PUBLIC_GOOGLE_CLIENT_ID=_____.apps.googleusercontent.com
NEXT_PUBLIC_APP_URL=https://mayastudio.vercel.app
```

---

## 📅 Important Dates

```
Supabase Created:     _____
Google Cloud Created: _____
Railway Connected:    _____
Vercel Connected:     _____
First Deployment:     _____
```

---

## 💰 Billing Information

### Google Cloud Budget

```
Budget Amount:        $20/month
Alert Thresholds:     50%, 90%, 100%
Billing Email:        _____
```

### Railway

```
Monthly Credit:       $5
Current Usage:        $_____
Days Remaining:       ___
```

### Vercel

```
Bandwidth Used:       ___ GB / 100 GB
Plan:                 Hobby (Free)
```

### Supabase

```
Database Size:        ___ MB / 500 MB
Storage Used:         ___ MB / 1 GB
Plan:                 Free
```

---

## 🔒 Security Notes

- [ ] Service role key is only in Railway (never in frontend)
- [ ] All secrets stored in environment variables (not in code)
- [ ] .env files are in .gitignore
- [ ] Service account JSON not committed to Git
- [ ] Google OAuth configured with correct redirect URLs
- [ ] Supabase RLS policies enabled

---

## 📞 Support Contacts

**Supabase Support:** https://supabase.com/dashboard/support
**Google Cloud Support:** https://console.cloud.google.com/support
**Railway Support:** https://railway.app/help
**Vercel Support:** https://vercel.com/help

---

**Last Updated:** _____
**Next Review:** _____

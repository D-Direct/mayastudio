# MayaStudio AI - Free Tier Limits & Optimization Guide

## 📊 Free Tier Summary

| Service | Free Tier Limits | Estimated Usage | Status |
|---------|------------------|-----------------|--------|
| **Vercel** | 100GB bandwidth/mo | ~10-20GB (MVP) | ✅ Safe |
| **Railway** | $5 credit/mo (~500hrs) | ~$0.50-2/mo | ✅ Safe |
| **Supabase** | 500MB DB, 1GB storage | ~50-100MB DB | ✅ Safe |
| **Google Drive** | 15GB per user | User-paid | ✅ Free |
| **Google Cloud** | Pay-per-use | ~$5-20/mo | ⚠️ Monitor |

**Total Cost: $5-20/month** (mostly Google API usage)

---

## 🎯 Vercel Free Tier

### Limits
```yaml
Bandwidth: 100 GB/month
Build Time: 6000 minutes/month
Serverless Functions:
  - Execution: 100 GB-hours/month
  - Duration: 10 seconds max
  - Size: 50 MB max
Edge Functions: 100,000 requests/month
Deployments: Unlimited
Domains: 1 production domain
Team Members: 1 (Hobby tier)
```

### Optimization Tips

#### 1. Reduce Bandwidth Usage
```javascript
// Use Next.js Image optimization
import Image from 'next/image'

<Image
  src="/thumbnail.jpg"
  width={300}
  height={200}
  quality={75}  // Lower quality = smaller size
  loading="lazy"
/>
```

#### 2. Static Generation
```javascript
// Use Static Site Generation (SSG) where possible
export async function generateStaticParams() {
  // Generate static pages at build time
}
```

#### 3. Edge Caching
```javascript
// Add cache headers
export const revalidate = 3600 // Cache for 1 hour
```

#### 4. Avoid Heavy API Routes
```javascript
// DON'T do this in Vercel API routes (use Railway instead):
export async function POST(request) {
  // ❌ Heavy video processing
  // ❌ Long-running tasks
  // ❌ Large file uploads
}

// DO this instead:
export async function POST(request) {
  // ✅ Forward to Railway backend
  const response = await fetch(RAILWAY_API_URL, {...})
  return response
}
```

### Monitoring
- Dashboard: https://vercel.com/dashboard/usage
- Set up alerts when approaching 80GB bandwidth
- Check bandwidth usage weekly

---

## 🚂 Railway Free Tier

### Limits
```yaml
Monthly Credit: $5
CPU: Shared vCPU
RAM: 512MB per service
Disk: 1GB per service
Uptime: ~500 hours/month (with $5 credit)
Services: Multiple allowed
Concurrent Builds: 1
```

### Cost Calculation
```
Cost = (vCPU × $0.000463/hr) + (RAM GB × $0.000231/hr)

Example (our setup):
- API: 0.5 vCPU, 512MB RAM = $0.00035/hr
- Redis: 0.1 vCPU, 256MB RAM = $0.00010/hr
- Worker: 0.5 vCPU, 512MB RAM = $0.00035/hr

Total: $0.0008/hr × 730 hrs = ~$0.58/month
```

**✅ You have $4.42 headroom!**

### Optimization Tips

#### 1. Use Railway's Sleep Feature
```yaml
# railway.toml (if available)
[deploy]
sleepAfter = "5m"  # Sleep after 5 minutes of inactivity
```

Services auto-wake on new requests.

#### 2. Combine Services (If Needed)
```python
# Run FastAPI + Celery in same container for development
# Only separate when scaling needed

# Dockerfile
CMD ["sh", "-c", "celery -A app.worker worker --detach && uvicorn app.main:app"]
```

#### 3. Optimize Worker Usage
```python
# Only run workers when needed
# Use task routing to prioritize critical tasks

@celery_app.task(priority=5)  # Higher priority
def generate_audio(block_id):
    pass

@celery_app.task(priority=1)  # Lower priority
def cleanup_old_files():
    pass
```

#### 4. Use Redis Efficiently
```python
# Set expiration on cached data
redis_client.setex('audio:123', 86400, audio_data)  # 24hr expiry

# Clean up old keys regularly
redis_client.delete(*old_keys)
```

### Monitoring
- Dashboard: https://railway.app/project/usage
- Check daily usage
- Set up email alerts at $4/month threshold
- Review service logs for memory leaks

---

## 🗄️ Supabase Free Tier

### Limits
```yaml
Database:
  - Size: 500 MB
  - Connections: Direct connections unlimited
  - Rows: Unlimited (within 500MB)

Storage:
  - Size: 1 GB
  - Bandwidth: 2 GB/month
  - File uploads: 50 MB max per file

Auth:
  - Users: 50,000 MAU (Monthly Active Users)

API Requests: Unlimited
Edge Functions: 500,000 invocations/month
Realtime: 200 concurrent connections

Pauses: After 1 week inactivity (dev projects only)
```

### Database Size Optimization

#### 1. Store Minimal Data
```sql
-- ✅ DO: Store only metadata
CREATE TABLE dialogue_blocks (
  id UUID PRIMARY KEY,
  sinhala_text TEXT,
  audio_drive_id TEXT,  -- ✅ ID only, file in Google Drive
  duration_seconds NUMERIC(5,2)
);

-- ❌ DON'T: Store large binary data
CREATE TABLE dialogue_blocks (
  audio_file BYTEA  -- ❌ This fills up DB quickly
);
```

#### 2. Use Cascading Deletes
```sql
-- Automatically clean up related data
ON DELETE CASCADE
```

#### 3. Regular Cleanup
```sql
-- Delete old processed temp files
DELETE FROM temp_files
WHERE created_at < NOW() - INTERVAL '24 hours';
```

#### 4. Archive Old Projects
```python
# Move old projects to Google Drive JSON backups
def archive_project(project_id):
    project_data = get_full_project(project_id)
    drive.upload_json(f'archives/{project_id}.json', project_data)
    delete_project(project_id)
```

### Storage Size Optimization

**Strategy: Use Google Drive for 99% of files**

```python
# Supabase Storage: Only for app-level assets
- User avatars (< 1MB each)
- Thumbnails (< 100KB each)
- Temp processing files (deleted after 24hr)

# Google Drive: User's media
- Source videos
- Generated audio
- Final exports
```

### Monitoring
- Dashboard: https://app.supabase.com/project/_/reports
- Check database size weekly
- Monitor storage usage
- Set up Supabase email alerts

---

## ☁️ Google Cloud Free Tier

### Always Free Tier
```yaml
Cloud Text-to-Speech:
  - Standard voices: 0-4 million characters/month FREE
  - WaveNet voices: 0-1 million characters FREE
  - Neural2 voices: 0-1 million characters FREE

Generative AI (Gemini):
  - Free tier: 60 requests/minute
  - Paid tier: Pay-per-use (~$0.00025/1K chars)

Cloud Storage: 5 GB/month (if not using Drive)

Google Drive API: Free (unlimited calls)
```

### Cost Estimation

#### Text-to-Speech Usage
```
Average dialogue: 50 characters
Scenes per project: 10 scenes × 15 lines = 150 lines
Characters per project: 150 × 50 = 7,500 characters

Projects per month: 10-20
Total characters: 75,000 - 150,000 characters

Cost: $0 (within free tier of 4 million!)
```

#### Gemini API Usage
```
Script parsing: ~2,000 characters per scene
Cost: $0.00025/1K chars × 2K = $0.0005 per scene
Monthly (20 scenes): 20 × $0.0005 = $0.01

Tone analysis: ~500 chars per request
Cost: Negligible

Monthly estimate: < $1
```

### Optimization Tips

#### 1. Cache TTS Results
```python
# Don't regenerate same text
def get_audio(text, voice_id):
    cache_key = f"tts:{hash(text)}:{voice_id}"

    # Check cache first
    cached = redis.get(cache_key)
    if cached:
        return cached

    # Generate new
    audio = tts_api.synthesize(text, voice_id)
    redis.setex(cache_key, 86400, audio)  # 24hr cache
    return audio
```

#### 2. Batch Gemini Requests
```python
# Process multiple scenes in one request
def parse_full_script(script_text):
    # Parse entire script at once instead of scene-by-scene
    response = gemini.generate_content(f"""
        Parse this full screenplay into JSON:
        {script_text}
    """)
    return response
```

#### 3. Use Cheaper Models When Possible
```python
# For simple tasks, use cheaper models
def simple_validation(text):
    # Use gemini-1.5-flash (cheaper) instead of gemini-1.5-pro
    model = genai.GenerativeModel('gemini-1.5-flash')
    return model.generate_content(text)
```

#### 4. Set Budget Alerts
```bash
# In Google Cloud Console:
Billing → Budgets & Alerts → Create Budget
- Amount: $20/month
- Email alerts at 50%, 90%, 100%
```

### Monitoring
- Console: https://console.cloud.google.com/billing
- Enable billing reports
- Set up budget alerts
- Review API usage weekly

---

## 💾 Google Drive (User Storage)

### Per-User Limits
```yaml
Free Gmail Account: 15 GB (shared with Gmail, Photos)
Google Workspace: Unlimited (with 5+ users) or 30GB-5TB
Google One (Paid): 100GB ($1.99/mo), 200GB ($2.99/mo), 2TB ($9.99/mo)
```

### API Quotas
```yaml
Queries: 20,000/day per project
Uploads/Downloads: Unlimited (bandwidth throttled)
Files per folder: 500,000+
Max file size: 5 TB
```

### Optimization

#### 1. Compress Files
```python
# Compress audio before upload
import pydub
audio = pydub.AudioSegment.from_file('input.wav')
audio.export('output.mp3', format='mp3', bitrate='128k')  # Smaller
```

#### 2. Delete Temp Files
```python
# Clean up processing artifacts
def cleanup_after_export(scene_id):
    temp_files = drive.list_files(folder_id, pattern='temp_*')
    for file in temp_files:
        drive.delete(file.id)
```

#### 3. Shared Team Drives (Future)
```python
# For team collaboration (Google Workspace)
drive.create_shared_drive('MayaStudio Projects')
```

---

## 🚨 Warning Signs & Limits

### When to Upgrade

**Vercel → Pro ($20/mo)**
- Bandwidth > 80GB/month consistently
- Need team collaboration
- Custom domains > 1

**Railway → Pay-as-you-go**
- Monthly cost > $4
- Services need more RAM (>512MB)
- Need faster CPUs

**Supabase → Pro ($25/mo)**
- Database > 400MB
- Storage > 800MB
- Need daily backups
- Pausing becomes annoying

**Google Cloud → Set Budget**
- TTS > 3 million chars/month
- Gemini usage > $10/month

---

## 📈 Growth Plan

### MVP (0-10 users) - FREE
- Everything on free tiers
- **Cost: $5-10/month**

### Beta (10-100 users) - HYBRID
- Railway: Pay-as-you-go (~$15/mo)
- Vercel: Stay on free tier
- Supabase: Upgrade to Pro ($25/mo)
- **Cost: $45-60/month**

### Launch (100-1000 users) - PAID
- Railway: ~$50/mo (or migrate to Hetzner VPS)
- Vercel: Pro ($20/mo)
- Supabase: Pro ($25/mo) + extra storage
- Google Cloud: ~$50-100/mo
- **Cost: $145-200/month**

### Scale (1000+ users) - OPTIMIZED
- Migrate to VPS ($50/mo) or AWS/GCP with autoscaling
- CDN for media delivery
- Caching layer (Cloudflare R2)
- **Cost: $200-500/month**

---

## 🛠️ Monitoring Tools

### Set Up Alerts

**Email Alerts:**
```yaml
Vercel: 80GB bandwidth → Warning email
Railway: $4 usage → Warning email
Supabase: 400MB DB → Warning email
Google Cloud: $15 spend → Warning email
```

**Weekly Reviews:**
```bash
Monday morning:
1. Check Railway usage dashboard
2. Check Vercel analytics
3. Review Supabase database size
4. Review Google Cloud billing
5. Adjust if needed
```

### Simple Monitoring Script

```python
# monitor.py - Run weekly
import requests

def check_limits():
    # Railway
    railway_usage = get_railway_usage()
    if railway_usage > 4:
        send_alert("Railway usage high: $" + str(railway_usage))

    # Supabase
    db_size = get_supabase_db_size()
    if db_size > 400:
        send_alert("Database size: " + str(db_size) + "MB")

    # Google Cloud
    gcp_cost = get_gcp_cost_this_month()
    if gcp_cost > 15:
        send_alert("Google Cloud cost: $" + str(gcp_cost))

check_limits()
```

---

## ✅ Best Practices

1. **Start Small**: Use free tiers fully before upgrading
2. **Monitor Weekly**: Check all dashboards every Monday
3. **Optimize First**: Before upgrading, optimize code/queries
4. **Cache Aggressively**: Reduce API calls with smart caching
5. **Clean Regularly**: Delete old temp files, unused data
6. **User Storage**: Leverage Google Drive for 99% of files
7. **Set Alerts**: Know when you're approaching limits
8. **Plan Ahead**: Know your upgrade path before hitting limits

---

**Last Updated:** 2024-11-06
**Review Quarterly:** Update limits as providers change terms

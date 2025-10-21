# Complete Free Deployment Guide - Consolidated

**Date**: October 21, 2025
**Last Updated**: October 21, 2025

This is a **complete, consolidated guide** covering everything you need to deploy VibePoint **100% free without AWS**.

---

## 📋 Table of Contents

1. [Quick Summary](#quick-summary)
2. [What You're Replacing](#what-youre-replacing)
3. [Verified Free Tier Limits](#verified-free-tier-limits)
4. [Recommended Setup](#recommended-setup)
5. [Step-by-Step Setup](#step-by-step-setup)
6. [Variable Naming](#variable-naming)
7. [Code Changes](#code-changes)
8. [AI Service Options](#ai-service-options)
9. [Storage Without S3/boto3](#storage-without-s3boto3)
10. [Cost Comparison](#cost-comparison)
11. [Troubleshooting](#troubleshooting)
12. [Next Steps](#next-steps)

---

## Quick Summary

### Your Friend's Setup (Requires AWS)
```
Storage: AWS S3 → ~$2-9/month + AWS account
AI: OpenAI GPT-4 → ~$100-300/month
Backend: AWS EC2 → ~$5-50/month + AWS account
Frontend: AWS Amplify → ~$0-20/month + AWS account
Video: TwelveLabs Paid → Varies

Total: $107-379/month + AWS account required
```

### Your Setup (NO AWS Required)
```
Storage: Backblaze B2 or Cloudflare R2 → FREE (10 GB)
AI: Google Gemini or Groq → FREE (1,500 req/day or rate-limited)
Backend: Render → FREE (750 hrs/month)
Frontend: Vercel → FREE (100 GB bandwidth)
Video: TwelveLabs Free → FREE (10 hours indexing)

Total: $0/month + NO AWS account needed
```

**Savings: $107-379/month + no AWS complexity!**

---

## What You're Replacing

| Component | Friend's AWS | Your Free Alternative | AWS Account? |
|-----------|--------------|----------------------|--------------|
| **Video Storage** | AWS S3 | Backblaze B2 (10 GB) | ❌ NO |
| **AI Matching** | OpenAI GPT-4 | Google Gemini (1,500/day) | ❌ NO |
| **Backend Hosting** | AWS EC2/Lambda | Render (750 hrs/month) | ❌ NO |
| **Frontend Hosting** | AWS Amplify | Vercel (unlimited projects) | ❌ NO |
| **Video Analysis** | TwelveLabs Paid | TwelveLabs Free (10 hrs) | ❌ NO |

**Code changes needed**: ~10-15 lines total
**Setup time**: 30-60 minutes
**AWS accounts**: 0

---

## Verified Free Tier Limits

**Last Verified**: October 21, 2025 (triple-checked from official sources)

### Storage Options

| Service | Free Storage | Downloads | boto3? | AWS Account? | Verified |
|---------|--------------|-----------|--------|--------------|----------|
| **Backblaze B2** ⭐ | **10 GB** | 1 GB/day | ❌ NO | ❌ NO | ✅ YES |
| **Cloudflare R2** ⭐ | **10 GB** | Unlimited | ✅ YES | ❌ NO | ✅ YES |
| Supabase | 1 GB | Unlimited | ❌ NO | ❌ NO | ✅ YES |
| ~~Firebase~~ | ~~1 GB~~ | ~~10 GB/mo~~ | ❌ NO | ❌ NO | ⚠️ Requires paid plan |

**Recommendation**:
- **Backblaze B2** if you want NO boto3 (10 GB free)
- **Cloudflare R2** if boto3 is OK (10 GB free, unlimited egress)

### AI Services

| Service | Daily Limit | Cost | AWS Account? | Verified |
|---------|-------------|------|--------------|----------|
| **Google Gemini** ⭐ | **1,500 req/day** | FREE | ❌ NO | ✅ YES |
| Groq | Rate limited (undisclosed) | FREE | ❌ NO | ✅ YES |
| Hugging Face API | Few hundred/hour | FREE | ❌ NO | ⚠️ Vague |
| OpenAI | $5 credit only | Trial | ❌ NO | ✅ YES |

**Recommendation**: **Google Gemini** (1,500 requests/day is generous)

**Important Corrections**:
- ❌ Groq is NOT unlimited (has rate limits)
- ❌ Gemini is NOT 1M tokens/day (it's 1,500 requests/day)
- ✅ Both are still excellent free options

### Hosting

| Service | Free Tier | AWS Account? | Verified |
|---------|-----------|--------------|----------|
| **Render** ⭐ | 750 hrs/month, 512 MB RAM | ❌ NO | ✅ YES |
| **Vercel** ⭐ | 100 GB bandwidth, unlimited projects | ❌ NO | ✅ YES |

**Limitations**:
- Render: Sleeps after 15 min inactivity (30s cold start)
- Vercel: Non-commercial use only on free tier

### Video Analysis

| Service | Free Tier | AWS Account? | Verified |
|---------|-----------|--------------|----------|
| **TwelveLabs** | 10 hours indexing, 90-day expiry | ❌ NO | ✅ YES |

**Daily API Limits** (free tier):
- Search: 50 calls/day
- Summarize: 50 calls/day
- Generate: 50 calls/day
- Embed: 100 calls/day

---

## Recommended Setup

### Best Setup (No boto3, Maximum Clarity)

```
Storage:   Backblaze B2
           - Sign up: backblaze.com
           - Free: 10 GB storage
           - No boto3 needed
           - No AWS account

AI:        Google Gemini
           - Sign up: aistudio.google.com
           - Free: 1,500 requests/day
           - No AWS account

Backend:   Render
           - Sign up: render.com
           - Free: 750 hrs/month
           - No AWS account

Frontend:  Vercel
           - Sign up: vercel.com
           - Free: 100 GB bandwidth
           - No AWS account

Video:     TwelveLabs
           - Sign up: twelvelabs.io
           - Free: 10 hours indexing
           - No AWS account

Total: $0/month
AWS Accounts: 0
Storage: 10 GB (enough for 20-100 videos)
```

### Alternative Setup (With boto3, Maximum Storage Egress)

```
Storage:   Cloudflare R2
           - Sign up: cloudflare.com
           - Free: 10 GB storage, unlimited egress
           - Uses boto3 (but NOT AWS!)
           - No AWS account

(Rest same as above)
```

---

## Step-by-Step Setup

### Phase 1: Create Free Accounts (20 min)

**Storage - Choose ONE**:

**Option A: Backblaze B2** (No boto3)
1. Go to https://www.backblaze.com/b2/sign-up.html
2. Create account (email + password, NO credit card)
3. Go to "B2 Cloud Storage"
4. Create bucket: "vibepoint-videos"
5. Go to "App Keys" > "Add a New Application Key"
6. Save credentials:
   - Application Key ID
   - Application Key
   - Bucket Name

**Option B: Cloudflare R2** (Uses boto3)
1. Go to https://dash.cloudflare.com/sign-up
2. Create account (email + password, NO credit card)
3. Go to "R2 Object Storage"
4. Create bucket: "vibepoint-videos"
5. Go to "Manage R2 API Tokens" > "Create API Token"
6. Save credentials:
   - Access Key ID
   - Secret Access Key
   - Endpoint URL (e.g., https://abc123.r2.cloudflarestorage.com)

---

**AI Service - Choose ONE**:

**Option A: Google Gemini** (Recommended)
1. Go to https://aistudio.google.com
2. Sign in with Google account
3. Click "Get API key"
4. Create new project (if needed)
5. Copy API key

**Option B: Groq**
1. Go to https://console.groq.com
2. Sign up (email + password)
3. Go to "API Keys"
4. Create new key
5. Copy API key

---

**Backend Hosting**:

1. Go to https://dashboard.render.com/register
2. Sign up with GitHub (recommended) or email
3. Connect GitHub repository
4. **Don't create service yet** (we'll do this after code changes)

---

**Frontend Hosting**:

1. Go to https://vercel.com/signup
2. Sign up with GitHub (recommended)
3. **Don't deploy yet** (we'll do this after code changes)

---

**Video Analysis**:

1. Go to https://twelvelabs.io
2. Sign up (email + password)
3. Create new project
4. Go to "API Keys" > Create key
5. Go to "Indexes" > Create two indexes:
   - Name: "creators" (for creator videos)
   - Name: "ads" (for advertisements)
6. Save:
   - API Key
   - Creators Index ID
   - Ads Index ID

---

### Phase 2: Update Code (15 min)

#### Option 1: Better Variable Names (Recommended)

This avoids the confusing "AWS" prefix when you're NOT using AWS.

**Step 1: Update config.py**

File: `amber_aim/src/aim/config.py`

```python
"""Application configuration management."""

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    """Application settings loaded from environment variables.

    All settings are prefixed with APP_ in environment variables.
    """

    # Storage configuration (clear naming, NO AWS prefix)
    storage_bucket_name: str
    storage_region: str = "auto"
    storage_access_key_id: str
    storage_secret_access_key: str
    storage_endpoint_url: str | None = None

    # Upload settings
    upload_url_expiration: int = 1800
    s3_base_path: str = "upload"

    # Logging
    log_level: str = "INFO"

    # TwelveLabs configuration
    twelve_labs_api_key: str
    twelve_labs_creators_index_id: str
    twelve_labs_ads_index_id: str

    # AI configuration
    ai_api_key: str
    ai_base_url: str | None = None
    ai_model: str = "gemini-2.0-flash-exp"

    class Config:
        """Pydantic settings configuration."""

        env_file = ".env"
        env_prefix = "APP_"
        extra = "ignore"
```

**Step 2: Update storage service**

File: `amber_aim/src/aim/services/s3_service.py`

```python
"""Storage service using boto3 for S3-compatible storage."""

import uuid
from datetime import datetime, timedelta
from typing import Any

import boto3
from botocore.config import Config

from aim.config import Settings


class S3Service:
    """Service for generating presigned upload URLs for S3-compatible storage.

    Works with Cloudflare R2, Backblaze B2 (S3-compatible mode), AWS S3, etc.
    """

    def __init__(self, settings: Settings):
        """Initialize S3 service with explicit credentials."""
        self.s3_client = boto3.client(
            "s3",
            region_name=settings.storage_region,
            endpoint_url=settings.storage_endpoint_url,
            aws_access_key_id=settings.storage_access_key_id,
            aws_secret_access_key=settings.storage_secret_access_key,
            config=Config(signature_version="s3v4"),
        )
        self.bucket = settings.storage_bucket_name
        self.base_path = settings.s3_base_path
        self.expiration = settings.upload_url_expiration

    def generate_presigned_upload_url(
        self, filename: str
    ) -> dict[str, Any]:
        """Generate presigned URL for uploading a file."""
        # Generate unique filename
        file_ext = filename.split(".")[-1] if "." in filename else ""
        unique_filename = f"{uuid.uuid4()}.{file_ext}" if file_ext else str(uuid.uuid4())
        s3_key = f"{self.base_path}/{unique_filename}"

        # Generate presigned URL
        upload_url = self.s3_client.generate_presigned_url(
            "put_object",
            Params={"Bucket": self.bucket, "Key": s3_key},
            ExpiresIn=self.expiration,
        )

        expires_at = datetime.utcnow() + timedelta(seconds=self.expiration)

        return {
            "upload_url": upload_url,
            "s3_path": s3_key,
            "expires_in": self.expiration,
            "expires_at": expires_at.isoformat() + "Z",
        }

    def upload_json_file(self, path: str, data: dict):
        """Upload JSON data to storage."""
        import json
        json_str = json.dumps(data, indent=2)
        self.s3_client.put_object(
            Bucket=self.bucket,
            Key=path,
            Body=json_str.encode('utf-8'),
            ContentType='application/json'
        )
```

**Step 3: Create .env file**

File: `amber_aim/.env`

**For Backblaze B2**:
```bash
# Storage (Backblaze B2 - NO boto3, NO AWS)
APP_STORAGE_BUCKET_NAME=vibepoint-videos
APP_STORAGE_REGION=us-west-004  # Your B2 region
APP_STORAGE_ACCESS_KEY_ID=your-b2-application-key-id
APP_STORAGE_SECRET_ACCESS_KEY=your-b2-application-key
APP_STORAGE_ENDPOINT_URL=https://s3.us-west-004.backblazeb2.com  # Your B2 endpoint

# Upload settings
APP_UPLOAD_URL_EXPIRATION=1800
APP_S3_BASE_PATH=upload

# TwelveLabs
APP_TWELVE_LABS_API_KEY=your-twelvelabs-api-key
APP_TWELVE_LABS_CREATORS_INDEX_ID=your-creators-index-id
APP_TWELVE_LABS_ADS_INDEX_ID=your-ads-index-id

# AI (Google Gemini)
APP_AI_API_KEY=your-gemini-api-key
APP_AI_MODEL=gemini-2.0-flash-exp

# Application
APP_LOG_LEVEL=INFO
```

**For Cloudflare R2**:
```bash
# Storage (Cloudflare R2 - uses boto3, NOT AWS)
APP_STORAGE_BUCKET_NAME=vibepoint-videos
APP_STORAGE_REGION=auto
APP_STORAGE_ACCESS_KEY_ID=your-r2-access-key-id
APP_STORAGE_SECRET_ACCESS_KEY=your-r2-secret-access-key
APP_STORAGE_ENDPOINT_URL=https://[account-id].r2.cloudflarestorage.com

# Upload settings
APP_UPLOAD_URL_EXPIRATION=1800
APP_S3_BASE_PATH=upload

# TwelveLabs
APP_TWELVE_LABS_API_KEY=your-twelvelabs-api-key
APP_TWELVE_LABS_CREATORS_INDEX_ID=your-creators-index-id
APP_TWELVE_LABS_ADS_INDEX_ID=your-ads-index-id

# AI (Google Gemini)
APP_AI_API_KEY=your-gemini-api-key
APP_AI_MODEL=gemini-2.0-flash-exp

# Application
APP_LOG_LEVEL=INFO
```

---

### Phase 3: Test Locally (10 min)

```bash
# Install dependencies
cd amber_aim
uv pip install -e .

# Start backend
uvicorn aim.main:app --reload

# In new terminal, start frontend
cd amber_aim_web
npm install
npm run dev
```

Test:
1. Upload a video
2. Check it appears in storage (B2 or R2 dashboard)
3. Verify AI processing works

---

### Phase 4: Deploy to Production (20 min)

**Backend (Render)**:

1. Go to https://dashboard.render.com
2. New > Web Service
3. Connect your GitHub repo
4. Configure:
   - Name: `vibepoint-backend`
   - Root Directory: `amber_aim`
   - Build Command: `pip install -e .`
   - Start Command: `uvicorn aim.main:app --host 0.0.0.0 --port $PORT`
   - Instance Type: **Free**

5. Add Environment Variables (click "Environment"):
   - Copy all `APP_*` variables from your `.env`
   - Add each one individually

6. Click "Create Web Service"
7. Wait for deploy (~2-5 minutes)
8. Copy your backend URL: `https://vibepoint-backend.onrender.com`

**Frontend (Vercel)**:

```bash
cd amber_aim_web

# Install Vercel CLI
npm i -g vercel

# Deploy
vercel

# Follow prompts
# When asked for environment variables:
vercel env add NEXT_PUBLIC_API_URL production

# Enter your Render backend URL
# Example: https://vibepoint-backend.onrender.com

# Deploy to production
vercel --prod
```

Your site: `https://vibepoint.vercel.app`

---

## Variable Naming

### The Problem

Many guides use confusing variable names like:
```bash
AWS_ACCESS_KEY_ID=your-cloudflare-r2-key  # ❌ Says AWS but it's Cloudflare!
```

This is **misleading** when you're NOT using AWS.

### Better Naming

Use `STORAGE_*` prefix instead:

```bash
# Clear, not misleading
APP_STORAGE_ACCESS_KEY_ID=your-r2-or-b2-key  # ✅ Clear purpose
APP_STORAGE_SECRET_ACCESS_KEY=your-secret    # ✅ Not AWS-specific
APP_STORAGE_BUCKET_NAME=vibepoint-videos     # ✅ Generic
APP_STORAGE_ENDPOINT_URL=https://...         # ✅ Works for any provider
```

### Why Old Guides Use AWS_*

**Reason**: boto3 library was built for AWS and automatically reads `AWS_ACCESS_KEY_ID` from environment.

**Solution**: Pass credentials explicitly to boto3:
```python
boto3.client(
    "s3",
    aws_access_key_id=settings.storage_access_key_id,  # Explicit
    aws_secret_access_key=settings.storage_secret_access_key,
    # ...
)
```

**Benefits**:
- ✅ Clear you're not using AWS
- ✅ Works with any S3-compatible service
- ✅ Easy to swap providers
- ✅ Better documentation

---

## Code Changes

### Summary

| File | Lines Changed | Purpose |
|------|--------------|---------|
| `config.py` | ~10 lines | Update variable names |
| `s3_service.py` | ~5 lines | Pass credentials explicitly |
| `.env` | ~5-10 lines | Set new variable names |

**Total**: ~20-25 lines
**Time**: 10-15 minutes

---

## AI Service Options

### Detailed Comparison

| Service | Free Limit | Quality | Speed | Best For |
|---------|-----------|---------|-------|----------|
| **Google Gemini** ⭐ | 1,500 req/day | High | Fast | Most users |
| **Groq** | Rate limited | High | Very Fast | Speed priority |
| **Hugging Face API** | Few hundred/hour | Varies | Medium | Model variety |
| **Local Models** | Unlimited | High | Slow | Privacy/offline |
| **Transformers.js** | Unlimited | Medium | Slow | Browser-based |

### Google Gemini (Recommended)

**Free Tier**:
- 1,500 requests/day
- 15 requests/minute
- 1M tokens/minute (throughput)

**Setup**:
```bash
# Get API key at https://aistudio.google.com
uv pip install google-generativeai

# .env
APP_AI_API_KEY=your-gemini-api-key
APP_AI_MODEL=gemini-2.0-flash-exp
```

**Why Gemini**:
- ✅ Best free tier (1,500 req/day)
- ✅ High quality
- ✅ Fast
- ✅ Multimodal (can analyze images)
- ✅ No credit card for free tier

### Groq

**Free Tier**:
- Rate limited (exact limits undisclosed)
- Still generous for testing

**Setup**:
```bash
# Get API key at https://console.groq.com
# Uses OpenAI SDK (already installed)

# .env
APP_AI_API_KEY=your-groq-api-key
APP_AI_BASE_URL=https://api.groq.com/openai/v1
APP_AI_MODEL=llama-3.1-70b-versatile
```

**Why Groq**:
- ✅ Very fast inference (LPU technology)
- ✅ OpenAI-compatible (easy swap)
- ✅ Good quality
- ⚠️ Rate limits (but generous)

### Local Models (Advanced)

**Requirements**:
- 16+ GB RAM (for 7B models)
- 8+ GB VRAM (for GPU acceleration)

**Setup**:
```bash
uv pip install transformers torch accelerate

# Use models like:
# - Qwen/Qwen2.5-7B-Instruct (8 GB RAM)
# - meta-llama/Llama-3.2-3B-Instruct (4 GB RAM)
```

**Pros**:
- ✅ Unlimited usage
- ✅ Complete privacy
- ✅ Works offline
- ✅ No API costs ever

**Cons**:
- ⚠️ Slower than cloud APIs
- ⚠️ Requires good hardware
- ⚠️ Can't deploy to Render free tier (512 MB RAM limit)

---

## Storage Without S3/boto3

If you want to avoid S3-compatible APIs entirely:

### Supabase Storage

**Free Tier**: 1 GB (too small for most video use)

**Setup**:
```bash
uv pip install supabase

# .env
APP_SUPABASE_URL=https://your-project.supabase.co
APP_SUPABASE_KEY=your-anon-key
APP_SUPABASE_BUCKET=videos
```

**Pros**:
- ✅ Simple REST API (no boto3)
- ✅ Free PostgreSQL database included
- ✅ Easy to use

**Cons**:
- ⚠️ Only 1 GB (not enough for many videos)
- ⚠️ Projects pause after 1 week inactivity

### Direct Upload to Backend

**Setup**: Store files directly on Render

**Pros**:
- ✅ Simplest (no external storage)
- ✅ No API keys needed

**Cons**:
- ⚠️ Files lost on restart (Render free tier)
- ⚠️ Limited disk space (512 MB)
- ⚠️ Not suitable for production

---

## Cost Comparison

### What 10 GB Can Store

| Video Type | Duration | Size | How Many |
|------------|----------|------|----------|
| **Short clips** | 1-2 min | ~100 MB | 50-100 videos |
| **Medium videos** | 5 min | ~250-500 MB | 20-40 videos |
| **Long videos** | 10 min | ~500 MB-1 GB | 10-20 videos |
| **4K videos** | 5 min | ~2-4 GB | 2-5 videos |

### Monthly Costs

| Usage Level | Your Friend (AWS) | You (Free Tier) | Savings |
|-------------|-------------------|-----------------|---------|
| **Low** (10 videos/mo) | $107-150 | $0 | $107-150 |
| **Medium** (100 videos/mo) | $150-250 | $0 | $150-250 |
| **High** (1000 videos/mo) | $250-379 | $0* | $250-379 |

*May need to delete old videos to stay in 10 GB limit

### 1-Year Savings

| Component | Friend (12 months) | You (12 months) |
|-----------|-------------------|-----------------|
| Storage | ~$60 | $0 |
| AI | ~$1,800 | $0 |
| Backend | ~$300 | $0 |
| Frontend | ~$120 | $0 |
| **TOTAL** | **~$2,280** | **$0** |

**You save over $2,000 per year!**

---

## Troubleshooting

### Storage Issues

**Error**: "Could not connect to endpoint"
- Check `APP_STORAGE_ENDPOINT_URL` is set
- Verify endpoint URL is correct for your provider
- For B2: `https://s3.us-west-004.backblazeb2.com` (or your region)
- For R2: `https://[account-id].r2.cloudflarestorage.com`

**Error**: "Access Denied"
- Verify credentials are correct
- For B2: Check Application Key has write permissions
- For R2: Check API token has Admin Read & Write

**Uploads timeout**
- Check firewall/network
- Try smaller test file first
- Verify storage service is accessible

### AI Issues

**Gemini: "Rate limit exceeded"**
- You've exceeded 1,500 requests/day or 15/minute
- Wait for limit reset (midnight Pacific Time for daily)
- Consider caching responses

**Groq: "Model not available"**
- Try different model: `mixtral-8x7b-32768`
- Check API key is valid
- Verify account has access

**Response quality poor**
- Try different model (e.g., Gemini 2.5 Pro)
- Adjust prompts
- Increase temperature for creativity

### Backend Issues

**Render: Cold starts (30s delay)**
- Normal for free tier after 15 min inactivity
- **Solution**: Use UptimeRobot (free) to ping every 10 min
  - Sign up at https://uptimerobot.com
  - Create HTTP monitor
  - URL: `https://your-backend.onrender.com/health`
  - Interval: 10 minutes
  - Keeps backend always warm!

**Render: Out of memory**
- Free tier has 512 MB RAM only
- Reduce model size if using local AI
- Optimize code for memory usage
- Consider upgrading to Starter ($7/mo) for more RAM

**Render: Build failed**
- Check `pyproject.toml` has all dependencies
- Verify Python version (3.12+)
- Check build logs for specific errors

### Frontend Issues

**Vercel: Build failed**
- Check Node.js version (20+)
- Verify `package.json` is correct
- Check build logs

**Vercel: Environment variables missing**
- Add `NEXT_PUBLIC_API_URL` in Vercel dashboard
- Format: `https://your-backend.onrender.com` (no trailing slash)

**CORS errors**
- Backend needs to allow frontend origin
- Check FastAPI CORS middleware configuration

### TwelveLabs Issues

**Error**: "Index not found"
- Verify index IDs are correct
- Check indexes exist in dashboard
- Make sure API key has access to indexes

**Error**: "Indexing failed"
- Check video format is supported
- Verify video URL is accessible
- Check free tier limits (10 hours total)

**Indexes expired**
- Free tier indexes expire after 90 days
- Re-index videos if needed
- Upgrade to paid tier for longer retention

---

## Next Steps

### When to Upgrade

Consider upgrading when:

1. **Storage** > 10 GB
   - Backblaze B2: $0.005/GB/month (cheapest!)
   - Cloudflare R2: $0.015/GB/month

2. **AI requests** > 1,500/day (Gemini)
   - Groq stays free with rate limits
   - Google Gemini: $0.075 per 1M tokens
   - OpenAI: Pay-as-you-go

3. **Cold starts** annoying (Render)
   - Render Starter: $7/month (always-on, 512 MB RAM)
   - Railway: Similar pricing, no cold starts

4. **Commercial use** (Vercel)
   - Vercel Pro: $20/month per user
   - Or use Netlify, Cloudflare Pages

### Estimated Upgrade Costs

**Small production app**:
- Storage (50 GB): $0.25-0.75/month
- Backend (Render Starter): $7/month
- Frontend (still free or $20/month)
- AI (Groq/Gemini): Still free or minimal

**Total after upgrades**: $10-30/month (still 90% cheaper than AWS!)

---

## Appendix: Alternative Services

### Other Free Backend Hosts

| Platform | Free Tier | Cold Start | Notes |
|----------|-----------|------------|-------|
| Railway | $5 credit/month | No | Credit runs out |
| Fly.io | 3 VMs, 3 GB | No | More complex setup |
| Koyeb | 1 service, 512 MB | 30 min | Similar to Render |

### Other Free Frontend Hosts

| Platform | Free Tier | Notes |
|----------|-----------|-------|
| Netlify | 100 GB bandwidth | Similar to Vercel |
| Cloudflare Pages | Unlimited | No build minutes on free |
| GitHub Pages | Static only | No SSR |

### Other Free Storage

| Platform | Free Tier | S3 Compatible? |
|----------|-----------|----------------|
| Supabase | 1 GB | Yes (limited) |
| Wasabi | 1 TB trial (30 days) | Yes |

---

## Summary Checklist

### Accounts Needed (All Free, NO AWS):
- [ ] Backblaze B2 or Cloudflare R2 (storage)
- [ ] Google Gemini or Groq (AI)
- [ ] Render (backend)
- [ ] Vercel (frontend)
- [ ] TwelveLabs (video analysis)
- [ ] UptimeRobot (optional - keeps backend warm)

### Code Changes:
- [ ] Update `config.py` (~10 lines)
- [ ] Update `s3_service.py` (~5 lines)
- [ ] Create `.env` file with new variables
- [ ] Test locally

### Deployment:
- [ ] Push code to GitHub
- [ ] Deploy backend to Render
- [ ] Deploy frontend to Vercel
- [ ] Test production

### Cost:
- [x] Storage: $0/month (10 GB free)
- [x] AI: $0/month (1,500 req/day or rate-limited)
- [x] Backend: $0/month (750 hrs)
- [x] Frontend: $0/month (100 GB bandwidth)
- [x] Video: $0/month (10 hrs indexing)
- [x] **TOTAL: $0/month**

### AWS Accounts Needed:
- [x] **ZERO** ✅

---

**End of Guide**

This consolidated guide contains everything from the session. You can now run VibePoint completely free without AWS!

**Date**: October 21, 2025
**Next Review**: January 2026 (check for free tier changes)

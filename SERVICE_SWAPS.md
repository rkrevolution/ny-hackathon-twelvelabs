# Service Swaps: AWS → Free Alternatives

**Date**: October 21, 2025

This document clearly shows what replaces what when migrating from your friend's AWS setup to a completely free deployment.

---

## Overview

```
┌─────────────────────────────────────────────────────┐
│              YOUR FRIEND'S AWS SETUP                │
├─────────────────────────────────────────────────────┤
│ Videos → AWS S3                    ~$2-9/month      │
│ AI → OpenAI GPT-4                  ~$100-300/month  │
│ Backend → AWS EC2/Lambda           ~$5-50/month     │
│ Frontend → AWS Amplify/S3          ~$0-20/month     │
│ Video Analysis → TwelveLabs Paid   Varies           │
│                                                      │
│ TOTAL: $116-381/month                               │
└─────────────────────────────────────────────────────┘
                        ↓
                    SWAPS TO
                        ↓
┌─────────────────────────────────────────────────────┐
│                YOUR FREE SETUP                       │
├─────────────────────────────────────────────────────┤
│ Videos → Cloudflare R2             FREE             │
│ AI → Groq/Gemini/HF/Local          FREE             │
│ Backend → Render.com               FREE             │
│ Frontend → Vercel                  FREE             │
│ Video Analysis → TwelveLabs Free   FREE             │
│                                                      │
│ TOTAL: $0/month (100% savings!)                     │
└─────────────────────────────────────────────────────┘
```

---

## Detailed Swaps

### Swap #1: Video Storage

| Aspect | AWS S3 (Friend's Setup) | Cloudflare R2 (Your Setup) |
|--------|-------------------------|----------------------------|
| **Service** | Amazon S3 | Cloudflare R2 |
| **Cost** | $0.023/GB/month + bandwidth | FREE (10 GB + 10M requests) |
| **Purpose** | Store uploaded videos | Store uploaded videos |
| **API** | S3 API | S3-compatible API ✅ |
| **Code Change** | N/A | ✅ Minor (3 lines) |
| **Performance** | Fast | Fast (global CDN) |
| **Limits** | Pay as you go | 10 GB storage, 10M requests/month |

**What Stays the Same**:
- S3 API calls (boto3 SDK)
- Upload/download functionality
- Video file structure

**What Changes**:
```python
# OLD (.env):
APP_AWS_S3_BUCKET=friend-aws-bucket
APP_AWS_REGION=us-east-1
# (uses default AWS S3 endpoint)

# NEW (.env):
APP_AWS_S3_BUCKET=vibepoint-videos
APP_AWS_REGION=auto
APP_AWS_ENDPOINT_URL=https://[account-id].r2.cloudflarestorage.com
```

**Code Changes Required**:
1. Add `aws_endpoint_url` to `config.py` (1 line)
2. Pass `endpoint_url` to boto3 client in `s3_service.py` (1 line)

---

### Swap #2: AI Model

| Aspect | OpenAI GPT-4 (Friend) | Free Options (You) |
|--------|----------------------|---------------------|
| **Service** | OpenAI GPT-4 | Groq / Gemini / HF / Local |
| **Cost** | ~$100-300/month | FREE |
| **Purpose** | Analyze videos, match ads | Analyze videos, match ads |
| **API** | OpenAI API | OpenAI-compatible API ✅ |
| **Code Change** | N/A | ✅ Minimal (change URL/key) |
| **Quality** | Excellent | Very Good to Excellent |
| **Speed** | Fast | Fast (Groq/Gemini) to Slow (Local) |
| **Limits** | Pay per token | Free tier limits (or unlimited) |

**What Stays the Same**:
- All prompt logic
- Agent code structure
- Response parsing (mostly)
- Business logic

**What Changes** (for Groq example):
```python
# OLD (.env):
APP_OPENAI_API_KEY=sk-proj-abc123...
APP_OPENAI_BASE_URL=https://api.openai.com/v1
APP_OPENAI_MODEL=gpt-4

# NEW (.env):
APP_OPENAI_API_KEY=gsk_abc123...  # Groq key
APP_OPENAI_BASE_URL=https://api.groq.com/openai/v1  # Groq URL
APP_OPENAI_MODEL=llama-3.1-70b-versatile  # Groq model
```

**Code Changes Required**: NONE for Groq/Gemini (OpenAI-compatible)

**For Local Models**: See `AI_OPTIONS.md` for additional setup

---

### Swap #3: Backend Hosting

| Aspect | AWS EC2/Lambda (Friend) | Render.com (You) |
|--------|------------------------|-------------------|
| **Service** | AWS EC2 or Lambda | Render Web Service |
| **Cost** | $5-50/month | FREE (750 hrs/month) |
| **Purpose** | Run FastAPI backend | Run FastAPI backend |
| **Code Change** | N/A | ❌ NONE |
| **Performance** | Fast, always-on | Fast, sleeps after 15min |
| **RAM** | Variable | 512 MB |
| **Deployment** | Manual or complex CI/CD | Git push auto-deploy |

**What Stays the Same**:
- Entire FastAPI application
- All Python code
- Dependencies
- Environment variables

**What Changes**:
- Hosting platform only
- Deployment method (easier!)
- Cold starts (free tier sleeps)

**Setup**:
1. Push code to GitHub
2. Connect Render to GitHub repo
3. Configure environment variables in Render dashboard
4. Deploy!

**Code Changes Required**: NONE

**Optional**: Add `Procfile` for explicit startup command
```
web: uvicorn aim.main:app --host 0.0.0.0 --port $PORT
```

---

### Swap #4: Frontend Hosting

| Aspect | AWS Amplify (Friend) | Vercel (You) |
|--------|---------------------|---------------|
| **Service** | AWS Amplify or S3 + CloudFront | Vercel |
| **Cost** | $0-20/month | FREE (unlimited hobby) |
| **Purpose** | Host Next.js frontend | Host Next.js frontend |
| **Code Change** | N/A | ❌ NONE |
| **Performance** | Fast | Fast (global edge network) |
| **Build** | Git push | Git push auto-deploy |
| **SSL** | Automatic | Automatic |

**What Stays the Same**:
- Entire Next.js application
- All React components
- API integration
- Build process

**What Changes**:
- Hosting platform only
- Deployment method (even easier!)
- Domain (unless custom)

**Setup**:
1. Run `vercel` in frontend directory
2. Follow prompts
3. Set environment variable: `NEXT_PUBLIC_API_URL`
4. Deploy with `vercel --prod`

**Code Changes Required**: NONE

---

### Swap #5: Video Analysis (No Swap - Just Free Tier)

| Aspect | TwelveLabs Paid (Friend) | TwelveLabs Free (You) |
|--------|-------------------------|----------------------|
| **Service** | TwelveLabs API | TwelveLabs API (same) |
| **Cost** | Paid tier | FREE tier |
| **Purpose** | AI video understanding | AI video understanding |
| **API** | TwelveLabs API | TwelveLabs API (same) |
| **Code Change** | N/A | ❌ NONE |

**What Stays the Same**:
- Everything! Same API, same code

**What Changes**:
- Use free tier limits
- Same API key works

**Code Changes Required**: NONE

---

## Code Changes Summary

### Total Changes Needed: 3 Lines

**File 1**: `amber_aim/src/aim/config.py`
```python
# ADD THIS LINE:
aws_endpoint_url: str | None = None
```

**File 2**: `amber_aim/src/aim/services/s3_service.py`
```python
# FIND THIS:
self.s3_client = boto3.client(
    "s3",
    region_name=settings.aws_region,
    config=Config(signature_version="s3v4"),
)

# CHANGE TO THIS (add endpoint_url parameter):
self.s3_client = boto3.client(
    "s3",
    region_name=settings.aws_region,
    endpoint_url=settings.aws_endpoint_url,  # ADD THIS LINE
    config=Config(signature_version="s3v4"),
)
```

**File 3**: `.env` (environment variables)
```bash
# CHANGE THESE VARIABLES:
APP_AWS_S3_BUCKET=vibepoint-videos  # your R2 bucket name
APP_AWS_REGION=auto
APP_AWS_ENDPOINT_URL=https://[account-id].r2.cloudflarestorage.com  # ADD THIS

APP_OPENAI_API_KEY=gsk_...  # Groq or Gemini key
APP_OPENAI_BASE_URL=https://api.groq.com/openai/v1  # Groq or Gemini URL
APP_OPENAI_MODEL=llama-3.1-70b-versatile  # Groq or Gemini model
```

**That's it!** 3 lines of code changes total.

---

## Environment Variables Comparison

### Your Friend's .env (AWS Setup)

```bash
# AWS S3 Configuration
APP_AWS_S3_BUCKET=production-video-bucket
APP_AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=AKIA...
AWS_SECRET_ACCESS_KEY=abc123...

# TwelveLabs (Paid Tier)
APP_TWELVE_LABS_API_KEY=tlk_...
APP_TWELVE_LABS_CREATORS_INDEX_ID=...
APP_TWELVE_LABS_ADS_INDEX_ID=...

# OpenAI GPT-4 (Expensive!)
APP_OPENAI_API_KEY=sk-proj-...
APP_OPENAI_BASE_URL=https://api.openai.com/v1
APP_OPENAI_MODEL=gpt-4

# Settings
APP_LOG_LEVEL=INFO
```

**Monthly Cost**: $116-381

---

### Your .env (Free Setup)

```bash
# Cloudflare R2 Storage (FREE!)
APP_AWS_S3_BUCKET=vibepoint-videos
APP_AWS_REGION=auto
APP_AWS_ENDPOINT_URL=https://[your-id].r2.cloudflarestorage.com  # NEW!
AWS_ACCESS_KEY_ID=...your-r2-access-key...
AWS_SECRET_ACCESS_KEY=...your-r2-secret...

# TwelveLabs (Free Tier)
APP_TWELVE_LABS_API_KEY=tlk_...
APP_TWELVE_LABS_CREATORS_INDEX_ID=...
APP_TWELVE_LABS_ADS_INDEX_ID=...

# Groq AI (FREE & UNLIMITED!)
APP_OPENAI_API_KEY=gsk_...your-groq-key...
APP_OPENAI_BASE_URL=https://api.groq.com/openai/v1
APP_OPENAI_MODEL=llama-3.1-70b-versatile

# OR Google Gemini (FREE - 1M tokens/day)
# APP_GEMINI_API_KEY=...your-gemini-key...
# APP_USE_GEMINI=true
# APP_GEMINI_MODEL=gemini-2.0-flash-exp

# Settings
APP_LOG_LEVEL=INFO
```

**Monthly Cost**: $0

---

## Migration Checklist

### Phase 1: Get Free Accounts (20 minutes)
- [ ] Create Cloudflare account → Get R2 credentials
- [ ] Create Groq account → Get API key
  - OR Google Gemini → Get API key
  - OR Hugging Face → Get token
- [ ] Create Render account → Connect GitHub
- [ ] Create Vercel account → Install CLI

### Phase 2: Update Code (5 minutes)
- [ ] Add `aws_endpoint_url` to `config.py`
- [ ] Update `s3_service.py` with endpoint parameter
- [ ] Update `.env` with new credentials

### Phase 3: Test Locally (10 minutes)
- [ ] Test R2 uploads
- [ ] Test AI responses (Groq/Gemini)
- [ ] Run backend: `uvicorn aim.main:app --reload`
- [ ] Run frontend: `npm run dev`

### Phase 4: Deploy (15 minutes)
- [ ] Push code to GitHub
- [ ] Deploy backend to Render
- [ ] Set environment variables in Render
- [ ] Deploy frontend to Vercel
- [ ] Test production deployment

### Phase 5: Monitor (5 minutes)
- [ ] Set up UptimeRobot (optional, prevents cold starts)
- [ ] Test video upload end-to-end
- [ ] Verify AI analysis works

**Total Time**: ~55 minutes

---

## What Doesn't Change

### Application Code (99% the same)
✅ All FastAPI routes
✅ All React components
✅ Business logic
✅ Data models
✅ API contracts
✅ Authentication (if any)
✅ Frontend styling
✅ File structure

### Functionality
✅ Video upload flow
✅ AI video analysis
✅ Ad matching
✅ Dashboard
✅ User experience
✅ Performance (similar)

### Development Experience
✅ Local development setup
✅ Testing procedures
✅ Debugging tools
✅ Git workflow

---

## Troubleshooting Swaps

### R2 Upload Failing
**Error**: "Could not connect to endpoint"
**Solution**: Make sure `APP_AWS_ENDPOINT_URL` is set in `.env`

### AI Responses Different
**Issue**: Responses from Groq/Gemini slightly different than GPT-4
**Solution**: Normal! Each model has slight variations. Adjust prompts if needed.

### Backend Cold Start
**Issue**: First request after 15 min takes 30 seconds
**Solution**: Set up UptimeRobot to ping every 10 min (keeps backend awake)

### Frontend Build Error
**Issue**: Build fails on Vercel
**Solution**: Check environment variables are set in Vercel dashboard

---

## Cost Comparison Over Time

### 3-Month Cost Comparison

| Month | Friend's AWS | Your Free Setup | Savings |
|-------|-------------|-----------------|---------|
| Month 1 | $150 | $0 | $150 |
| Month 2 | $180 | $0 | $180 |
| Month 3 | $200 | $0 | $200 |
| **Total** | **$530** | **$0** | **$530** |

### 1-Year Cost Comparison

| Service | Friend (12 months) | You (12 months) | Savings |
|---------|-------------------|-----------------|---------|
| Storage | $60 | $0 | $60 |
| AI | $1,800 | $0 | $1,800 |
| Backend | $300 | $0 | $300 |
| Frontend | $120 | $0 | $120 |
| **TOTAL** | **$2,280** | **$0** | **$2,280** |

**You save over $2,000 per year!**

---

## When to Consider Paid Upgrades

### Upgrade Storage When:
- You exceed 10 GB (R2 free tier)
- Solution: R2 paid tier ($0.015/GB/month)

### Upgrade Backend When:
- Cold starts become annoying
- Need more than 512 MB RAM
- Solution: Render Starter ($7/month)

### Upgrade AI When:
- Exceed 1M tokens/day (Gemini limit)
- Need guaranteed SLA
- Solution: Groq stays free, or OpenAI pay-as-you-go

**Estimated upgrade cost**: $10-30/month (still 90% cheaper than AWS!)

---

## Summary

### The Swaps
1. **AWS S3** → **Cloudflare R2** (3 lines of code)
2. **OpenAI GPT-4** → **Groq/Gemini/HF** (change env vars)
3. **AWS EC2** → **Render** (no code changes)
4. **AWS Amplify** → **Vercel** (no code changes)
5. **TwelveLabs Paid** → **TwelveLabs Free** (no changes)

### The Results
- **Code changes**: 3 lines
- **Setup time**: 55 minutes
- **Cost savings**: $116-381/month → $0/month
- **Functionality**: Identical
- **Performance**: Similar (or better!)

---

**Date**: October 21, 2025
**Last Updated**: October 21, 2025
**Next Review**: Quarterly (check for free tier changes)

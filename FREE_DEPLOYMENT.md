# Free Deployment Guide for VibePoint

This guide explains how to run VibePoint completely **free of charge** using free-tier services and open-source alternatives.

## Current Requirements vs. Free Alternatives

| Service | Current Setup | Cost | Free Alternative | Free Tier Limits |
|---------|--------------|------|------------------|------------------|
| **Video Storage** | AWS S3 | ~$0.023/GB/month | Cloudflare R2 | 10 GB storage, 10M requests/month |
| **Video Analysis** | TwelveLabs API | Paid API | TwelveLabs Free Tier | Check current limits at twelvelabs.io |
| **AI Matching** | OpenAI GPT-4 | ~$0.01-0.03/1K tokens | OpenAI Free Trial / Groq | $5 free credit / Unlimited free tier |
| **Backend Hosting** | AWS EC2/Lambda | $5-50/month | Render.com | 750 hrs/month, 512 MB RAM |
| **Frontend Hosting** | AWS Amplify/Vercel | $0-20/month | Vercel Free Tier | Unlimited hobby projects |

**Total Monthly Cost:**
- **Current setup**: $20-100+/month
- **Free setup**: $0/month

---

## Prerequisites

Before starting, create free accounts for:

1. **Cloudflare** (https://cloudflare.com) - For R2 storage
2. **TwelveLabs** (https://twelvelabs.io) - For video analysis API
3. **Groq** (https://groq.com) OR **OpenAI** (https://openai.com) - For AI matching
4. **Render** (https://render.com) - For backend hosting
5. **Vercel** (https://vercel.com) - For frontend hosting

---

## Step 1: Set Up Free Video Storage (Cloudflare R2)

Cloudflare R2 is S3-compatible with a generous free tier (10 GB storage, 10M reads/month).

### 1.1 Create R2 Bucket

1. Go to Cloudflare Dashboard > R2
2. Click "Create bucket"
3. Name: `vibepoint-videos`
4. Click "Create bucket"

### 1.2 Get R2 Credentials

1. In R2 dashboard, click "Manage R2 API Tokens"
2. Click "Create API Token"
3. Permissions: "Admin Read & Write"
4. Click "Create API Token"
5. **Save these values** (you won't see them again):
   - Access Key ID
   - Secret Access Key
   - Endpoint URL (e.g., `https://[account-id].r2.cloudflarestorage.com`)

### 1.3 Enable Public Access

1. Go to your bucket settings
2. Under "Public Access", enable public bucket access (for video playback)
3. Note the public bucket URL

---

## Step 2: Get Free API Keys

### 2.1 TwelveLabs API (Video Analysis)

1. Sign up at https://twelvelabs.io
2. Create a new project
3. Copy your API key from the dashboard
4. Create two indexes:
   - **Creators Index**: For creator content videos
   - **Ads Index**: For advertisement videos
5. Note both index IDs

**Free Tier**: Check current limits at https://docs.twelvelabs.io/docs/pricing

### 2.2 Groq API (Free AI Matching - Recommended)

**Groq offers unlimited free tier for LLM inference!**

1. Sign up at https://console.groq.com
2. Generate an API key
3. Use model: `llama-3.1-70b-versatile` (free, fast, and powerful)

**Alternative: OpenAI**
1. Sign up at https://platform.openai.com
2. Get $5 free credit (new accounts)
3. Create API key

---

## Step 3: Backend Setup (Local Development)

### 3.1 Clone and Install

```bash
cd amber_aim
uv pip install -e .
```

### 3.2 Configure Environment Variables

Create `.env` file in `amber_aim/` directory:

```bash
# Cloudflare R2 Storage (S3-Compatible)
APP_AWS_S3_BUCKET=vibepoint-videos
APP_AWS_REGION=auto
APP_AWS_ENDPOINT_URL=https://[your-account-id].r2.cloudflarestorage.com
AWS_ACCESS_KEY_ID=your-r2-access-key
AWS_SECRET_ACCESS_KEY=your-r2-secret-key

# Upload Settings
APP_UPLOAD_URL_EXPIRATION=1800
APP_S3_BASE_PATH=upload

# TwelveLabs Configuration
APP_TWELVE_LABS_API_KEY=your-twelvelabs-api-key
APP_TWELVE_LABS_CREATORS_INDEX_ID=your-creators-index-id
APP_TWELVE_LABS_ADS_INDEX_ID=your-ads-index-id

# AI Configuration (Groq - Free!)
APP_OPENAI_API_KEY=your-groq-api-key
APP_OPENAI_BASE_URL=https://api.groq.com/openai/v1
APP_OPENAI_MODEL=llama-3.1-70b-versatile

# OR if using OpenAI:
# APP_OPENAI_API_KEY=your-openai-api-key
# APP_OPENAI_BASE_URL=https://api.openai.com/v1
# APP_OPENAI_MODEL=gpt-4o-mini

# Application Settings
APP_LOG_LEVEL=INFO
```

### 3.3 Update S3 Service for R2 Compatibility

You'll need to modify the S3 service to use the R2 endpoint. Edit `amber_aim/src/aim/services/s3_service.py` and update the boto3 client initialization:

```python
# Add endpoint_url parameter
self.s3_client = boto3.client(
    "s3",
    region_name=settings.aws_region,
    endpoint_url=settings.aws_endpoint_url,  # Add this line
    config=Config(signature_version="s3v4"),
)
```

Then update `config.py` to include the endpoint:

```python
aws_endpoint_url: str | None = None
```

### 3.4 Run Backend Locally

```bash
uvicorn aim.main:app --reload
```

Backend will be at http://localhost:8000

---

## Step 4: Frontend Setup (Local Development)

### 4.1 Install Dependencies

```bash
cd amber_aim_web
npm install
```

### 4.2 Configure Environment

Create `.env.local`:

```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### 4.3 Run Frontend Locally

```bash
npm run dev
```

Frontend will be at http://localhost:3000

---

## Step 5: Deploy Backend to Render (Free)

Render offers **750 hours/month free** (enough for a single service running 24/7).

### 5.1 Prepare for Deployment

1. Add `Procfile` to `amber_aim/`:

```bash
web: uvicorn aim.main:app --host 0.0.0.0 --port $PORT
```

2. Ensure `pyproject.toml` has all dependencies

### 5.2 Deploy to Render

1. Go to https://dashboard.render.com
2. Click "New +" > "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Name**: `vibepoint-backend`
   - **Root Directory**: `amber_aim`
   - **Build Command**: `pip install -e .`
   - **Start Command**: `uvicorn aim.main:app --host 0.0.0.0 --port $PORT`
   - **Instance Type**: Free

5. Add Environment Variables (from your `.env` file):
   - Click "Environment" tab
   - Add all `APP_*` and `AWS_*` variables from above

6. Click "Create Web Service"

Your backend will be deployed at: `https://vibepoint-backend.onrender.com`

**Note**: Free tier sleeps after 15 min of inactivity (takes ~30s to wake up).

---

## Step 6: Deploy Frontend to Vercel (Free)

Vercel offers **unlimited free hosting** for hobby projects.

### 6.1 Deploy to Vercel

1. Install Vercel CLI:

```bash
npm i -g vercel
```

2. Deploy from frontend directory:

```bash
cd amber_aim_web
vercel
```

3. Follow prompts:
   - Link to existing project? **No**
   - Project name: `vibepoint`
   - Directory: `./`

4. Set production environment variable:

```bash
vercel env add NEXT_PUBLIC_API_URL production
```

Enter your Render backend URL: `https://vibepoint-backend.onrender.com`

5. Deploy to production:

```bash
vercel --prod
```

Your frontend will be at: `https://vibepoint.vercel.app`

---

## Cost Breakdown: Free vs. Paid

### Monthly Costs Comparison

| Component | AWS Setup | Free Setup |
|-----------|-----------|------------|
| Video Storage (100 GB) | ~$2.30 | **$0** (within 10 GB free tier) |
| Bandwidth (100 GB) | ~$9.00 | **$0** (within R2 free tier) |
| TwelveLabs API | Varies | **$0** (free tier) |
| AI API (10M tokens) | ~$100-300 | **$0** (Groq unlimited) |
| Backend Server | ~$5-50 | **$0** (Render free tier) |
| Frontend Hosting | ~$0-20 | **$0** (Vercel free tier) |
| **TOTAL** | **$116-381/month** | **$0/month** |

---

## Limitations of Free Tier

### Storage (Cloudflare R2)
- 10 GB storage limit (about 20-50 videos depending on quality)
- 10 million requests/month
- **Solution**: Delete old videos or upgrade to paid tier ($0.015/GB)

### Backend (Render)
- 512 MB RAM
- Sleeps after 15 min inactivity (30s cold start)
- **Solution**: Use a free uptime monitor like UptimeRobot to ping every 10 min

### Frontend (Vercel)
- 100 GB bandwidth/month
- **Solution**: Unlikely to hit this limit for personal/demo use

### TwelveLabs API
- Check current free tier limits at https://docs.twelvelabs.io/docs/pricing
- **Solution**: Use free tier wisely, cache results

### Groq API
- No limits! Completely free (as of 2025)
- **Alternative**: OpenAI free trial ($5 credit)

---

## Monitoring and Keeping Free Tier Active

### Keep Render Backend Active (Avoid Cold Starts)

Use a free uptime monitor to ping your backend every 10 minutes:

1. Sign up at https://uptimerobot.com (free)
2. Create new monitor:
   - Type: HTTP(s)
   - URL: `https://vibepoint-backend.onrender.com/health`
   - Interval: 10 minutes
3. Your backend will never sleep!

---

## Alternative Free Options

### Other Free Backend Hosting

| Platform | Free Tier | Cold Start |
|----------|-----------|------------|
| **Railway** | $5 credit/month (limited time) | No sleep |
| **Fly.io** | 3 shared VMs, 3 GB storage | No sleep |
| **Koyeb** | 1 web service, 512 MB | Sleeps after 30 min |
| **Cyclic** | 10K requests/month | No sleep |

### Other Free Storage

| Platform | Free Tier | S3 Compatible? |
|----------|-----------|----------------|
| **Supabase Storage** | 1 GB | Yes (S3-compatible API) |
| **Backblaze B2** | 10 GB, 1 GB download/day | Yes (S3-compatible) |
| **Wasabi** | 1 TB trial (30 days) | Yes |

---

## Quick Start Commands

### Local Development

```bash
# Backend
cd amber_aim
uv pip install -e .
# Create .env with your credentials
uvicorn aim.main:app --reload

# Frontend (new terminal)
cd amber_aim_web
npm install
# Create .env.local with API URL
npm run dev
```

### Production Deployment

```bash
# Backend - push to GitHub, deploy via Render dashboard
git push origin main

# Frontend - deploy to Vercel
cd amber_aim_web
vercel --prod
```

---

## Troubleshooting

### R2 Connection Issues

**Error**: "Could not connect to the endpoint URL"

**Solution**: Make sure you've added `APP_AWS_ENDPOINT_URL` to your environment variables and updated the S3 service code.

### Render Cold Starts

**Issue**: Backend takes 30s to respond after inactivity

**Solution**: Set up UptimeRobot monitoring (see above) or upgrade to paid tier ($7/month for always-on).

### TwelveLabs Rate Limits

**Error**: "Rate limit exceeded"

**Solution**: Implement caching, reduce video analysis frequency, or upgrade to paid tier.

### Groq API Issues

**Error**: "Model not available"

**Solution**: Try alternative model `mixtral-8x7b-32768` or switch to OpenAI with free credits.

---

## Next Steps After Free Tier

When you outgrow the free tier:

1. **Storage**: Upgrade to Cloudflare R2 paid ($0.015/GB/month)
2. **Backend**: Upgrade Render to Starter ($7/month) for always-on + 512 MB RAM
3. **Frontend**: Vercel Pro ($20/month) for higher bandwidth
4. **AI**: Groq remains free, or switch to OpenAI pay-as-you-go

**Estimated cost for small production app**: $10-30/month

---

## Summary

You can run VibePoint **completely free** using:

✅ **Cloudflare R2** - Free 10 GB storage
✅ **Groq** - Free unlimited LLM inference
✅ **TwelveLabs** - Free tier video analysis
✅ **Render** - Free backend hosting (with cold starts)
✅ **Vercel** - Free frontend hosting
✅ **UptimeRobot** - Free monitoring to avoid cold starts

**Total cost: $0/month** for small-scale usage!

---

## Need Help?

- TwelveLabs Docs: https://docs.twelvelabs.io
- Groq Docs: https://console.groq.com/docs
- Render Docs: https://render.com/docs
- Vercel Docs: https://vercel.com/docs
- Cloudflare R2 Docs: https://developers.cloudflare.com/r2

Happy deploying! 🚀

# Free Deployment Guide for VibePoint

This guide explains how to run VibePoint completely **free of charge** using free-tier services and open-source alternatives.

## Current Requirements vs. Free Alternatives

| Service | Current Setup | Cost | Free Alternative | Free Tier Limits |
|---------|--------------|------|------------------|------------------|
| **Video Storage** | AWS S3 | ~$0.023/GB/month | Cloudflare R2 | 10 GB storage, 10M requests/month |
| **Video Analysis** | TwelveLabs API | Paid API | TwelveLabs Free Tier | Check current limits at twelvelabs.io |
| **AI Matching** | OpenAI GPT-4 | ~$0.01-0.03/1K tokens | Groq / Gemini / HF / Local | Unlimited / 1M tokens/day / 1K req/day / Unlimited |
| **Backend Hosting** | AWS EC2/Lambda | $5-50/month | Render.com | 750 hrs/month, 512 MB RAM |
| **Frontend Hosting** | AWS Amplify/Vercel | $0-20/month | Vercel Free Tier | Unlimited hobby projects |

**Total Monthly Cost:**
- **Current setup**: $20-100+/month
- **Free setup**: $0/month

---

## Prerequisites

Before starting, create free accounts for:

### Required Services
1. **Cloudflare** (https://cloudflare.com) - For R2 storage
2. **TwelveLabs** (https://twelvelabs.io) - For video analysis API
3. **Render** (https://render.com) - For backend hosting
4. **Vercel** (https://vercel.com) - For frontend hosting

### AI Service (Choose ONE)
Pick the option that best fits your needs:

- **Groq** (https://groq.com) - Fastest, unlimited free tier ⭐ Recommended
- **Google Gemini** (https://aistudio.google.com) - Best free tier (1M tokens/day) ⭐ Best Value
- **Hugging Face** (https://huggingface.co) - Access to 100K+ models, 1K requests/day
- **Local Models** - No account needed, runs on your computer (requires 8+ GB RAM)
- **Transformers.js** - No account needed, runs in browser (requires WebGPU browser)
- **OpenAI** (https://openai.com) - $5 free credit (limited)

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

### 2.2 AI Matching - Three Free Options

#### Option A: Groq API (Recommended - Fastest)

**Groq offers unlimited free tier for LLM inference!**

1. Sign up at https://console.groq.com
2. Generate an API key
3. Use model: `llama-3.1-70b-versatile` (free, fast, and powerful)

**Pros**: Unlimited free, very fast inference, no setup
**Cons**: Requires internet connection

#### Option B: Hugging Face Inference API (Free Tier)

**Hugging Face offers free API access to thousands of models!**

1. Sign up at https://huggingface.co
2. Go to Settings > Access Tokens
3. Create a new token with "read" permissions
4. Choose a model:
   - **Recommended**: `meta-llama/Llama-3.1-70B-Instruct` (powerful, good for structured output)
   - **Alternative**: `mistralai/Mixtral-8x7B-Instruct-v0.1` (fast, multilingual)
   - **Lightweight**: `meta-llama/Llama-3.2-3B-Instruct` (faster, lower quality)

**Pros**: Access to 100,000+ models, free tier available, simple API
**Cons**: Free tier has rate limits (1,000 requests/day), slower than Groq

#### Option C: Local Hugging Face Models (100% Free - No API)

**Run models directly on your computer - completely free!**

This option requires more setup but gives you:
- ✅ **Zero cost** - No API fees ever
- ✅ **No rate limits** - Unlimited usage
- ✅ **Privacy** - All processing happens locally
- ✅ **Offline** - Works without internet

**Requirements**:
- 16+ GB RAM (for 7B models)
- OR 32+ GB RAM (for 13B models)
- OR GPU with 8+ GB VRAM (recommended for speed)

**Recommended Models for Local Use**:
- `meta-llama/Llama-3.2-3B-Instruct` (4 GB RAM, good quality)
- `Qwen/Qwen2.5-7B-Instruct` (8 GB RAM, excellent quality)
- `mistralai/Mistral-7B-Instruct-v0.3` (8 GB RAM, versatile)

Setup instructions in Step 3.3 below.

#### Option D: Google Gemini (Free - Best Free Tier!)

**Google offers the most generous free tier for AI!**

1. Go to https://aistudio.google.com
2. Click "Get API key"
3. Create a new API key
4. Use model: `gemini-2.0-flash-exp` (free, very fast)

**Free Tier Limits** (as of 2025):
- 15 requests per minute
- 1 million tokens per day
- 1,500 requests per day

**Pros**: Most generous free tier, fast, high quality, multimodal support
**Cons**: Slightly lower quality than GPT-4 (but better than GPT-3.5)

#### Option E: Transformers.js (Browser-Based - 100% Free)

**Run AI models directly in the browser - no backend needed!**

This revolutionary option uses WebGPU/WebAssembly to run models client-side:
- ✅ **Zero cost** - Runs in user's browser
- ✅ **No API** - No server needed
- ✅ **Privacy** - All processing happens client-side
- ✅ **Fast** - Uses WebGPU acceleration

**Best Models for Browser**:
- `Xenova/Llama-3.2-1B-Instruct` (1 GB, runs on most devices)
- `Xenova/Phi-3-mini-4k-instruct` (2 GB, good quality)
- `onnx-community/Qwen2.5-3B-Instruct` (3 GB, excellent quality)

**Requirements**: Modern browser with WebGPU support (Chrome 113+, Edge 113+)

Setup instructions in Step 3.4 below.

#### Option F: OpenAI (Free Trial - Limited)

1. Sign up at https://platform.openai.com
2. Get $5 free credit (new accounts)
3. Create API key

**Pros**: High quality, structured output support
**Cons**: Limited free credit ($5), then paid

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

# AI Configuration - Choose ONE option below:

# Option A: Groq (Recommended - Free & Fast)
APP_OPENAI_API_KEY=your-groq-api-key
APP_OPENAI_BASE_URL=https://api.groq.com/openai/v1
APP_OPENAI_MODEL=llama-3.1-70b-versatile

# Option B: Hugging Face Inference API
# APP_OPENAI_API_KEY=your-huggingface-token
# APP_OPENAI_BASE_URL=https://api-inference.huggingface.co/models/meta-llama/Llama-3.1-70B-Instruct
# APP_OPENAI_MODEL=tgi  # Use 'tgi' for Hugging Face TGI-compatible endpoints
# APP_USE_HUGGINGFACE=true

# Option C: Local Hugging Face Models (see Step 3.3 below)
# APP_USE_LOCAL_MODEL=true
# APP_LOCAL_MODEL_NAME=Qwen/Qwen2.5-7B-Instruct
# APP_LOCAL_MODEL_DEVICE=cpu  # or 'cuda' if you have GPU

# Option D: Google Gemini (Recommended - Best Free Tier!)
# APP_GEMINI_API_KEY=your-gemini-api-key
# APP_USE_GEMINI=true
# APP_GEMINI_MODEL=gemini-2.0-flash-exp

# Option E: Transformers.js (Browser-based - see Step 3.4 below)
# This runs in the frontend, no backend config needed!

# Option F: OpenAI (Free Trial - Limited)
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

### 3.4 Set Up Local Hugging Face Models (Optional)

**Only follow this if you chose Option C (Local Models) in Step 2.2**

#### Install Dependencies

```bash
# Add to pyproject.toml dependencies
uv pip install transformers torch accelerate bitsandbytes
```

#### Create Model Service

Create `amber_aim/src/aim/services/local_llm.py`:

```python
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

class LocalLLMService:
    def __init__(self, model_name: str, device: str = "cpu"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.float16 if device == "cuda" else torch.float32,
            device_map=device,
            load_in_8bit=True if device == "cuda" else False,  # Quantization for GPU
        )
        self.device = device

    def generate(self, prompt: str, max_tokens: int = 2000) -> str:
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)
        outputs = self.model.generate(
            **inputs,
            max_new_tokens=max_tokens,
            temperature=0.7,
            do_sample=True,
        )
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)
```

#### Update agent.py to use Local Model

In `amber_aim/src/aim/services/agent.py`, replace OpenAI client:

```python
from aim.services.local_llm import LocalLLMService
from aim.config import Settings

settings = Settings()

if settings.use_local_model:
    llm = LocalLLMService(
        model_name=settings.local_model_name,
        device=settings.local_model_device
    )
    # Use llm.generate() instead of OpenAI client
```

**Note**: Local models are slower but completely free and private.

### 3.5 Set Up Transformers.js (Browser-Based - Optional)

**Only follow this if you chose Option E (Transformers.js) in Step 2.2**

#### Install in Frontend

```bash
cd amber_aim_web
npm install @huggingface/transformers
```

#### Create AI Service in Frontend

Create `amber_aim_web/src/lib/ai-service.ts`:

```typescript
import { pipeline } from '@huggingface/transformers';

class AIService {
  private generator: any = null;

  async initialize() {
    if (!this.generator) {
      // Load model in browser
      this.generator = await pipeline(
        'text-generation',
        'onnx-community/Qwen2.5-3B-Instruct',
        { device: 'webgpu' }  // Use WebGPU for acceleration
      );
    }
  }

  async generate(prompt: string): Promise<string> {
    await this.initialize();
    const result = await this.generator(prompt, {
      max_new_tokens: 2000,
      temperature: 0.7,
    });
    return result[0].generated_text;
  }
}

export const aiService = new AIService();
```

#### Use in Components

```typescript
import { aiService } from '@/lib/ai-service';

// In your component
const result = await aiService.generate("Your prompt here");
```

**Benefits**:
- ✅ No backend needed for AI processing
- ✅ Works offline once model is cached
- ✅ Privacy - data never leaves browser
- ✅ Zero API costs

**Limitations**:
- Slower than cloud APIs on first load (model download)
- Requires modern browser with WebGPU
- Smaller models = lower quality

### 3.6 Set Up Google Gemini (Optional)

**Only follow this if you chose Option D (Gemini) in Step 2.2**

#### Install SDK

```bash
cd amber_aim
uv pip install google-generativeai
```

#### Create Gemini Service

Create `amber_aim/src/aim/services/gemini_service.py`:

```python
import google.generativeai as genai
from aim.config import Settings

settings = Settings()
genai.configure(api_key=settings.gemini_api_key)

class GeminiService:
    def __init__(self):
        self.model = genai.GenerativeModel(settings.gemini_model)

    def generate(self, prompt: str) -> str:
        response = self.model.generate_content(prompt)
        return response.text
```

#### Update config.py

```python
gemini_api_key: str | None = None
use_gemini: bool = False
gemini_model: str = "gemini-2.0-flash-exp"
```

**Why Gemini?**
- 1M tokens/day free (vs OpenAI's $5 credit)
- Fast inference
- Multimodal support (can analyze video frames)
- Better free tier than any alternative

### 3.7 Run Backend Locally

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
| AI API (10M tokens) | ~$100-300 | **$0** (Groq/Gemini/Local) |
| Backend Server | ~$5-50 | **$0** (Render free tier) |
| Frontend Hosting | ~$0-20 | **$0** (Vercel free tier) |
| **TOTAL** | **$116-381/month** | **$0/month** |

**Note**: With Transformers.js, you can even run AI in the browser for zero backend costs!

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

### AI Services

**Groq**
- ✅ Unlimited free tier (as of 2025)
- No restrictions on usage

**Google Gemini**
- 15 requests/minute
- 1 million tokens/day
- 1,500 requests/day
- **Solution**: More than enough for most use cases

**Hugging Face Inference API**
- 1,000 requests/day on free tier
- **Solution**: Use for lower-volume projects or upgrade to Pro ($9/month)

**Local Models & Transformers.js**
- ✅ No limits! Completely free
- **Trade-off**: Slower inference, requires local resources

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

### AI Service Issues

**Groq - Model not available**
- Try alternative model: `mixtral-8x7b-32768`

**Gemini - Rate limit exceeded**
- Implement request caching
- Add delays between requests (15 req/min limit)

**Hugging Face - Model loading timeout**
- Use smaller model (e.g., Llama-3.2-3B instead of 70B)
- Switch to dedicated endpoint (Pro plan)

**Local Models - Out of memory**
- Reduce model size (use 3B instead of 7B)
- Enable quantization (8-bit or 4-bit)
- Close other applications

**Transformers.js - WebGPU not supported**
- Update browser to Chrome 113+ or Edge 113+
- Fall back to CPU mode (slower): `{ device: 'wasm' }`

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

### Infrastructure
✅ **Cloudflare R2** - Free 10 GB storage
✅ **Render** - Free backend hosting (with cold starts)
✅ **Vercel** - Free frontend hosting
✅ **UptimeRobot** - Free monitoring to avoid cold starts

### AI Services (Choose ONE)
✅ **Groq** - Free unlimited LLM inference (Recommended for speed)
✅ **Google Gemini** - Free 1M tokens/day (Recommended for best free tier)
✅ **Hugging Face API** - Free 1K requests/day (Access to 100K+ models)
✅ **Local Models** - Unlimited free usage (Requires 8+ GB RAM)
✅ **Transformers.js** - Browser-based AI (No backend needed)

### Video Analysis
✅ **TwelveLabs** - Free tier video analysis

**Total cost: $0/month** for small-scale usage!

### Recommended Setup for Beginners
- **Storage**: Cloudflare R2 (10 GB free)
- **AI**: Google Gemini (1M tokens/day) or Groq (unlimited)
- **Backend**: Render (free tier + UptimeRobot)
- **Frontend**: Vercel (free tier)
- **Total Setup Time**: ~30 minutes
- **Monthly Cost**: $0

---

## Need Help?

### Documentation Links

**Video Analysis**
- TwelveLabs Docs: https://docs.twelvelabs.io

**AI Services**
- Groq Docs: https://console.groq.com/docs
- Google Gemini Docs: https://ai.google.dev/gemini-api/docs
- Hugging Face Docs: https://huggingface.co/docs/api-inference
- Transformers.js Docs: https://huggingface.co/docs/transformers.js
- Local Models (Hugging Face): https://huggingface.co/docs/transformers

**Infrastructure**
- Cloudflare R2 Docs: https://developers.cloudflare.com/r2
- Render Docs: https://render.com/docs
- Vercel Docs: https://vercel.com/docs
- UptimeRobot: https://uptimerobot.com

Happy deploying! 🚀

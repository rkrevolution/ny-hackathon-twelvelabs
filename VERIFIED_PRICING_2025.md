# VERIFIED Free Tier Pricing (Triple-Checked)

**Last Verified**: October 21, 2025
**Sources**: Official provider websites and documentation

⚠️ **IMPORTANT**: This document contains verified, accurate pricing information. Previous estimates have been corrected based on official sources.

---

## 🚨 Major Corrections from Previous Docs

### ❌ INCORRECT Information I Previously Gave:

1. **Firebase Storage**: Said "5 GB free" ❌
   - **ACTUAL**: Only **1 GB free** on Spark plan
   - **BREAKING CHANGE**: As of Oct 2024, new buckets require paid Blaze plan

2. **Groq API**: Said "unlimited free tier" ❌
   - **ACTUAL**: Has **rate limits** (not unlimited)
   - Exact limits not publicly disclosed, but definitely has caps

3. **Google Gemini**: Said "1M tokens/day" ❌
   - **ACTUAL**: 1M tokens per **MINUTE** (throughput), but only **1,500 requests/day**
   - Big difference!

4. **Hugging Face API**: Said "1,000 requests/day" ❌
   - **ACTUAL**: "Few hundred requests per **hour**" (vague, undocumented)

---

## ✅ VERIFIED Storage Pricing

### Cloudflare R2 ⭐ BEST (S3-compatible, uses boto3)

**Free Tier** (verified from cloudflare.com):
- ✅ **10 GB storage** (at any given time, not cumulative)
- ✅ **10 million operations/month** (Class B)
- ✅ **Unlimited egress** (zero bandwidth fees!)

**After Free Tier**:
- $0.015 per GB/month storage
- Still zero egress fees

**Important**: The 10 GB is a capacity limit (like a container), not monthly cumulative.

**Requires**: boto3 (S3-compatible API)

---

### Backblaze B2 ⭐ BEST (No S3, no boto3)

**Free Tier** (verified from backblaze.com):
- ✅ **10 GB storage** (first 10 GB always free)
- ✅ **1 GB/day downloads** (first 1 GB/day free)
- ✅ **Free Class A API calls**
- ✅ **2,500/day Class B & C calls free**

**After Free Tier**:
- $0.005 per GB/month ($6/TB) - **CHEAPEST!**
- $0.01 per GB download (after 1 GB/day)

**Requires**: b2sdk (native Python SDK, NO boto3)

**Best for**: No-boto3 deployments with good storage

---

### Supabase Storage ⚠️ LIMITED

**Free Tier** (verified from supabase.com):
- ⚠️ **1 GB storage only**
- ✅ **Unlimited bandwidth**
- ⚠️ **Projects pause after 1 week inactivity**
- ⚠️ **Max 2 active free projects**

**After Free Tier**:
- $25/month Pro plan (includes 100 GB storage)
- $0.021 per GB/month for overages

**Requires**: supabase Python client (NO boto3)

**Best for**: Testing/demos only (not production due to 1 GB limit)

---

### Firebase Storage ⚠️ MAJOR CHANGES

**Free Tier (Spark Plan)** (verified from firebase.google.com):
- ⚠️ **1 GB storage** (NOT 5 GB!)
- ⚠️ **10 GB downloads/month**

**🚨 CRITICAL CHANGES (as of Oct 2024)**:
- **New buckets require paid Blaze plan** (starting Oct 30, 2024)
- **Existing buckets require Blaze plan** (by Oct 1, 2025)
- Legacy buckets keep free tier limits on Blaze

**After Free Tier** (Blaze Plan):
- $0.026 per GB/month storage
- $0.15 per GB download

**Requires**: firebase-admin SDK (NO boto3)

**Verdict**: ❌ **NOT RECOMMENDED** due to forced upgrade to Blaze plan

---

## ✅ VERIFIED AI Service Pricing

### Groq API ⚠️ NOT UNLIMITED

**Free Tier** (verified from groq.com):
- ⚠️ **Has rate limits** (NOT unlimited as I said before!)
- Exact limits **not publicly disclosed**
- Described as "generous" but capped
- Free tier exists, but with quotas

**Rate Limiting**:
- Applied at organization level
- Can view exact limits in account settings
- Cached tokens don't count toward limits

**Developer Tier**:
- 10x higher limits than free tier
- Requires payment

**Models Available**:
- llama-3.1-70b-versatile
- llama-3.1-8b-instant
- mixtral-8x7b-32768
- gemma2-9b-it

**Requires**: OpenAI Python SDK (OpenAI-compatible API)

**Verdict**: ✅ Still good, but **NOT unlimited**. Expect rate limits.

---

### Google Gemini API ⭐ BEST FREE TIER

**Free Tier - Gemini 1.5 Flash** (verified from ai.google.dev):
- ✅ **1,500 requests/day** (daily quota)
- ✅ **15 requests/minute** (rate limit)
- ✅ **1M tokens/minute** (throughput, NOT daily limit!)

**Free Tier - Gemini 2.5 Flash**:
- 10 requests/minute
- 250 requests/day
- 250,000 tokens/minute

**Free Tier - Gemini 2.5 Flash-Lite**:
- 15 requests/minute
- 1,000 requests/day
- 250,000 tokens/minute

**Important Clarification**:
- ❌ **NOT** 1M tokens/day
- ✅ 1M tokens/minute = throughput speed
- ✅ 1,500 requests/day = actual daily limit

**After Free Tier**:
- Gemini 1.5 Flash: $0.075 per 1M input tokens
- Gemini 1.5 Pro: $1.25 per 1M input tokens

**Requires**: google-generativeai SDK

**Verdict**: ⭐ **BEST FREE TIER** - 1,500 requests/day is generous

---

### Hugging Face Inference API ⚠️ VAGUE LIMITS

**Free Tier** (verified from huggingface.co):
- ⚠️ **"Few hundred requests per hour"** (not specific!)
- ❌ **NOT** 1,000 requests/day as I said
- No official documented limits
- Monthly credits system

**PRO Tier** ($9/month):
- 20x more credits than free tier
- Higher rate limits

**Requires**: requests library (REST API) or OpenAI SDK

**Verdict**: ⚠️ **Unclear limits** - use with caution for production

---

### OpenAI (Limited Free Trial)

**Free Trial**:
- ❌ **$5 credit only** (NOT unlimited)
- Expires after 3 months
- Requires credit card

**Paid Pricing**:
- GPT-4o: $2.50/$10 per 1M tokens (input/output)
- GPT-4o-mini: $0.15/$0.60 per 1M tokens
- GPT-3.5-turbo: $0.50/$1.50 per 1M tokens

**Verdict**: ❌ Not truly free

---

## ✅ VERIFIED Video Analysis Pricing

### TwelveLabs API

**Free Tier** (verified from twelvelabs.io):
- ✅ **10 hours (600 minutes) video indexing**
- ⚠️ **Indexes expire after 90 days**
- **Daily API Limits**:
  - Search: 50 calls/day
  - Summarize: 50 calls/day
  - Generate: 50 calls/day
  - Embed: 100 calls/day
  - Task: 50 calls/day

**Indexing Options (Free)**:
- Marengo: Visual, Audio, Text, Logo
- Pegasus: Visual, Audio
- Embed API: Video, Audio, Image, Text

**After Free Tier**:
- Developer plan (paid)
- Enterprise plan (custom pricing)

**Verdict**: ✅ Good for testing (10 hours = 60-120 videos depending on length)

---

## ✅ VERIFIED Hosting Pricing

### Render.com

**Free Tier** (verified from render.com):
- ✅ **750 hours/month** (enough for 1 service 24/7)
- ✅ **512 MB RAM**
- ✅ **0.1 vCPU**
- ⚠️ **Sleeps after 15 min inactivity**
- ✅ **100 GB bandwidth**
- ✅ **500 build minutes/month**

**Shared Pool**:
- All free services share 750-hour pool
- Hours reset monthly (don't roll over)
- If depleted, services suspended until next month

**After Free Tier**:
- Starter: $7/month (always-on, 512 MB RAM)
- Standard: $25/month (2 GB RAM)

**Verdict**: ✅ Great for free hosting with cold start trade-off

---

### Vercel

**Free Tier (Hobby Plan)** (verified from vercel.com):
- ✅ **100 GB bandwidth/month**
- ✅ **Unlimited projects**
- ✅ **1,000 build minutes/month**
- ✅ **100 GB-hours serverless function execution**
- ✅ **150,000 serverless function invocations**

**Important Limits**:
- ⚠️ **Non-commercial use only**
- ⚠️ **Hard caps** - can't buy overages
- ⚠️ **30-day rolling window** for usage
- When limit hit, must wait 30 days

**After Free Tier**:
- Pro: $20/month per user
- Higher limits, commercial use allowed

**Verdict**: ✅ Excellent for hobby/personal projects

---

## 📊 Corrected Comparison Tables

### Storage (No boto3 Options)

| Service | Free Storage | Downloads | boto3? | Verdict |
|---------|--------------|-----------|--------|---------|
| **Backblaze B2** ⭐ | **10 GB** | 1 GB/day | ❌ NO | BEST |
| Supabase | 1 GB | Unlimited | ❌ NO | Too small |
| ~~Firebase~~ | ~~1 GB~~ | ~~10 GB/mo~~ | ❌ NO | ❌ Requires paid plan |

### Storage (With boto3 OK)

| Service | Free Storage | Downloads | boto3? | Verdict |
|---------|--------------|-----------|--------|---------|
| **Cloudflare R2** ⭐ | **10 GB** | Unlimited | ✅ YES | BEST |
| Backblaze B2 | 10 GB | 1 GB/day | ❌ NO | Alternative |

### AI Services (Corrected)

| Service | Daily Limit | Cost | Verdict |
|---------|-------------|------|---------|
| **Google Gemini** ⭐ | **1,500 req/day** | FREE | BEST |
| Groq | Rate limited (unknown) | FREE | Good but vague |
| HuggingFace | ~Few hundred/hour | FREE | Very vague |
| OpenAI | $5 credit only | $5 trial | Not free |

---

## 🎯 UPDATED Recommendations

### Best Stack (No boto3, Maximum Storage)

```
Storage:   Backblaze B2 (10 GB free, no boto3) ⭐
AI:        Google Gemini (1,500 req/day) ⭐
Backend:   Render (750 hrs/month, 512 MB)
Frontend:  Vercel (100 GB bandwidth)
Video:     TwelveLabs (10 hours free)

Cost: $0/month
Storage: 10 GB (enough for 20-100 videos)
AI Requests: 1,500/day (enough for heavy use)
```

### Best Stack (With boto3 OK, Maximum Storage)

```
Storage:   Cloudflare R2 (10 GB free, unlimited egress) ⭐
AI:        Google Gemini (1,500 req/day) ⭐
Backend:   Render (750 hrs/month, 512 MB)
Frontend:  Vercel (100 GB bandwidth)
Video:     TwelveLabs (10 hours free)

Cost: $0/month
Storage: 10 GB (enough for 20-100 videos)
AI Requests: 1,500/day (enough for heavy use)
```

---

## ⚠️ What I Got Wrong in Previous Docs

| Service | What I Said | Actually | Impact |
|---------|-------------|----------|---------|
| Firebase | "5 GB free" | 1 GB + requires paid plan | ❌ Major |
| Groq | "Unlimited" | Rate limited (unknown) | ⚠️ Medium |
| Gemini | "1M tokens/day" | 1,500 requests/day | ⚠️ Medium |
| HuggingFace | "1K requests/day" | Few hundred/hour (vague) | ⚠️ Medium |

---

## 💡 Key Takeaways

### For Storage:

1. **If you can use boto3**: Use **Cloudflare R2** (10 GB, unlimited egress)
2. **If you can't use boto3**: Use **Backblaze B2** (10 GB, native SDK)
3. ❌ **Don't use Firebase** - requires paid plan now
4. ❌ **Don't use Supabase** - only 1 GB (too small)

### For AI:

1. **Best free tier**: **Google Gemini** (1,500 requests/day is generous)
2. **Good alternative**: **Groq** (but expect rate limits, not unlimited)
3. ⚠️ **Avoid HuggingFace** - limits too vague for production

### For Video Analysis:

1. **TwelveLabs** - 10 hours free is decent (60-120 videos)
2. Indexes expire after 90 days (plan accordingly)

---

## 📅 Verification Date

**Last Verified**: October 21, 2025

**Next Review Recommended**: January 2026 (quarterly check)

**Sources**:
- cloudflare.com/r2 (R2 pricing)
- backblaze.com/b2 (B2 pricing)
- supabase.com/pricing (Supabase pricing)
- firebase.google.com/pricing (Firebase pricing)
- groq.com/pricing (Groq pricing)
- ai.google.dev/pricing (Gemini pricing)
- huggingface.co/pricing (HF pricing)
- twelvelabs.io/pricing (TwelveLabs pricing)
- render.com/pricing (Render pricing)
- vercel.com/pricing (Vercel pricing)

---

## 🚨 Action Required

**If you're using my previous recommendations**:

1. ✅ **R2/B2 storage** - No changes, still accurate
2. ⚠️ **Groq** - Expect rate limits (not unlimited)
3. ⚠️ **Gemini** - 1,500 requests/day (not 1M tokens/day)
4. ❌ **Firebase** - Switch to B2 or R2 immediately (requires paid plan)

---

**This document contains VERIFIED information only.**
**Previous estimates have been corrected.**
**Date**: October 21, 2025

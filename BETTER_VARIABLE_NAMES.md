# Better Variable Names (No AWS Prefix)

**Date**: October 21, 2025

You're RIGHT - variables shouldn't say "AWS" if you're not using AWS! This guide shows how to fix the naming.

---

## 🤔 The Problem

### Current (Confusing) Naming:
```bash
AWS_ACCESS_KEY_ID=your-cloudflare-r2-key
AWS_SECRET_ACCESS_KEY=your-cloudflare-secret
```

**Problems**:
- ❌ Says "AWS" but it's Cloudflare
- ❌ Misleading for future developers
- ❌ Confusing when debugging
- ❌ Makes you think you need AWS

---

## ✅ Better Naming Options

### Option 1: Use Storage-Specific Names (Recommended)

#### For Cloudflare R2:
```bash
# Instead of AWS_ACCESS_KEY_ID
R2_ACCESS_KEY_ID=your-cloudflare-r2-key
R2_SECRET_ACCESS_KEY=your-cloudflare-secret
R2_ENDPOINT_URL=https://[account-id].r2.cloudflarestorage.com
R2_BUCKET_NAME=vibepoint-videos
R2_REGION=auto
```

#### For Backblaze B2:
```bash
# Clear B2 naming
B2_APPLICATION_KEY_ID=your-b2-key-id
B2_APPLICATION_KEY=your-b2-app-key
B2_BUCKET_NAME=vibepoint-videos
```

---

### Option 2: Use Generic Storage Names

```bash
# Generic, works for any service
STORAGE_ACCESS_KEY_ID=your-key
STORAGE_SECRET_ACCESS_KEY=your-secret
STORAGE_ENDPOINT_URL=https://...
STORAGE_BUCKET_NAME=vibepoint-videos
STORAGE_REGION=auto
```

---

### Option 3: Keep AWS Names (NOT Recommended)

```bash
# Confusing but works with boto3 automatically
AWS_ACCESS_KEY_ID=your-cloudflare-r2-key  # ❌ Misleading!
AWS_SECRET_ACCESS_KEY=your-cloudflare-secret  # ❌ Misleading!
```

**Why people do this**: boto3 library automatically reads `AWS_*` variables
**Why it's bad**: Super confusing, misleading

---

## 🔧 Code Changes for Better Names

### Current Code (Confusing Names)

```python
# config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    aws_s3_bucket: str
    aws_region: str = "us-east-1"

    class Config:
        env_prefix = "APP_"
```

```python
# s3_service.py
import boto3

class S3Service:
    def __init__(self, settings):
        self.s3_client = boto3.client(
            "s3",
            region_name=settings.aws_region,
            # boto3 reads AWS_ACCESS_KEY_ID automatically
        )
```

---

### Updated Code (Clear Names) ⭐ RECOMMENDED

```python
# config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Storage settings (clear naming)
    storage_access_key_id: str
    storage_secret_access_key: str
    storage_endpoint_url: str | None = None
    storage_bucket_name: str
    storage_region: str = "auto"

    class Config:
        env_prefix = "APP_"
```

```python
# storage_service.py (renamed from s3_service.py)
import boto3
from botocore.config import Config

class StorageService:
    def __init__(self, settings):
        self.s3_client = boto3.client(
            "s3",
            region_name=settings.storage_region,
            endpoint_url=settings.storage_endpoint_url,
            aws_access_key_id=settings.storage_access_key_id,  # Explicit pass
            aws_secret_access_key=settings.storage_secret_access_key,
            config=Config(signature_version="s3v4"),
        )
        self.bucket = settings.storage_bucket_name
```

```bash
# .env (clear naming)
APP_STORAGE_ACCESS_KEY_ID=your-r2-key
APP_STORAGE_SECRET_ACCESS_KEY=your-r2-secret
APP_STORAGE_ENDPOINT_URL=https://[account-id].r2.cloudflarestorage.com
APP_STORAGE_BUCKET_NAME=vibepoint-videos
APP_STORAGE_REGION=auto
```

**Benefits**:
- ✅ Clear what service you're using
- ✅ No AWS confusion
- ✅ Easy to swap storage providers
- ✅ Better documentation

---

## 📊 Comparison

| Aspect | AWS_* Names | STORAGE_* Names | R2_* / B2_* Names |
|--------|-------------|-----------------|-------------------|
| **Clarity** | ❌ Poor | ✅ Good | ✅ Excellent |
| **Misleading** | ❌ Yes | ✅ No | ✅ No |
| **Code Changes** | ✅ None | ⚠️ Some | ⚠️ Some |
| **boto3 Auto-read** | ✅ Yes | ❌ No | ❌ No |
| **Maintainability** | ❌ Poor | ✅ Good | ✅ Excellent |
| **Future-proof** | ❌ No | ✅ Yes | ⚠️ Service-specific |

---

## 🎯 My Recommendation

### Use Generic `STORAGE_*` Names ⭐

**Why**:
1. ✅ Not misleading (doesn't say AWS)
2. ✅ Provider-agnostic (works with R2, B2, S3, etc.)
3. ✅ Easy to swap providers later
4. ✅ Clear purpose (storage)
5. ⚠️ Requires small code changes (but worth it!)

### Implementation Steps:

**Step 1: Update config.py**
```python
# Change from:
aws_s3_bucket: str
aws_region: str

# To:
storage_bucket_name: str
storage_region: str
storage_access_key_id: str
storage_secret_access_key: str
storage_endpoint_url: str | None = None
```

**Step 2: Update storage_service.py**
```python
# Explicitly pass credentials to boto3
self.s3_client = boto3.client(
    "s3",
    aws_access_key_id=settings.storage_access_key_id,
    aws_secret_access_key=settings.storage_secret_access_key,
    # ... rest
)
```

**Step 3: Update .env**
```bash
# Change from:
APP_AWS_S3_BUCKET=...
AWS_ACCESS_KEY_ID=...

# To:
APP_STORAGE_BUCKET_NAME=...
APP_STORAGE_ACCESS_KEY_ID=...
APP_STORAGE_SECRET_ACCESS_KEY=...
APP_STORAGE_ENDPOINT_URL=...
```

**Total changes**: ~10 lines of code
**Time**: 5 minutes
**Clarity gained**: 💯

---

## 🔄 Migration Guide

### From AWS_* to STORAGE_*

**1. Update config.py**
```python
# amber_aim/src/aim/config.py

# OLD:
class Settings(BaseSettings):
    aws_s3_bucket: str
    aws_region: str = "us-east-1"
    upload_url_expiration: int = 1800
    s3_base_path: str = "upload"
    log_level: str = "INFO"

# NEW:
class Settings(BaseSettings):
    # Storage configuration
    storage_bucket_name: str
    storage_region: str = "auto"
    storage_access_key_id: str
    storage_secret_access_key: str
    storage_endpoint_url: str | None = None

    # App configuration
    upload_url_expiration: int = 1800
    s3_base_path: str = "upload"
    log_level: str = "INFO"
```

**2. Update s3_service.py (or rename to storage_service.py)**
```python
# amber_aim/src/aim/services/s3_service.py

# OLD:
def __init__(self, settings: Settings):
    self.s3_client = boto3.client(
        "s3",
        region_name=settings.aws_region,
        config=Config(signature_version="s3v4"),
    )
    self.bucket = settings.aws_s3_bucket

# NEW:
def __init__(self, settings: Settings):
    self.s3_client = boto3.client(
        "s3",
        region_name=settings.storage_region,
        endpoint_url=settings.storage_endpoint_url,
        aws_access_key_id=settings.storage_access_key_id,
        aws_secret_access_key=settings.storage_secret_access_key,
        config=Config(signature_version="s3v4"),
    )
    self.bucket = settings.storage_bucket_name
```

**3. Update .env**
```bash
# OLD .env:
APP_AWS_S3_BUCKET=vibepoint-videos
APP_AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=your-key
AWS_SECRET_ACCESS_KEY=your-secret

# NEW .env:
APP_STORAGE_BUCKET_NAME=vibepoint-videos
APP_STORAGE_REGION=auto
APP_STORAGE_ACCESS_KEY_ID=your-r2-or-b2-key
APP_STORAGE_SECRET_ACCESS_KEY=your-r2-or-b2-secret
APP_STORAGE_ENDPOINT_URL=https://[account-id].r2.cloudflarestorage.com
```

**4. Update all references**
```bash
# Search and replace in codebase
settings.aws_s3_bucket → settings.storage_bucket_name
settings.aws_region → settings.storage_region
```

---

## 📝 Complete Example

### Before (Confusing):
```bash
# .env
APP_AWS_S3_BUCKET=vibepoint-videos
APP_AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=abc123...
AWS_SECRET_ACCESS_KEY=xyz789...

# But you're using Cloudflare R2, not AWS! ❌
```

### After (Clear):
```bash
# .env
APP_STORAGE_BUCKET_NAME=vibepoint-videos
APP_STORAGE_REGION=auto
APP_STORAGE_ACCESS_KEY_ID=abc123...
APP_STORAGE_SECRET_ACCESS_KEY=xyz789...
APP_STORAGE_ENDPOINT_URL=https://abc.r2.cloudflarestorage.com
APP_STORAGE_PROVIDER=cloudflare-r2  # Optional: document which provider

# Clear that it's NOT AWS! ✅
```

---

## 🎨 Service-Specific Naming (Alternative)

If you want to be VERY specific about the provider:

### For Cloudflare R2:
```bash
APP_R2_BUCKET_NAME=vibepoint-videos
APP_R2_ACCESS_KEY_ID=...
APP_R2_SECRET_ACCESS_KEY=...
APP_R2_ENDPOINT_URL=...
APP_R2_REGION=auto
```

### For Backblaze B2:
```bash
APP_B2_BUCKET_NAME=vibepoint-videos
APP_B2_APPLICATION_KEY_ID=...
APP_B2_APPLICATION_KEY=...
APP_B2_ENDPOINT_URL=...
```

**Pros**: Crystal clear which service
**Cons**: Harder to swap providers (need to rename variables)

---

## 💡 Why boto3 Uses AWS_* by Default

**Historical reason**: boto3 was built for AWS S3

**How it works**:
1. boto3 automatically looks for `AWS_ACCESS_KEY_ID` environment variable
2. If found, uses it without needing to pass explicitly
3. This is convenient but misleading if not using AWS

**Solution**: Pass credentials explicitly
```python
# Instead of relying on AWS_* env vars
boto3.client(
    "s3",
    aws_access_key_id=your_custom_var,  # Explicit
    aws_secret_access_key=your_custom_var,  # Explicit
)
```

---

## ✅ Recommended Variable Names

### All Services (Complete List)

```bash
# Storage (Cloudflare R2 or Backblaze B2)
APP_STORAGE_PROVIDER=cloudflare-r2  # or backblaze-b2
APP_STORAGE_BUCKET_NAME=vibepoint-videos
APP_STORAGE_REGION=auto
APP_STORAGE_ACCESS_KEY_ID=...
APP_STORAGE_SECRET_ACCESS_KEY=...
APP_STORAGE_ENDPOINT_URL=https://...
APP_UPLOAD_URL_EXPIRATION=1800
APP_S3_BASE_PATH=upload

# AI Service (Google Gemini or Groq)
APP_AI_PROVIDER=gemini  # or groq
APP_AI_API_KEY=...
APP_AI_MODEL=gemini-2.0-flash-exp
APP_AI_BASE_URL=https://...  # if needed

# Video Analysis (TwelveLabs)
APP_VIDEO_ANALYSIS_PROVIDER=twelvelabs
APP_VIDEO_API_KEY=...
APP_VIDEO_CREATORS_INDEX_ID=...
APP_VIDEO_ADS_INDEX_ID=...

# Application
APP_LOG_LEVEL=INFO
```

**Clear, descriptive, NO AWS confusion!**

---

## 🎯 Summary

### Should variables say "AWS" if you're not using AWS?

**Answer**: ❌ **NO!**

### Better alternatives:

1. **Best**: `STORAGE_*` (generic, swappable)
2. **Good**: `R2_*` or `B2_*` (service-specific)
3. **Worst**: `AWS_*` (misleading)

### Code changes needed:

- Update `config.py`: ~5 lines
- Update `s3_service.py`: ~5 lines
- Update `.env`: ~5 lines
- Total time: 5 minutes
- Clarity gained: 💯

### Recommendation:

✅ **Use `STORAGE_*` prefix** for all storage-related variables
- Not misleading
- Provider-agnostic
- Easy to maintain
- Worth the small code change!

---

**Date**: October 21, 2025
**TL;DR**: Don't use AWS_* names if you're not using AWS. Use STORAGE_* instead!

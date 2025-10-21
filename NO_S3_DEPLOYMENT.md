# Free Deployment WITHOUT S3 or boto3

**Date**: October 21, 2025

This guide shows how to deploy VibePoint **without using S3, R2, or boto3** - using completely different storage solutions.

---

## Why No S3/boto3?

You don't want to:
- ❌ Use AWS S3
- ❌ Use Cloudflare R2 (S3-compatible)
- ❌ Use boto3 library
- ❌ Deal with S3 APIs

**Solution**: Use alternatives with simpler APIs!

---

## Storage Alternatives (No S3, No boto3)

### Option 1: Supabase Storage (Recommended - Easiest)

**What it is**: PostgreSQL-based storage with REST API (NOT S3-compatible)

**Free Tier**:
- 1 GB storage (free forever)
- Unlimited bandwidth
- Built-in CDN
- Simple REST API (no boto3 needed!)

**Setup**:
```bash
# Install Supabase Python client
uv pip install supabase

# No boto3 needed!
```

**Code Example**:
```python
# Replace amber_aim/src/aim/services/s3_service.py with supabase_service.py

from supabase import create_client
import uuid
from datetime import datetime, timedelta

class SupabaseStorageService:
    def __init__(self, url: str, key: str, bucket: str):
        self.client = create_client(url, key)
        self.bucket = bucket

    def generate_upload_url(self, filename: str) -> dict:
        """Generate signed upload URL for Supabase Storage"""
        # Generate unique filename
        file_ext = filename.split('.')[-1]
        unique_name = f"{uuid.uuid4()}.{file_ext}"
        path = f"upload/{unique_name}"

        # Create signed upload URL (valid for 30 minutes)
        signed_url = self.client.storage.from_(self.bucket).create_signed_upload_url(path)

        return {
            "upload_url": signed_url['signedURL'],
            "path": path,
            "expires_in": 1800,
            "expires_at": (datetime.utcnow() + timedelta(seconds=1800)).isoformat() + "Z"
        }

    def get_public_url(self, path: str) -> str:
        """Get public URL for uploaded video"""
        return self.client.storage.from_(self.bucket).get_public_url(path)
```

**Environment Variables**:
```bash
# .env - NO AWS/boto3 variables!
APP_SUPABASE_URL=https://your-project.supabase.co
APP_SUPABASE_KEY=your-anon-key
APP_SUPABASE_BUCKET=videos

# Remove these:
# APP_AWS_S3_BUCKET=...
# APP_AWS_REGION=...
# AWS_ACCESS_KEY_ID=...
# AWS_SECRET_ACCESS_KEY=...
```

**Pros**:
- ✅ No boto3 dependency
- ✅ Simple REST API
- ✅ Free 1 GB (enough for ~5-10 videos)
- ✅ Built-in PostgreSQL database (bonus!)
- ✅ Easy authentication
- ✅ Automatic CDN

**Cons**:
- ⚠️ Only 1 GB free (vs R2's 10 GB)
- ⚠️ Need to upgrade for more storage

**Get Started**:
1. Sign up at https://supabase.com
2. Create new project
3. Go to Storage > Create bucket: "videos"
4. Get URL and anon key from Settings > API
5. Update code (see below)

---

### Option 2: Firebase Storage (Google Cloud)

**What it is**: Google's cloud storage with Firebase SDK (NOT S3-compatible)

**Free Tier**:
- 5 GB storage
- 1 GB/day downloads
- Simple SDK (no boto3!)

**Setup**:
```bash
# Install Firebase Admin SDK
uv pip install firebase-admin

# No boto3 needed!
```

**Code Example**:
```python
# Replace s3_service.py with firebase_service.py

import firebase_admin
from firebase_admin import credentials, storage
import uuid
from datetime import timedelta

class FirebaseStorageService:
    def __init__(self, cred_path: str, bucket_name: str):
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred, {
            'storageBucket': bucket_name
        })
        self.bucket = storage.bucket()

    def generate_upload_url(self, filename: str) -> dict:
        """Generate signed upload URL for Firebase Storage"""
        file_ext = filename.split('.')[-1]
        unique_name = f"upload/{uuid.uuid4()}.{file_ext}"
        blob = self.bucket.blob(unique_name)

        # Generate signed URL valid for 30 minutes
        url = blob.generate_signed_url(
            version="v4",
            expiration=timedelta(minutes=30),
            method="PUT"
        )

        return {
            "upload_url": url,
            "path": unique_name,
            "expires_in": 1800
        }

    def get_public_url(self, path: str) -> str:
        """Get public URL"""
        blob = self.bucket.blob(path)
        blob.make_public()
        return blob.public_url
```

**Environment Variables**:
```bash
# .env - NO AWS/boto3!
APP_FIREBASE_CREDENTIALS=/path/to/serviceAccountKey.json
APP_FIREBASE_BUCKET=your-project.appspot.com

# Remove AWS variables
```

**Pros**:
- ✅ No boto3
- ✅ 5 GB free (better than Supabase)
- ✅ Built by Google (reliable)
- ✅ Good documentation

**Cons**:
- ⚠️ Requires service account JSON file
- ⚠️ More complex setup than Supabase

**Get Started**:
1. Create Firebase project at https://console.firebase.google.com
2. Enable Storage
3. Download service account key (Settings > Service Accounts)
4. Update code

---

### Option 3: Direct Upload to Backend (Simplest - No External Storage)

**What it is**: Store videos directly on your backend server

**Free Tier**: Depends on hosting
- Render: 512 MB disk (very limited)
- Railway: 1 GB disk
- Fly.io: 3 GB disk

**Setup**:
```bash
# No external dependencies needed!
# Just use Python's built-in libraries
```

**Code Example**:
```python
# Replace s3_service.py with local_storage_service.py

import os
import uuid
import aiofiles
from pathlib import Path

class LocalStorageService:
    def __init__(self, upload_dir: str = "/app/uploads"):
        self.upload_dir = Path(upload_dir)
        self.upload_dir.mkdir(parents=True, exist_ok=True)

    async def save_file(self, file, filename: str) -> dict:
        """Save file directly to local disk"""
        file_ext = filename.split('.')[-1]
        unique_name = f"{uuid.uuid4()}.{file_ext}"
        file_path = self.upload_dir / unique_name

        # Save file
        async with aiofiles.open(file_path, 'wb') as f:
            content = await file.read()
            await f.write(content)

        return {
            "path": str(file_path),
            "filename": unique_name,
            "url": f"/videos/{unique_name}"
        }

    def get_file_path(self, filename: str) -> Path:
        """Get local file path"""
        return self.upload_dir / filename
```

**FastAPI Endpoint**:
```python
# In main.py
from fastapi import UploadFile, File

@app.post("/upload-direct")
async def upload_video(file: UploadFile = File(...)):
    """Direct file upload to backend"""
    storage = LocalStorageService()
    result = await storage.save_file(file, file.filename)
    return result

@app.get("/videos/{filename}")
async def get_video(filename: str):
    """Serve video file"""
    file_path = storage.get_file_path(filename)
    return FileResponse(file_path)
```

**Environment Variables**:
```bash
# .env - Super simple!
APP_UPLOAD_DIR=/app/uploads

# No AWS, no external storage variables
```

**Pros**:
- ✅ No boto3
- ✅ No external dependencies
- ✅ Simplest code
- ✅ No API keys needed
- ✅ Complete control

**Cons**:
- ⚠️ Limited disk space on free hosting
- ⚠️ Files lost if server restarts (on Render)
- ⚠️ Need persistent volume for production
- ⚠️ Not good for many/large videos

**Best For**: Testing, demos, small projects

---

### Option 4: Backblaze B2 (Native API - No S3 Mode)

**What it is**: Cloud storage with its own API (can avoid S3-compatibility)

**Free Tier**:
- 10 GB storage
- 1 GB/day downloads
- Native Python SDK (no boto3!)

**Setup**:
```bash
# Install B2 SDK (not boto3!)
uv pip install b2sdk

# No boto3 needed!
```

**Code Example**:
```python
# Replace s3_service.py with b2_service.py

from b2sdk.v2 import InMemoryAccountInfo, B2Api
import uuid

class B2StorageService:
    def __init__(self, app_key_id: str, app_key: str, bucket_name: str):
        info = InMemoryAccountInfo()
        self.b2_api = B2Api(info)
        self.b2_api.authorize_account("production", app_key_id, app_key)
        self.bucket = self.b2_api.get_bucket_by_name(bucket_name)

    def generate_upload_url(self, filename: str) -> dict:
        """Generate upload URL for B2"""
        file_ext = filename.split('.')[-1]
        unique_name = f"upload/{uuid.uuid4()}.{file_ext}"

        # Get upload URL
        upload_url_response = self.bucket.get_upload_url()

        return {
            "upload_url": upload_url_response.upload_url,
            "auth_token": upload_url_response.auth_token,
            "path": unique_name
        }

    def upload_file(self, file_path: str, remote_name: str):
        """Direct file upload"""
        self.bucket.upload_local_file(
            local_file=file_path,
            file_name=remote_name
        )
```

**Environment Variables**:
```bash
# .env - NO boto3!
APP_B2_APP_KEY_ID=your-key-id
APP_B2_APP_KEY=your-app-key
APP_B2_BUCKET_NAME=your-bucket

# Remove AWS variables
```

**Pros**:
- ✅ No boto3
- ✅ 10 GB free (same as R2)
- ✅ Native Python SDK
- ✅ Good free tier

**Cons**:
- ⚠️ Less popular than S3/R2
- ⚠️ Different API to learn

**Get Started**:
1. Sign up at https://www.backblaze.com/b2
2. Create bucket
3. Generate app key
4. Update code

---

## Recommended: Supabase Storage

**Why Supabase is best for "no S3/boto3"**:

1. **Simplest API** - Just REST calls
2. **Free tier** - 1 GB forever free
3. **Bonus features** - Get PostgreSQL database too
4. **No boto3** - Uses `supabase` Python client
5. **Good docs** - Easy to learn

---

## Code Migration: Remove boto3

### Step 1: Remove boto3 from dependencies

**OLD** (`pyproject.toml`):
```toml
dependencies = [
    "boto3>=1.29.0",  # REMOVE THIS
    "fastapi>=0.104.0",
    # ... other deps
]
```

**NEW** (`pyproject.toml`):
```toml
dependencies = [
    "supabase>=2.0.0",  # ADD THIS instead
    "fastapi>=0.104.0",
    # ... other deps
]
```

### Step 2: Replace s3_service.py

**Delete**: `amber_aim/src/aim/services/s3_service.py`

**Create**: `amber_aim/src/aim/services/supabase_storage.py`
```python
from supabase import create_client, Client
import uuid
from datetime import datetime, timedelta

class SupabaseStorageService:
    def __init__(self, url: str, key: str, bucket: str):
        self.supabase: Client = create_client(url, key)
        self.bucket = bucket

    def generate_upload_url(self, filename: str) -> dict:
        """Generate upload URL for Supabase Storage"""
        # Generate unique path
        file_ext = filename.split('.')[-1]
        unique_name = f"{uuid.uuid4()}.{file_ext}"
        path = f"upload/{unique_name}"

        # Supabase upload URL
        signed_url = self.supabase.storage.from_(self.bucket).create_signed_upload_url(path)

        return {
            "upload_url": signed_url['signedURL'],
            "s3_path": path,  # Keep same response format
            "expires_in": 1800,
            "expires_at": (datetime.utcnow() + timedelta(seconds=1800)).isoformat() + "Z"
        }

    def get_public_url(self, path: str) -> str:
        """Get public URL"""
        return self.supabase.storage.from_(self.bucket).get_public_url(path)

    def upload_json_file(self, path: str, data: dict):
        """Upload JSON data"""
        import json
        json_bytes = json.dumps(data, indent=2).encode('utf-8')
        self.supabase.storage.from_(self.bucket).upload(
            path,
            json_bytes,
            {"content-type": "application/json"}
        )
```

### Step 3: Update config.py

**OLD**:
```python
aws_s3_bucket: str
aws_region: str = "us-east-1"
```

**NEW**:
```python
supabase_url: str
supabase_key: str
supabase_bucket: str = "videos"
```

### Step 4: Update main.py

**OLD**:
```python
from aim.services.s3_service import S3Service

s3_service = S3Service(settings)
```

**NEW**:
```python
from aim.services.supabase_storage import SupabaseStorageService

storage_service = SupabaseStorageService(
    url=settings.supabase_url,
    key=settings.supabase_key,
    bucket=settings.supabase_bucket
)
```

### Step 5: Update .env

**OLD** (.env):
```bash
APP_AWS_S3_BUCKET=...
APP_AWS_REGION=...
AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...
```

**NEW** (.env):
```bash
APP_SUPABASE_URL=https://xxxxx.supabase.co
APP_SUPABASE_KEY=your-anon-key
APP_SUPABASE_BUCKET=videos
```

---

## Complete Migration Example: boto3 → Supabase

### Before (with boto3/S3)
```python
# s3_service.py
import boto3
from botocore.config import Config

class S3Service:
    def __init__(self, settings):
        self.s3_client = boto3.client(
            "s3",
            region_name=settings.aws_region,
            config=Config(signature_version="s3v4"),
        )
        self.bucket = settings.aws_s3_bucket

    def generate_presigned_url(self, filename: str) -> str:
        key = f"upload/{uuid.uuid4()}.{filename.split('.')[-1]}"
        url = self.s3_client.generate_presigned_url(
            'put_object',
            Params={'Bucket': self.bucket, 'Key': key},
            ExpiresIn=1800
        )
        return url
```

### After (with Supabase, no boto3)
```python
# supabase_storage.py
from supabase import create_client

class SupabaseStorageService:
    def __init__(self, settings):
        self.supabase = create_client(
            settings.supabase_url,
            settings.supabase_key
        )
        self.bucket = settings.supabase_bucket

    def generate_upload_url(self, filename: str) -> dict:
        path = f"upload/{uuid.uuid4()}.{filename.split('.')[-1]}"
        signed = self.supabase.storage.from_(self.bucket).create_signed_upload_url(path)
        return {
            "upload_url": signed['signedURL'],
            "path": path
        }
```

**Difference**: No boto3 import, simpler code!

---

## Full Stack WITHOUT S3/boto3

### Recommended Free Stack

```
Storage:     Supabase Storage (1 GB free, no boto3)
AI:          Groq or Gemini (free, unlimited/1M tokens)
Backend:     Render (750 hrs/month free)
Frontend:    Vercel (unlimited free)
Database:    Supabase PostgreSQL (500 MB free) - Bonus!

Total: $0/month
boto3: NOT NEEDED!
```

---

## Quick Start Commands (No boto3)

### Install Dependencies
```bash
cd amber_aim

# Remove boto3, add Supabase
uv pip uninstall boto3
uv pip install supabase

# Or update pyproject.toml and reinstall
uv pip install -e .
```

### Create Supabase Service
```bash
# Delete old service
rm src/aim/services/s3_service.py

# Create new service
touch src/aim/services/supabase_storage.py
# (Copy code from above)
```

### Update Config
```bash
# Edit .env
nano .env

# Remove AWS variables
# Add Supabase variables
```

### Test
```bash
# Run backend
uvicorn aim.main:app --reload

# Should work without boto3!
```

---

## Comparison: With vs Without boto3

| Aspect | With boto3/S3 | Without boto3 (Supabase) |
|--------|--------------|-------------------------|
| **Dependencies** | boto3, botocore | supabase |
| **Code Complexity** | Medium | Simple |
| **Free Storage** | 10 GB (R2) | 1 GB (Supabase) |
| **Setup Difficulty** | Medium | Easy |
| **API Complexity** | S3 API (complex) | REST API (simple) |
| **Vendor Lock-in** | AWS ecosystem | Supabase ecosystem |

---

## Cost Comparison (No S3/boto3 options)

| Storage | Free Tier | Cost After Free |
|---------|-----------|----------------|
| **Supabase** | 1 GB | $25/mo (Pro: 100 GB) |
| **Firebase** | 5 GB | $0.026/GB/mo |
| **B2** | 10 GB | $0.005/GB/mo |
| **Local Storage** | Depends on host | Depends on host |

**vs S3/R2**:
| Storage | Free Tier | Cost After Free |
|---------|-----------|----------------|
| AWS S3 | None | $0.023/GB/mo |
| Cloudflare R2 | 10 GB | $0.015/GB/mo |

---

## Troubleshooting No-boto3 Setup

### Error: "Module 'boto3' not found"
**Solution**: Good! This means boto3 is removed. Make sure you've installed replacement:
```bash
uv pip install supabase
```

### Error: "Supabase bucket not found"
**Solution**:
1. Go to Supabase dashboard
2. Storage > Create bucket "videos"
3. Make it public if needed

### Uploads Failing
**Solution**: Check signed URL generation:
```python
# Debug
print(signed_url['signedURL'])
# Should start with https://
```

---

## Summary

### What You Get (No S3/boto3):

✅ **No boto3 dependency** - Simpler requirements
✅ **No AWS** - Completely AWS-free
✅ **Simpler code** - REST APIs are easier than S3 API
✅ **Still free** - Supabase/Firebase have good free tiers
✅ **Bonus features** - Supabase includes database!

### What You Lose:

⚠️ **Less storage** - 1 GB (Supabase) vs 10 GB (R2)
⚠️ **Different API** - Need to learn new API
⚠️ **Less common** - Fewer tutorials/resources

### Best Choice:

🌟 **Supabase Storage** - Best no-boto3 option
- 1 GB free forever
- Simple REST API
- Includes PostgreSQL database
- Good documentation
- Easy to use

---

**Date**: October 21, 2025
**Last Updated**: October 21, 2025

Happy deploying without S3! 🚀

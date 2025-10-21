"""Application configuration management."""

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    """Application settings loaded from environment variables.

    All settings are prefixed with APP_ in environment variables.
    Example: APP_AWS_S3_BUCKET=my-bucket

    Attributes:
        aws_s3_bucket: S3-compatible bucket name for video uploads (required)
        aws_region: S3-compatible region (default: us-east-1)
        upload_url_expiration: URL expiration time in seconds (default: 1800)
        s3_base_path: Base path prefix in S3 (default: upload)
        log_level: Logging level (default: INFO)
        twelve_labs_api_key: TwelveLabs API key (required)
        twelve_labs_creators_index_id: TwelveLabs index ID for creator videos (required)
        twelve_labs_ads_index_id: TwelveLabs index ID for ad videos (required)
        cache_dir: Directory for caching TwelveLabs API responses (default: /tmp/twelvelabs_cache)
        cache_ttl_days: Number of days to cache API responses (default: 7)
        rate_limit_state_file: File path for rate limiter state (default: /tmp/twelvelabs_rate_limit.json)
    """

    # S3-compatible storage settings
    aws_s3_bucket: str
    aws_region: str = "us-east-1"
    upload_url_expiration: int = 1800
    s3_base_path: str = "upload"

    # Logging
    log_level: str = "INFO"

    # TwelveLabs API settings
    twelve_labs_api_key: str
    twelve_labs_creators_index_id: str
    twelve_labs_ads_index_id: str

    # Cache and rate limiting settings
    cache_dir: str = "/tmp/twelvelabs_cache"
    cache_ttl_days: int = 7
    rate_limit_state_file: str = "/tmp/twelvelabs_rate_limit.json"

    class Config:
        """Pydantic settings configuration."""

        env_file = ".env"
        env_prefix = "APP_"
        extra = "ignore"

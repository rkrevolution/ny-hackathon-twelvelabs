"""TwelveLabs video analysis service."""

import json
import logging
import random
import time
from pathlib import Path
from typing import Literal, TypedDict

from twelvelabs import TwelveLabs

from aim.models.ads import AdClip, AdSearchResult
from aim.models.placement import PlacementResult
from aim.services import S3Service
from aim.services.cache_service import CacheService
from aim.services.rate_limiter import RateLimiter, RateLimitExceeded

logger = logging.getLogger(__name__)


class TaskResponse(TypedDict):
    """Type definition for TwelveLabs task response."""

    id: str
    video_id: str


class TwelveLabsServiceError(Exception):
    """Base exception for TwelveLabs service errors."""

    def __init__(self, message: str, error_code: str = "TWELVE_LABS_ERROR") -> None:
        """Initialize TwelveLabsServiceError.

        Args:
            message: Error message
            error_code: Error code for classification
        """
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)


class TwelveLabsService:
    """Service for interacting with TwelveLabs API."""

    def __init__(
        self,
        api_key: str,
        creators_index_id: str,
        ads_index_id: str,
        s3_service: S3Service,
        cache_dir: str = "/tmp/twelvelabs_cache",
        rate_limit_state_file: str = "/tmp/twelvelabs_rate_limit.json",
    ) -> None:
        """Initialize TwelveLabs service.

        Args:
            api_key: TwelveLabs API key
            creators_index_id: Index ID for creator videos
            ads_index_id: Index ID for ad videos
            s3_service: S3Service instance
            cache_dir: Directory for caching API responses
            rate_limit_state_file: File path for rate limiter state
        """
        try:
            self.client = TwelveLabs(api_key=api_key)
            self.creators_index_id = creators_index_id
            self.ads_index_id = ads_index_id
            self.s3_service = s3_service

            # Initialize caching and rate limiting with configurable paths
            self.cache = CacheService(cache_dir=cache_dir)
            self.rate_limiter = RateLimiter(state_file=rate_limit_state_file)

            logger.info("TwelveLabs service initialized successfully")
        except Exception as e:
            logger.error("Failed to initialize TwelveLabs client", exc_info=True)
            raise TwelveLabsServiceError(
                "Failed to initialize TwelveLabs client",
                error_code="INITIALIZATION_ERROR",
            ) from e

    def _get_index_id(self, video_type: Literal["creator", "ad"]) -> str:
        """Get the appropriate index ID based on video type.

        Args:
            video_type: Type of video (creator or ad)

        Returns:
            The corresponding index ID

        Raises:
            ValueError: If video_type is invalid
        """
        if video_type == "creator":
            return self.creators_index_id
        elif video_type == "ad":
            return self.ads_index_id
        else:
            raise ValueError(f"Invalid video type: {video_type}")

    def create_video_indexing_task(
        self, video_path: str, video_type: Literal["creator", "ad"]
    ) -> TaskResponse:
        """Create a video indexing task in TwelveLabs.

        Args:
            video_path: Path to the video to analyze
            video_type: Type of video (creator or ad)

        Returns:
            Dictionary containing task ID and video ID

        Raises:
            TwelveLabsServiceError: If the API request fails
        """
        try:
            index_id = self._get_index_id(video_type)
            video_url = self.s3_service.generate_get_url(video_path)

            logger.info(
                "Creating video indexing task",
                extra={
                    "video_path": video_path,
                    "video_url": video_url,
                    "video_type": video_type,
                    "index_id": index_id,
                },
            )

            task = self.client.tasks.create(
                index_id=index_id,
                video_url=video_url,
            )

            result: TaskResponse = {"id": task.id, "video_id": task.video_id}

            logger.info(
                "Video indexing task created successfully",
                extra={
                    "task_id": result["id"],
                    "video_id": result["video_id"],
                    "video_type": video_type,
                },
            )

            return result

        except ValueError as e:
            logger.warning("Invalid video type", extra={"video_type": video_type})
            raise TwelveLabsServiceError(str(e), error_code="INVALID_VIDEO_TYPE") from e

        except Exception as e:
            logger.error("Failed to create video indexing task", exc_info=True)
            raise TwelveLabsServiceError(
                f"Failed to create video indexing task: {str(e)}",
                error_code="API_ERROR",
            ) from e

    def analyze_video(
        self,
        index_id: str,
        video_id: str,
        type: Literal["creator", "ad"],
    ) -> PlacementResult:
        """Analyze a video using TwelveLabs.

        Args:
            index_id: Index ID for the video
            video_id: ID of the video
            type: Type of video (creator or ad)
        """

        task = None
        for task in self.client.tasks.list(index_id=index_id):
            if task.video_id == video_id:
                break

        while True:
            if task is None:
                break

            logger.info("Checking task status", extra={"task_id": task.id})
            if task.status == "ready":
                logger.info("Task completed", extra={"task_id": task.id})
                break
            time.sleep(1)

        prompts = [
            (Path(path).stem, Path(path).read_text())
            for path in sorted(
                Path(__file__).parent.parent.parent.glob("prompts/twelvelabs/*.txt")
            )
        ]
        prompts = [
            (Path(path).stem, Path(path).read_text())
            for path in sorted(
                Path(__file__).parent.parent.parent.glob("prompts/twelvelabs/*.txt")
            )
        ]

        task_id = task.id if task else None
        logger.info(
            f"Loaded {len(prompts)} prompts",
            extra={"task_id": task_id, "video_id": video_id},
        )

        results = {}

        logger.info("Analyzing video", extra={"task_id": task_id, "video_id": video_id})

        for prompt_name, prompt in prompts:
            # Check cache first
            cache_params = {
                'video_id': video_id,
                'prompt_name': prompt_name,
                'prompt': prompt[:50]  # Use first 50 chars as cache key
            }

            cached_result = self.cache.get('analyze', cache_params)
            if cached_result is not None:
                logger.info(
                    f"✅ Cache HIT for prompt {prompt_name}",
                    extra={"video_id": video_id}
                )
                results[prompt_name] = cached_result
                continue

            # Check rate limit
            if not self.rate_limiter.can_make_request('analyze'):
                logger.error(
                    f"⚠️ Rate limit exceeded for analyze endpoint. "
                    f"Remaining: {self.rate_limiter.get_remaining('analyze')}/50"
                )
                raise TwelveLabsServiceError(
                    f"Daily rate limit exceeded for analyze endpoint. "
                    f"Resets at midnight UTC.",
                    error_code="RATE_LIMIT_EXCEEDED"
                )

            # Make API call
            logger.info(
                f"📡 API CALL: Analyzing video with prompt {prompt_name} "
                f"(remaining: {self.rate_limiter.get_remaining('analyze')}/50)",
                extra={"task_id": task_id, "video_id": video_id},
            )

            result = self.client.analyze(
                video_id=video_id, prompt=prompt, temperature=0.2
            )

            # Record usage
            self.rate_limiter.record_request('analyze')

            # Cache result
            self.cache.set('analyze', cache_params, result.data)

            results[prompt_name] = result.data

        logger.info("Saving results", extra={"task_id": task_id, "video_id": video_id})
        with open(f"video_{video_id}.json", "w") as f:
            json.dump(results, f)

        placement_result = self.analyze_with_agent(video_id, results)

        logger.info("Task completed", extra={"task_id": task_id, "results": results})

        return placement_result

    def analyze_with_agent(
        self,
        video_id: str,
        results_data: dict[str, str],
    ) -> PlacementResult:
        """Analyze video results using OpenAI agent and return structured placement data.

        Args:
            video_id: ID of the video
            results_data: Dictionary containing the analysis results from TwelveLabs

        Returns:
            PlacementResult: Structured placement data

        Raises:
            TwelveLabsServiceError: If the agent analysis fails
        """
        try:
            # Load the prompt template
            prompt_path = (
                Path(__file__).parent.parent.parent.parent
                / "prompts"
                / "openai"
                / "prompt.txt"
            )
            logger.info(
                "Loading prompt template", extra={"prompt_path": str(prompt_path)}
            )

            with open(prompt_path) as f:
                prompt_template = f.read()

            # Format context from results data
            context = "\n\n".join(str(value) for value in results_data.values())
            final_prompt = prompt_template.format(context=context)

            # Create and run agent with structured output
            logger.info(
                "Creating agent for video analysis",
                extra={"video_id": video_id},
            )

            # Import and call the placements agent
            from aim.services.agent import find_placements

            placement_result = find_placements(final_prompt)

            # Save intermediate results to JSON
            output_path = f"video_{video_id}_placement.json"
            logger.info(
                "Saving placement results",
                extra={"video_id": video_id, "output_path": output_path},
            )

            with open(output_path, "w") as f:
                json.dump(placement_result.model_dump(), f, indent=2)

            logger.info(
                "Agent analysis completed successfully",
                extra={"video_id": video_id, "output_path": output_path},
            )

            self.s3_service.upload_json_file(
                f"results/placement_{video_id}.json",
                placement_result.model_dump(),
            )

            return placement_result

        except FileNotFoundError as e:
            logger.error("Prompt template not found", exc_info=True)
            raise TwelveLabsServiceError(
                f"Prompt template not found: {str(e)}",
                error_code="PROMPT_NOT_FOUND",
            ) from e

        except Exception as e:
            logger.error("Failed to analyze with agent", exc_info=True)
            raise TwelveLabsServiceError(
                f"Failed to analyze with agent: {str(e)}",
                error_code="AGENT_ANALYSIS_ERROR",
            ) from e

    def search_ads(
        self,
        query_text: str,
        page_limit: int = 5,
    ) -> list[AdSearchResult]:
        """Search for ads in the ads index using TwelveLabs search API.

        Args:
            query_text: The search query describing the desired ad content
            page_limit: Maximum number of results to return (default: 5)

        Returns:
            List of AdSearchResult objects containing matched ads

        Raises:
            TwelveLabsServiceError: If the search request fails
        """
        try:
            # Check cache first
            cache_params = {
                'index_id': self.ads_index_id,
                'query': query_text,
                'page_limit': page_limit
            }

            cached_result = self.cache.get('search', cache_params)
            if cached_result is not None:
                logger.info(
                    f"✅ Cache HIT for search query: {query_text}",
                    extra={"query": query_text}
                )
                # Convert back to AdSearchResult objects
                return [
                    AdSearchResult(**item) if isinstance(item, dict) else item
                    for item in cached_result
                ]

            # Check rate limit
            if not self.rate_limiter.can_make_request('search'):
                logger.error(
                    f"⚠️ Rate limit exceeded for search endpoint. "
                    f"Remaining: {self.rate_limiter.get_remaining('search')}/50"
                )
                raise TwelveLabsServiceError(
                    f"Daily rate limit exceeded for search endpoint. "
                    f"Resets at midnight UTC.",
                    error_code="RATE_LIMIT_EXCEEDED"
                )

            # Make API call
            logger.info(
                f"📡 API CALL: Searching ads "
                f"(remaining: {self.rate_limiter.get_remaining('search')}/50)",
                extra={
                    "query": query_text,
                    "page_limit": page_limit,
                    "index_id": self.ads_index_id,
                },
            )

            # Remove random sleep - not needed with proper rate limiting
            # time.sleep(random.random() * 3)

            response = self.client.search.query(
                index_id=self.ads_index_id,
                search_options=["visual", "audio"],
                query_text=query_text,
                page_limit=page_limit,
                group_by="video",
                sort_option="score",
            )

            # Record usage
            self.rate_limiter.record_request('search')

            results = []
            for item in response:
                if item.id and item.clips:  # Grouped by video
                    clips = [
                        AdClip(
                            score=float(clip.score) if clip.score is not None else 0.0,
                            start=float(clip.start) if clip.start is not None else 0.0,
                            end=float(clip.end) if clip.end is not None else 0.0,
                            video_id=str(clip.video_id) if clip.video_id else "",
                            confidence=str(clip.confidence) if clip.confidence else "",
                            thumbnail_url=getattr(clip, "thumbnail_url", None),
                            transcription=getattr(clip, "transcription", None),
                        )
                        for clip in item.clips
                        if clip.score is not None and clip.score > 0.7
                    ]
                    results.append(AdSearchResult(id=item.id, clips=clips))

            # Cache results (convert to dict for JSON serialization)
            results_dict = [result.model_dump() for result in results]
            self.cache.set('search', cache_params, results_dict)

            logger.info(
                "✅ Ad search completed",
                extra={"query": query_text, "result_count": len(results)},
            )

            return results

        except Exception as e:
            logger.error("Failed to search ads", exc_info=True)
            raise TwelveLabsServiceError(
                f"Failed to search ads: {str(e)}",
                error_code="SEARCH_ERROR",
            ) from e

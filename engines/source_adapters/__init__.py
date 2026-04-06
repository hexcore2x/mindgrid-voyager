"""Optional live source adapters for social retrieval."""

from .reddit_adapter import RedditAdapter
from .youtube_adapter import YouTubeAdapter

__all__ = ["RedditAdapter", "YouTubeAdapter"]

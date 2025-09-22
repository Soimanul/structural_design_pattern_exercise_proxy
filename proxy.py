"""
Implement a Proxy for the slow RealVideoService that provides:
- Lazy loading: do NOT construct the real service until it's actually needed.
- Caching: cache results of download_compressed(video_id, quality).
"""
from __future__ import annotations
from typing import Callable, Dict, Tuple, Optional, Type
from unittest import result

# NOTE: We only import the class name to use it as a type. The tests may supply
# their own fake service via the factory.
from video_service import RealVideoService

class ProxyVideoService:
    def __init__(self, service_factory: Callable[[], RealVideoService]) -> None:
        """
        Initialize the proxy with a factory that can build the real service.
        Do NOT call the factory here (lazy construction!).
        """
        # TODO: store the factory, set the underlying service to None,
        # and initialize an in-memory cache (e.g., a dict).
        
        if not callable(service_factory):
            raise TypeError("service_factory must be callable and take no args")
        self._service_factory: Callable[[], RealVideoService] = service_factory
        self._service: Optional[RealVideoService] = None
        self._cache: Dict[Tuple[str, str], bytes] = {}
        
    def _ensure_service(self) -> RealVideoService:
        """Construct the real service on demand (only when needed)."""
        # TODO: if we don't have a real service yet, call the factory and store it.
        # Then, return the real service.
        if self._service is None:
            svc = self._service_factory()
            if svc is None:
                raise RuntimeError("service_factory returned None")
            self._service = svc
            
        return self._service

    def download_compressed(self, video_id: str, quality: str) -> bytes:
        """Return compressed bytes for (video_id, quality), using a cache."""
        # TODO:
        # 1) Create a cache key (video_id, quality).
        key: Tuple[str, str] = (video_id, quality)
        # 2) If present in cache, return it directly.
        cached = self._cache.get(key)
        if cached is not None:
            return cached
        # 3) Otherwise, ensure the service exists, call its download_compressed,
        #    store the result in cache, and return it.
        service = self._ensure_service()
        result = service.download_compressed(video_id, quality)
        if not isinstance(result, (bytes,bytearray)):
            raise TypeError("download_compressed must return bytes")
        self._cache[key] = bytes(result)
        return self._cache[key]
        

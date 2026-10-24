"""Storage adapter for Cloudflare R2-backed persistence."""

from __future__ import annotations

from typing import Any, Dict, Optional


class StorageAdapter:
    """Thin wrapper around a Cloudflare R2 client or compatible backend."""

    def __init__(self, client: Optional[Any] = None, bucket: Optional[str] = None):
        self.client = client
        self.bucket = bucket or "default-bucket"

    def get_client(self) -> Any:
        return self.client

    def put_object(self, key: str, value: Any, **kwargs: Dict[str, Any]) -> Any:
        if self.client is None:
            raise RuntimeError("No R2 client configured")
        return self.client.put_object(self.bucket, key, value, **kwargs)

    def get_object(self, key: str, **kwargs: Dict[str, Any]) -> Any:
        if self.client is None:
            raise RuntimeError("No R2 client configured")
        return self.client.get_object(self.bucket, key, **kwargs)

    def delete_object(self, key: str, **kwargs: Dict[str, Any]) -> Any:
        if self.client is None:
            raise RuntimeError("No R2 client configured")
        return self.client.delete_object(self.bucket, key, **kwargs)

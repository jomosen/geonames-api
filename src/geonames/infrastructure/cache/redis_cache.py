from typing import Optional

import redis


class RedisCache:
    """
    Redis implementation of CachePort.
    Stores values as strings (JSON) with optional TTL.
    """

    def __init__(self, client: redis.Redis):
        self._client = client

    def get(self, key: str) -> Optional[str]:
        try:
            return self._client.get(key)
        except redis.RedisError:
            return None

    def set(self, key: str, value: str, ttl: int = 3600) -> None:
        try:
            self._client.setex(key, ttl, value)
        except redis.RedisError:
            pass

    def delete(self, key: str) -> None:
        try:
            self._client.delete(key)
        except redis.RedisError:
            pass

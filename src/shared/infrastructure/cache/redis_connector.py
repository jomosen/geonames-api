import redis


class RedisConnector:
    """
    Manages a Redis connection from a URL.
    Analogous to PostgreSQLConnector in the database layer.
    """

    def __init__(self, url: str):
        self._client = redis.from_url(url, decode_responses=True)

    def get_client(self) -> redis.Redis:
        return self._client

    def ping(self) -> bool:
        try:
            return self._client.ping()
        except redis.RedisError:
            return False

import os
import json
import redis


class RedisClient:
    def __init__(self):
        self.redis_host = os.getenv("REDIS_HOST", "localhost")
        self.redis_port = int(os.getenv("REDIS_PORT", 6379))
        self.redis_password = os.getenv("REDIS_PASSWORD", None)

        # Azure Cache for Redis requires SSL on port 6380.
        # Local Redis uses port 6379 with no SSL.
        # Auto-detect: if port is 6380 or REDIS_SSL=true, enable SSL.
        use_ssl = os.getenv("REDIS_SSL", "false").lower() == "true" or self.redis_port == 6380

        try:
            self.r = redis.Redis(
                host=self.redis_host,
                port=self.redis_port,
                password=self.redis_password,
                ssl=use_ssl,
                decode_responses=True,
                socket_connect_timeout=5,
            )
            # Verify connection
            self.r.ping()
            print(f"✅ Connected to Redis at {self.redis_host}:{self.redis_port} (ssl={use_ssl})")
        except Exception as e:
            print(f"⚠️  Redis connection failed: {e}. Recommendations will not be cached.")
            self.r = None

    def set_recommendations(self, user_id: str, recommendations: list):
        """Stores top-5 recommendations for a user in Redis."""
        if self.r is None:
            return
        try:
            self.r.set(f"recs:{user_id}", json.dumps(recommendations), ex=3600)
        except Exception as e:
            print(f"Redis set error: {e}")

    def get_recommendations(self, user_id: str):
        """Retrieves top-5 recommendations for a user from Redis."""
        if self.r is None:
            return []
        try:
            data = self.r.get(f"recs:{user_id}")
            if data:
                return json.loads(data)
            return []
        except Exception as e:
            print(f"Redis get error: {e}")
            return []


redis_client = RedisClient()

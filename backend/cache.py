import os
import json
import logging
from typing import Optional
from redis.asyncio import Redis, ConnectionPool
from redis.exceptions import RedisError, ConnectionError as RedisConnectionError

# Configuration
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
REDIS_CACHE_TTL = int(os.getenv("REDIS_CACHE_TTL", "300"))  # 5 minutes default
REDIS_ENABLED = os.getenv("REDIS_ENABLED", "true").lower() == "true"

# Logging
logger = logging.getLogger(__name__)

# Global Redis client
redis_client: Optional[Redis] = None
cache_enabled = REDIS_ENABLED
connection_pool: Optional[ConnectionPool] = None


async def initialize_redis():
    """Initialize Redis connection pool"""
    global redis_client, connection_pool, cache_enabled

    if not REDIS_ENABLED:
        logger.info("Redis caching is disabled via configuration")
        cache_enabled = False
        return

    try:
        connection_pool = ConnectionPool.from_url(
            REDIS_URL,
            max_connections=10,
            decode_responses=True,  # Auto-decode bytes to strings
            socket_connect_timeout=5,
            socket_timeout=5,
            retry_on_timeout=True
        )

        redis_client = Redis(connection_pool=connection_pool)

        # Test connection
        await redis_client.ping()
        cache_enabled = True
        logger.info(f"✅ Redis connected at {REDIS_URL}")

    except (RedisError, RedisConnectionError) as e:
        logger.error(f"❌ Redis connection failed: {e}. Caching disabled.")
        cache_enabled = False
        redis_client = None


async def get_cached_session(session_id: str) -> Optional[dict]:
    """Get session from cache"""
    if not cache_enabled or not redis_client:
        return None

    try:
        key = f"session:{session_id}"
        data = await redis_client.get(key)

        if data:
            logger.debug(f"✅ CACHE HIT: {session_id}")
            return json.loads(data)

        logger.debug(f"❌ CACHE MISS: {session_id}")
        return None

    except RedisError as e:
        logger.warning(f"Redis GET error for {session_id}: {e}")
        return None  # Graceful fallback to database


async def set_cached_session(session_id: str, session_data: dict, ttl: int = REDIS_CACHE_TTL):
    """Cache session data"""
    if not cache_enabled or not redis_client:
        return False

    try:
        key = f"session:{session_id}"
        # Serialize GameSession to JSON
        json_data = json.dumps(session_data, default=str)  # default=str handles datetime

        await redis_client.setex(key, ttl, json_data)
        logger.debug(f"✅ CACHED: {session_id} (TTL: {ttl}s)")
        return True

    except RedisError as e:
        logger.warning(f"Redis SET error for {session_id}: {e}")
        return False


async def invalidate_session_cache(session_id: str):
    """Remove session from cache"""
    if not cache_enabled or not redis_client:
        return False

    try:
        key = f"session:{session_id}"
        deleted = await redis_client.delete(key)
        logger.debug(f"🗑️ INVALIDATED: {session_id} (deleted: {deleted})")
        return deleted > 0

    except RedisError as e:
        logger.warning(f"Redis DELETE error for {session_id}: {e}")
        return False


async def check_redis_connection() -> str:
    """Check Redis connection status"""
    if not REDIS_ENABLED:
        return "disabled"

    if not redis_client:
        return "not_initialized"

    try:
        await redis_client.ping()
        return "connected"
    except RedisError:
        return "error"


async def close_redis():
    """Close Redis connection pool"""
    global redis_client, connection_pool

    if redis_client:
        await redis_client.close()
        redis_client = None

    if connection_pool:
        await connection_pool.disconnect()
        connection_pool = None

    logger.info("Redis connection closed")

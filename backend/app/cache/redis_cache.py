import redis
import json

cache = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)


def set_cache(key: str, value: dict, ttl: int = 3600):
    cache.setex(key, ttl, json.dumps(value))


def get_cache(key: str):
    data = cache.get(key)
    return json.loads(data) if data else None
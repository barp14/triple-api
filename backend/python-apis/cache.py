# cache.py
import os
import json
import redis
from redis.exceptions import ConnectionError

REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))

redis_client = redis.StrictRedis(
	host=REDIS_HOST,
	port=REDIS_PORT,
	db=0,
	decode_responses=True
)

def get(key):
	try:
		raw = redis_client.get(key)
		if raw:
			print(f"-----> Hit Cache ")
			return json.loads(raw)
		else:
			print(f"-----> Miss Cache")
			return None
	except ConnectionError:
		print(f"(Connection Error)")
		return None

def set(key, value, expire_seconds=300):
	try:
		redis_client.set(key, json.dumps(value), ex=expire_seconds)
	except ConnectionError:
		pass

def invalidate(key):
	try:
		redis_client.delete(key)
	except ConnectionError:
		pass

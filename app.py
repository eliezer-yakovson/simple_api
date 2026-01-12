from fastapi import FastAPI
from pydantic import BaseModel
import os
import redis

app = FastAPI()

# פרטי Redis
REDIS_HOST = os.getenv("REDIS_SERVICE_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_SERVICE_PORT", "6379"))
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")

r = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    password=REDIS_PASSWORD,
    decode_responses=True
)


class Item(BaseModel):
    key: str
    value: str

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/cache")
def set_cache(item: Item):
    r.set(item.key, item.value)
    return {"saved": item.key}

@app.get("/cache/{key}")
def get_cache(key: str):
    value = r.get(key)
    if value is None:
        return {"error": "not found"}
    return {"key": key, "value": value}

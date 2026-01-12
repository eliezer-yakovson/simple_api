from fastapi import FastAPI
from pydantic import BaseModel
import os
import redis

app = FastAPI()

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))

r = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
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


if __name__ == "__main__":
    import uvicorn
    import os

    port = int(os.getenv("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)

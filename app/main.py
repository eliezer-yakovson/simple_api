from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.redis_client import redis_client

app = FastAPI()


class CacheItem(BaseModel):
    key: str
    value: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/cache")
def set_cache(item: CacheItem):
    redis_client.set(item.key, item.value)
    return {"message": "saved", "key": item.key}


@app.get("/cache/{key}")
def get_cache(key: str):
    value = redis_client.get(key)
    if value is None:
        raise HTTPException(status_code=404, detail="Key not found")
    return {"key": key, "value": value}

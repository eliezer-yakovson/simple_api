from fastapi import FastAPI
from pydantic import BaseModel
import os
import redis

# יצירת אפליקציית FastAPI
app = FastAPI()

# הגדרות Redis דרך Service פנימי של OpenShift
REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))

# חיבור ל-Redis
r = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    decode_responses=True
)

# מודל נתונים ל-POST
class Item(BaseModel):
    key: str
    value: str

# בדיקת חיים
@app.get("/health")
def health():
    return {"status": "ok"}

# שמירה ל-Redis
@app.post("/cache")
def set_cache(item: Item):
    r.set(item.key, item.value)
    return {"saved": item.key}

# שליפה מ-Redis
@app.get("/cache/{key}")
def get_cache(key: str):
    value = r.get(key)
    if value is None:
        return {"error": "not found"}
    return {"key": key, "value": value}

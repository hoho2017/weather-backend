# app.py
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sse_starlette.sse import EventSourceResponse
import os
from extract import generate_images_stream
import asyncio

app = FastAPI()

BASE_IMAGE_DIR = "images"
if not os.path.exists(BASE_IMAGE_DIR):
    os.makedirs(BASE_IMAGE_DIR)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/static", StaticFiles(directory=BASE_IMAGE_DIR), name="static")

@app.get("/images")
async def get_images(lon: float = Query(...), lat: float = Query(...)):
    folder_name = f"lon_{lon}_lat_{lat}"
    folder_path = os.path.join(BASE_IMAGE_DIR, folder_name)

    async def event_generator():
        for url in generate_images_stream(lat, lon, folder_path, folder_name):
            await asyncio.sleep(0)  # 让出事件循环，及时推送
            yield {"event": "image", "data": url}
    return EventSourceResponse(event_generator())
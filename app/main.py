"""InspireWorks Plivo IVR Demo - FastAPI App."""
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
from app.routers import ivr, call

app = FastAPI(title="InspireWorks IVR Demo", version="1.0.0")

app.include_router(ivr.router)
app.include_router(call.router)

static_dir = os.path.join(os.path.dirname(__file__), "static")
app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/")
async def root():
    return FileResponse(os.path.join(static_dir, "index.html"))
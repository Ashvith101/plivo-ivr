"""InspireWorks Plivo IVR Demo - FastAPI App."""
from fastapi import FastAPI
from app.routers import ivr, call

app = FastAPI(title="InspireWorks IVR Demo", version="1.0.0")

app.include_router(ivr.router)
app.include_router(call.router)


@app.get("/")
async def root():
    return {
        "status": "running",
        "endpoints": {
            "trigger_call": "POST /call/trigger",
            "ivr_answer": "POST /ivr/answer",
            "docs": "/docs",
        }
    }

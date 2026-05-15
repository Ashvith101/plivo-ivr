"""Endpoint to trigger outbound calls via Plivo API."""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import plivo
from app.config import (
    PLIVO_AUTH_ID, PLIVO_AUTH_TOKEN,
    PLIVO_FROM_NUMBER, PLIVO_TO_NUMBER, BASE_URL
)

router = APIRouter(prefix="/call", tags=["Call"])


class CallRequest(BaseModel):
    to_number: str | None = None  # override PLIVO_TO_NUMBER if provided


@router.post("/trigger")
async def trigger_call(req: CallRequest = CallRequest()):
    """Trigger an outbound call. to_number defaults to .env PLIVO_TO_NUMBER."""
    to = req.to_number or PLIVO_TO_NUMBER
    if not to:
        raise HTTPException(status_code=400, detail="to_number not configured")

    client = plivo.RestClient(PLIVO_AUTH_ID, PLIVO_AUTH_TOKEN)

    try:
        response = client.calls.create(
            from_=PLIVO_FROM_NUMBER,
            to_=to,
            answer_url=f"{BASE_URL}/ivr/answer",
            answer_method="POST",
        )
        return {"status": "success", "api_id": response["api_id"], "to": to}
    except plivo.exceptions.PlivoRestError as e:
        raise HTTPException(status_code=500, detail=str(e))

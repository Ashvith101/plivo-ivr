"""IVR webhook endpoints - all Plivo XML responses."""
from fastapi import APIRouter, Form, Query
from typing import Optional
from app.config import BASE_URL, OTP_CODE, AUDIO_MP3_URL, PLIVO_ASSOCIATE_NUMBER, PLIVO_FROM_NUMBER
from app.xml_helpers import (
    xml_response, otp_prompt_xml, invalid_otp_xml, language_menu_xml,
    action_menu_xml, play_audio_xml, transfer_call_xml, invalid_input_redirect_xml
)

router = APIRouter(prefix="/ivr", tags=["IVR"])


@router.post("/answer")
async def answer():
    """Called when the outbound call is answered. Start OTP flow."""
    return xml_response(otp_prompt_xml(BASE_URL))


@router.post("/otp-prompt")
async def otp_prompt():
    """Re-prompt for OTP (used on redirect)."""
    return xml_response(otp_prompt_xml(BASE_URL))


@router.post("/validate-otp")
async def validate_otp(Digits: Optional[str] = Form(None)):
    """Validate the entered OTP."""
    if Digits == OTP_CODE:
        return xml_response(language_menu_xml(BASE_URL))
    return xml_response(invalid_otp_xml(BASE_URL))


@router.post("/language-menu")
async def language_menu():
    """Show language selection menu."""
    return xml_response(language_menu_xml(BASE_URL))


@router.post("/language")
async def language(Digits: Optional[str] = Form(None)):
    """Handle language selection."""
    if Digits in ("1", "2"):
        return xml_response(action_menu_xml(BASE_URL, Digits))
    return xml_response(invalid_input_redirect_xml(BASE_URL, "/ivr/language-menu"))


@router.post("/action-menu")
async def action_menu(lang: str = Query("1")):
    """Show action menu for the chosen language."""
    return xml_response(action_menu_xml(BASE_URL, lang))


@router.post("/action")
async def action(
    Digits: Optional[str] = Form(None),
    lang: str = Query("1")
):
    """Handle action selection: play audio or transfer."""
    if Digits == "1":
        return xml_response(play_audio_xml(AUDIO_MP3_URL))
    elif Digits == "2":
        return xml_response(transfer_call_xml(PLIVO_ASSOCIATE_NUMBER, PLIVO_FROM_NUMBER))
    return xml_response(invalid_input_redirect_xml(BASE_URL, f"/ivr/action-menu?lang={lang}"))

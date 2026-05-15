"""Plivo XML response builders."""
from fastapi.responses import Response


def xml_response(content: str) -> Response:
    return Response(content=content, media_type="application/xml")


def otp_prompt_xml(base_url: str, attempt: int = 1) -> str:
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
  <GetDigits action="{base_url}/ivr/validate-otp" method="POST" numDigits="4" timeout="10" retries="1" validDigits="0123456789">
    <Speak>Please enter your 4 digit O T P.</Speak>
  </GetDigits>
  <Speak>We did not receive your input. Please try again.</Speak>
  <Redirect method="POST">{base_url}/ivr/otp-prompt</Redirect>
</Response>"""


def invalid_otp_xml(base_url: str) -> str:
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
  <Speak>Incorrect O T P. Please try again.</Speak>
  <Redirect method="POST">{base_url}/ivr/otp-prompt</Redirect>
</Response>"""


def language_menu_xml(base_url: str) -> str:
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
  <GetDigits action="{base_url}/ivr/language" method="POST" numDigits="1" timeout="10" retries="1" validDigits="12">
    <Speak>Authentication successful. Welcome to InspireWorks. Press 1 for English. Press 2 for Spanish.</Speak>
  </GetDigits>
  <Speak>We did not receive your input. Please try again.</Speak>
  <Redirect method="POST">{base_url}/ivr/language-menu</Redirect>
</Response>"""


def action_menu_xml(base_url: str, lang: str) -> str:
    if lang == "2":
        prompt = "Presione 1 para escuchar un mensaje. Presione 2 para hablar con un asociado."
    else:
        prompt = "Press 1 to hear an audio message. Press 2 to connect to a live associate."
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
  <GetDigits action="{base_url}/ivr/action?lang={lang}" method="POST" numDigits="1" timeout="10" retries="1" validDigits="12">
    <Speak>{prompt}</Speak>
  </GetDigits>
  <Speak>We did not receive your input. Please try again.</Speak>
  <Redirect method="POST">{base_url}/ivr/action-menu?lang={lang}</Redirect>
</Response>"""


def play_audio_xml(audio_url: str) -> str:
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
  <Speak>Playing your audio message now.</Speak>
  <Play>{audio_url}</Play>
  <Speak>Thank you for calling InspireWorks. Goodbye.</Speak>
  <Hangup/>
</Response>"""


def transfer_call_xml(associate_number: str, from_number: str) -> str:
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
  <Speak>Connecting you to a live associate. Please hold.</Speak>
  <Dial callerId="{from_number}">
    <Number>{associate_number}</Number>
  </Dial>
</Response>"""


def invalid_input_redirect_xml(base_url: str, redirect_path: str) -> str:
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
  <Speak>Invalid input. Please try again.</Speak>
  <Redirect method="POST">{base_url}{redirect_path}</Redirect>
</Response>"""

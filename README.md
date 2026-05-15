# InspireWorks Plivo IVR Demo

A FastAPI-based outbound IVR system using Plivo's Voice API with OTP authentication and multi-level menus.

## Features

- Outbound call trigger via REST endpoint
- 4-digit OTP authentication (DDMM birthdate, retries indefinitely on wrong input)
- Level 1: Language selection (English / Spanish)
- Level 2: Play audio OR transfer to associate
- Full Plivo XML call flow
- ngrok-compatible webhook setup

---

## Project Structure

```
plivo-ivr/
├── app/
│   ├── main.py           # FastAPI app entry point
│   ├── config.py         # Environment config
│   ├── xml_helpers.py    # Plivo XML response builders
│   └── routers/
│       ├── ivr.py        # IVR webhook endpoints
│       └── call.py       # Outbound call trigger endpoint
├── .env                  # Credentials & config (DO NOT COMMIT)
├── requirements.txt
└── README.md
```

---

## Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure `.env`

Edit `.env` with your Plivo credentials:

```env
PLIVO_AUTH_ID=YOUR_AUTH_ID
PLIVO_AUTH_TOKEN=YOUR_AUTH_TOKEN
PLIVO_FROM_NUMBER=14692463987       # Plivo number
PLIVO_TO_NUMBER=14692463990         # Number to call
PLIVO_ASSOCIATE_NUMBER=14692463990  # Transfer target
OTP_CODE=1503                       # Birthdate in DDMM (e.g. 15 March = 1503)
BASE_URL=https://YOUR_NGROK_URL     # Updated after ngrok starts
AUDIO_MP3_URL=https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3
```

### 3. Start ngrok

```bash
ngrok http 8000
```

Copy the HTTPS URL (e.g. `https://abc123.ngrok.io`) and update `BASE_URL` in `.env`.

### 4. Run the server

```bash
cd plivo-ivr
uvicorn app.main:app --reload --port 8000
```

Verify it's running: http://localhost:8000/docs

---

## Triggering a Call

### Using curl (default number from .env)

```bash
curl -X POST http://localhost:8000/call/trigger \
  -H "Content-Type: application/json" \
  -d '{}'
```

### With a custom number

```bash
curl -X POST http://localhost:8000/call/trigger \
  -H "Content-Type: application/json" \
  -d '{"to_number": "91803127412"}'
```

Expected response:
```json
{"status": "success", "api_id": "...", "to": "14692463990"}
```

---

## IVR Call Flow

```
[Call Answered]
      │
      ▼
[OTP Prompt] ──wrong──► [Re-prompt OTP] (loops forever)
      │ correct
      ▼
[Language Menu]
  1 → English ─┐
  2 → Spanish ─┤
               ▼
         [Action Menu]
           1 → Play MP3
           2 → Transfer to associate
```

---

## Webhook Endpoints (called by Plivo)

| Endpoint | Method | Description |
|---|---|---|
| `/ivr/answer` | POST | Called when outbound call is answered |
| `/ivr/otp-prompt` | POST | Re-prompt for OTP |
| `/ivr/validate-otp` | POST | Validates DTMF OTP input |
| `/ivr/language-menu` | POST | Show language selection |
| `/ivr/language` | POST | Handle language choice |
| `/ivr/action-menu` | POST | Show action menu |
| `/ivr/action` | POST | Handle action choice |
| `/call/trigger` | POST | Trigger outbound call |

---

## OTP

OTP is hardcoded as birthdate in DDMM format. Change `OTP_CODE` in `.env`.

Example: March 15 → `1503`

---

## Testing Tips

1. Start ngrok first, update `BASE_URL` in `.env`, then start the server.
2. Use the `/docs` Swagger UI to test endpoints interactively.
3. On a live call, entering a wrong OTP will loop back to the prompt.
4. The Indian number `91803127412` requires E.164 format: already correct.

---

## Plivo Credentials

- **Auth ID**: See `.env`
- **Auth Token**: See `.env`
- **Plivo Numbers**: 14692463987, 14692463990
- **Indian test number**: 91803127412

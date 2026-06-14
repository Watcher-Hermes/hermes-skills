# RunwayML & Kling AI — Direct REST API

> When fal.ai MCP is unavailable or you need direct API access.
> RunwayML and Kling models are also accessible via fal.ai, but their
> native APIs give different model selections and pricing.

## RunwayML API

**Base URL:** `https://api.dev.runwayml.com`
**Auth Header:** `X-Runway-Version: 2024-11-06` (required — doc says `2024-11-06`)
**Auth:** `Authorization: Bearer <RUNWAYML_API_KEY>`

### Endpoints

| Method | Path | Purpose |
|--------|------|---------|
| POST | `/v1/text_to_video` | Text-to-video generation |
| POST | `/v1/image_to_video` | Image-to-video |
| POST | `/v1/text_to_image` | Text-to-image |
| POST | `/v1/sound_effect` | Sound effect generation |
| GET | `/v1/tasks/{uuid}` | Check task status |

### Available Models (via RunwayML)

| Model Key | Resolution | Notes |
|-----------|-----------|-------|
| `gen4.5` | 1280:720 or 720:1280 | Latest Runway model |
| `gen3a_turbo` | varies | Not always available per-key |
| `kling3.0_4k` | **3840:2160**, 2160:3840, 2880:2880 | **4K output** |
| `kling3.0_pro` | 1920:1080, 1080:1920, 1440:1440 | Full HD |
| `kling3.0_standard` | varies | Lower quality tier |
| `kling2.5_turbo_pro` | varies | Older Kling model |

### Text-to-Video Payload

```python
import requests

headers = {
    'Authorization': f'Bearer {key}',
    'X-Runway-Version': '2024-11-06',
    'Content-Type': 'application/json'
}

payload = {
    'promptText': 'detailed description of the video scene',
    'model': 'kling3.0_4k',       # or gen4.5, kling3.0_pro, etc.
    'ratio': '3840:2160',          # depends on model (see table)
    'duration': 10                  # seconds
}

r = requests.post('https://api.dev.runwayml.com/v1/text_to_video',
                  headers=headers, json=payload, timeout=30)

if r.status_code == 201:
    task_id = r.json()['id']
    # Poll GET /v1/tasks/{task_id} until status='completed'
```

### Error Codes

| Code | Meaning | Action |
|------|---------|--------|
| `403` | Model not available on this key | Try a different model |
| `429` | No credits / Account balance not enough | Top up RunwayML credits |
| `400` | Validation error | Check payload fields match model |

---

## Kling AI API (Direct)

**Base URL:** `https://api.klingai.com`
**Auth:** JWT Bearer token (HMAC-SHA256 signed)

### JWT Token Generation

```python
import hmac, hashlib, base64, json, time

access_key = 'Aamyy...'  # KLING_ACCESS_KEY
secret_key = 'fHTf...'   # KLING_SECRET_KEY

header = base64.urlsafe_b64encode(
    json.dumps({'alg': 'HS256', 'typ': 'JWT'}).encode()
).decode().rstrip('=')

now = int(time.time())
payload_data = {
    'iss': access_key,
    'exp': now + 1800,      # 30 minutes
    'nbf': now - 60
}
payload_b64 = base64.urlsafe_b64encode(
    json.dumps(payload_data, separators=(',', ':')).encode()
).decode().rstrip('=')

signing_input = f'{header}.{payload_b64}'
signature = base64.urlsafe_b64encode(
    hmac.new(secret_key.encode(), signing_input.encode(), hashlib.sha256).digest()
).decode().rstrip('=')

jwt_token = f'{signing_input}.{signature}'
```

### Endpoints

| Method | Path | Purpose |
|--------|------|---------|
| POST | `/v1/videos/text2video` | Text-to-video |
| POST | `/v1/images/image2video` | Image-to-video |
| POST | `/v1/images/generations` | Image generation |

### Payload

```python
headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {jwt_token}'
}

payload = {
    'model_name': 'kling-v1',
    'prompt': 'description of the video',
    'duration': 5,
    'mode': 'pro'
}
```

### Error Codes

| Code | Meaning |
|------|---------|
| `1001` | Authorization is empty — regenerate JWT |
| `1002` | Authorization prefix should start with Bearer |
| `1102` | Account balance not enough — add Kling credits |

---

## Credit Check Workflow

When any video API returns 429/1102:

1. Try a different model (cheaper tier, e.g. gen4.5 instead of kling3.0_4k)
2. If all models reject: **fall back to programmatic Python video** (see SKILL.md)
3. Report back: which APIs/models were tried, which had credits, which didn't

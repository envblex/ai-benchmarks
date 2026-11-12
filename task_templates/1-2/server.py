from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from verifier import WebhookVerifier

verifier = WebhookVerifier()

async def handle_webhook(request):
    raw_body = await request.body()
    sig = request.headers.get("X-Signature", "")
    ts_header = request.headers.get("X-Timestamp", "0")
    nonce = request.headers.get("X-Nonce", "")

    try:
        ts = int(ts_header)
    except ValueError:
        return JSONResponse({"error": "Invalid timestamp"}, status_code=400)

    if not verifier.verify(raw_body, sig, ts, nonce):
        return JSONResponse({"error": "Unauthorized or replay detected"}, status_code=401)

    return JSONResponse({"status": "received", "body_size": len(raw_body)})

app = Starlette(routes=[
    Route("/webhook", handle_webhook, methods=["POST"])
])

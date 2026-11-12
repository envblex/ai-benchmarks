import hmac
import hashlib
import time
import pytest
from starlette.testclient import TestClient
from server import app
from verifier import SECRET_KEY

client = TestClient(app)

def generate_signature(raw_body: bytes, timestamp: int, nonce: str) -> str:
    message = f"{timestamp}:{nonce}:".encode("utf-8") + raw_body
    return hmac.new(SECRET_KEY, message, hashlib.sha256).hexdigest()

def test_valid_raw_json_signature():
    """Valid request with raw formatted JSON must be accepted (no False Positive)."""
    # Raw JSON with deliberate formatting spaces
    raw_body = b'{\n  "event": "payment.succeeded",\n  "amount": 5000\n}'
    ts = int(time.time())
    nonce = "nonce_1001"
    sig = generate_signature(raw_body, ts, nonce)

    resp = client.post(
        "/webhook",
        content=raw_body,
        headers={
            "X-Signature": sig,
            "X-Timestamp": str(ts),
            "X-Nonce": nonce,
            "Content-Type": "application/json"
        }
    )
    assert resp.status_code == 200, f"Expected 200, got {resp.status_code}: {resp.text}"
    assert resp.json().get("status") == "received"

def test_replay_attack_prevention():
    """Identical request with the same nonce must be rejected on second delivery."""
    raw_body = b'{"event":"payout","id":"tx_123"}'
    ts = int(time.time())
    nonce = "replay_nonce_abc"
    sig = generate_signature(raw_body, ts, nonce)
    headers = {
        "X-Signature": sig,
        "X-Timestamp": str(ts),
        "X-Nonce": nonce,
        "Content-Type": "application/json"
    }

    # First delivery: success
    resp1 = client.post("/webhook", content=raw_body, headers=headers)
    assert resp1.status_code == 200

    # Second delivery (replay attack): MUST BE REJECTED
    resp2 = client.post("/webhook", content=raw_body, headers=headers)
    assert resp2.status_code == 401, f"Replay attack was NOT rejected! Status: {resp2.status_code}"

def test_expired_timestamp_rejected():
    """Request outside the timestamp tolerance window must be rejected."""
    raw_body = b'{"event":"test"}'
    old_ts = int(time.time()) - 600 # 10 minutes ago
    nonce = "old_nonce"
    sig = generate_signature(raw_body, old_ts, nonce)

    resp = client.post(
        "/webhook",
        content=raw_body,
        headers={"X-Signature": sig, "X-Timestamp": str(old_ts), "X-Nonce": nonce}
    )
    assert resp.status_code == 401

import hmac
import hashlib
import json
import time

SECRET_KEY = b"webhook_super_secret_key_2026"
TIMESTAMP_TOLERANCE_SEC = 300 # 5 minutes

class WebhookVerifier:
    def __init__(self):
        # BUG: Nonce cache is not tracking used nonces properly!
        self.seen_nonces = set()

    def verify(self, raw_body: bytes, signature: str, timestamp: int, nonce: str) -> bool:
        # Check timestamp window
        now = int(time.time())
        if abs(now - timestamp) > TIMESTAMP_TOLERANCE_SEC:
            return False

        # BUG: Does not check or record nonce! Replay attacks succeed!
        # if nonce in self.seen_nonces:
        #     return False
        # self.seen_nonces.add(nonce)

        # BUG: Re-serializing JSON changes whitespace/key-ordering, causing False Positives!
        try:
            parsed = json.loads(raw_body.decode("utf-8"))
            payload_to_sign = json.dumps(parsed).encode("utf-8")
        except Exception:
            payload_to_sign = raw_body

        message = f"{timestamp}:{nonce}:".encode("utf-8") + payload_to_sign
        expected_sig = hmac.new(SECRET_KEY, message, hashlib.sha256).hexdigest()

        # BUG: Insecure string equality comparison vulnerable to timing attacks
        return signature == expected_sig

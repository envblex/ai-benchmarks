import os
import time
import httpx
import pytest

PROXY_SOCK = "/tmp/proxy.sock"

def test_proxy_health():
    """Verify that proxy recovers and returns HTTP 200 with status healthy."""
    assert os.path.exists(PROXY_SOCK), f"Proxy socket not found at {PROXY_SOCK}. Did you start the services?"
    
    transport = httpx.HTTPTransport(uds=PROXY_SOCK)
    with httpx.Client(transport=transport, timeout=5.0) as client:
        resp = client.get("http://localhost/health")
        assert resp.status_code == 200, f"Expected 200 OK, got {resp.status_code}: {resp.text}"
        data = resp.json()
        assert data.get("status") == "healthy", f"Expected status healthy, got {data}"

def test_concurrency_stress():
    """Verify proxy handles sequential and rapid health check requests without failing."""
    transport = httpx.HTTPTransport(uds=PROXY_SOCK)
    with httpx.Client(transport=transport, timeout=5.0) as client:
        for i in range(20):
            resp = client.get("http://localhost/health")
            assert resp.status_code == 200, f"Request {i+1} failed with {resp.status_code}"
            assert resp.json().get("status") == "healthy"

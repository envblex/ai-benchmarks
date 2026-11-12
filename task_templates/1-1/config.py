# Configuration for ASGI Reverse Proxy & Backend Worker
import os

# BUG: PROXY_BACKEND_SOCKET points to backend_worker.sock, but backend binds to backend.sock!
PROXY_LISTEN_SOCKET = "/tmp/proxy.sock"
PROXY_BACKEND_SOCKET = "/tmp/backend_worker.sock"

BACKEND_LISTEN_SOCKET = "/tmp/backend.sock"

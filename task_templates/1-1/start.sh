#!/bin/bash
# Service startup script for proxy_service
set -e

# Kill old instances
pkill -9 -f "uvicorn backend:app" 2>/dev/null || true
pkill -9 -f "uvicorn proxy:app" 2>/dev/null || true

# BUG: Does not unlink old socket files, which can cause bind errors!
# rm -f /tmp/proxy.sock /tmp/backend.sock

# Start backend worker on config.BACKEND_LISTEN_SOCKET
nohup uvicorn backend:app --uds /tmp/backend.sock > logs/backend.log 2>&1 &

# Start proxy on config.PROXY_LISTEN_SOCKET
nohup uvicorn proxy:app --uds /tmp/proxy.sock > logs/proxy_stdout.log 2>&1 &

sleep 2
echo "Services started."

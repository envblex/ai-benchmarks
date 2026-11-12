import os
import sys
import httpx
import logging
from starlette.applications import Starlette
from starlette.responses import Response, JSONResponse
import config

os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    filename="logs/proxy.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

async def proxy_request(request):
    backend_sock = config.PROXY_BACKEND_SOCKET
    path = request.url.path
    query = request.url.query
    url = f"http://localhost{path}" + (f"?{query}" if query else "")
    
    if not os.path.exists(backend_sock):
        err_msg = f"502 Bad Gateway: Backend socket not found at {backend_sock}"
        logging.error(err_msg)
        return JSONResponse({"error": "Bad Gateway", "detail": err_msg}, status_code=502)
        
    try:
        transport = httpx.AsyncHTTPTransport(uds=backend_sock)
        async with httpx.AsyncClient(transport=transport, timeout=5.0) as client:
            body = await request.body()
            headers = dict(request.headers)
            headers.pop("host", None)
            
            resp = await client.request(
                method=request.method,
                url=url,
                headers=headers,
                content=body
            )
            logging.info(f"Forwarded {request.method} {path} -> {resp.status_code}")
            return Response(content=resp.content, status_code=resp.status_code, headers=dict(resp.headers))
    except Exception as e:
        err_msg = f"502 Bad Gateway: Connection failed to {backend_sock}: {str(e)}"
        logging.error(err_msg)
        return JSONResponse({"error": "Bad Gateway", "detail": err_msg}, status_code=502)

from starlette.routing import Route

app = Starlette(routes=[
    Route("/{path:path}", endpoint=proxy_request, methods=["GET", "POST", "PUT", "DELETE"])
])

import uuid
import json
from fastapi import Request
from starlette.concurrency import iterate_in_threadpool
from app.utils import decode_access_token, main_logger, filter_sensitive


async def jwt_decoder(request: Request, call_next):
    token = request.headers.get("Authorization")
    if token and token.startswith("Bearer "):
        payload = decode_access_token(token.split(" ")[1])
        request.state.user = {
            "username": payload.get("username"),
            "email": payload.get("email"),
        }
    else:
        request.state.user = None
    return await call_next(request)


async def logging_middleware(request: Request, call_next):
    request.state.req_id = str(uuid.uuid4())
    with main_logger.contextualize(req_id=request.state.req_id, ip=request.client.host):
        try:
            body = (
                await request.json()
                if request.headers.get("content-type") == "application/json"
                else {}
            )
            # Redact body before logging
            redacted_body = filter_sensitive(
                body.copy() if isinstance(body, dict) else {}
            )
            main_logger.bind(
                method=request.method,
                path=request.url.path,
                headers=dict(request.headers),
            ).info(f"Incoming request: {redacted_body}")
        except:
            main_logger.info("Incoming request: [Non-JSON body]")

        try:
            response = await call_next(request)
            response_body = [chunk async for chunk in response.body_iterator]
            response.body_iterator = iterate_in_threadpool(iter(response_body))
            try:
                resp_body = (
                    json.loads(b"".join(response_body).decode())
                    if response.headers.get("content-type") == "application/json"
                    else b"".join(response_body).decode()
                )
                redacted_resp_body = None
                # Redact response body
                if isinstance(resp_body, list):
                    redacted_resp_body = [filter_sensitive(item) for item in resp_body]
                elif isinstance(resp_body, dict):
                    redacted_resp_body = filter_sensitive(resp_body)

            except:
                redacted_resp_body = "[Non-JSON response]"
            main_logger.bind(status_code=response.status_code).info(
                f"Response sent: {redacted_resp_body}"
            )
            return response
        except Exception as e:
            main_logger.exception(f"Request failed: {e}")
            raise

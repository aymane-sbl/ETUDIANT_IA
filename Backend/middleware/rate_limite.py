from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request, Depends,HTTPException,status
from fastapi.responses import JSONResponse
import json


class IpRateLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        user_path = request.url.path
        if not user_path.startswith("/api/") or request.method == "OPTIONS":
            return await call_next(request)

        redis_client = request.app.state.redis
        ip = request.client.host
        redis_key = f"ETUDIANT_IA:{ip}"

        ip_attempts = await redis_client.incr(redis_key)

        if ip_attempts == 1:
            await redis_client.expire(redis_key, 60)

        if ip_attempts > 50:
            return JSONResponse(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                content={"error": "Too many attempts"}
            )

        return await call_next(request)
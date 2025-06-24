from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from jose import JWTError, jwt
from app.core.config import settings
from app.core.response_engine import error

EXCLUDED_PATHS = [
    "/", 
    "/docs", 
    "/redoc", 
    "/openapi.json", 
    "/api/v1/auth"  # login or token endpoint
]

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        path = request.url.path

        # Check if the path should skip auth
        if any(path == ep or path.startswith(ep + "/") for ep in EXCLUDED_PATHS):
            #print(f"Skipping authentication for path: {path}")
            return await call_next(request)

        # Authorization header check
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("bearer "):
            return JSONResponse(
                status_code=401,
                content=error("Unauthorized: Missing or invalid token", 401)
            )

        token = auth_header.split(" ")[1]

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            request.state.user = payload.get("sub")
        except JWTError as e:
            return JSONResponse(
                status_code=401,
                content=error(f"Unauthorized: {str(e)}", 401)
            )

        return await call_next(request)

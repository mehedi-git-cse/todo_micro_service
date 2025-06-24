from fastapi import FastAPI, Request
from app.routes import todo_route
from app.core.response_engine import success, error
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.exceptions import RequestValidationError
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY

app = FastAPI(
    title="FAST API",
    description="A simple TODO API built with FastAPI project",
    version="1.0.0"
)

# Include routers
app.include_router(todo_route.router, prefix="/api/v1", tags=["todos"])

@app.get("/", tags=["root"])
def root():
    return success(msg="Welcome to FAST API!", data=None)

@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request: Request, exc: StarletteHTTPException):
    if exc.status_code == 404:
        msg = "The requested resource was not found."
        return JSONResponse(
            status_code=404,
            content=error(msg, status_code=404, data=None)
        )
    return JSONResponse(
        status_code=exc.status_code,
        content=error(msg=exc.detail, status_code=exc.status_code, data=None)
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    # Validation error গুলো exc.errors() থেকে detailed পাওয়া যায়
    return JSONResponse(
        status_code=HTTP_422_UNPROCESSABLE_ENTITY,
        content=error(
            msg="Validation Error",
            status_code=HTTP_422_UNPROCESSABLE_ENTITY,
            data=exc.errors()
        )
    )
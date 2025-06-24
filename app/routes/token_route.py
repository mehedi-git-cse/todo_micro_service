from fastapi import APIRouter, Form
from datetime import timedelta
from app.core.auth import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from app.core.response_engine import success, error

router = APIRouter()

@router.post("/get-token", tags=["authentication"])
async def login(username: str = Form(...), password: str = Form(...)):
    try:
        if username == "admin" and password == "admin123":
            token = create_access_token(
                data={"sub": username},
                expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            )
            return success(
                msg="Token generated successfully",
                data={"access_token": token, "token_type": "bearer"}
            )
        else:
            return error(msg="Invalid username or password", status_code=401)
    except Exception as e:
        return error(msg=f"Unexpected error: {str(e)}", status_code=500)

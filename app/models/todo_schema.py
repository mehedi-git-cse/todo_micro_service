from datetime import datetime
from pydantic import BaseModel, Field, EmailStr
from typing import Optional

class TodoBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    is_completed: bool = Field(default=False)
    name: str = Field(..., min_length=1, max_length=100)
    mobile: str = Field(..., min_length=11, max_length=15)
    email: EmailStr = Field(...)
    address: Optional[str] = Field(None, max_length=255)

class TodoCreate(TodoBase):
    pass

class TodoUpdate(TodoBase):
    pass

class TodoInDB(TodoBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

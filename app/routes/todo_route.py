from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.controllers.todo_controller import todo_controller
from app.core.response_engine import success, error
from app.models.todo_schema import TodoCreate
from app.core.database import get_db

router = APIRouter()

@router.post("/todos/create")
async def create_todo(todo: TodoCreate, db: AsyncSession = Depends(get_db)):
    try:
        todo_obj = await todo_controller.create_todo(todo, db)
        return success(data=todo_obj, msg="Todo created successfully", status_code=201)
    except Exception as e:
        print(f"[ERROR] Todo creation failed atik: {e}")
        return error(msg=str(e), status_code=500)

@router.get("/todos")
async def get_todos(db: AsyncSession = Depends(get_db)):
    try:
        todos = await todo_controller.get_todos(db)
        return success(data=todos, msg="Todos fetched successfully")
    except Exception as e:
        print(e)
        return error(msg=str(e), status_code=500)

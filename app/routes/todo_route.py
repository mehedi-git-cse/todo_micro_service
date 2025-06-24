from fastapi import APIRouter, Depends, Query, Path
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.controllers.todo_controller import todo_controller
from app.core.response_engine import success, error
from app.models.todo_schema import TodoCreate, TodoUpdate
from app.core.database import get_db
from typing import List, Optional

router = APIRouter()

@router.post("/todos/create")
async def create_todo(todo: TodoCreate, db: AsyncSession = Depends(get_db)):
    try:
        todo_obj = await todo_controller.create_todo(todo, db)
        return success(data=todo_obj, msg="Todo created successfully", status_code=201)
    except Exception as e:
        print(f"[ERROR] Todo creation failed atik: {e}")
        return error(msg=str(e), status_code=500)

@router.get("/todos/list")
async def get_todos(db: AsyncSession = Depends(get_db)):
    try:
        todos = await todo_controller.get_all_todos(db)
        return success(data=todos, msg="Todos fetched successfully")
    except Exception as e:
        print(f"[ERROR] Hello: {e}")
        return error(msg=str(e), status_code=500)

@router.get("/todos")
async def get_todos(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, le=100),
    is_completed: Optional[bool] = None,
    search: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    try:
        todos = await todo_controller.get_filtered_todos(
            db=db,
            skip=skip,
            limit=limit,
            is_completed=is_completed,
            search=search
        )
        return success(data=todos, msg="Filtered todos fetched")
    except Exception as e:
        return error(msg=str(e), status_code=500)
    
@router.get("/todos/{todo_id}")
async def get_todo_by_id(
    todo_id: int = Path(..., title="The ID of the Todo to retrieve"),
    db: AsyncSession = Depends(get_db)
):
    try:
        todo = await todo_controller.get_todo_by_id(todo_id=todo_id, db=db)
        return success(data=todo, msg=f"Todo with ID {todo_id} fetched")
    except Exception as e:
        return error(msg=str(e), status_code=404)
    
@router.put("/todos/{todo_id}")
async def update_todo(
    todo_id: int = Path(..., title="Todo ID"),
    todo_data: TodoUpdate = Depends(),
    db: AsyncSession = Depends(get_db)
):
    try:
        updated = await todo_controller.update_todo(todo_id, todo_data, db)
        return success(data=updated, msg="Todo updated successfully")
    except Exception as e:
        return error(msg=str(e), status_code=404)
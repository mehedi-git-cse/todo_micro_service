from datetime import datetime
from app.models.todo_schema import TodoCreate, TodoUpdate, TodoInDB
from app.models.todo_db_model import Todo
from app.core.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import insert
from typing import Optional

class TodoController:
    async def create_todo(self, todo: TodoCreate, db: AsyncSession) -> TodoInDB:
        try:
            # For debugging, print the received todo data
            # print("Received todo data:", todo) 
            # print("Title:", todo.title)
            # print("Mobile:", todo.mobile)
            # return todo
            new_todo = Todo(
                title=todo.title,
                description=todo.description,
                is_completed=todo.is_completed,
                name=todo.name,
                mobile=todo.mobile,
                email=todo.email,
                address=todo.address,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            db.add(new_todo)
            await db.commit()
            await db.refresh(new_todo)

            return TodoInDB(
                id=new_todo.id,
                title=new_todo.title,
                description=new_todo.description,
                is_completed=new_todo.is_completed,
                name=new_todo.name,
                mobile=new_todo.mobile,
                email=new_todo.email,
                address=new_todo.address,
                created_at=new_todo.created_at,
                updated_at=new_todo.updated_at
            )
        except Exception as e:
            await db.rollback()  # rollback for DB safety
            raise Exception(f"[ERROR] Todo creation failed: {e}")  # exception route এ পাঠাবে

todo_controller = TodoController()

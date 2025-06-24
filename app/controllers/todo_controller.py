from datetime import datetime
from app.models.todo_schema import TodoCreate, TodoUpdate, TodoInDB
from app.models.todo_db_model import Todo
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import insert
from typing import List, Optional

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
        
    async def get_all_todos(self, db: AsyncSession) -> TodoInDB:
        try:
            result = await db.execute(select(Todo))
            todos= result.scalars().all()

            return [TodoInDB.model_validate(todo) for todo in todos]
        
        except Exception as e:
            raise Exception(f"[ERROR] Failed to fetch todos: {e}")
        
    async def get_filtered_todos(
        self,
        db: AsyncSession,
        skip: int = 0,
        limit: int = 10,
        is_completed: Optional[bool] = None,
        search: Optional[str] = None
    ) -> List[TodoInDB]:
        try:
            query = select(Todo)

            if is_completed is not None:
                query = query.where(Todo.is_completed == is_completed)

            if search:
                like_term = f"%{search}%"
                query = query.where(
                    (Todo.title.ilike(like_term)) |
                    (Todo.description.ilike(like_term)) |
                    (Todo.name.ilike(like_term))
                )

            query = query.offset(skip).limit(limit)

            result = await db.execute(query)
            todos = result.scalars().all()

            return [TodoInDB.model_validate(todo) for todo in todos]

        except Exception as e:
            raise Exception(f"[ERROR] Filtered todos fetch failed: {e}")

    async def get_todo_by_id(self, todo_id: int, db: AsyncSession) -> TodoInDB:
        try:
            result = await db.execute(select(Todo).where(Todo.id == todo_id))
            todo = result.scalars().first()

            if not todo:
                raise Exception(f"Todo with ID {todo_id} not found")

            return TodoInDB.model_validate(todo)
        except Exception as e:
            raise Exception(f"[ERROR] Failed to fetch todo: {e}")
            
    async def update_todo(self, todo_id: int, todo_data: TodoUpdate, db: AsyncSession) -> TodoInDB:
        result = await db.execute(select(Todo).where(Todo.id == todo_id))
        todo = result.scalar_one_or_none()

        if not todo:
            raise Exception("Todo not found")

        for field, value in todo_data.model_dump(exclude_unset=True).items():
            setattr(todo, field, value)

        todo.updated_at = datetime.utcnow()

        await db.commit()
        await db.refresh(todo)

        return TodoInDB.from_orm(todo)
    
    async def delete_todo(self, todo_id: int, db: AsyncSession) -> None:
        result = await db.execute(select(Todo).where(Todo.id == todo_id))
        todo = result.scalar_one_or_none()

        if not todo:
            raise Exception("Todo not found")

        await db.delete(todo)
        await db.commit()

todo_controller = TodoController()

from typing import Annotated

from pydantic import BaseModel, Field

from fastapi import Depends, APIRouter, HTTPException, Path
from sqlalchemy.orm import Session

from database import Base, SessionLocal
from models import Todo

from starlette import status

from routers.auth import get_current_user

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


class TodoRequest(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    description: str = Field(min_length=1, max_length=100)
    priority: int = Field(gt=0, lt=6)
    complete: bool



@router.get("/", status_code=status.HTTP_200_OK)
def read_all(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication failed")
    return db.query(Todo).filter(Todo.owner_id == user.get("id")).all()


@router.get("/todo/{todo_id}", status_code=status.HTTP_200_OK)
def read_todo(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication failed")

    todo_return = (
        db.query(Todo)
        .filter(Todo.id == todo_id, Todo.owner_id == user.get("id"))
        .first()
    )
    if todo_return is not None:
        return todo_return

    raise HTTPException(status_code=404, detail="Todo not found")


@router.post("/todo", status_code=status.HTTP_201_CREATED)
def create_todo(user: user_dependency, db: db_dependency, todo_request: TodoRequest):

    if user is None:
        raise HTTPException(status_code=401, detail="Authentication failed")
    todo_created = Todo(**todo_request.model_dump(), owner_id=user.get("id"))

    db.add(todo_created)
    db.commit()


@router.put("/todo/{todo_id}")
def update_todo(
    user: user_dependency,
    db: db_dependency,
    new_todo: TodoRequest,
    todo_id: int = Path(gt=0),
):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication failed")
    todo_from_db = (
        db.query(Todo)
        .filter(Todo.id == todo_id, Todo.owner_id == user.get("id"))
        .first()
    )
    if todo_from_db is None:
        raise HTTPException(status_code=404, detail="Todo not found")

    todo_from_db.title = new_todo.title
    todo_from_db.description = new_todo.description
    todo_from_db.priority = new_todo.priority
    todo_from_db.complete = new_todo.complete

    db.commit()
    db.refresh(todo_from_db)
    return todo_from_db


@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(user:user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail = "Authentication failed")
    
    db_todo = db.query(Todo).filter(Todo.id == todo_id, Todo.owner_id == user.get('id')).first()

    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")

    db.delete(db_todo)
    db.commit()

from typing import Annotated

from pydantic import BaseModel, Field
from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session

from database import SessionLocal
from models import User

from starlette import status

from routers.auth import bcrypt_context, get_current_user

router = APIRouter(
    prefix='/user',
    tags=['user']
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


class UserVerification(BaseModel):
    password:str
    new_password:str = Field(min_length=6)

@router.get('/', status_code=status.HTTP_200_OK)
def get_user(user:user_dependency, db:db_dependency):
    if user is None:
        raise HTTPException(status_code=404, detail='User not Authenticated')
    db_user = db.query(User).filter(User.id == user.get('id')).first()

    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')

    return db_user


@router.put('/password', status_code=status.HTTP_204_NO_CONTENT)
def change_password(user:user_dependency, db:db_dependency, user_verify:UserVerification):
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not Authenticated")

    user_model = db.query(User).filter(User.id == user.get('id')).first()

    if user_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not FOund")

    if not bcrypt_context.verify(user_verify.password, user_model.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password is incorrect",
        )

    user_model.hashed_password = bcrypt_context.hash(user_verify.new_password)

    db.commit()
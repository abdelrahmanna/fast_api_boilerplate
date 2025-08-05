"""
FastAPI route definitions for the User entity.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.user import User, UserCreate, UserUpdate, UserOut
from app.crud.user import create_user, get_user, update_user, delete_user
from app.api.deps import get_db

user_router = APIRouter()


@user_router.post("/", response_model=UserOut)
def create(item: UserCreate, db: Session = Depends(get_db)):
    """
    Create a new User.
    """
    return User.create(db, **item.model_dump())


@user_router.get("/{id}", response_model=UserOut)
def read(id: int, db: Session = Depends(get_db)):
    """
    Retrieve a single User by ID.
    """
    obj = User.get(db, id)

    if not obj:
        raise HTTPException(status_code=404, detail="Not found")
    return obj


@user_router.put("/{id}", response_model=UserOut)
def update(id: int, item: UserUpdate, db: Session = Depends(get_db)):
    """
    Update an existing User.
    """
    db_obj = User.get(db, id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Not found")
    return User.update(db, db_obj, **item.model_dump())


@user_router.delete("/{id}")
def delete(id: int, db: Session = Depends(get_db)):
    """
    Delete a User by ID.
    """
    db_obj = get_user(db, id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Not found")
    return delete_user(db, db_obj)

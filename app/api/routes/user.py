"""
FastAPI route definitions for the User entity.
"""

from fastapi import APIRouter, HTTPException
from app.models.user import User, UserCreate, UserUpdate, UserOut
from app.api.deps import SessionDependency

user_router = APIRouter()


@user_router.post("/", response_model=UserOut)
def create(item: UserCreate, db: SessionDependency):
    """
    Create a new User.
    """
    return User.create(db, **item.model_dump())


@user_router.get("/{id}", response_model=UserOut)
def read(id: int, db: SessionDependency):
    """
    Retrieve a single User by ID.
    """
    obj = User.get(db, id)

    if not obj:
        raise HTTPException(status_code=404, detail="Not found")
    return obj


@user_router.put("/{id}", response_model=UserOut)
def update(id: int, item: UserUpdate, db: SessionDependency):
    """
    Update an existing User.
    """
    db_obj = User.get(db, id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Not found")
    return User.update(db, db_obj, **item.model_dump())


@user_router.delete("/{id}")
def delete(id: int, db: SessionDependency):
    """
    Delete a User by ID.
    """
    db_obj = User.get(db, id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Not found")
    return User.delete(db, db_obj)


@user_router.put("/soft-delete/{id}", response_model=UserOut)
def soft_delete(id: int, db: SessionDependency):
    """
    Soft delete a User by ID.
    """
    db_obj = User.get(db, id)

    if not db_obj:
        raise HTTPException(status_code=404, detail="Not found")

    return User.soft_delete(db, db_obj)

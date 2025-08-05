"""
CRUD operations for the User entity.
"""

from sqlalchemy.orm import Session
from app.models.user import User, UserCreate, UserUpdate


def create_user(db: Session, obj_in: UserCreate) -> User:
    """
    Create a new User in the database.
    """
    db_obj = User(**obj_in.dict())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def get_user(db: Session, id: int) -> User | None:
    """
    Retrieve a single User by its ID.
    """
    return db.query(User).filter(User.id == id).first()


def update_user(db: Session, db_obj: User, obj_in: UserUpdate) -> User:
    """
    Update an existing User instance.
    """
    for key, value in obj_in.dict(exclude_unset=True).items():
        setattr(db_obj, key, value)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def delete_user(db: Session, db_obj: User) -> User:
    """
    Delete an existing User instance from the database.
    """
    db.delete(db_obj)
    db.commit()
    return db_obj

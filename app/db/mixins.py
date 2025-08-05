# app/db/mixins.py
from sqlalchemy import DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import Session
from sqlalchemy import select

import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import DateTime, func


class TimestampMixin:
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=func.now(), onupdate=func.now()
    )


class SoftDeleteMixin:
    deleted_at: Mapped[datetime.datetime | None] = mapped_column(DateTime, default=None)

    def soft_delete(self):
        self.deleted_at = func.now()


class CRUDMixin:
    """
    Mixin that provides basic class-level CRUD operations.
    Requires the class to inherit from SQLAlchemy Base and have an `id` field.
    """

    @classmethod
    def get(cls, db: Session, id: int):
        return db.get(cls, id)

    @classmethod
    def get_all(cls, db: Session, limit: int = 100):
        return db.scalars(select(cls).limit(limit)).all()

    @classmethod
    def create(cls, db: Session, **kwargs):
        obj = cls(**kwargs)
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    @classmethod
    def update(cls, db: Session, obj, **kwargs):
        for key, value in kwargs.items():
            setattr(obj, key, value)
        db.commit()
        db.refresh(obj)
        return obj

    @classmethod
    def delete(cls, db: Session, obj):
        db.delete(obj)
        db.commit()
        return obj

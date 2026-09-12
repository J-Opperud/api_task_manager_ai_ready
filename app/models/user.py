from datetime import datetime

from sqlalchemy import Boolean, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        primary_key=True
        )

    name: Mapped[str] = mapped_column(
        String(70),
        nullable=False
        )

    email: Mapped[str] = mapped_column(
        String(250),
        unique=True,
        nullable=False
        )

    hashed_password: Mapped[str] = mapped_column(
        String(250),
        nullable=False
        )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False
        )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now()
        )

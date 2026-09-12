from datetime import datetime
from enum import Enum

from sqlalchemy import DateTime, Enum as SQLEnum, ForeignKey, String, Text, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from app.database import Base


class Priority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(
        primary_key=True
        )

    title: Mapped[str] = mapped_column(
        String(200),
        nullable=False
        )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
        )

    priority: Mapped[Priority] = mapped_column(
        SQLEnum(Priority),
        default=Priority.medium,
        nullable=False
        )

    completed: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False
        )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
        )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now()
        )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now(),
        onupdate=func.now()
        )

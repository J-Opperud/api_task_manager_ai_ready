from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.task import Priority


class TaskCreate(BaseModel):
    title: str = Field(
        min_length=1,
        max_length=200,
        description="Short name describing the task.",
        examples=["Write unit tests"],
        )

    description: str | None = Field(
        default=None,
        max_length=2000,
        description="Detailed description of the work to complete.",
        examples=["Add tests for registration, login, and task ownership."],
        )

    priority: Priority = Field(
        default=Priority.medium,
        description="Task priority level.",
        examples=["high"],
        )


class TaskUpdate(BaseModel):
    title: str | None = Field(
        default=None,
        min_length=1,
        max_length=200,
        description="Updated task title.",
        )
    description: str | None = Field(
        default=None,
        max_length=2000,
        description="Updated task description.",
        )
    priority: Priority | None = Field(
        default=None,
        description="Updated task priority.",
        )
    completed: bool | None = Field(
        default=None,
        description="Whether the task has been completed.",
        )   




class TaskResponse(BaseModel):
    id: int
    title: str
    description: str | None
    priority: Priority
    completed: bool
    user_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "title": "Write unit tests",
                "description": "Add tests for authentication and task ownership.",
                "priority": "high",
                "completed": False,
                "user_id": 1,
                "created_at": "2026-09-11T07:30:00",
                "updated_at": "2026-09-11T07:30:00",}
            },
        )

class TaskSuggestionResponse(BaseModel):
    suggestion: str = Field(
        description="Placeholder AI-generated suggestion for the task.",
        examples=[
            "Break this task into smaller actionable steps."
            ],
        )

from pydantic import BaseModel, ConfigDict, EmailStr, Field
from datetime import datetime

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "name": "Alice Smith",
                "email": "alice@example.com",
                "is_active": True,
                "created_at": "2026-09-11T07:30:00",}
            },
        )

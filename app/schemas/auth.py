from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):
    name: str = Field(
        min_length=1,
        max_length=70,
        description="User's display name.",
        examples=["Alice Smith"],
    )
    email: EmailStr = Field(
        description="User's email address.",
        examples=["alice@example.com"],
    )
    password: str = Field(
        min_length=8,
        max_length=72,
        description="Password used to authenticate the user.",
    )


class LoginRequest(BaseModel):
    email: EmailStr = Field(
        description="Registered email address.",
        examples=["alice@example.com"],
    )
    password: str = Field(
        min_length=1,
        max_length=72,
        description="Account password.",
    )


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"



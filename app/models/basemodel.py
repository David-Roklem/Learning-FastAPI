from pydantic import BaseModel, EmailStr, PositiveInt


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    age: PositiveInt
    is_subscribed: bool | None = None


class Feedback(BaseModel):
    name: str
    message: str

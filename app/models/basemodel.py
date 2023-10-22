from pydantic import BaseModel, EmailStr, PositiveInt, PositiveFloat


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    age: PositiveInt
    is_subscribed: bool | None = None


class Feedback(BaseModel):
    name: str
    message: str


class Product(BaseModel):
    product_id: int
    name: str
    category: str
    price: PositiveFloat

# app/schemas/order.py

from pydantic import BaseModel


class OrderCreate(BaseModel):
    product_id: int
    quantity: int


class OrderResponse(BaseModel):
    id: int
    user_id: int
    product_id: int
    quantity: int
    total_amount: float
    status: str

    class Config:
        from_attributes = True
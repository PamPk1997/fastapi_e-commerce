from pydantic import BaseModel
from datetime import datetime
from typing import List
from src.models import OrderStatus


class User(BaseModel):
    id:int


class OrderItem(BaseModel):
    product_id: int
    quantity: int

    class Config:
        from_attributes = True

class OrderCreate(BaseModel):
    address: str

    class Config:
        from_attributes = True

class OrderUpdate(BaseModel):
    status: OrderStatus


class OrderOut(OrderUpdate):
    id: int
    order_items: list[OrderItem]
    total_amount: float
    created_at: datetime

    class Config:
        from_attributes = True

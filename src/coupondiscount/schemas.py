from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CouponBase(BaseModel):
    code: str
    discount_percentage: float
    max_discount_amount: Optional[float]
    valid_from: datetime
    valid_to: datetime
    min_purchase_amount: Optional[float]
    usage_limit: Optional[int]
    is_active: bool = True

class CouponCreate(CouponBase):
    pass

class CouponOut(CouponBase):
    id: int
    usage_count: int

    class Config:
        from_attributes = True


class DiscountBase(BaseModel):
    product_id: int
    discount_percentage: float
    valid_from: datetime
    valid_to: datetime
    is_active: bool = True

class DiscountCreate(DiscountBase):
    pass

class DiscountOut(DiscountBase):
    id: int

    class Config:
        from_attributes = True

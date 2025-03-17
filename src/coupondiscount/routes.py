from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from src.cart import schemas
from src.coupondiscount import schemas
from src import models
from config.database import get_async_db
from auth.oauth2 import get_current_user


# Coupon Router
coupon_router = APIRouter(
    prefix="/coupon",
    tags=["Coupon"]
)

# Discount Router
discount_router = APIRouter(
    prefix="/discount",
    tags=["Discount"]
)


@coupon_router.post("/coupons", response_model=schemas.CouponOut)
async def create_coupon(
    coupon: schemas.CouponCreate,
    db: AsyncSession = Depends(get_async_db),
    current_user: models.UserTable = Depends(get_current_user)):

    """
    Creating  new coupon.
    """
    new_coupon = models.CouponsTable(**coupon.model_dump())
    db.add(new_coupon)
    await db.commit()
    await db.refresh(new_coupon)
    return new_coupon


@coupon_router.get("/coupons/{code}", response_model=schemas.CouponOut)
async def get_coupon(
    code: str,
    db: AsyncSession = Depends(get_async_db),
     current_user: models.UserTable = Depends(get_current_user)):
    
    """
    Retrieve an active coupon by code.
    """
    result = await db.execute(
        select(models.CouponsTable).filter(models.CouponsTable.code == code, models.CouponsTable.is_active == True)
    )
    coupon = result.scalar_one_or_none()
    if not coupon:
        raise HTTPException(status_code=404, detail="Coupon not found or inactive")
    return coupon




@discount_router.post("/discount", response_model=schemas.DiscountOut)
async def create_discount(
    discount: schemas.DiscountCreate,
    db: AsyncSession = Depends(get_async_db),
    current_user: models.UserTable = Depends(get_current_user)):

    """
    Creating a new discount.
    """
    new_discount = models.DiscountTable(**discount.model_dump())
    db.add(new_discount)
    await db.commit()
    await db.refresh(new_discount)
    return new_discount


@discount_router.get("/discount/{product_id}", response_model=List[schemas.DiscountOut])
async def get_discounts(
    product_id: int,
    db: AsyncSession = Depends(get_async_db),
    current_user: models.UserTable = Depends(get_current_user)):

    """
    Retrieve all active discounts for a given product.
    """
    result = await db.execute(
        select(models.DiscountTable).filter(models.DiscountTable.product_id == product_id, models.DiscountTable.is_active == True)
    )
    discounts = result.scalars().all()
    if not discounts:
        raise HTTPException(status_code=404, detail="No discounts found for this product")
    return discounts

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from src.cart import schemas, services
from src import models
from config.database import get_async_db  # Async session
from auth.oauth2 import get_current_user

cart_router = APIRouter(
    prefix="/api/cart",
    tags=["Cart"]
)

@cart_router.get("/", response_model=schemas.Cart)
async def get_cart(
    db: AsyncSession = Depends(get_async_db), 
    current_user: models.UserTable = Depends(get_current_user)
):
    """
    Retrieve the cart for the currently authenticated user.
    """
    cart = await services.get_cart_by_user(db, current_user.id)
    if not cart:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Cart not found"
        )
    return cart


@cart_router.post("/add", response_model=schemas.CartItem)
async def add_to_cart(
    item: schemas.CartItemCreate, 
    db: AsyncSession = Depends(get_async_db), 
    current_user: models.UserTable = Depends(get_current_user)
):
    """
    Add an item to the cart for the currently authenticated user.
    """
    return await services.add_item_to_cart(db, item, current_user.id)


@cart_router.delete("/remove/{cart_item_id}", response_model=schemas.CartItem)
async def remove_from_cart(
    cart_item_id: int, 
    db: AsyncSession = Depends(get_async_db), 
    current_user: models.UserTable = Depends(get_current_user)
):
    """
    Remove a specific item from the cart by its ID.
    """
    item = await services.remove_item_from_cart(db, cart_item_id, current_user.id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Item not found in cart"
        )
    return item


@cart_router.delete("/clear", response_model=schemas.Cart)
async def clear_cart(
    db: AsyncSession = Depends(get_async_db), 
    current_user: models.UserTable = Depends(get_current_user)
):
    """
    Clear all items from the cart for the currently authenticated user.
    """
    return await services.clear_cart(db, current_user.id)

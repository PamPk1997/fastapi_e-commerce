from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.cart import schemas
from src import models

# Current user's cart
async def get_cart_by_user(db: AsyncSession, user_id: int):
    result = await db.execute(
        select(models.CartTable).filter(models.CartTable.user_id == user_id)
    )
    return result.scalar_one_or_none()


# Add an item to the cart
async def add_item_to_cart(db: AsyncSession, cart_data: schemas.CartItemCreate, user_id: int):
    cart = await get_cart_by_user(db, user_id)
    if not cart:
        cart = models.CartTable(user_id=user_id)
        db.add(cart)
        await db.commit()
        await db.refresh(cart)

    cart_item = models.CartItemTable(**cart_data.model_dump(), user_id=user_id)
    cart.items.append(cart_item)
    db.add(cart_item)
    await db.commit()
    await db.refresh(cart_item)
    return cart_item


# Remove an item from the cart
async def remove_item_from_cart(db: AsyncSession, cart_item_id: int, user_id: int):
    result = await db.execute(
        select(models.CartItemTable).filter(
            models.CartItemTable.id == cart_item_id,
            models.CartItemTable.user_id == user_id
        )
    )
    cart_item = result.scalar_one_or_none()

    if cart_item:
        await db.delete(cart_item)
        await db.commit()
    return cart_item


# Clear the cart
async def clear_cart(db: AsyncSession, user_id: int):
    cart = await get_cart_by_user(db, user_id)
    if cart:
        for item in cart.items:
            await db.delete(item)
        await db.commit()
    return cart

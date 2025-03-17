from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.orders import schemas
from src import models



async def place_order(db: AsyncSession, current_user: schemas.User, order: schemas.OrderCreate):
    result = await db.execute(
        select(models.CartItemTable).filter(models.CartItemTable.user_id == current_user.id)
    )
    cart_items = result.scalars().all()
    
    if not cart_items:
        raise HTTPException(status_code=400, detail="No items in cart")

    total_amount = 0
    items_for_order = []

    for cart_item in cart_items:
        result = await db.execute(
            select(models.ProductTable).filter(models.ProductTable.id == cart_item.product_id)
        )
        product = result.scalar_one_or_none()

        if not product:
            raise HTTPException(status_code=404, detail=f"Product {cart_item.product_id} not found")

        if product.stock_quantity < cart_item.quantity:
            raise HTTPException(status_code=400, detail=f"Product {product.name} out of stock")

        total_amount += product.price * cart_item.quantity

        items_for_order.append({
            "product_id": cart_item.product_id,
            "quantity": cart_item.quantity
        })

    # Create order in the database
    new_order = models.OrderTable(
        user_id=current_user.id,
        total_amount=total_amount,
        address=order.address
    )

    db.add(new_order)
    await db.commit()
    await db.refresh(new_order)

    # Create order items and update product stock
    for item in items_for_order:
        order_item = models.OrderItemTable(
            order_id=new_order.id,
            product_id=item['product_id'],
            quantity=item['quantity']
        )
        db.add(order_item)

        result = await db.execute(
            select(models.ProductTable).filter(models.ProductTable.id == item['product_id'])
        )
        product = result.scalar_one_or_none()
        product.stock_quantity -= item['quantity']
        await db.commit()

    # Clear the cart
    await db.execute(
        select(models.CartItemTable).filter(models.CartItemTable.user_id == current_user.id).delete()
    )
    await db.commit()

    return new_order




async def get_order(order_id: int, current_user: schemas.User, db: AsyncSession):
    result = await db.execute(
        select(models.OrderTable).filter(
            models.OrderTable.id == order_id, 
            models.OrderTable.user_id == current_user.id
        )
    )
    order = result.scalar_one_or_none()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order






async def list_orders(current_user: schemas.User, db: AsyncSession):
    result = await db.execute(
        select(models.OrderTable).filter(models.OrderTable.user_id == current_user.id)
    )
    orders = result.scalars().all()
    return orders






async def update_order(order_id: int, order_update: schemas.OrderUpdate, current_user: schemas.User, db: AsyncSession):
    result = await db.execute(
        select(models.OrderTable).filter(
            models.OrderTable.id == order_id, 
            models.OrderTable.user_id == current_user.id
        )
    )
    order = result.scalar_one_or_none()
    
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    order.status = order_update.status
    await db.commit()
    await db.refresh(order)
    return order



async def delete_order(order_id: int, current_user: schemas.User, db: AsyncSession):
    result = await db.execute(
        select(models.OrderTable).filter(
            models.OrderTable.id == order_id, 
            models.OrderTable.user_id == current_user.id
        )
    )
    order = result.scalar_one_or_none()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    await db.delete(order)
    await db.commit()
    return {"message": "Order deleted successfully"}

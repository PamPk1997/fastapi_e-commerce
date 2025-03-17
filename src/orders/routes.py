from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from src.orders import schemas, services
from config.database import get_async_db
from typing import List
from src import models
from auth.oauth2 import get_current_user
from src.notifications.email_services import send_email_order_place, send_email_order_cancel
from src.notifications.sms_services import send_sms_notification


order_router = APIRouter(
    prefix="/orders",
    tags=["Orders"])


@order_router.post("/", response_model=schemas.OrderOut)
async def place_order(
    order_data: schemas.OrderCreate, 
    db: AsyncSession = Depends(get_async_db),
    current_user: models.UserTable = Depends(get_current_user),
    background_tasks: BackgroundTasks = BackgroundTasks()
):
    order = await services.place_order(db, current_user, order_data)

    message = f"The order has been placed and your order ID is {order.id}."
    background_tasks.add_task(send_sms_notification, current_user.phone_number, message)
    background_tasks.add_task(send_email_order_place, current_user.email, current_user.username, order.id)

    return order


@order_router.get("/{order_id}", response_model=schemas.OrderOut)
async def get_order(
    order_id: int, 
    db: AsyncSession = Depends(get_async_db), 
    current_user: schemas.User = Depends(get_current_user)
):
    return await services.get_order(order_id, current_user, db)


@order_router.get("/", response_model=List[schemas.OrderOut])
async def list_orders(
    db: AsyncSession = Depends(get_async_db), 
    current_user: schemas.User = Depends(get_current_user)
):
    return await services.list_orders(current_user, db)


@order_router.put("/{order_id}", response_model=schemas.OrderOut)
async def update_order(
    order_id: int, 
    order_update: schemas.OrderUpdate, 
    db: AsyncSession = Depends(get_async_db), 
    current_user: schemas.User = Depends(get_current_user)
):
    return await services.update_order(order_id, order_update, current_user, db)


@order_router.delete("/{order_id}", response_model=dict)
async def delete_order(
    order_id: int, 
    db: AsyncSession = Depends(get_async_db), 
    current_user: schemas.User = Depends(get_current_user),
    background_tasks: BackgroundTasks = BackgroundTasks()
):

    message = f"The order has been cancelled with the order ID {order_id}."
    background_tasks.add_task(send_sms_notification, current_user.phone_number, message)
    background_tasks.add_task(send_email_order_cancel, current_user.email, current_user.username, order_id)

    return await services.delete_order(order_id, current_user, db)

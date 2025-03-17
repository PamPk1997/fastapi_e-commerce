from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from config.database import get_async_db
from src.notifications.email_services import send_email_NewUser
from src.users import schemas, services
from src import models
from auth.oauth2 import get_current_user
from config.enums import RoleType


user_router = APIRouter(
    prefix="/users", tags=["Users"]
)

role_router = APIRouter(
    prefix="/role", tags=["Roles"]
)

# User Routers

@user_router.get('/', response_model=List[schemas.UserOut])
async def get_users(
    db: AsyncSession = Depends(get_async_db), 
    current_user: models.UserTable = Depends(get_current_user)
):
    return await services.get_all_users(db)


@user_router.get("/{user_id}", response_model=schemas.UserOut)
async def get_user(
    user_id: int, 
    db: AsyncSession = Depends(get_async_db), 
    current_user: models.UserTable = Depends(get_current_user)
):
    user = await services.user_by_id(user_id, db)

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User was not found")  
    return user


@user_router.post("/register", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)

async def user_registration(
    user: schemas.UserCreate, 
    db: AsyncSession = Depends(get_async_db),
    background_tasks: BackgroundTasks = BackgroundTasks(),
):
    # Create the user and generate a verification token
    new_user, token = await services.create_user(user, db)

    # Send verification email asynchronously
    verification_url = f"http://127.0.0.1:8000/api/v1/auth/verify-email?token={token}"
    background_tasks.add_task(
        send_email_NewUser, 
        user.first_name, 
        user.last_name, 
        user.username, 
        user.email, 
        verification_url
    )

    return new_user



@user_router.put('/{user_id}', response_model=schemas.UserUpdate)
async def update_user(
    user_id: int,
    updated_user: schemas.UserUpdate, 
    db: AsyncSession = Depends(get_async_db)):

    user = await services.update_user(user_id, updated_user, db)

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User was not found")
    
    return user


@user_router.delete("/{user_id}")
async def delete_user(
    user_id: int, 
    db: AsyncSession = Depends(get_async_db), 
    current_user: models.UserTable = Depends(get_current_user)):

    user = await services.delete_user(user_id, db)

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User was not found")
    
    return {"message": "User deleted successfully"}



# Role Routers

@role_router.put("/assign-role", response_model=schemas.RoleRequest)
async def assign_role_to_user(
    user_id: int,
    role_name: schemas.RoleType,
    db: AsyncSession = Depends(get_async_db),
    background_tasks: BackgroundTasks = BackgroundTasks(),
    current_user: models.UserTable = Depends(get_current_user)):

    return await services.assign_role_to_user(
        user_id=user_id,
        role_name=role_name,
        db=db,
        current_user=current_user,
        background_tasks=background_tasks
    )



@role_router.get('/{user_id}', response_model=schemas.RoleRequest)
async def get_roles(
    user_id: int,
    db: AsyncSession = Depends(get_async_db),
    current_user: models.UserTable = Depends(get_current_user)):

    return await services.get_user_roles(user_id, db)   



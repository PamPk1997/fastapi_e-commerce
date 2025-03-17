from fastapi import HTTPException,BackgroundTasks,status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update
from auth.utils import hash
from src import models
from src.users import schemas
from auth.utils import create_email_verification_token
from src.notifications.email_services import send_email_assign_role
from config.enums import RoleType


async def get_all_users(db: AsyncSession):
    result = await db.execute(select(models.UserTable))
    return result.scalars().all()


async def user_by_id(user_id: int, db: AsyncSession):
    result = await db.execute(select(models.UserTable).filter(models.UserTable.id == user_id))
    return result.scalar_one_or_none()


async def create_user(user: schemas.UserCreate, db: AsyncSession):

    # Check if the username already exists
    result = await db.execute(select(models.UserTable).filter(models.UserTable.username == user.username))
    existing_user_by_username = result.scalar_one_or_none()
    if existing_user_by_username:
        raise HTTPException(status_code=400, detail="Username already exists")

    # Check if the mobile number already exists
    result = await db.execute(select(models.UserTable).filter(models.UserTable.phone_number == user.phone_number))
    existing_user_by_mobile = result.scalar_one_or_none()
    if existing_user_by_mobile:
        raise HTTPException(status_code=400, detail="Mobile number already registered")
    
    # Check if the email already exists
    result = await db.execute(select(models.UserTable).filter(models.UserTable.email == user.email))
    existing_user_by_email = result.scalar_one_or_none()
    if existing_user_by_email:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Hash the password
    hashed_password = hash(user.password_hash)
    user.password_hash = hashed_password

    # Create a new user with inactive status
    new_user = models.UserTable(
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        phone_number=user.phone_number,
        address= user.address,
        password_hash=hashed_password,
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    assign_role = await db.execute(select(models.RoleTable).filter(models.RoleTable.role_name == RoleType.CUSTOMER)) 
    customer_role = assign_role.scalar_one_or_none()

    if customer_role:
        user_role = models.UserRoles(user_by_id = new_user.id, role_id = customer_role.id)
        db.add (user_role)
        await db.commit()

    # Generate an email verification token
    token = create_email_verification_token(email=user.email)

    return new_user, token


async def update_user(user_id: int, updated_user: schemas.UserUpdate, db: AsyncSession):
    result = await db.execute(select(models.UserTable).filter(models.UserTable.id == user_id))
    user = result.scalar_one_or_none()

    if not user:
        return None

    stmt = (
        update(models.UserTable)
        .where(models.UserTable.id == user_id)
        .values(**updated_user.model_dump(exclude_unset=True))
        .execution_options(synchronize_session="fetch")
    )
    await db.execute(stmt)
    await db.commit()
    await db.refresh(user)
    return user


async def delete_user(user_id: int, db: AsyncSession):
    result = await db.execute(select(models.UserTable).filter(models.UserTable.id == user_id))
    user = result.scalar_one_or_none()

    if not user:
        return None

    await db.delete(user)
    await db.commit()
    return True


async def get_all_roles(db: AsyncSession):
    result = await db.execute(select(models.RoleTable))
    return result.scalars().all()


async def get_user_roles(user_id: int, db: AsyncSession):
    result = await db.execute(select(models.UserTable).filter(models.UserTable.id == user_id))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Extract role names from the user's roles
    roles = [role.role_name for role in user.roles]

    return {
        "username": user.username,
        "role_name": roles
    }



async def assign_role_to_user(
        user_id:int,
        role_name:schemas.RoleType,
        db:AsyncSession,
        current_user: models.UserTable,
        background_tasks: BackgroundTasks = BackgroundTasks()
):
    
    #check current user is an admin
    if current_user.roles[0].role_name != schemas.RoleType.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Only Admin Can Assign Roles to Users")
    

    #fetch the user 
    result = await db.execute(
    select(models.UserTable).filter(models.UserTable.id == user_id))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")
    
    
    role_result = await db.execute(
        select(models.RoleTable).filter(models.RoleTable.role_name == role_name)
    )
    role = role_result.scalar_one_or_none()
    if not role:
        raise HTTPException(status_code=400, detail="Role not found")

    # Check if the user already has this role
    existing_role_result = await db.execute(
        select(models.UserRoles).filter_by(user_id=user.id, role_id=role.id)
    )
    if existing_role_result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="User already has this role")

    # Restrict assigning multiple admin/seller roles
    if role.role_name in [schemas.RoleType.ADMIN, schemas.RoleType.SELLER] and user.roles:
        raise HTTPException(
            status_code=400,
            detail="Cannot assign multiple admin/seller roles."
        )

    # Assign the role
    user_role = models.UserRoles(user_id=user.id, role_id=role.id)
    db.add(user_role)
    await db.commit()
    await db.refresh(user)

    # Add background task to send email
    background_tasks.add_task(send_email_assign_role, user.email, user.username, role_name)

    # Return response data
    return schemas.RoleRequest(
        username=user.username,
        role_name=[role.role_name]
    )

    



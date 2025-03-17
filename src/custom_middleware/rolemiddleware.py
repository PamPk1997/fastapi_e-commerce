from typing import List
from fastapi import Depends,HTTPException,status
from models import UserTable
from config.enums import RoleType
from auth.oauth2 import get_current_user







def role_required(required_roles: list[RoleType]):
    async def verify_user_role(
        current_user: UserTable = Depends(get_current_user)):
        user_roles = [role.role_name for role in current_user.roles]
        if not any(role in user_roles for role in required_roles):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Insufficient permission. Required roles: {required_roles}")
        return current_user
    return verify_user_role
 

 
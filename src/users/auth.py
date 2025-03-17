from fastapi import APIRouter, Depends, HTTPException, status, Request,BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete
from starlette.responses import RedirectResponse, Response, JSONResponse 
from authlib.integrations.base_client.errors import OAuthError
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from urllib.parse import urlparse, urlunparse
from config.database import get_async_db
from auth.utils import verify_pass,hash
from src import models
from auth import schemas, oauth2
from auth.oauth2 import oauth
from src.notifications.email_services import send_email_otp,send_email_resetpass
import random, hashlib, hmac
from datetime import datetime, timedelta, timezone
from config.settings import settings
import asyncio
from auth.utils import verify_email_verification_token


auth_router = APIRouter(prefix="/auth", tags=["Authentication"])


# Endpoint for user login to send OTP
@auth_router.post('/login', status_code=status.HTTP_200_OK)
async def login(
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_async_db)
):
    # Fetch user by username or phone number
    if user_credentials.username.isdigit():
        
        user = await db.execute(select(models.UserTable).filter(models.UserTable.phone_number == user_credentials.username))
    else:
        user = await db.execute(select(models.UserTable).filter(models.UserTable.username == user_credentials.username))
    
    user = user.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Username or phone number")

    # Verify password (adapt to async if required)
    if not await asyncio.to_thread(verify_pass, user_credentials.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")

    # Delete old OTPs for this user
    dltotp = delete(models.OTPModel).where(models.OTPModel.user_id == user.id)
    await db.execute(dltotp)
    await db.commit()

    # Generate OTP
    otp = random.randint(10000, 99999)
    print(otp,"New genrated OTP------------------------------")
    hashed_otp = hashlib.sha256(str(otp).encode()).hexdigest()
    expires_at = datetime.now(timezone.utc) + timedelta(minutes=5)

    # Store OTP in the database
    new_otp = models.OTPModel(
        user_id=user.id,
        hashed_otp=hashed_otp,
        expires_at=expires_at
    )
    db.add(new_otp)
    await db.commit()

    # Send OTP via email
    # await send_email_otp(user.email, user.username, otp)

    return {"message": "OTP sent to your email"}



# Endpoint for OTP verification to get the access token
@auth_router.post('/verify-otp', response_model=schemas.Token)
async def verify_otp(
    otp_data: schemas.OTPVerification,
    db: AsyncSession = Depends(get_async_db)
):
    user = await db.execute(
        select(models.UserTable).filter(models.UserTable.id == otp_data.user_id)
    )
    user = user.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    user_otp = await db.execute(
        select(models.OTPModel).filter(models.OTPModel.user_id == user.id)
    )
    user_otp = user_otp.scalar_one_or_none()

    # Check if OTP exists, matches, and hasn't expired
    if not user_otp or datetime.now(timezone.utc) > user_otp.expires_at:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or expired OTP")

    hashed_input_otp = hashlib.sha256(str(otp_data.otp).encode()).hexdigest()
    if not hmac.compare_digest(user_otp.hashed_otp, hashed_input_otp):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid OTP")

    # Delete OTP after successful verification
    await db.delete(user_otp)
    await db.commit()

    access_token = await asyncio.to_thread(oauth2.create_access_token, data={"user_id": user.id})

    response = JSONResponse(content={"message": "OTP verified successfully"})
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=False,  # Set to True in production
        samesite='lax'
    )
    return response



@auth_router.get("/verify-email")
async def verify_email(token: str, db: AsyncSession = Depends(get_async_db)):

    email = verify_email_verification_token(token)  # Decode and validate token

    result = await db.execute(select(models.UserTable).filter(models.UserTable.email == email))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.is_active = True  # Activate the user
    await db.commit()

    return {"message": "Email verified successfully."}


# Logout endpoint
@auth_router.post('/logout', status_code=status.HTTP_200_OK)
async def logout(response: Response, current_user: int = Depends(oauth2.get_current_user)):
    response.delete_cookie(
        key="access_token",
        httponly=True,
        secure=False,  # Set to True in production
        samesite='lax'
    )
    return {"message": "Successfully logged out"}


@auth_router.post("/forgot-password")
async def forgot_password(email:str , db:AsyncSession=Depends(get_async_db),
                          background_tasks: BackgroundTasks = BackgroundTasks()):

    result = await db.execute(select(models.UserTable).filter(models.UserTable.email == email))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User not found")
    
    reset_token=oauth2.create_access_token({"user_id": user.id,"email":user.email})
    
    reset_link= f"http://127.0.0.1:8000/api/v1/auth/reset_password?token={reset_token}"

    background_tasks.add_task(
        send_email_resetpass, 
        user.username, 
        user.email, 
        reset_link
    )
    return {"message": "Password reset link sent to your email"}



@auth_router.post("/reset_password")
async def reset_password(token:str, new_password:str,db:AsyncSession = Depends(get_async_db)):

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Not Authenticated",
        headers={"WWW-Authenticate": "Bearer"},)

    token_data = oauth2.verify_access_token(token,credentials_exception) 

    if not token_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired token"
        )
    
    user = await db.execute(
        select(models.UserTable).filter(models.UserTable.id == int(token_data.id))
    )
    user = user.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="user not found"
        )
    
    hashed_password = hash(new_password)
    user.password_hash = hashed_password
    await db.commit()

    return {"message": "Password reset successfully"}


@auth_router.get("/login/google")
async def login_via_google(request: Request):
    redirect_uri = request.url_for("google_callback")
    return await oauth.google.authorize_redirect(request, redirect_uri)



@auth_router.get("/callback/google")
async def google_callback(request: Request, db: AsyncSession = Depends(get_async_db)):

    token = await oauth.google.authorize_access_token(request)
    user_info = token.get("userinfo")

    user = await db.execute(
        select(models.UserTable).filter(models.UserTable.email == user_info['email'])
    )
    user = user.scalar_one_or_none()

    if not user:
        user = models.UserTable(
            username=user_info.get('name', user_info['email']),
            email=user_info['email'],
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)

    access_token = await asyncio.to_thread(oauth2.create_access_token, data={"user_id": user.id})

    response = RedirectResponse(url="/docs")
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=False,  # Set to True in production-- for https
        samesite='lax'
    )
    return response


# Login using Facebook
@auth_router.get("/login/facebook")
async def login_via_facebook(request: Request):
    redirect_uri = str(request.url_for("facebook_callback"))

    ngrok_url = settings.NGROK_URL

    parsed_redirect_uri = urlparse(redirect_uri)
    parsed_ngrok_url = urlparse(ngrok_url)
    redirect_uri = urlunparse((
        parsed_ngrok_url.scheme,
        parsed_ngrok_url.netloc,
        parsed_redirect_uri.path,
        parsed_redirect_uri.params,
        parsed_redirect_uri.query,
        parsed_redirect_uri.fragment
    ))
    return await oauth.facebook.authorize_redirect(request, redirect_uri)


# Facebook OAuth callback route
@auth_router.get("/callback/facebook")
async def facebook_callback(request: Request, db: AsyncSession = Depends(get_async_db)):

    token = await oauth.facebook.authorize_access_token(request)
    resp = await oauth.facebook.get('me?fields=name,email', token=token)
    user_info = resp.json()


    user = await db.execute(
        select(models.UserTable).filter(models.UserTable.email == user_info.get('email'))
    )
    user = user.scalar_one_or_none()

    if not user:
        user = models.UserTable(
            username=user_info.get('name', user_info.get('email')),
            email=user_info.get('email'),
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)

    access_token = await asyncio.to_thread(oauth2.create_access_token, data={"user_id": user.id})

    response = RedirectResponse(url="/docs")
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=False,  # Set to True in production
        samesite='lax'
    )
    return response

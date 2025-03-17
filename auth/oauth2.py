from datetime import datetime, timedelta, timezone
from fastapi import Depends, status, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from authlib.integrations.starlette_client import OAuth
from config.settings import settings
from config.database import get_async_db
from src import models
from auth import schemas


# Set tokenUrl to an existing endpoint for Swagger UI
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='api/v1/auth/login')

oauth = OAuth()

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES


def create_access_token(data: dict):
    """
    Create a JWT access token.
    """
    to_encode = data.copy()
    expire = datetime.now(tz=timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encode_jwt


def verify_access_token(token: str, credentials_exception):
    """
    Verify the validity of the access token.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")
        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=str(id))
    except JWTError:
        raise credentials_exception
    return token_data


async def get_current_user(
    request: Request,
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_async_db)
):
    """
    Get the currently authenticated user based on the access token.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Not Authenticated",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # Try to get token from cookie
    token_from_cookie = request.cookies.get("access_token")
    if token_from_cookie:
        token = token_from_cookie
    elif token:
        # Token from Authorization header (for Swagger UI)
        token = token
    else:
        raise credentials_exception

    token_data = verify_access_token(token, credentials_exception)
    user_id = int(token_data.id) 
    # Fetch user asynchronously
    result = await db.execute(
        select(models.UserTable).filter(models.UserTable.id == user_id)
    )
    user = result.scalar_one_or_none()

    if not user:
        raise credentials_exception

    return user



# Google OAuth client registration
oauth.register(
    name='google',
    client_id=settings.GOOGLE_CLIENT_ID,
    client_secret=settings.GOOGLE_CLIENT_SECRET,
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={'scope': 'openid email profile'}
)


# Facebook OAuth client registration
oauth.register(
    name='facebook',
    client_id=settings.FACEBOOK_APP_ID,
    client_secret=settings.FACEBOOK_APP_SECRET,
    access_token_url='https://graph.facebook.com/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
    client_kwargs={'scope': 'email'},
    api_base_url='https://graph.facebook.com/'
)

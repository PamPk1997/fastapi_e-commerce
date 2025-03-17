from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException
from jose import JWTError, jwt
from config.settings import settings



pwd_context = CryptContext(schemes=['bcrypt'],deprecated= "auto") #deprecated="auto": This tells the CryptContext to automatically mark older, weaker schemes as deprecated if they are found

def hash(password: str):
    return pwd_context.hash(password)

def verify_pass(plain_password,hashed_password):
    return pwd_context.verify(plain_password,hashed_password)



def create_email_verification_token(email: str):
    """
    Create a JWT token for email verification.
    """
    to_encode = {
        "email": email,
        "type": "email_verification"  # Include token type for validation
    }
    expire = datetime.now(tz=timezone.utc) + timedelta(minutes=15)  # Token valid for 15 minutes
    to_encode.update({"exp": expire})
    encode_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encode_jwt


def verify_email_verification_token(token: str):
    """
    Verify the validity of the email verification token.
    """
    credentials_exception = HTTPException(
        status_code=401,
        detail="Invalid or expired token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=settings.ALGORITHM)
        email: str = payload.get("email")
        token_type: str = payload.get("type")
        if email is None or token_type != "email_verification":
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return email

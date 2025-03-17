from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_HOSTNAME: str
    DATABASE_PORT: int
    DATABASE_PASSWORD: str
    DATABASE_NAME: str
    DATABASE_USERNAME: str
    SECRET_KEY: str
    ALGORITHM: str
    DEBUGGING: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    Email_FROM: str 
    EMAIL_PASSWORD: str
    SMTP_SERVER: str 
    SMTP_PORT: int 
    TWILIO_ACCOUNT_SID: str
    TWILIO_AUTH_TOKEN: str
    TWILIO_PHONE_NUMBER: int
    STRIPE_SECRET_KEY: str
    STRIPE_PUBLIC_KEY: str
    STRIPE_WEBHOOK_SECRET:str

    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str

    FACEBOOK_APP_ID: int
    FACEBOOK_APP_SECRET: str
    NGROK_URL:str


    class Config:
        env_file = "./.env"

settings = Settings()
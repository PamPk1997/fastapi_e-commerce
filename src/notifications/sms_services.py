import asyncio
from twilio.rest import Client
from config.settings import settings

# Initialize Twilio client
twilio_client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)


async def send_sms_notification(to_phone_num: str, message: str):
    """
    Sends an SMS notification using Twilio in a non-blocking manner.
    """
    try:
        # Offload Twilio's blocking call to a separate thread
        result = await asyncio.to_thread(
            twilio_client.messages.create,
            body=message,
            from_=settings.TWILIO_PHONE_NUMBER,
            to=to_phone_num
        )
        print(f"SMS sent successfully, Message SID: {result.sid}")
    except Exception as e:
        print(f"Error sending SMS: {e}")


async def send_sms_otp(to_phone_num: str, message: str):
    """
    Sends an OTP SMS using Twilio in a non-blocking manner.
    """
    try:
        # Offload Twilio's blocking call to a separate thread
        result = await asyncio.to_thread(
            twilio_client.messages.create,
            body=message,
            from_=settings.TWILIO_PHONE_NUMBER,
            to=to_phone_num
        )
        print(f"SMS sent successfully, Message SID: {result.sid}")
    except Exception as e:
        print(f"Error sending SMS: {e}")

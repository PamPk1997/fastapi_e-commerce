import aiosmtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config.settings import settings


async def send_email_assign_role(user_email: str, username: str, role_name: str):
    sender_email = settings.Email_FROM
    password = settings.EMAIL_PASSWORD

    subject = "You Have been Assigned a New Role"
    body = f"Hello {username},\n\nYou have been assigned the role: {role_name}."

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = user_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    try:
        await aiosmtplib.send(
            message,
            hostname=settings.SMTP_SERVER,
            port=settings.SMTP_PORT,
            username=sender_email,
            password=password,
            start_tls=True,
        )
        print(f"Email successfully sent to {user_email}")
    except Exception as e:
        print(f"Error sending email: {e}")


async def send_email_order_place(user_email: str, user_name: str, order_id: int):
    sender_email = settings.Email_FROM
    password = settings.EMAIL_PASSWORD

    subject = "Your Order is Placed"
    body = f"Hello {user_name},\n\nYour order has been placed.\n\nThis is your Order ID: {order_id}\n\nThank you for shopping with us."

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = user_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    try:
        await aiosmtplib.send(
            message,
            hostname=settings.SMTP_SERVER,
            port=settings.SMTP_PORT,
            username=sender_email,
            password=password,
            start_tls=True,
        )
        print(f"Email successfully sent to {user_email}")
    except Exception as e:
        print(f"Error sending email: {e}")


async def send_email_order_cancel(user_email: str, user_name: str, order_id: int):
    sender_email = settings.Email_FROM
    password = settings.EMAIL_PASSWORD

    subject = "Your Order is Cancelled"
    body = f"Hello {user_name},\n\nYour order with Order ID {order_id} has been cancelled.\n\nThank you for shopping with us."

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = user_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    try:
        await aiosmtplib.send(
            message,
            hostname=settings.SMTP_SERVER,
            port=settings.SMTP_PORT,
            username=sender_email,
            password=password,
            start_tls=True,
        )
        print(f"Email successfully sent to {user_email}")
    except Exception as e:
        print(f"Error sending email: {e}")


async def send_email_product_added(product_name: str, user_email: str):
    sender_email = settings.Email_FROM
    password = settings.EMAIL_PASSWORD

    subject = "A New Product Has Been Added"
    body = f"A new product has been added to the website.\n\nThe name of the product is: {product_name}"

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = user_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    try:
        await aiosmtplib.send(
            message,
            hostname=settings.SMTP_SERVER,
            port=settings.SMTP_PORT,
            username=sender_email,
            password=password,
            start_tls=True,
        )
        print(f"Email successfully sent to {user_email}")
    except Exception as e:
        print(f"Error sending email: {e}")


async def send_email_NewUser(firstname: str, lastname: str, user_name: str, user_email: str,verification_url:str):
    sender_email = settings.Email_FROM
    password = settings.EMAIL_PASSWORD

    subject = "Verify Your Email"
    body =  f"""
    Hello {firstname} {lastname},

    Thank you for registering. Please verify your email by clicking the link below:

    {verification_url}

    If you did not register, please ignore this email.

    Regards,
    Your Team
    """
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = user_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    try:
        await aiosmtplib.send(
            message,
            hostname=settings.SMTP_SERVER,
            port=settings.SMTP_PORT,
            username=sender_email,
            password=password,
            start_tls=True,
        )
        print(f"Email successfully sent to {user_email}")
    except Exception as e:
        print(f"Error sending email: {e}")


async def send_email_otp(user_email: str, user_name: str, otp: int):
    sender_email = settings.Email_FROM
    password = settings.EMAIL_PASSWORD

    subject = "User Login OTP"
    body = f"Hello {user_name},\n\nYour OTP for login is: {otp}"

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = user_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    try:
        await aiosmtplib.send(
            message,
            hostname=settings.SMTP_SERVER,
            port=settings.SMTP_PORT,
            username=sender_email,
            password=password,
            start_tls=True,
        )
        print(f"Email successfully sent to {user_email}")
    except Exception as e:
        print(f"Error sending email: {e}")


async def send_email_resetpass(user_name: str,user_email: str,reset_link:str):
    sender_email = settings.Email_FROM
    password = settings.EMAIL_PASSWORD

    subject = "Reset Password"
    body = f"""Hello {user_name},

Please click the link below to reset your password:

{reset_link}

If you did not request this password reset, please ignore this email.

Thank you.
"""
    
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = user_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    try:
        await aiosmtplib.send(
            message,
            hostname=settings.SMTP_SERVER,
            port=settings.SMTP_PORT,
            username=sender_email,
            password=password,
            start_tls=True,
        )
        print(f"Email successfully sent to {user_email}")
    except Exception as e:
        print(f"Error sending email: {e}")
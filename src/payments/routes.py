import stripe
import os
from fastapi import APIRouter, Depends, HTTPException,Request
from sqlalchemy.orm import Session
from config.database import get_async_db
from src import models
from auth import oauth2
from config.settings import settings
from src.models import PaymentMethod,PaymentStatus
from fastapi.templating import Jinja2Templates


# Initialize Stripe with the secret key
stripe.api_key = settings.STRIPE_SECRET_KEY

dir_path = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(dir_path, 'templates'))

payment_router = APIRouter(
    prefix="/payments",
    tags=["Payments"]
)



@payment_router.post("/create-payment")
async def create_payment_intent(
    order_id: int,
    request: Request,
    db: Session = Depends(get_async_db),
    current_user: int = Depends(oauth2.get_current_user)
):
    # Retrieve the order
    order = db.query(models.OrderTable).filter(models.OrderTable.id == order_id, models.OrderTable.user_id == current_user.id).first()
    
    total_quantity = len(order.order_items)

    try:
        # Create a Checkout session for Stripe
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'inr',
                        'product_data': {
                            'name': f"Order {order.id}",
                        },
                        'unit_amount': int(order.total_amount * 100),
                    },
                    'quantity': total_quantity,
                },
            ],
            mode='payment',
            success_url=f"{request.base_url}api/payments/success?session_id={{CHECKOUT_SESSION_ID}}",
            cancel_url=f"{request.base_url}api/payments/cancel",
            metadata={
                "order_id": order.id,
                "user_id": current_user.id
            }
        )

        # Create a payment intent if needed
        payment_intent = stripe.PaymentIntent.create(
            amount=int(order.total_amount * 100),  # Amount in cents (Stripe uses the smallest unit)
            currency="inr",  # Adjust the currency to your preference
            metadata={"order_id": order.id, "user_id": current_user.id}
        )

        # Save the payment in the database as pending
        new_payment = models.PaymentTable(
            order_id=order.id,
            user_id=current_user.id,
            payment_amount=order.total_amount,
            payment_status=PaymentStatus.PENDING,  # Set status to pending
            payment_method=PaymentMethod.CREDIT_CARD,
            transction_id=payment_intent['id']
        )

        db.add(new_payment)
        db.commit()

        return {"checkout_url": checkout_session.url, "client_secret": payment_intent['client_secret']}
    
    except stripe.error.StripeError as e:
        raise HTTPException(status_code=400, detail=str(e))


@payment_router.get("/success")
async def payment_success(session_id: str, db: Session = Depends(get_async_db),current_user: int = Depends(oauth2.get_current_user)):
    # Retrieve the session to verify payment
    session = stripe.checkout.Session.retrieve(session_id)

    if session.payment_status != 'paid':
        raise HTTPException(status_code=400, detail="Payment not successful")

    # Retrieve order ID and user ID from metadata
    order_id = session.metadata['order_id']
    user_id = session.metadata['user_id']

    # Retrieve the order
    order = db.query(models.OrderTable).filter(models.OrderTable.id == order_id).first()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    # Update payment status to completed
    payment = db.query(models.PaymentTable).filter(models.PaymentTable.order_id == order.id).first()
    payment.payment_status = PaymentStatus.COMPLETED
    db.commit()

    return {"message": "Payment successful", "order_id": order.id, "payment_status": PaymentStatus.COMPLETED}


@payment_router.get("/cancel")
async def payment_cancel(current_user: int = Depends(oauth2.get_current_user)):
    return {"message": "Payment canceled"}

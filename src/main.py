from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from config.settings import settings
from src.users.routes import user_router,role_router
from src.products.routes import product_router,category_router,subcategory_router
from src.users.auth import auth_router
from src.cart.routes import cart_router
from src.orders.routes import order_router
from src.coupondiscount.routes import coupon_router,discount_router
from src.payments.routes import payment_router
from src.logger import log_router
from src.support.chat import chat_router
# from src.tasks import send_email_task




base_end_point= "/api/v1"

app = FastAPI(title="This is a Ecommerce-Website",
              description="This documentation includes all the API specification of Ecommerce-Website",
              version="1.0",
              debug=True, reload=True)


app.mount("/static", StaticFiles(directory="src/static"), name="static")
app.mount ("/support/uploads",StaticFiles(directory="src/support/uploads"),name="uploads")

app.add_middleware(
    SessionMiddleware,
    secret_key= settings.SECRET_KEY ,
    same_site= 'lax',
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://bf29-106-219-164-104.ngrok-free.app",'0.0.0.0'],  # Adjust this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def home():
    return {"Hello": "Welcome To the Ecommerce-website"}


@app.get("/health")
def health_check():
    return {"status": "OK"}

app.include_router(auth_router,prefix=base_end_point)
app.include_router(user_router,prefix=base_end_point)
app.include_router(role_router,prefix=base_end_point)
app.include_router(category_router,prefix=base_end_point)
app.include_router(subcategory_router,prefix=base_end_point)
app.include_router(product_router,prefix=base_end_point)
app.include_router(coupon_router,prefix=base_end_point)
app.include_router(discount_router,prefix=base_end_point)
app.include_router(cart_router,prefix=base_end_point)
app.include_router(order_router,prefix=base_end_point)
app.include_router(payment_router,prefix=base_end_point)
app.include_router(log_router,prefix=base_end_point)
app.include_router(chat_router,prefix=base_end_point)

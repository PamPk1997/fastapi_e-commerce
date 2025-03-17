from fastapi import APIRouter
import logging
from logging.handlers import RotatingFileHandler

# Setup logging
logger = logging.getLogger("uvicorn")
handler = RotatingFileHandler("app.log", maxBytes=10**6, backupCount=3)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)


log_router = APIRouter(
    prefix="/log", tags=["Logs"])


# Test logging
@log_router.get("/logs")
def read_root():
    logger.info("log endpoint hit")
    return {"message": "Hi, Every Thing is Fine"}



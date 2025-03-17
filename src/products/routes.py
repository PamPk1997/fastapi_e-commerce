from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from src import models
from config.database import get_async_db
from . import schemas, services
from auth.oauth2 import get_current_user
from src.notifications.email_services import send_email_product_added


product_router = APIRouter(
    prefix="/products",
    tags=["Products"]
)

category_router = APIRouter(
    prefix="/category",
    tags=["Category"]
)

subcategory_router = APIRouter(
    prefix="/subcategory",
    tags=["SubCategory"]
)


# Product Routers

@product_router.get("/", response_model=List[schemas.ProductOut])
async def get_products(db: AsyncSession = Depends(get_async_db), current_user: models.UserTable = Depends(get_current_user)):
    return await services.get_all_products(db)


@product_router.get("/{product_id}", response_model=schemas.ProductOut)
async def get_product(product_id: int, db: AsyncSession = Depends(get_async_db), current_user: models.UserTable = Depends(get_current_user)):
    product = await services.get_product_by_id(product_id, db)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product


@product_router.post("/", response_model=schemas.ProductOut, status_code=status.HTTP_201_CREATED)
async def create_product(product: schemas.ProductCreate, db: AsyncSession = Depends(get_async_db), current_user: models.UserTable = Depends(get_current_user),
                         background_task: BackgroundTasks = BackgroundTasks()):
    background_task.add_task(send_email_product_added, product.name, current_user.email)
    return await services.create_product(product, db)


@product_router.put("/{product_id}", response_model=schemas.ProductOut)
async def update_product(product_id: int, product_update: schemas.ProductUpdate, db: AsyncSession = Depends(get_async_db), current_user: models.UserTable = Depends(get_current_user)):
    product = await services.update_product(product_id, product_update, db)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product


@product_router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(product_id: int, db: AsyncSession = Depends(get_async_db), current_user: models.UserTable = Depends(get_current_user)):
    deleted = await services.delete_product(product_id, db)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return {"message": "Product deleted successfully"}



# Category Routers

@category_router.get("/", response_model=List[schemas.CategoryOut])
async def get_category(db: AsyncSession = Depends(get_async_db), current_user: models.UserTable = Depends(get_current_user)):
    return await services.get_all_category(db)


@category_router.get("/{category_id}", response_model=schemas.CategoryOut)
async def get_category(category_id: int, db: AsyncSession = Depends(get_async_db), current_user: models.UserTable = Depends(get_current_user)):
    category = await services.get_category_by_id(category_id, db)
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    return category


@category_router.post("/", response_model=schemas.CategoryOut, status_code=status.HTTP_201_CREATED)
async def create_category(category: schemas.CategoryCreate, db: AsyncSession = Depends(get_async_db), current_user: models.UserTable = Depends(get_current_user)):
    return await services.create_category(category, db)


@category_router.put("/{category_id}", response_model=schemas.CategoryOut)
async def update_category(category_id: int, category_update: schemas.CategoryUpdate, db: AsyncSession = Depends(get_async_db), current_user: models.UserTable = Depends(get_current_user)):
    category = await services.update_category(category_id, category_update, db)
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    return category


@category_router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(category_id: int, db: AsyncSession = Depends(get_async_db), current_user: models.UserTable = Depends(get_current_user)):
    db_category = await services.delete_category(category_id, db)
    if not db_category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    return {"message": "Category deleted successfully"}



# Subcategory Routers

@subcategory_router.get("/", response_model=List[schemas.SubCategoryOut])
async def get_subcategory(db: AsyncSession = Depends(get_async_db), current_user: models.UserTable = Depends(get_current_user)):
    return await services.get_all_subcategory(db)


@subcategory_router.get("/{subcategory_id}", response_model=schemas.SubCategoryOut)
async def get_subcategory(subcategory_id: int, db: AsyncSession = Depends(get_async_db), current_user: models.UserTable = Depends(get_current_user)):
    db_subcategory = await services.get_subcategory_by_id(subcategory_id, db)
    if not db_subcategory:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Subcategory not found")
    return db_subcategory


@subcategory_router.post("/", response_model=schemas.SubCategoryOut, status_code=status.HTTP_201_CREATED)
async def create_subcategory(subcategory: schemas.SubCategoryCreate, db: AsyncSession = Depends(get_async_db), current_user: models.UserTable = Depends(get_current_user)):
    return await services.create_subcategory(subcategory, db)


@subcategory_router.put("/{subcategory_id}", response_model=schemas.SubCategoryOut)
async def update_subcategory(subcategory_id: int, subcategory_update: schemas.SubCategoryUpdate, db: AsyncSession = Depends(get_async_db), current_user: models.UserTable = Depends(get_current_user)):
    db_subcategory = await services.update_subcategory(subcategory_id, subcategory_update, db)
    if not db_subcategory:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Subcategory not found")
    return db_subcategory


@subcategory_router.delete("/{subcategory_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_subcategory(subcategory_id: int, db: AsyncSession = Depends(get_async_db), current_user: models.UserTable = Depends(get_current_user)):
    db_subcategory = await services.delete_subcategory(subcategory_id, db)
    if not db_subcategory:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Subcategory not found")
    return {"message": "Subcategory deleted successfully"}

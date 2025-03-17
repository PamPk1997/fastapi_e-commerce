from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.products import schemas
from src import models


# Product Services

async def get_all_products(db: AsyncSession):
    result = await db.execute(select(models.ProductTable))
    return result.scalars().all()


async def get_product_by_id(product_id: int, db: AsyncSession):
    result = await db.execute(
        select(models.ProductTable).filter(models.ProductTable.id == product_id)
    )
    return result.scalar_one_or_none()


async def create_product(product: schemas.ProductCreate, db: AsyncSession):
    new_product = models.ProductTable(**product.model_dump())

    db.add(new_product)
    await db.commit()
    await db.refresh(new_product)
    return new_product


async def update_product(product_id: int, product_update: schemas.ProductUpdate, db: AsyncSession):
    result = await db.execute(
        select(models.ProductTable).filter(models.ProductTable.id == product_id)
    )
    product = result.scalar_one_or_none()

    if not product:
        return None

    for key, value in product_update.model_dump().items():
        setattr(product, key, value)

    await db.commit()
    await db.refresh(product)
    return product


async def delete_product(product_id: int, db: AsyncSession):
    result = await db.execute(
        select(models.ProductTable).filter(models.ProductTable.id == product_id)
    )
    product = result.scalar_one_or_none()

    if not product:
        return None

    await db.delete(product)
    await db.commit()
    return True


# Category Services

async def get_all_category(db: AsyncSession):
    result = await db.execute(select(models.CategoriesTable))
    return result.scalars().all()


async def get_category_by_id(category_id: int, db: AsyncSession):
    result = await db.execute(
        select(models.CategoriesTable).filter(models.CategoriesTable.id == category_id)
    )
    return result.scalar_one_or_none()


async def create_category(category: schemas.CategoryCreate, db: AsyncSession):
    new_category = models.CategoriesTable(**category.model_dump())

    db.add(new_category)
    await db.commit()
    await db.refresh(new_category)
    return new_category


async def update_category(category_id: int, category_update: schemas.CategoryUpdate, db: AsyncSession):
    result = await db.execute(
        select(models.CategoriesTable).filter(models.CategoriesTable.id == category_id)
    )
    category = result.scalar_one_or_none()

    if not category:
        return None

    for key, value in category_update.model_dump().items():
        setattr(category, key, value)

    await db.commit()
    await db.refresh(category)
    return category


async def delete_category(category_id: int, db: AsyncSession):
    result = await db.execute(
        select(models.CategoriesTable).filter(models.CategoriesTable.id == category_id)
    )
    category = result.scalar_one_or_none()

    if not category:
        return None

    await db.delete(category)
    await db.commit()
    return True


#subcategory services

async def get_all_subcategory(db: AsyncSession):
    result = await db.execute(select(models.SubCategoriesTable))
    return result.scalars().all()


async def get_subcategory_by_id(subcategory_id: int, db: AsyncSession):
    result = await db.execute(
        select(models.SubCategoriesTable).filter(models.SubCategoriesTable.id == subcategory_id)
    )
    return result.scalar_one_or_none()


async def create_subcategory(subcategory: schemas.SubCategoryCreate, db: AsyncSession):
    new_subcategory = models.SubCategoriesTable(**subcategory.model_dump())

    db.add(new_subcategory)
    await db.commit()
    await db.refresh(new_subcategory)
    return new_subcategory


async def update_subcategory(subcategory_id: int, subcategory_update: schemas.SubCategoryUpdate, db: AsyncSession):
    result = await db.execute(
        select(models.SubCategoriesTable).filter(models.SubCategoriesTable.id == subcategory_id)
    )
    subcategory = result.scalar_one_or_none()

    if not subcategory:
        return None

    for key, value in subcategory_update.model_dump().items():
        setattr(subcategory, key, value)

    await db.commit()
    await db.refresh(subcategory)
    return subcategory


async def delete_subcategory(subcategory_id: int, db: AsyncSession):
    result = await db.execute(
        select(models.SubCategoriesTable).filter(models.SubCategoriesTable.id == subcategory_id)
    )
    subcategory = result.scalar_one_or_none()

    if not subcategory:
        return None

    await db.delete(subcategory)
    await db.commit()
    return True








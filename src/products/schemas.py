from pydantic import BaseModel
from typing import Optional,List
from datetime import datetime


class ProductBase(BaseModel):
    name:str
    desc: Optional[str] = None
    price: float
    stock_quantity: int
    category_id: int
    subcategory_id:int

class ProductCreate(ProductBase):
    pass 


class ProductUpdate(BaseModel):
    name: Optional[str]
    desc: Optional[str]
    price: Optional[str]
    stock_quantity: Optional[int]
    category_id: Optional[str]
    subcategory_id: Optional[str]



class ProductOut(ProductBase):
    id:int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class CategoryBase(BaseModel):
    name: str
    desc: Optional[str] = None


class CategoryCreate(CategoryBase):
    pass 


class CategoryUpdate(BaseModel):
    name: Optional[str]
    desc: Optional[str]


class CategoryOut(CategoryBase):
    id: int
    created_at: datetime
    # products:List[ProductOut] = []
    
    class Config:
        from_attributes = True



class SubCategoryBase(BaseModel):
    name: str
    desc: Optional[str] = None
    category_id: int



class SubCategoryCreate(SubCategoryBase):
    pass



class SubCategoryUpdate(BaseModel):
    name: Optional[str]
    desc: Optional[str]
    category_id: Optional[int]


class SubCategoryOut(SubCategoryBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True




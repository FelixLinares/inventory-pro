from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Dict

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    is_admin: bool
    class Config: from_attributes = True

class UserAdminCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    is_admin: bool = False

class ResetPasswordIn(BaseModel):
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class CategoryIn(BaseModel):
    name: str

class CategoryOut(BaseModel):
    id: int
    name: str
    class Config: from_attributes = True

class WarehouseIn(BaseModel):
    name: str

class WarehouseOut(BaseModel):
    id: int
    name: str
    class Config: from_attributes = True

class ProductIn(BaseModel):
    code: str
    name: str
    category_id: Optional[int] = None
    min_stock: int = 0

class ProductOut(BaseModel):
    id: int
    code: str
    name: str
    category_id: Optional[int]
    min_stock: int
    class Config: from_attributes = True

class MovementIn(BaseModel):
    product_id: int
    warehouse_id: int
    type: str = Field(pattern="^(in|out)$")
    qty: int
    note: Optional[str] = ""

class MovementOut(BaseModel):
    id: int
    product_id: int
    warehouse_id: int
    type: str
    qty: int
    note: str
    class Config: from_attributes = True

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, ForeignKey, Boolean, DateTime, Text, func
from .db import Base

class User(Base):
    __allow_unmapped__ = True
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(120))
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    failed_attempts: Mapped[int] = mapped_column(Integer, default=0)
    is_locked: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped = mapped_column(DateTime(timezone=True), server_default=func.now())

class Category(Base):
    __allow_unmapped__ = True
    __tablename__ = "categories"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True)

class Warehouse(Base):
    __allow_unmapped__ = True
    __tablename__ = "warehouses"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True)

class Product(Base):
    __allow_unmapped__ = True
    __tablename__ = "products"
    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(String(80), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(255))
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"), nullable=True)
    min_stock: Mapped[int] = mapped_column(Integer, default=0)

class Stock(Base):
    __allow_unmapped__ = True
    __tablename__ = "stocks"
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), primary_key=True)
    warehouse_id: Mapped[int] = mapped_column(ForeignKey("warehouses.id"), primary_key=True)
    qty: Mapped[int] = mapped_column(Integer, default=0)

class Movement(Base):
    __allow_unmapped__ = True
    __tablename__ = "movements"
    id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), index=True)
    warehouse_id: Mapped[int] = mapped_column(ForeignKey("warehouses.id"), index=True)
    type: Mapped[str] = mapped_column(String(20))  # in|out
    qty: Mapped[int] = mapped_column(Integer)
    note: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped = mapped_column(DateTime(timezone=True), server_default=func.now())

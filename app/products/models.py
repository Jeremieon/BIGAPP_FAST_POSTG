from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.db import Base

class Categories(Base):
    __tablename__ = "category"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    image_url = Column(String)
    product = relationship("Product", back_populates="category")


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    quantity = Column(Integer)
    description = Column(Text)
    price = Column(Float)
    image_url = Column(String)
    category_id = Column(Integer, ForeignKey('category.id', ondelete="CASCADE"), )
    category = relationship("Categories", back_populates="product")
    order_details = relationship("OrderDetails", back_populates="product_order_details")
    cart_items = relationship("CartItems", back_populates="products")


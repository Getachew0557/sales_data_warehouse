from sqlalchemy import Column, Integer, String, Float, DateTime
from .database import Base

# Bronze Layer
class RawSale(Base):
    __tablename__ = "raw_sales"
    order_id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer)
    product_id = Column(Integer)
    region = Column(String)
    quantity = Column(Integer)
    unit_price = Column(Float)
    order_date = Column(DateTime)

# Silver Layer
class CleanSale(Base):
    __tablename__ = "clean_sales"
    order_id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer)
    product_id = Column(Integer)
    region = Column(String)
    quantity = Column(Integer)
    unit_price = Column(Float)
    order_date = Column(DateTime)

# Gold Layer: Star Schema
class DimCustomer(Base):
    __tablename__ = "dim_customers"
    customer_id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String)

class DimProduct(Base):
    __tablename__ = "dim_products"
    product_id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String)

class DimRegion(Base):
    __tablename__ = "dim_regions"
    region_id = Column(Integer, primary_key=True, index=True)
    region_name = Column(String)

class DimDate(Base):
    __tablename__ = "dim_dates"
    date_id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime)
    year = Column(Integer)
    month = Column(Integer)
    day = Column(Integer)

class FactSale(Base):
    __tablename__ = "fact_sales"
    sale_id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer)
    product_id = Column(Integer)
    region_id = Column(Integer)
    date_id = Column(Integer)
    quantity = Column(Integer)
    total_price = Column(Float)
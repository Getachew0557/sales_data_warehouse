import sys
import pytest
# Add project root to sys.path
sys.path.append(r"C:\Users\gech\Documents\Getachew_project\sales_data_warehouse")
from src.database import SessionLocal
from src.models import RawSale, CleanSale, FactSale, DimCustomer, DimProduct, DimRegion, DimDate
from scripts.bronze.load_raw import load_raw_data
from scripts.silver.clean_transform import clean_transform_data
from scripts.gold.create_analytics import create_analytics

@pytest.fixture
def db():
    db = SessionLocal()
    yield db
    db.close()

def test_load_raw(db):
    load_raw_data(r'C:\Users\gech\Documents\Getachew_project\sales_data_warehouse\datasets\sample_sales.csv')
    count = db.query(RawSale).count()
    assert count == 4

def test_clean_transform(db):
    load_raw_data(r'C:\Users\gech\Documents\Getachew_project\sales_data_warehouse\datasets\sample_sales.csv')
    clean_transform_data()
    clean_sale = db.query(CleanSale).first()
    assert clean_sale.region == "North"
    assert clean_sale.quantity >= 0

def test_create_analytics(db):
    load_raw_data(r'C:\Users\gech\Documents\Getachew_project\sales_data_warehouse\datasets\sample_sales.csv')
    clean_transform_data()
    create_analytics()
    fact = db.query(FactSale).first()
    assert fact.quantity == 5
    assert fact.total_price == 5 * 20.50
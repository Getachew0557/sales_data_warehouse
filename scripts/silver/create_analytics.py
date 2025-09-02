from sqlalchemy.orm import Session
from src.database import SessionLocal
from src.models import CleanSale, DimCustomer, DimProduct, DimRegion, DimDate, FactSale
from datetime import datetime

def create_analytics():
    db = SessionLocal()
    try:
        # Populate dimension tables
        customers = db.query(CleanSale.customer_id).distinct().all()
        for customer_id in customers:
            if not db.query(DimCustomer).filter(DimCustomer.customer_id == customer_id[0]).first():
                db.add(DimCustomer(customer_id=customer_id[0], customer_name=f"Customer_{customer_id[0]}"))
        
        products = db.query(CleanSale.product_id).distinct().all()
        for product_id in products:
            if not db.query(DimProduct).filter(DimProduct.product_id == product_id[0]).first():
                db.add(DimProduct(product_id=product_id[0], product_name=f"Product_{product_id[0]}"))
        
        regions = db.query(CleanSale.region).distinct().all()
        for idx, region in enumerate(regions, 1):
            if not db.query(DimRegion).filter(DimRegion.region_name == region[0]).first():
                db.add(DimRegion(region_id=idx, region_name=region[0]))
        
        dates = db.query(CleanSale.order_date).distinct().all()
        for idx, date in enumerate(dates, 1):
            date_val = date[0]
            if not db.query(DimDate).filter(DimDate.date == date_val).first():
                db.add(DimDate(
                    date_id=idx,
                    date=date_val,
                    year=date_val.year,
                    month=date_val.month,
                    day=date_val.day
                ))
        
        # Populate fact table
        sales = db.query(CleanSale).all()
        for sale in sales:
            date_id = db.query(DimDate).filter(DimDate.date == sale.order_date).first().date_id
            region_id = db.query(DimRegion).filter(DimRegion.region_name == sale.region).first().region_id
            fact_sale = FactSale(
                customer_id=sale.customer_id,
                product_id=sale.product_id,
                region_id=region_id,
                date_id=date_id,
                quantity=sale.quantity,
                total_price=sale.quantity * sale.unit_price
            )
            db.add(fact_sale)
        db.commit()
    finally:
        db.close()
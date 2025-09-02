from sqlalchemy.orm import Session
from src.database import SessionLocal
from src.models import RawSale, CleanSale

def clean_transform_data():
    db = SessionLocal()
    try:
        raw_sales = db.query(RawSale).all()
        for raw in raw_sales:
            # Clean data: Standardize region, validate quantity
            region = raw.region.strip().capitalize() if raw.region else "Unknown"
            quantity = max(0, raw.quantity)  # Ensure non-negative
            unit_price = round(raw.unit_price, 2) if raw.unit_price else 0.0
            
            clean_sale = CleanSale(
                order_id=raw.order_id,
                customer_id=raw.customer_id,
                product_id=raw.product_id,
                region=region,
                quantity=quantity,
                unit_price=unit_price,
                order_date=raw.order_date
            )
            db.add(clean_sale)
        db.commit()
    finally:
        db.close()
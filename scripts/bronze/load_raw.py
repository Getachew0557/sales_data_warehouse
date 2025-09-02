import pandas as pd
from sqlalchemy.orm import Session
from src.database import SessionLocal
from src.models import RawSale

def load_raw_data(csv_path: str):
    db = SessionLocal()
    try:
        df = pd.read_csv(csv_path)
        for _, row in df.iterrows():
            sale = RawSale(
                order_id=row['order_id'],
                customer_id=row['customer_id'],
                product_id=row['product_id'],
                region=row['region'],
                quantity=row['quantity'],
                unit_price=row['unit_price'],
                order_date=row['order_date']
            )
            db.add(sale)
        db.commit()
    finally:
        db.close()
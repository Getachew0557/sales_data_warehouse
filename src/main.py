from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas, database

app = FastAPI()

@app.post("/sales/", response_model=schemas.SaleResponse)
def create_sale(sale: schemas.SaleCreate, db: Session = Depends(database.get_db)):
    db_sale = models.RawSale(**sale.dict())
    db.add(db_sale)
    db.commit()
    db.refresh(db_sale)
    return db_sale

@app.get("/sales/", response_model=list[schemas.SaleResponse])
def read_sales(db: Session = Depends(database.get_db)):
    return db.query(models.RawSale).all()
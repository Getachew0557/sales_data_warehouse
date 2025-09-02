from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class SaleCreate(BaseModel):
    customer_id: int
    product_id: int
    region: str
    quantity: int
    unit_price: float
    order_date: datetime

class SaleResponse(BaseModel):
    order_id: int
    customer_id: int
    product_id: int
    region: str
    quantity: int
    unit_price: float
    order_date: datetime

    model_config = ConfigDict(from_attributes=True)
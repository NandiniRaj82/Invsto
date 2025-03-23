from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal

class TickerDataModel(BaseModel):
    datetime: datetime
    open: Decimal
    high: Decimal
    low: Decimal
    close: Decimal
    volume: int

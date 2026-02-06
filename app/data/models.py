from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class Candle:

    symbol: str
    timeframe: str

    open_time: datetime
    close_time: datetime

    open_price: float
    high_price: float
    low_price: float
    close_price: float

    volume: float
    number_of_trades: int

    is_closed: bool

    mode:str
   

    


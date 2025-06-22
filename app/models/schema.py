from pydantic import BaseModel, Field
from typing import List

class Candle(BaseModel):
    """
    Represents a single candlestick with OHLC (Open, High, Low, Close) data.
    
    Attributes:
        open (float): Opening price of the candle
        high (float): Highest price reached during the candle period
        low (float): Lowest price reached during the candle period
        close (float): Closing price of the candle
    """
    open: float = Field(..., gt=0, description="Opening price")
    high: float = Field(..., gt=0, description="Highest price")
    low: float = Field(..., gt=0, description="Lowest price")
    close: float = Field(..., gt=0, description="Closing price")

class SignalRequest(BaseModel):
    """
    Request model for generating breakout signals.
    
    Attributes:
        symbol (str): Trading symbol (e.g., 'INFY', 'AAPL')
        price_data (List[Candle]): List of candlestick data for analysis
    """
    symbol: str = Field(..., min_length=1, description="Trading symbol")
    price_data: List[Candle] = Field(..., min_items=1, description="Price data for analysis")
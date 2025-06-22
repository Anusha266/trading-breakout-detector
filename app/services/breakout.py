def detect_breakout(price_data):
    """
    Detect breakout signals based on price data.
    
    A breakout is detected when the last candle closes above the maximum high
    of the previous 3 candles, indicating a potential upward momentum.
    
    Args:
        price_data (List[Candle]): List of candle data with OHLC values
        
    Returns:
        dict: Breakout signal with type, stop-loss, and take-profit levels
              Returns None if no breakout is detected or insufficient data
    """
    # Validate minimum data requirement (need at least 4 candles)
    if len(price_data) < 4:
        return None
    
    # Get the last candle (most recent)
    last_candle = price_data[-1]
    
    # Extract high values from previous 3 candles
    previous_highs = [candle.high for candle in price_data[-4:-1]]
    
    # Check if last candle closes above the maximum of previous 3 highs
    if last_candle.close > max(previous_highs):
        # Calculate stop-loss: lowest low from previous 3 candles
        recent_low = min([candle.low for candle in price_data[-4:-1]])
        
        # Calculate take-profit: Entry price + 2 × (Entry price - Stop Loss)
        # This provides a 1:2 risk-reward ratio
        risk = last_candle.close - recent_low
        take_profit = last_candle.close + (2 * risk)
        
        return {
            "type": "BUY",
            "sl": recent_low,    
            "tp": round(take_profit, 2)
        }
    
    return None
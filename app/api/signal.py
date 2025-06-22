from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from app.models.schema import SignalRequest
from app.services.breakout import detect_breakout

router = APIRouter()

@router.post("/generate-signal")
def generate_signal(data: SignalRequest):
    """
    Generate breakout trading signals based on price data.
    
    Analyzes the provided price data to detect breakout patterns and returns
    trading signals with stop-loss and take-profit levels.
    
    Args:
        data (SignalRequest): Request containing symbol and price data
        
    Returns:
        JSONResponse: Trading signal or no-signal message
    """
    # Validate that price data is not empty
    if not data.price_data:
        raise HTTPException(status_code=400, detail="Price data cannot be empty")
    
    # Detect breakout using the service
    signal = detect_breakout(data.price_data)
    
    if signal:
        return JSONResponse(content=signal)
    
    return JSONResponse(content={"message": "No Breakout signal detected"})
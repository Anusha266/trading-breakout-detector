from fastapi import FastAPI
from fastapi.responses import JSONResponse
from app.api.signal import router as signal_router

app = FastAPI(
    title="Breakout Signal API",
    description="A FastAPI application that detects breakout signals in financial price data and generates trading signals with stop-loss and take-profit levels.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

@app.get("/")
def root():
    """
    Root endpoint providing API information and available endpoints.
    """
    return JSONResponse(content={
        "message": "Breakout Signal API",
        "version": "1.0.0",
        "endpoints": {
            "generate_signal": "/generate-signal",
            "docs": "/docs",
            "redoc": "/redoc"
        }
    })

app.include_router(signal_router)
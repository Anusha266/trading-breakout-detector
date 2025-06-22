# Breakout Signal API

A FastAPI application that detects breakout signals in financial price data and generates trading signals with stop-loss and take-profit levels.

## Features

- **Breakout Detection**: Identifies when the last candle closes above the previous 3 highs
- **Risk Management**: Automatically calculates stop-loss (recent low) and take-profit (1:2 risk-reward ratio)
- **RESTful API**: Clean JSON-based API endpoints
- **Input Validation**: Comprehensive data validation with Pydantic models
- **API Documentation**: Interactive Swagger UI and ReDoc documentation

## Installation

1. **Clone the repository:**

```bash
git clone https://github.com/Anusha266/trading-breakout-detector.git
cd breakout_signal_api
```

2. **Install Python dependencies:**

```bash
# Navigate to the app directory
cd app

# Install required packages
pip install -r requirements.txt
```

**Note**: If you encounter "python command not found", use `python3` instead:

```bash
python3 -m pip install -r requirements.txt
```

## Usage

### Starting the Server

```bash
# Make sure you're in the app directory
cd app

# Start the FastAPI server
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Alternative commands if python is not available:**

```bash
# Using python3
python3 -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Using uvicorn directly (if installed globally)
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

### API Endpoints

#### 1. Root Endpoint

**GET** `/`

Returns API information and available endpoints.

**Response:**

```json
{
  "message": "Breakout Signal API",
  "version": "1.0.0",
  "endpoints": {
    "generate_signal": "/generate-signal",
    "docs": "/docs",
    "redoc": "/redoc"
  }
}
```

#### 2. Generate Signal

**POST** `/generate-signal`

Generates a breakout signal based on price data.

**Request Body:**

```json
{
  "symbol": "INFY",
  "price_data": [
    {
      "open": 100.0,
      "high": 102.0,
      "low": 99.0,
      "close": 101.0
    },
    {
      "open": 101.0,
      "high": 103.0,
      "low": 100.0,
      "close": 102.0
    },
    {
      "open": 102.0,
      "high": 104.0,
      "low": 101.0,
      "close": 103.0
    },
    {
      "open": 103.0,
      "high": 105.0,
      "low": 102.0,
      "close": 104.5
    }
  ]
}
```

**Response (Breakout Detected):**

```json
{
  "type": "BUY",
  "sl": 99.0,
  "tp": 115.5
}
```

**Response (No Breakout):**

```json
{
  "message": "No Breakout signal detected"
}
```

**Error Response (Invalid Data):**

```json
{
  "detail": "Price data cannot be empty"
}
```

### Breakout Logic

The API detects a breakout when:

1. **Minimum Data**: At least 4 candles of data are provided
2. **Breakout Condition**: The last candle closes above the maximum high of the previous 3 candles
3. **Signal Generation**: When conditions are met, generates a BUY signal

When a breakout is detected:

- **Type**: "BUY" signal
- **Stop Loss (sl)**: The lowest low from the previous 3 candles
- **Take Profit (tp)**: Entry price + 2 × (Entry price - Stop Loss) for 1:2 risk-reward ratio

**Example Calculation:**

- Last candle close: 104.5
- Previous 3 highs: [102, 103, 104] → Max: 104
- Previous 3 lows: [99, 100, 101] → Min: 99
- Risk: 104.5 - 99 = 5.5
- Take Profit: 104.5 + (2 × 5.5) = 115.5

## API Documentation

Once the server is running, you can access:

- **Interactive API docs (Swagger UI)**: `http://localhost:8000/docs`
- **ReDoc documentation**: `http://localhost:8000/redoc`

## Example Usage

### Using curl

```bash
# Test with breakout data
curl -X POST "http://localhost:8000/generate-signal" \
     -H "Content-Type: application/json" \
     -d '{
       "symbol": "INFY",
       "price_data": [
         {"open": 100, "high": 102, "low": 99, "close": 101},
         {"open": 101, "high": 103, "low": 100, "close": 102},
         {"open": 102, "high": 104, "low": 101, "close": 103},
         {"open": 103, "high": 105, "low": 102, "close": 104.5}
       ]
     }'

# Test with no breakout data
curl -X POST "http://localhost:8000/generate-signal" \
     -H "Content-Type: application/json" \
     -d '{
       "symbol": "INFY",
       "price_data": [
         {"open": 100, "high": 102, "low": 99, "close": 101},
         {"open": 101, "high": 103, "low": 100, "close": 102},
         {"open": 102, "high": 104, "low": 101, "close": 103},
         {"open": 103, "high": 105, "low": 102, "close": 103.5}
       ]
     }'
```

### Using Python requests

```python
import requests
import json

# API endpoint
url = "http://localhost:8000/generate-signal"

# Sample data
data = {
    "symbol": "INFY",
    "price_data": [
        {"open": 100, "high": 102, "low": 99, "close": 101},
        {"open": 101, "high": 103, "low": 100, "close": 102},
        {"open": 102, "high": 104, "low": 101, "close": 103},
        {"open": 103, "high": 105, "low": 102, "close": 104.5}
    ]
}

# Make request
response = requests.post(url, json=data)
result = response.json()
print(json.dumps(result, indent=2))
```

## Project Structure

```
app/
├── main.py              # FastAPI application entry point with metadata
├── api/
│   └── signal.py        # API routes and endpoints with error handling
├── models/
│   └── schema.py        # Pydantic models for request/response validation
├── services/
│   └── breakout.py      # Breakout detection business logic
├── requirements.txt     # Python dependencies
└── README.md           # This documentation file
```

### File Descriptions

- **`main.py`**: FastAPI application configuration, metadata, and root endpoint
- **`api/signal.py`**: REST API endpoints for signal generation with proper error handling
- **`models/schema.py`**: Pydantic data models for input validation and type safety
- **`services/breakout.py`**: Core business logic for breakout detection algorithm
- **`requirements.txt`**: List of Python package dependencies
- **`README.md`**: Comprehensive documentation and usage instructions

## Dependencies

The application requires the following Python packages:

- **FastAPI**: Modern web framework for building APIs
- **Uvicorn**: ASGI server for running FastAPI applications
- **Pydantic**: Data validation and settings management

## Troubleshooting

### Common Issues

1. **"python command not found"**

   ```bash
   # Use python3 instead
   python3 -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Port already in use**

   ```bash
   # Use a different port
   uvicorn main:app --reload --host 0.0.0.0 --port 8001
   ```

3. **Import errors**
   ```bash
   # Make sure you're in the app directory
   cd app
   # Install dependencies
   pip install -r requirements.txt
   ```

## Development

### Code Quality Features

- **Type Safety**: Full type hints and Pydantic validation
- **Error Handling**: Comprehensive error responses and validation
- **Documentation**: Detailed docstrings and inline comments
- **Modular Design**: Clean separation of concerns
- **API Documentation**: Auto-generated interactive docs

### Testing the API

1. Start the server using the instructions above
2. Open `http://localhost:8000/docs` in your browser
3. Use the interactive Swagger UI to test endpoints
4. Or use curl commands provided in the examples

## License

This project is provided as-is for educational and development purposes.

from fastapi import FastAPI, HTTPException
from model import TickerDataModel
from dbConnect import get_db_connection

app = FastAPI()

# Fetch all data
@app.get("/data")
def get_data():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ticker_data")
    records = cursor.fetchall()
    cursor.close()
    conn.close()

    # Convert to JSON format
    result = [
        {
            "id": row[0],
            "datetime": row[1],
            "open": row[2],
            "high": row[3],
            "low": row[4],
            "close": row[5],
            "volume": row[6]
        }
        for row in records
    ]
    return result

# Add new data
@app.post("/data")
def add_data(data: TickerDataModel):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO ticker_data (datetime, open, high, low, close, volume)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            data.datetime,
            data.open,
            data.high,
            data.low,
            data.close,
            data.volume
        ))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        conn.close()
    
    return {"message": "Record added successfully"}

# Moving Average Strategy Endpoint
@app.get("/strategy/performance")
def strategy_performance():
    from strategy import calculate_performance
    performance = calculate_performance()
    return performance

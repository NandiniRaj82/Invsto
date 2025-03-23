import pandas as pd
from dbConnect import get_db_connection

# Path to Excel file
excel_file = "data.xlsx"  # Replace with the actual file path

try:
    # Load Excel data with openpyxl for better compatibility
    df = pd.read_excel(excel_file, engine='openpyxl')

    # Normalize column names
    df.columns = df.columns.str.strip().str.lower()

    # Check for required columns
    required_columns = {'datetime', 'open', 'high', 'low', 'close', 'volume'}
    if not required_columns.issubset(set(df.columns)):
        print(f"❌ Missing required columns! Found: {df.columns}")
        exit()

    # Convert datetime to proper format
    df['datetime'] = pd.to_datetime(df['datetime'], errors='coerce')

    # Ensure numeric columns are properly formatted
    numeric_cols = ['open', 'high', 'low', 'close', 'volume']
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    # Check for any NaN or invalid rows
    if df.isnull().sum().sum() > 0:
        print("⚠️ Warning: Some rows contain invalid data. Cleaning the data...")
        df.dropna(inplace=True)

    # Connect to the database
    conn = get_db_connection()
    cursor = conn.cursor()

    # Insert Excel data into MySQL
    inserted_rows = 0

    for _, row in df.iterrows():
        try:
            cursor.execute("""
                INSERT INTO ticker_data (datetime, open, high, low, close, volume)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                row['datetime'],
                row['open'],
                row['high'],
                row['low'],
                row['close'],
                int(row['volume'])  # Ensure volume is an integer
            ))
            inserted_rows += 1

        except Exception as e:
            print(f"❌ Error inserting row: {row}\nError: {e}")

    # Commit changes
    conn.commit()

    print(f"✅ {inserted_rows} rows inserted successfully!")

except Exception as e:
    print(f"❌ Error: {e}")

finally:
    if 'cursor' in locals() and cursor:
        cursor.close()
    if 'conn' in locals() and conn:
        conn.close()

    print("🛑 Database connection closed.")

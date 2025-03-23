import pandas as pd
from dbConnect import get_db_connection


def calculate_performance(short_window=10, long_window=50):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Fetch price data
    cursor.execute("SELECT datetime, close FROM ticker_data ORDER BY datetime ASC")
    data = cursor.fetchall()

    cursor.close()
    conn.close()

    # Convert to DataFrame
    df = pd.DataFrame(data, columns=['datetime', 'close'])
    df['close'] = pd.to_numeric(df['close'])

    # Calculate moving averages
    df['short_ma'] = df['close'].rolling(window=short_window).mean()
    df['long_ma'] = df['close'].rolling(window=long_window).mean()

    # Generate buy/sell signals
    df['signal'] = 0
    df['signal'][short_window:] = (df['short_ma'][short_window:] > df['long_ma'][short_window:]).astype(int)
    df['positions'] = df['signal'].diff()

    buy_signals = df[df['positions'] == 1].to_dict(orient='records')
    sell_signals = df[df['positions'] == -1].to_dict(orient='records')

    return {
        "buy_signals": buy_signals,
        "sell_signals": sell_signals
    }

# signals/indicators.py
import talib
import numpy as np

def calculate_signal():
    # Example placeholder data (closing prices)
    close_prices = np.random.random(50) * 100  

    # EMA
    ema = talib.EMA(close_prices, timeperiod=10)
    # RSI
    rsi = talib.RSI(close_prices, timeperiod=14)
    # MACD
    macd, macdsignal, macdhist = talib.MACD(close_prices, fastperiod=12, slowperiod=26, signalperiod=9)

    # Simple signal logic
    if rsi[-1] < 30 and close_prices[-1] > ema[-1]:
        return "BUY"
    elif rsi[-1] > 70 and close_prices[-1] < ema[-1]:
        return "SELL"
    else:
        return "HOLD"

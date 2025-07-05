# market_indicators.py

from typing import List, Dict, Optional
import numpy as np
import pandas as pd

def compute_indicators(candles: List[Dict[str, float]]) -> Dict[str, Optional[float]]:
    """
    Compute advanced technical indicators from OHLCV candle data.

    Parameters:
        candles (List[Dict[str, float]]): List of candle dicts with keys:
            'open', 'high', 'low', 'close', 'volume'

    Returns:
        Dict[str, Optional[float]]: Dictionary of indicators.
    """
    # Check for empty input
    if not candles or not isinstance(candles, list):
        return {
            'rsi': None,
            'sma': None,
            'ema': None,
            'macd': None,
            'macd_signal': None,
            'bb_upper': None,
            'bb_lower': None,
            'bb_width': None,
            'atr': None,
            'vwap': None,
            'momentum': None,
            'close': None
        }

    df = pd.DataFrame(candles)
    # Ensure all required columns are present
    required_cols = {'open', 'high', 'low', 'close', 'volume'}
    if not required_cols.issubset(df.columns):
        raise ValueError(f"Input candles missing required columns: {required_cols - set(df.columns)}")

    # Use only the last 100 candles for efficiency (enough for all indicators)
    df = df.tail(100).reset_index(drop=True)

    # Parameters
    rsi_period = 14
    sma_period = 14
    ema_period = 14
    macd_fast = 12
    macd_slow = 26
    macd_signal = 9
    bb_period = 20
    bb_std = 2
    atr_period = 14
    momentum_period = 10

    indicators = {}

    # --- RSI ---
    if len(df) >= rsi_period:
        delta = df['close'].diff()
        gain = np.where(delta > 0, delta, 0)
        loss = np.where(delta < 0, -delta, 0)
        avg_gain = pd.Series(gain).rolling(window=rsi_period, min_periods=rsi_period).mean()
        avg_loss = pd.Series(loss).rolling(window=rsi_period, min_periods=rsi_period).mean()
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        indicators['rsi'] = float(rsi.iloc[-1]) if not np.isnan(rsi.iloc[-1]) else None
    else:
        indicators['rsi'] = None

    # --- SMA ---
    if len(df) >= sma_period:
        sma = df['close'].rolling(window=sma_period).mean()
        indicators['sma'] = float(sma.iloc[-1])
    else:
        indicators['sma'] = None

    # --- EMA ---
    if len(df) >= ema_period:
        ema = df['close'].ewm(span=ema_period, adjust=False).mean()
        indicators['ema'] = float(ema.iloc[-1])
    else:
        indicators['ema'] = None

    # --- MACD & MACD Signal ---
    if len(df) >= macd_slow:
        ema_fast = df['close'].ewm(span=macd_fast, adjust=False).mean()
        ema_slow = df['close'].ewm(span=macd_slow, adjust=False).mean()
        macd_line = ema_fast - ema_slow
        macd_signal_line = macd_line.ewm(span=macd_signal, adjust=False).mean()
        indicators['macd'] = float(macd_line.iloc[-1])
        indicators['macd_signal'] = float(macd_signal_line.iloc[-1])
    else:
        indicators['macd'] = None
        indicators['macd_signal'] = None

    # --- Bollinger Bands ---
    if len(df) >= bb_period:
        bb_mid = df['close'].rolling(window=bb_period).mean()
        bb_stddev = df['close'].rolling(window=bb_period).std()
        bb_upper = bb_mid + bb_std * bb_stddev
        bb_lower = bb_mid - bb_std * bb_stddev
        bb_width = bb_upper - bb_lower
        indicators['bb_upper'] = float(bb_upper.iloc[-1])
        indicators['bb_lower'] = float(bb_lower.iloc[-1])
        indicators['bb_width'] = float(bb_width.iloc[-1])
    else:
        indicators['bb_upper'] = None
        indicators['bb_lower'] = None
        indicators['bb_width'] = None

    # --- ATR ---
    if len(df) >= atr_period:
        high_low = df['high'] - df['low']
        high_close_prev = np.abs(df['high'] - df['close'].shift(1))
        low_close_prev = np.abs(df['low'] - df['close'].shift(1))
        tr = pd.concat([high_low, high_close_prev, low_close_prev], axis=1).max(axis=1)
        atr = tr.rolling(window=atr_period).mean()
        indicators['atr'] = float(atr.iloc[-1])
    else:
        indicators['atr'] = None

    # --- VWAP ---
    # VWAP is typically calculated over the session; here, we use all available candles
    if len(df) > 0:
        typical_price = (df['high'] + df['low'] + df['close']) / 3
        vwap = (typical_price * df['volume']).cumsum() / df['volume'].cumsum()
        indicators['vwap'] = float(vwap.iloc[-1])
    else:
        indicators['vwap'] = None

    # --- Momentum ---
    if len(df) >= momentum_period + 1:
        momentum = df['close'] - df['close'].shift(momentum_period)
        indicators['momentum'] = float(momentum.iloc[-1])
    else:
        indicators['momentum'] = None

    # --- Close Price ---
    indicators['close'] = float(df['close'].iloc[-1]) if len(df) > 0 else None

    return indicators
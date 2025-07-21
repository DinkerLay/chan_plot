import pandas as pd
from typing import Tuple

# 缠论K线包含关系处理

def remove_kline_inclusion(df: pd.DataFrame) -> pd.DataFrame:
    """
    处理K线包含关系，返回无包含关系的K线DataFrame。
    按照缠论手册的合并规则，逐步处理包含关系。
    """
    klines = df.copy().reset_index(drop=True)
    result = []
    i = 0
    while i < len(klines):
        if i == 0 or i == len(klines) - 1:
            result.append(klines.iloc[i])
            i += 1
            continue
        prev = klines.iloc[i-1]
        curr = klines.iloc[i]
        next_ = klines.iloc[i+1]
        # 判断包含关系
        if (curr['high'] <= prev['high'] and curr['low'] >= prev['low']) or (curr['high'] >= prev['high'] and curr['low'] <= prev['low']):
            # 包含，合并
            direction = 'up' if prev['high'] < curr['high'] else 'down'
            if direction == 'up':
                new_high = max(prev['high'], curr['high'])
                new_low = max(prev['low'], curr['low'])
            else:
                new_high = min(prev['high'], curr['high'])
                new_low = min(prev['low'], curr['low'])
            klines.at[i, 'high'] = new_high
            klines.at[i, 'low'] = new_low
            klines = klines.drop(i-1).reset_index(drop=True)
            i = max(i-1, 0)
        else:
            result.append(curr)
            i += 1
    return pd.DataFrame(result).reset_index(drop=True)
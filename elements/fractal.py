import pandas as pd
from dataclasses import dataclass
from typing import List

@dataclass(frozen=True)
class Fractal:
    """Fenxing: 顶/底分型"""
    index: int
    type: str  # 'ding' or 'di'
    high: float
    low: float

def identify_fractals(df: pd.DataFrame) -> List[Fractal]:
    """
    识别顶分型和底分型。
    - 顶分型: 中间K线的最高点为三者最高，最低点也为三者最高。
    - 底分型: 中间K线的最低点为三者最低，最高点也为三者最低。
    返回分型列表。
    """
    fractals = []
    for i in range(1, len(df)-1):
        prev = df.iloc[i-1]
        curr = df.iloc[i]
        next_ = df.iloc[i+1]
        # 顶分型
        if curr['high'] > prev['high'] and curr['high'] > next_['high'] and \
           curr['low'] > prev['low'] and curr['low'] > next_['low']:
            fractals.append(Fractal(index=i, type='ding', high=curr['high'], low=curr['low']))
        # 底分型
        if curr['low'] < prev['low'] and curr['low'] < next_['low'] and \
           curr['high'] < prev['high'] and curr['high'] < next_['high']:
            fractals.append(Fractal(index=i, type='di', high=curr['high'], low=curr['low']))
    return fractals
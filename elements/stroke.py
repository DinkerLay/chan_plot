from dataclasses import dataclass
from typing import List
import pandas as pd
from elements.fractal import Fractal

@dataclass(frozen=True)
class Stroke:
    """Bi: 笔"""
    start_index: int
    end_index: int
    direction: str  # 'up' or 'down'
    high: float
    low: float

def identify_strokes(fractals: List[Fractal], df: pd.DataFrame) -> List[Stroke]:
    """
    识别笔（Bi/Stroke）。
    只连接相邻且满足分离条件的分型。
    - 条件1：分型在有效序列中必须相邻。
    - 条件2：两个分型的K线组合之间必须至少有1根不属于它们的K线。
    - 禁止：如果两个分型K线重叠或紧邻，则不能形成一笔。
    """
    strokes = []
    for i in range(1, len(fractals)):
        f1 = fractals[i-1]
        f2 = fractals[i]
        # 必须一顶一底且相邻
        if f1.type == f2.type:
            continue
        # 分型之间必须有至少1根K线不属于分型本身
        if abs(f2.index - f1.index) <= 2:
            continue
        direction = 'up' if f1.type == 'di' and f2.type == 'ding' else 'down'
        start_idx = min(f1.index, f2.index)
        end_idx = max(f1.index, f2.index)
        high = df.iloc[start_idx:end_idx+1]['high'].max()
        low = df.iloc[start_idx:end_idx+1]['low'].min()
        strokes.append(Stroke(start_index=f1.index, end_index=f2.index, direction=direction, high=high, low=low))
    return strokes
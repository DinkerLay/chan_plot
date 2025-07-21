from dataclasses import dataclass
from typing import List
from structures.center import Center

@dataclass(frozen=True)
class Trend:
    """Zoushi: 走势"""
    type: str  # 'panzheng' or 'qushi'
    centers: List[Center]

def classify_trend(centers: List[Center]) -> Trend:
    """
    分类走势（Zoushi/Trend）。
    - 盘整：仅包含一个中枢。
    - 趋势：包含至少两个同向且核心区间[ZD, ZG]互不重叠的中枢。
    """
    if len(centers) == 1:
        return Trend(type='panzheng', centers=centers)
    # 检查是否有两个及以上互不重叠的中枢
    for i in range(len(centers)-1):
        c1 = centers[i]
        c2 = centers[i+1]
        # 核心区间互不重叠
        if c1.zg < c2.zd or c2.zg < c1.zd:
            return Trend(type='qushi', centers=centers)
    return Trend(type='panzheng', centers=centers)
from dataclasses import dataclass
from typing import List
from elements.segment import Segment

@dataclass(frozen=True)
class Center:
    """Zhongshu: 中枢"""
    segments: List[Segment]
    zg: float  # ZG = MIN(g1, g2, g3)
    zd: float  # ZD = MAX(d1, d2, d3)
    state: str  # 新生/延伸/扩展

def identify_centers(segments: List[Segment]) -> List[Center]:
    """
    识别中枢（Zhongshu/Center）。
    - 由三段连续的线段构成。
    - 区间计算：ZG = MIN(g1, g2, g3)，ZD = MAX(d1, d2, d3)。
    - 生命周期：新生、延伸（最多9段）、扩展。
    """
    centers = []
    i = 0
    while i + 2 < len(segments):
        segs = segments[i:i+3]
        g1 = segs[0].overlap_high
        g2 = segs[1].overlap_high
        g3 = segs[2].overlap_high
        d1 = segs[0].overlap_low
        d2 = segs[1].overlap_low
        d3 = segs[2].overlap_low
        zg = min(g1, g2, g3)
        zd = max(d1, d2, d3)
        if zg >= zd:
            # 有中枢区间
            state = '新生'
            # 延伸逻辑
            j = i + 3
            while j < min(i+9, len(segments)):
                next_seg = segments[j]
                zg_new = min(zg, next_seg.overlap_high)
                zd_new = max(zd, next_seg.overlap_low)
                if zg_new >= zd_new:
                    zg = zg_new
                    zd = zd_new
                    j += 1
                    state = '延伸'
                else:
                    break
            centers.append(Center(segments=segments[i:j], zg=zg, zd=zd, state=state))
            i = j
        else:
            i += 1
    return centers
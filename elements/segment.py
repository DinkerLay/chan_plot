from dataclasses import dataclass
from typing import List
import pandas as pd
from elements.stroke import Stroke

@dataclass(frozen=True)
class Segment:
    """Xianduan: 线段"""
    strokes: List[Stroke]
    overlap_high: float
    overlap_low: float
    start_index: int
    end_index: int

def identify_segments(strokes: List[Stroke], df: pd.DataFrame) -> List[Segment]:
    """
    识别线段（Xianduan/Segment）。
    - 至少三段连续的笔。
    - 第1笔与第3笔的价格区间必须有重叠。
    - 特征序列破坏作为线段结束的唯一标准。
    """
    segments = []
    i = 0
    while i + 2 < len(strokes):
        s1, s2, s3 = strokes[i], strokes[i+1], strokes[i+2]
        # 计算第1笔与第3笔的重叠区间
        high1 = max(s1.high, s3.high)
        low1 = min(s1.low, s3.low)
        overlap_high = min(s1.high, s3.high)
        overlap_low = max(s1.low, s3.low)
        if overlap_high >= overlap_low:
            # 有重叠，形成线段
            seg_strokes = [s1, s2, s3]
            j = i + 3
            # 尝试延长线段，直到特征序列破坏
            while j < len(strokes):
                next_stroke = strokes[j]
                # 对于向上线段，后续向下一笔的低点低于前一高点则破坏
                if s1.direction == 'up':
                    if next_stroke.low <= s3.high:
                        break
                # 对于向下线段，后续向上一笔的高点高于前一低点则破坏
                else:
                    if next_stroke.high >= s3.low:
                        break
                seg_strokes.append(next_stroke)
                j += 1
            segment = Segment(
                strokes=seg_strokes,
                overlap_high=overlap_high,
                overlap_low=overlap_low,
                start_index=seg_strokes[0].start_index,
                end_index=seg_strokes[-1].end_index
            )
            segments.append(segment)
            i = j
        else:
            i += 1
    return segments
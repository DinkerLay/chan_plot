import pandas as pd
from typing import Dict, Any, List
from elements.fractal import Fractal
from elements.stroke import Stroke
from elements.segment import Segment
from structures.center import Center

def json_to_kline_df(data: Dict[str, Any]) -> pd.DataFrame:
    """
    将输入json格式的K线数据转换为DataFrame。
    """
    records = []
    for date, v in data.items():
        records.append({
            'datetime': date,
            'open': v['open'],
            'high': v['high'],
            'low': v['low'],
            'close': v['close'],
            'volume': v['vol'],
        })
    df = pd.DataFrame(records)
    df['datetime'] = pd.to_datetime(df['datetime'], format='%Y%m%d')
    df = df.sort_values('datetime').reset_index(drop=True)
    return df

def fractals_to_json(fractals: List[Fractal]) -> List[Dict[str, Any]]:
    """
    将分型列表转换为指定json格式。
    """
    return [
        {
            'start_index': f.index,  # 分型在K线中的索引
            'end_index': f.index,    # 分型只占一个K线
            'direction': 'up' if f.type == 'ding' else 'down',
            'type': f.type,
            'trigger_index': str(f.index),
        }
        for f in fractals
    ]

def strokes_to_json(strokes: List[Stroke]) -> List[Dict[str, Any]]:
    return [
        {
            'start_index': s.start_index,
            'end_index': s.end_index,
            'direction': s.direction,
            'high': s.high,
            'low': s.low,
        }
        for s in strokes
    ]

def segments_to_json(segments: List[Segment]) -> List[Dict[str, Any]]:
    return [
        {
            'start_index': seg.start_index,
            'end_index': seg.end_index,
            'overlap_high': seg.overlap_high,
            'overlap_low': seg.overlap_low,
        }
        for seg in segments
    ]

def centers_to_json(centers: List[Center]) -> List[Dict[str, Any]]:
    return [
        {
            'zg': c.zg,
            'zd': c.zd,
            'state': c.state,
            'start_index': c.segments[0].start_index if c.segments else None,
            'end_index': c.segments[-1].end_index if c.segments else None,
        }
        for c in centers
    ]

def analyze_chnl_structure(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    主流程：输入原始json数据，输出缠论结构化json。
    """
    from elements.kline import remove_kline_inclusion
    from elements.fractal import identify_fractals
    from elements.stroke import identify_strokes
    from elements.segment import identify_segments
    from structures.center import identify_centers
    from structures.trend import classify_trend

    df = json_to_kline_df(data)
    df_no_incl = remove_kline_inclusion(df)
    fractals = identify_fractals(df_no_incl)
    strokes = identify_strokes(fractals, df_no_incl)
    segments = identify_segments(strokes, df_no_incl)
    centers = identify_centers(segments)
    trend = classify_trend(centers)

    return {
        'fractal': fractals_to_json(fractals),
        'stroke': strokes_to_json(strokes),
        'segment': segments_to_json(segments),
        'center': centers_to_json(centers),
        'trend': trend.type,
    }
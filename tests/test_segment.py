import pandas as pd
from elements.stroke import Stroke
from elements.segment import identify_segments, Segment

def test_identify_segments_typical():
    strokes = [
        Stroke(0, 2, 'up', 7, 1),
        Stroke(2, 4, 'down', 6, 2),
        Stroke(4, 6, 'up', 8, 3),
    ]
    df = pd.DataFrame()
    segments = identify_segments(strokes, df)
    assert len(segments) == 1
    assert segments[0].start_index == 0
    assert segments[0].end_index == 6

def test_identify_segments_no_overlap():
    strokes = [
        Stroke(0, 2, 'up', 7, 1),
        Stroke(2, 4, 'down', 6, 2),
        Stroke(4, 6, 'up', 3, 2),  # 无重叠
    ]
    df = pd.DataFrame()
    segments = identify_segments(strokes, df)
    assert len(segments) == 0

def test_identify_segments_feature_broken():
    strokes = [
        Stroke(0, 2, 'up', 7, 1),
        Stroke(2, 4, 'down', 6, 2),
        Stroke(4, 6, 'up', 8, 3),
        Stroke(6, 8, 'down', 2, 1),  # 破坏
    ]
    df = pd.DataFrame()
    segments = identify_segments(strokes, df)
    assert len(segments) == 1
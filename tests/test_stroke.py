import pandas as pd
from elements.fractal import Fractal
from elements.stroke import identify_strokes, Stroke

def test_identify_strokes_typical():
    data = [
        {'datetime': '2023-01-01', 'open': 1, 'high': 5, 'low': 1, 'close': 4},
        {'datetime': '2023-01-02', 'open': 2, 'high': 7, 'low': 2, 'close': 6},
        {'datetime': '2023-01-03', 'open': 3, 'high': 4, 'low': 3, 'close': 3},
        {'datetime': '2023-01-04', 'open': 2, 'high': 8, 'low': 2, 'close': 7},
        {'datetime': '2023-01-05', 'open': 3, 'high': 3, 'low': 1, 'close': 2},
    ]
    df = pd.DataFrame(data)
    fractals = [
        Fractal(index=1, type='ding', high=7, low=2),
        Fractal(index=4, type='di', high=3, low=1),
    ]
    strokes = identify_strokes(fractals, df)
    assert len(strokes) == 1
    assert strokes[0].direction == 'down'
    assert strokes[0].start_index == 1
    assert strokes[0].end_index == 4

def test_identify_strokes_no_separation():
    data = [
        {'datetime': '2023-01-01', 'open': 1, 'high': 5, 'low': 1, 'close': 4},
        {'datetime': '2023-01-02', 'open': 2, 'high': 7, 'low': 2, 'close': 6},
        {'datetime': '2023-01-03', 'open': 3, 'high': 4, 'low': 3, 'close': 3},
    ]
    df = pd.DataFrame(data)
    fractals = [
        Fractal(index=0, type='di', high=5, low=1),
        Fractal(index=2, type='ding', high=4, low=3),
    ]
    strokes = identify_strokes(fractals, df)
    assert len(strokes) == 0

def test_identify_strokes_same_type():
    data = [
        {'datetime': '2023-01-01', 'open': 1, 'high': 5, 'low': 1, 'close': 4},
        {'datetime': '2023-01-02', 'open': 2, 'high': 7, 'low': 2, 'close': 6},
        {'datetime': '2023-01-03', 'open': 3, 'high': 4, 'low': 3, 'close': 3},
        {'datetime': '2023-01-04', 'open': 2, 'high': 8, 'low': 2, 'close': 7},
    ]
    df = pd.DataFrame(data)
    fractals = [
        Fractal(index=1, type='ding', high=7, low=2),
        Fractal(index=3, type='ding', high=8, low=2),
    ]
    strokes = identify_strokes(fractals, df)
    assert len(strokes) == 0
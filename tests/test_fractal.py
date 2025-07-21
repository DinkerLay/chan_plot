import pandas as pd
from elements.fractal import identify_fractals, Fractal

def test_identify_fractals_typical():
    data = [
        {'datetime': '2023-01-01', 'open': 1, 'high': 5, 'low': 1, 'close': 4},
        {'datetime': '2023-01-02', 'open': 2, 'high': 7, 'low': 2, 'close': 6},  # 顶分型
        {'datetime': '2023-01-03', 'open': 3, 'high': 4, 'low': 3, 'close': 3},
    ]
    df = pd.DataFrame(data)
    fractals = identify_fractals(df)
    assert len(fractals) == 1
    assert fractals[0].type == 'ding'
    assert fractals[0].index == 1

def test_identify_fractals_di():
    data = [
        {'datetime': '2023-01-01', 'open': 1, 'high': 5, 'low': 5, 'close': 4},
        {'datetime': '2023-01-02', 'open': 2, 'high': 3, 'low': 1, 'close': 2},  # 底分型
        {'datetime': '2023-01-03', 'open': 3, 'high': 4, 'low': 3, 'close': 3},
    ]
    df = pd.DataFrame(data)
    fractals = identify_fractals(df)
    assert len(fractals) == 1
    assert fractals[0].type == 'di'
    assert fractals[0].index == 1

def test_identify_fractals_none():
    data = [
        {'datetime': '2023-01-01', 'open': 1, 'high': 2, 'low': 1, 'close': 2},
        {'datetime': '2023-01-02', 'open': 2, 'high': 3, 'low': 2, 'close': 3},
        {'datetime': '2023-01-03', 'open': 3, 'high': 4, 'low': 3, 'close': 4},
    ]
    df = pd.DataFrame(data)
    fractals = identify_fractals(df)
    assert len(fractals) == 0
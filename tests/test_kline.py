import pandas as pd
from elements.kline import remove_kline_inclusion

def test_remove_kline_inclusion_typical():
    data = [
        {'datetime': '2023-01-01', 'open': 1, 'high': 5, 'low': 1, 'close': 4},
        {'datetime': '2023-01-02', 'open': 4, 'high': 6, 'low': 2, 'close': 5},
        {'datetime': '2023-01-03', 'open': 5, 'high': 7, 'low': 3, 'close': 6},
    ]
    df = pd.DataFrame(data)
    out = remove_kline_inclusion(df)
    assert len(out) == 3

def test_remove_kline_inclusion_with_inclusion():
    data = [
        {'datetime': '2023-01-01', 'open': 1, 'high': 5, 'low': 1, 'close': 4},
        {'datetime': '2023-01-02', 'open': 2, 'high': 4, 'low': 2, 'close': 3},  # 被包含
        {'datetime': '2023-01-03', 'open': 5, 'high': 7, 'low': 3, 'close': 6},
    ]
    df = pd.DataFrame(data)
    out = remove_kline_inclusion(df)
    assert len(out) == 2
    assert out.iloc[0]['high'] == 5
    assert out.iloc[1]['high'] == 7

def test_remove_kline_inclusion_all_inclusion():
    data = [
        {'datetime': '2023-01-01', 'open': 1, 'high': 10, 'low': 1, 'close': 9},
        {'datetime': '2023-01-02', 'open': 2, 'high': 9, 'low': 2, 'close': 8},
        {'datetime': '2023-01-03', 'open': 3, 'high': 8, 'low': 3, 'close': 7},
    ]
    df = pd.DataFrame(data)
    out = remove_kline_inclusion(df)
    assert len(out) == 1
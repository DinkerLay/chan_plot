import pandas as pd

def load_kline_from_csv(filepath: str) -> pd.DataFrame:
    """
    从CSV文件加载K线数据，返回DataFrame。
    要求包含列：datetime, open, high, low, close, volume。
    """
    df = pd.read_csv(filepath, parse_dates=['datetime'])
    df = df.reset_index(drop=False)
    return df
from structures.center import Center
from structures.trend import classify_trend, Trend

def test_classify_trend_panzheng():
    centers = [Center([], 6, 5, '新生')]
    trend = classify_trend(centers)
    assert trend.type == 'panzheng'

def test_classify_trend_qushi():
    centers = [
        Center([], 6, 5, '新生'),
        Center([], 4, 3, '新生'),
    ]
    trend = classify_trend(centers)
    assert trend.type == 'qushi'

def test_classify_trend_overlap():
    centers = [
        Center([], 6, 5, '新生'),
        Center([], 5.5, 5, '新生'),
    ]
    trend = classify_trend(centers)
    assert trend.type == 'panzheng'
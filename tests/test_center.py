from elements.segment import Segment
from structures.center import identify_centers, Center

def test_identify_centers_typical():
    segments = [
        Segment([], 8, 3, 0, 2),
        Segment([], 7, 4, 2, 4),
        Segment([], 6, 5, 4, 6),
    ]
    centers = identify_centers(segments)
    assert len(centers) == 1
    assert centers[0].zg == 6
    assert centers[0].zd == 5
    assert centers[0].state == '新生'

def test_identify_centers_no_center():
    segments = [
        Segment([], 8, 3, 0, 2),
        Segment([], 7, 4, 2, 4),
        Segment([], 5, 6, 4, 6),  # 无重叠
    ]
    centers = identify_centers(segments)
    assert len(centers) == 0

def test_identify_centers_extend():
    segments = [
        Segment([], 8, 3, 0, 2),
        Segment([], 7, 4, 2, 4),
        Segment([], 6, 5, 4, 6),
        Segment([], 6, 5, 6, 8),
        Segment([], 6, 5, 8, 10),
    ]
    centers = identify_centers(segments)
    assert len(centers) == 1
    assert centers[0].state == '延伸'
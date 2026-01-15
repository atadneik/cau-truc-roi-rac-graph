"""
THUẬT TOÁN PRIM - CÂY KHUNG NHỎ NHẤT (Prim's Minimum Spanning Tree)

 MỤC ĐÍCH:
    Tìm cây khung nhỏ nhất (MST) trong đồ thị vô hướng, liên thông có trọng số.

 ĐỊNH NGHĨA:
    - Cây khung: Đồ thị con liên thông, không có chu trình, chứa tất cả đỉnh
    - MST: Cây khung có tổng trọng số nhỏ nhất

 INPUT FORMAT:
    graph = {
        'nodes': [{'id': 'A'}, {'id': 'B'}, {'id': 'C'}],
        'edges': [
            {'from': 'A', 'to': 'B', 'weight': 5},
            {'from': 'B', 'to': 'C', 'weight': 3},
            {'from': 'A', 'to': 'C', 'weight': 10}
        ]
    }

 OUTPUT FORMAT:
    {
        'mst_edges': [              # Các cạnh trong MST
            {'from': 'A', 'to': 'B', 'weight': 5},
            {'from': 'B', 'to': 'C', 'weight': 3}
        ],
        'total_weight': 8,          # Tổng trọng số MST
        'complete': True,
        'steps': [...]
    }

 LƯU Ý:
    - Chỉ áp dụng cho đồ thị VÔ HƯỚNG, LIÊN THÔNG
    - Đồ thị có hướng → không có MST
    - Đồ thị không liên thông → có rừng khung nhỏ nhất (nhiều cây)
    - Sử dụng Priority Queue (heap) để tối ưu"""

import heapq
from collections import defaultdict


def find_mst_prim(graph):
    """
    Tìm cây khung nhỏ nhất bằng thuật toán Prim.
    
    Args:
        graph: Dict chứa đồ thị
    
    Returns:
        Dict {mst_edges: list, total_weight: float, complete: bool, steps: list}
    """
    # TODO: Implement Prim's algorithm
    pass

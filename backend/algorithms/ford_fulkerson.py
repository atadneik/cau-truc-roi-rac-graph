"""
THUẬT TOÁN FORD-FULKERSON - LUỒNG CỰC ĐẠI (Maximum Flow)

 MỤC ĐÍCH:
    Tìm luồng cực đại từ nguồn (source) đến đích (sink) trong mạng có dung lượng.

 ĐỊNH NGHĨA:
    - Luồng: Lượng "chất lỏng" chảy qua mỗi cạnh
    - Dung lượng (Capacity): Giới hạn luồng tối đa qua cạnh
    - Luồng cực đại: Luồng lớn nhất có thể từ source → sink

 INPUT FORMAT:
    graph = {
        'nodes': [{'id': 'S'}, {'id': 'A'}, {'id': 'T'}],
        'edges': [
            {'from': 'S', 'to': 'A', 'weight': 10},  # weight = capacity
            {'from': 'A', 'to': 'T', 'weight': 5}
        ]
    }

 OUTPUT FORMAT:
    {
        'max_flow': 5,              # Luồng cực đại
        'flow_edges': [...],        # Luồng trên mỗi cạnh
        'iterations': 2
    }

 LƯU Ý:
    - Implementation này dùng Edmonds-Karp (BFS) → O(VE²)
    - weight trong edges = capacity (dung lượng)"""

from collections import deque, defaultdict
import copy


def find_max_flow(graph, source, sink):
    """
    Tìm luồng cực đại bằng thuật toán Ford-Fulkerson.
    
    Args:
        graph: Dict chứa đồ thị
        source: Đỉnh nguồn
        sink: Đỉnh đích
    
    Returns:
        Dict {max_flow: float, flow_edges: list, iterations: int, steps: list}
    """
    # TODO: Implement Ford-Fulkerson algorithm
    pass

"""
THUẬT TOÁN TÌM ĐƯỜNG ĐI NGẮN NHẤT (Shortest Path Algorithms)

 MỤC ĐÍCH:
    Tìm đường đi ngắn nhất giữa 2 đỉnh trong đồ thị có trọng số.

 THUẬT TOÁN:
    - Dijkstra:      Đồ thị có trọng số KHÔNG ÂM (nhanh - O(E log V))
    - Bellman-Ford:  Đồ thị có trọng số ÂM (chậm hơn - O(VE), nhưng detect chu trình âm)

 INPUT FORMAT:
    graph = {
        'nodes': [{'id': 'A'}, {'id': 'B'}, {'id': 'C'}],
        'edges': [
            {'from': 'A', 'to': 'B', 'weight': 5},
            {'from': 'B', 'to': 'C', 'weight': 3}
        ],
        'directed': False  # True nếu đồ thị có hướng
    }

 OUTPUT FORMAT:
    {
        'path': ['A', 'B', 'C'],    # Đường đi tìm được
        'distance': 8,               # Tổng khoảng cách
        'found': True,               # Có tìm thấy đường đi không
        'steps': [...]               # Các bước để visualization
    }

 LƯU Ý:
    - Dijkstra KHÔNG hoạt động với trọng số âm → dùng Bellman-Ford
    - Bellman-Ford có thể phát hiện chu trình âm
    - Dijkstra nhanh hơn nên ưu tiên dùng khi không có trọng số âm"""

import heapq
from collections import defaultdict


def find_shortest_path(graph, start, end, algorithm='dijkstra'):
    """
    Tìm đường đi ngắn nhất từ start đến end.
    
    Args:
        graph: Dict chứa đồ thị dạng {nodes: [], edges: [{from, to, weight}]}
        start: Đỉnh bắt đầu
        end: Đỉnh kết thúc
        algorithm: 'dijkstra' hoặc 'bellman-ford'
    
    Returns:
        Dict {path: list, distance: float, steps: list, found: bool}
    """
    # TODO: Implement thuật toán tìm đường đi ngắn nhất
    pass

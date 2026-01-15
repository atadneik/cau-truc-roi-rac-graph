"""
THUẬT TOÁN DUYỆT ĐỒ THỊ (Graph Traversal Algorithms)

 MỤC ĐÍCH:
    Duyệt tất cả các đỉnh trong đồ thị theo một thứ tự nhất định.

 THUẬT TOÁN:
    - BFS (Breadth-First Search):  Duyệt theo chiều rộng - dùng Queue
    - DFS (Depth-First Search):    Duyệt theo chiều sâu - dùng Stack
    BFS:
        - Tìm đường đi ngắn nhất (không có trọng số)
        - Tìm cấp độ/level của các đỉnh
        - Tìm tất cả đỉnh trong khoảng cách k
    
    DFS:
        - Tìm chu trình
        - Kiểm tra liên thông
        - Topological sort
        - Tìm thành phần liên thông

 INPUT FORMAT:
    graph = {
        'nodes': [{'id': 1}, {'id': 2}, {'id': 3}],
        'edges': [
            {'from': 1, 'to': 2},
            {'from': 2, 'to': 3}
        ],
        'directed': False
    }

 OUTPUT FORMAT:
    {
        'order': [1, 2, 3],         # Thứ tự duyệt các đỉnh
        'visited_count': 3,         # Số đỉnh đã thăm
        'steps': [...]              # Các bước để visualization
    }

 LƯU Ý:
    - BFS dùng Queue (FIFO) → duyệt từng level
    - DFS dùng Stack (LIFO) → đi sâu trước
    - Có 2 cách implement DFS: iterative (dùng stack) và recursive"""

from collections import deque, defaultdict


def bfs(graph, start):
    """
    Duyệt đồ thị theo chiều rộng (Breadth-First Search).
    
    Args:
        graph: Dict chứa đồ thị
        start: Đỉnh bắt đầu
    
    Returns:
        Dict {order: list, visited_count: int, steps: list}
    """
    # TODO: Implement BFS
    pass


def dfs(graph, start):
    """
    Duyệt đồ thị theo chiều sâu (Depth-First Search).
    
    Args:
        graph: Dict chứa đồ thị
        start: Đỉnh bắt đầu
    
    Returns:
        Dict {order: list, visited_count: int, steps: list}
    """
    # TODO: Implement DFS
    pass

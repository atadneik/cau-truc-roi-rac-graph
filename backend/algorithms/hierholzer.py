"""
THUẬT TOÁN HIERHOLZER - CHU TRÌNH EULER (Euler Circuit)

 MỤC ĐÍCH:
    Tìm chu trình đi qua TẤT CẢ cạnh ĐÚNG 1 LẦN và QUAY VỀ điểm xuất phát.

 INPUT/OUTPUT:
    result = {
        'circuit': ['A', 'B', 'C', 'D', 'A'],
        'exists': True,
        'length': 5
    }

 LƯU Ý:
    - NHANH HƠN Fleury: O(E) vs O(E²)
    - Chỉ dùng cho CHU TRÌNH (quay về điểm xuất phát)
    - Nếu có đỉnh bậc lẻ → dùng Fleury tìm ĐƯỜNG ĐI"""

from collections import defaultdict, deque


def find_euler_circuit(graph):
    """
    Tìm chu trình Euler bằng thuật toán Hierholzer.
    
    Args:
        graph: Dict chứa đồ thị
    
    Returns:
        Dict {circuit: list, exists: bool, length: int, steps: list}
    """
    # TODO: Implement Hierholzer's algorithm
    pass

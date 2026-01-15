"""
THUẬT TOÁN FLEURY - ĐƯỜNG ĐI EULER (Euler Path)

 MỤC ĐÍCH:
    Tìm đường đi qua TẤT CẢ cạnh ĐÚNG 1 LẦN (không yêu cầu quay về điểm xuất phát).

 INPUT/OUTPUT:
    result = {
        'path': ['A', 'B', 'C', 'D', 'A'],
        'exists': True,
        'length': 5
    }

 LƯU Ý:
    - Fleury chậm (O(E²)) vì phải check bridge
    - Hierholzer nhanh hơn (O(E)) cho CHU TRÌNH Euler
    - Cầu (bridge): Cạnh mà nếu xóa sẽ làm đồ thị không liên thông"""

from collections import defaultdict
import copy


def find_euler_path(graph, start=None):
    """
    Tìm đường đi Euler bằng thuật toán Fleury.
    
    Args:
        graph: Dict chứa đồ thị
        start: Đỉnh bắt đầu (optional)
    
    Returns:
        Dict {path: list, exists: bool, length: int, steps: list}
    """
    # TODO: Implement Fleury's algorithm
    pass

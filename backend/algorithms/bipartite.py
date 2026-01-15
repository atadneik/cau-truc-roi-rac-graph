"""
KIỂM TRA ĐỒ THỊ 2 PHÍA (Bipartite Graph Check)

MỤC ĐÍCH:
    Kiểm tra đồ thị có phải là đồ thị 2 phía (Bipartite) không và tô màu các đỉnh.

ĐỊNH NGHĨA:
    Đồ thị 2 phía: Có thể chia các đỉnh thành 2 tập hợp sao cho không có cạnh nào
    nối 2 đỉnh cùng tập.

INPUT FORMAT:
    graph = {
        'nodes': [{'id': 'A'}, {'id': 'B'}, {'id': 'C'}, {'id': 'D'}],
        'edges': [
            {'from': 'A', 'to': 'B'},
            {'from': 'B', 'to': 'C'},
            {'from': 'C', 'to': 'D'},
            {'from': 'D', 'to': 'A'}
        ]
    }

OUTPUT FORMAT:
    {
        'is_bipartite': True,       # Có phải đồ thị 2 phía không
        'coloring': {                # Tô màu các đỉnh (0 hoặc 1)
            'A': 0,
            'B': 1,
            'C': 0,
            'D': 1
        },
        'groups': {                  # Phân nhóm
            'group0': ['A', 'C'],
            'group1': ['B', 'D']
        }
    }

LƯU Ý:
    - Đồ thị có chu trình LẺ → KHÔNG phải đồ thị 2 phía
    - Đồ thị có chu trình CHẴN → có thể là đồ thị 2 phía
    - Sử dụng BFS với 2 màu để kiểm tra"""

from collections import deque, defaultdict


def check_bipartite(graph):
    """
    Kiểm tra đồ thị có phải là đồ thị 2 phía không.
    
    Args:
        graph: Dict chứa đồ thị
    
    Returns:
        Dict {is_bipartite: bool, coloring: dict, groups: dict}
    """
    # TODO: Implement bipartite check
    pass

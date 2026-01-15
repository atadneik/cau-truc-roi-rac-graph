"""
CHUYỂN ĐỔI BIỂU DIỄN ĐỒ THỊ (Graph Representation Conversion)

MỤC ĐÍCH:
    Chuyển đổi giữa các dạng biểu diễn đồ thị khác nhau.

INPUT FORMAT (Adjacency List):
    graph = {
        'adjacency_list': {
            'A': [{'to': 'B', 'weight': 5}, {'to': 'C', 'weight': 3}],
            'B': [{'to': 'A', 'weight': 5}],
            'C': [{'to': 'A', 'weight': 3}]
        },
        'directed': False
    }

OUTPUT FORMAT (Adjacency Matrix):
    {
        'matrix': [
            [0, 5, 3],  # A -> A, B, C
            [5, 0, 0],  # B -> A, B, C
            [3, 0, 0]   # C -> A, B, C
        ],
        'nodes': ['A', 'B', 'C'],
        'directed': False
    }

LƯU Ý:
    - Ma trận kề tốn bộ nhớ O(V²) → không tốt cho đồ thị lớn, thưa
    - Danh sách kề tốn bộ nhớ O(V + E) → tốt hơn cho đồ thị thưa
    - from_type values: 'matrix', 'list', 'edges'
    - to_type values: 'matrix', 'list', 'edges'"""



def convert_graph(graph, from_type, to_type):
    """
    Chuyển đổi giữa các dạng biểu diễn đồ thị.
    
    Args:
        graph: Đồ thị ở dạng hiện tại
        from_type: 'matrix', 'list', hoặc 'edges'
        to_type: 'matrix', 'list', hoặc 'edges'
    
    Returns:
        Đồ thị ở dạng mới
    """
    # TODO: Implement graph conversion
    pass

"""
THUẬT TOÁN KRUSKAL - CÂY KHUNG NHỎ NHẤT (Kruskal's Minimum Spanning Tree)

 MỤC ĐÍCH:
    Tìm cây khung nhỏ nhất (MST) bằng cách sắp xếp cạnh và dùng Union-Find.

 INPUT/OUTPUT: Tương tự Prim

 LƯU Ý:
    - Sử dụng Union-Find để detect chu trình hiệu quả O(α(V))
    - Path compression + Union by rank để tối ưu
    - Time complexity: O(E log E) do sorting"""



def find_mst_kruskal(graph):
    """
    Tìm cây khung nhỏ nhất bằng thuật toán Kruskal.
    
    Args:
        graph: Dict chứa đồ thị
    
    Returns:
        Dict {mst_edges: list, total_weight: float, complete: bool, steps: list}
    """
    # TODO: Implement Kruskal's algorithm
    pass

"""
THUẬT TOÁN KRUSKAL - CÂY KHUNG NHỎ NHẤT (Kruskal's Minimum Spanning Tree)

MỤC ĐÍCH:
    Tìm cây khung nhỏ nhất (MST) bằng cách sắp xếp cạnh và dùng Union-Find.

INPUT/OUTPUT: Tương tự Prim

LƯU Ý:
    - Sử dụng Union-Find để detect chu trình hiệu quả O(α(V))
    - Path compression + Union by rank để tối ưu
    - Time complexity: O(E log E) do sorting
"""


def find_mst_kruskal(graph):
    """
    Tìm cây khung nhỏ nhất bằng thuật toán Kruskal.
    
    Args:
        graph: Dict chứa đồ thị
    
    Returns:
        Dict {mst_edges: list, total_weight: float, complete: bool, steps: list}
    """
    mst_edges = []
    total_weight = 0
    steps = []

    edges = graph.get("edges", [])
    nodes = list(graph.get("nodes", []))

    # Nếu không có nodes thì suy ra từ edges
    if not nodes:
        node_set = set()
        for u, v, _ in edges:
            node_set.add(u)
            node_set.add(v)
        nodes = list(node_set)

    # ===== UNION-FIND =====
    parent = {v: v for v in nodes}
    rank = {v: 0 for v in nodes}

    def find(u):
        if parent[u] != u:
            parent[u] = find(parent[u])
        return parent[u]

    def union(u, v):
        ru = find(u)
        rv = find(v)

        if ru == rv:
            return False

        if rank[ru] < rank[rv]:
            parent[ru] = rv
        elif rank[ru] > rank[rv]:
            parent[rv] = ru
        else:
            parent[rv] = ru
            rank[ru] += 1

        return True

    # ===== SORT EDGES =====
    edges = sorted(edges, key=lambda e: e[2])

    # ===== KRUSKAL =====
    for u, v, w in edges:
        if union(u, v):
            mst_edges.append((u, v, w))
            total_weight += w

            steps.append({
                "edge": (u, v, w),
                "action": "add"
            })

            if len(mst_edges) == len(nodes) - 1:
                break

    complete = (len(mst_edges) == len(nodes) - 1)

    return {
        "mst_edges": mst_edges,
        "total_weight": total_weight,
        "complete": complete,
        "steps": steps
    }

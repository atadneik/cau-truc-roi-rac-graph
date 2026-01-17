"""
Thuật toán Kruskal cho bài toán Cây khung nhỏ nhất (MST).
"""


def find_mst_kruskal(graph):
    """Tìm cây khung nhỏ nhất sử dụng thuật toán Kruskal."""
    mst_edges = []
    total_weight = 0
    steps = []

    edges_data = graph.get("edges", [])
    nodes_data = graph.get("nodes", [])

    # Parse edges to (u, v, w) tuples
    edges = []
    for e in edges_data:
        u = e.get('from')
        v = e.get('to')
        w = e.get('weight', 1)
        edges.append((u, v, w))

    # Get list of node IDs
    nodes = [n.get('id') for n in nodes_data]

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
                "action": "add_edge"
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

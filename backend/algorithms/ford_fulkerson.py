from collections import deque


def build_residual_graph(graph):
    """
    Xây dựng residual graph ban đầu cho Ford-Fulkerson.

    Args:
        graph: Dict chứa đồ thị gốc

    Returns:
        residual: Dict dạng residual[u][v] = capacity còn lại
    """
    residual = {}

    # Khởi tạo node
    for node in graph.get("nodes", []):
        node_id = node["id"] if isinstance(node, dict) else node
        residual[node_id] = {}

    # Thêm cạnh residual (có cộng dồn để tránh lỗi multi-edge)
    for edge in graph.get("edges", []):
        u = edge["from"]
        v = edge["to"]
        cap = edge["weight"]

        # cạnh xuôi
        residual[u][v] = residual[u].get(v, 0) + cap

        # cạnh ngược
        if u not in residual[v]:
            residual[v][u] = 0

    return residual


def bfs_find_augmenting_path(residual, source, sink):
    """
    BFS tìm đường tăng (augmenting path) trên residual graph.

    Returns:
        parent dict nếu tìm được đường, None nếu không tồn tại
    """
    visited = set()
    parent = {}

    queue = deque([source])
    visited.add(source)
    parent[source] = None

    while queue:
        u = queue.popleft()

        for v, cap in residual.get(u, {}).items():
            if v not in visited and cap > 0:
                visited.add(v)
                parent[v] = u

                if v == sink:
                    return parent

                queue.append(v)

    return None


def find_bottleneck_capacity(parent, residual, source, sink):
    """
    Tính bottleneck (min capacity) trên augmenting path.
    """
    path_flow = float("inf")
    v = sink

    while v != source:
        u = parent[v]
        path_flow = min(path_flow, residual[u][v])
        v = u

    return path_flow


def update_residual_graph(residual, parent, source, sink, path_flow):
    """
    Cập nhật residual graph sau khi tìm được augmenting path.
    """
    v = sink
    while v != source:
        u = parent[v]

        residual[u][v] -= path_flow
        residual[v][u] += path_flow

        v = u


def find_max_flow(graph, source, sink):
    """
    Tìm luồng cực đại bằng thuật toán Ford-Fulkerson (Edmonds-Karp).

    Returns:
        Dict {max_flow, flow_edges, iterations, steps}
    """
    residual = build_residual_graph(graph)

    max_flow = 0
    iterations = 0
    steps = []

    # Lưu luồng trên các cạnh gốc
    flow = {}
    for edge in graph.get("edges", []):
        flow[(edge["from"], edge["to"])] = 0

    while True:
        parent = bfs_find_augmenting_path(residual, source, sink)
        if parent is None:
            break

        iterations += 1

        path_flow = find_bottleneck_capacity(parent, residual, source, sink)
        update_residual_graph(residual, parent, source, sink, path_flow)

        v = sink
        path_edges = []

        while v != source:
            u = parent[v]

            if (u, v) in flow:
                flow[(u, v)] += path_flow
            elif (v, u) in flow:
                flow[(v, u)] -= path_flow

            path_edges.append((u, v))
            v = u

        max_flow += path_flow

        steps.append({
            "iteration": iterations,
            "path": list(reversed(path_edges)),
            "flow_added": path_flow
        })

    flow_edges = []
    for (u, v), f in flow.items():
        if f > 0:
            flow_edges.append({
                "from": u,
                "to": v,
                "flow": f
            })

    return {
        "max_flow": max_flow,
        "flow_edges": flow_edges,
        "iterations": iterations,
        "steps": steps
    }

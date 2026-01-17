"""
Các thuật toán duyệt đồ thị (BFS, DFS).
"""
from collections import deque, defaultdict


def build_adjacency_list(graph):
    """Xây dựng danh sách kề từ dữ liệu đồ thị."""
    adj = defaultdict(list)

    for edge in graph['edges']:
        u = edge['from']
        v = edge['to']

        adj[u].append(v)

        # Kiểm tra hướng của cạnh cụ thể trước, sau đó mới dùng cấu hình toàn cục
        is_directed = edge.get('isDirected')
        if is_directed is None:
            is_directed = graph.get('directed', False)
        
        if not is_directed:
            adj[v].append(u)

    return adj


def bfs(graph, start):
    """Breadth-First Search (BFS)."""
    adj = build_adjacency_list(graph)

    visited = set()
    queue = deque()
    order = []
    steps = []

    queue.append(start)
    visited.add(start)

    steps.append({
        'type': 'visit',
        'node': start,
        'description': f"Bắt đầu BFS từ đỉnh {start}"
    })

    while queue:
        current = queue.popleft()
        order.append(current)

        for neighbor in adj[current]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

                steps.append({
                    'type': 'visit',
                    'node': neighbor,
                    'from': current,
                    'description': f"Thăm đỉnh {neighbor} từ {current}"
                })

    return {
        'order': order,
        'visited_count': len(visited),
        'steps': steps
    }


def dfs(graph, start):
    """Depth-First Search (DFS)."""
    adj = build_adjacency_list(graph)

    visited = set()
    stack = []
    order = []
    steps = []

    stack.append((start, None)) # (node, parent)

    steps.append({
        'type': 'visit',
        'node': start,
        'description': f"Bắt đầu DFS từ đỉnh {start}"
    })

    while stack:
        current, parent = stack.pop()

        if current in visited:
            continue

        visited.add(current)
        order.append(current)

        if parent is not None:
             steps.append({
                'type': 'visit',
                'node': current,
                'from': parent,
                'description': f"Thăm đỉnh {current} từ {parent}"
            })

        # Sắp xếp các đỉnh kề theo thứ tự ngược lại để đảm bảo thứ tự duyệt tự nhiên khi dùng stack
        neighbors = adj[current]
        neighbors.sort(reverse=True)

        for neighbor in neighbors:
            if neighbor not in visited:
                stack.append((neighbor, current))

    return {
        'order': order,
        'visited_count': len(visited),
        'steps': steps
    }

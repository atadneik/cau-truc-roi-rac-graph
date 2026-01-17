"""
Các thuật toán tìm đường đi ngắn nhất (Dijkstra, Bellman-Ford).
"""
import heapq
from collections import defaultdict
import math


def find_shortest_path(graph, start, end, algorithm='dijkstra'):
    """Tìm đường đi ngắn nhất từ start đến end sử dụng thuật toán được chỉ định."""
    
    # Xây dựng danh sách kề
    adj = defaultdict(list)
    for edge in graph['edges']:
        u, v, w = edge['from'], edge['to'], edge['weight']
        adj[u].append((v, w))
        
        # Kiểm tra hướng của cạnh cụ thể trước, sau đó mới dùng cấu hình toàn cục
        is_directed = edge.get('isDirected')
        if is_directed is None:
            is_directed = graph.get('directed', False)
            
        if not is_directed:
            adj[v].append((u, w))

    nodes = {n['id'] for n in graph['nodes']}

    if start not in nodes or end not in nodes:
        return {
            'path': [],
            'distance': None,
            'found': False,
            'steps': []
        }

    # Thuật toán Dijkstra
    if algorithm.lower() == 'dijkstra':
        dist = {node: math.inf for node in nodes}
        prev = {node: None for node in nodes}
        dist[start] = 0

        pq = [(0, start)]
        steps = []

        while pq:
            current_dist, u = heapq.heappop(pq)

            if current_dist > dist[u]:
                continue

            if u == end:
                break

            for v, w in adj[u]:
                if w < 0:
                    raise ValueError("Dijkstra không hỗ trợ trọng số âm")

                new_dist = dist[u] + w
                if new_dist < dist[v]:
                    dist[v] = new_dist
                    prev[v] = u
                    heapq.heappush(pq, (new_dist, v))

                    steps.append({
                        'current': u,
                        'neighbor': v,
                        'new_distance': new_dist,
                        'distances_snapshot': {k: (v if v != math.inf else None) for k, v in dist.items()}
                    })

        # Tái tạo đường đi
        path = []
        cur = end
        found = dist[end] != math.inf
        
        if found:
            while cur is not None:
                path.append(cur)
                cur = prev[cur]
            path.reverse()

        return {
            'path': path if found else [],
            'distance': dist[end] if found else None,
            'found': found,
            'steps': steps
        }

    # Thuật toán Bellman-Ford
    elif algorithm.lower() == 'bellman-ford':
        dist = {node: math.inf for node in nodes}
        prev = {node: None for node in nodes}
        dist[start] = 0
        steps = []

        edges = []
        for u in adj:
            for v, w in adj[u]:
                edges.append((u, v, w))

        # Relax các cạnh |V|-1 lần
        for i in range(len(nodes) - 1):
            updated = False
            for u, v, w in edges:
                if dist[u] != math.inf and dist[u] + w < dist[v]:
                    dist[v] = dist[u] + w
                    prev[v] = u
                    updated = True

                    steps.append({
                        'iteration': i + 1,
                        'from': u,
                        'to': v,
                        'new_distance': dist[v],
                        'distances_snapshot': {k: (v if v != math.inf else None) for k, v in dist.items()}
                    })
            if not updated:
                break

        # Phát hiện chu trình âm
        for u, v, w in edges:
            if dist[u] != math.inf and dist[u] + w < dist[v]:
                raise ValueError("Phát hiện chu trình âm")

        # Tái tạo đường đi
        path = []
        cur = end
        found = dist[end] != math.inf
        
        if found:
            while cur is not None:
                path.append(cur)
                cur = prev[cur]
            path.reverse()

        return {
            'path': path if found else [],
            'distance': dist[end] if found else None,
            'found': found,
            'steps': steps
        }

    else:
        raise ValueError("Thuật toán không hợp lệ. Chọn 'dijkstra' hoặc 'bellman-ford'")

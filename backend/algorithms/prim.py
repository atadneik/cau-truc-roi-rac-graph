"""
Thuật toán Prim cho bài toán Cây khung nhỏ nhất (MST).
"""
import heapq
from collections import defaultdict


def find_mst_prim(graph):
    """Tìm cây khung nhỏ nhất sử dụng thuật toán Prim."""
    # 1. Build adjacency list (undirected)
    adj = defaultdict(list)
    nodes = set()
    
    for node in graph['nodes']:
        nodes.add(node['id'])
        
    for edge in graph['edges']:
        u, v = edge['from'], edge['to']
        try:
            w = float(edge['weight'])
        except (ValueError, KeyError):
            w = 1.0 # Default weight if missing
            
        adj[u].append((v, w))
        adj[v].append((u, w))
        nodes.add(u)
        nodes.add(v)
        
    if not nodes:
        return {'mst_edges': [], 'total_weight': 0, 'complete': True, 'steps': []}
        
    # 2. Prim's Algorithm
    # Start from an arbitrary node
    start_node = list(nodes)[0] # Or graph['nodes'][0]['id'] if available
    
    mst_edges = []
    total_weight = 0
    visited = {start_node}
    
    # Priority Queue: (weight, from_node, to_node)
    pq = []
    
    # Add initial edges
    for v, w in adj[start_node]:
        heapq.heappush(pq, (w, start_node, v))
        
    steps = []
    
    # Initial step
    steps.append({
        'action': 'start',
        'node': start_node,
        'visited': list(visited),
        'mst_edges': []
    })
    
    while pq and len(visited) < len(nodes):
        w, u, v = heapq.heappop(pq)
        
        if v in visited:
            continue
            
        # Add edge to MST
        visited.add(v)
        mst_edges.append({'from': u, 'to': v, 'weight': w})
        total_weight += w
        
        # Record step
        steps.append({
            'action': 'add_edge',
            'edge': {'from': u, 'to': v, 'weight': w},
            'visited': list(visited),
            'mst_edges': list(mst_edges) # Snapshot
        })
        
        # Add new edges
        for neighbor, weight in adj[v]:
            if neighbor not in visited:
                heapq.heappush(pq, (weight, v, neighbor))
                
    complete = len(visited) == len(nodes)
    
    return {
        'mst_edges': mst_edges,
        'total_weight': total_weight,
        'complete': complete,
        'steps': steps
    }

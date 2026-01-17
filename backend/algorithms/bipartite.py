"""
Thuật toán kiểm tra đồ thị hai phía (Bipartite Graph Check).
"""
from collections import deque, defaultdict


def check_bipartite(graph):
    """Kiểm tra xem đồ thị có phải là hai phía không và trả về cách tô màu."""
    # Build adjacency list (undirected)
    adj = defaultdict(list)
    nodes = set()
    
    # Get all nodes first
    for node in graph['nodes']:
        nodes.add(node['id'])
        
    for edge in graph['edges']:
        u, v = edge['from'], edge['to']
        adj[u].append(v)
        adj[v].append(u)
        # Ensure nodes in edges are in our node set (just in case)
        nodes.add(u)
        nodes.add(v)
        
    coloring = {} # node_id -> 0 or 1
    is_bipartite = True
    
    # Iterate through all nodes to handle disconnected components
    for start_node in nodes:
        if start_node in coloring:
            continue
            
        # Start BFS for this component
        queue = deque([start_node])
        coloring[start_node] = 0
        
        while queue:
            u = queue.popleft()
            current_color = coloring[u]
            
            for v in adj[u]:
                if v not in coloring:
                    coloring[v] = 1 - current_color
                    queue.append(v)
                elif coloring[v] == current_color:
                    is_bipartite = False
                    # We can stop early or continue to color the rest for partial result
                    # Usually stop early is fine for the boolean, but we might want full coloring attempt?
                    # The requirement asks for coloring, let's just break this loop but we might need to be careful.
                    # If not bipartite, the coloring is invalid anyway.
                    break
            if not is_bipartite:
                break
        
        if not is_bipartite:
            break
            
    # Group nodes by color
    groups = {'group0': [], 'group1': []}
    for node, color in coloring.items():
        if color == 0:
            groups['group0'].append(node)
        else:
            groups['group1'].append(node)
            
    return {
        'is_bipartite': is_bipartite,
        'coloring': coloring,
        'groups': groups
    }

"""
Các tiện ích chuyển đổi biểu diễn đồ thị.
"""

def convert_graph(graph_data, from_type, to_type):
    """Chuyển đổi giữa các biểu diễn đồ thị: 'matrix', 'list', 'edges'."""
    # lay thong tin
    is_directed = graph_data.get('directed', False)
    
    # dua ve dang trung gian
    adj_list = {}
    nodes = []

    if from_type == 'list':
        adj_list = graph_data['adjacency_list']
        # Sort nodes numerically if they are integers, otherwise alphabetically
        nodes_keys = list(adj_list.keys())
        try:
            nodes = sorted(nodes_keys, key=lambda x: int(x))
        except (ValueError, TypeError):
            nodes = sorted(nodes_keys)
        
    elif from_type == 'matrix':
        matrix = graph_data['matrix']
        nodes = graph_data['nodes']
        adj_list = {node: [] for node in nodes}
        for i, row in enumerate(matrix):
            for j, weight in enumerate(row):
                if weight != 0:
                    adj_list[nodes[i]].append({'to': nodes[j], 'weight': weight})
                    
    elif from_type == 'edges':
        edges = graph_data['edges']
        nodes_set = set([e['from'] for e in edges] + [e['to'] for e in edges])
        try:
            nodes = sorted(nodes_set, key=lambda x: int(x))
        except (ValueError, TypeError):
            nodes = sorted(nodes_set)
        adj_list = {node: [] for node in nodes}
        for edge in edges:
            adj_list[edge['from']].append({'to': edge['to'], 'weight': edge['weight']})

    # tu trung gian ve dich 
    if to_type == 'list':
        return {'adjacency_list': adj_list, 'directed': is_directed}

    elif to_type == 'matrix':
        node_to_idx = {node: i for i, node in enumerate(nodes)}
        size = len(nodes)
        matrix = [[0] * size for _ in range(size)]
        
        for u in adj_list:
            for neighbor in adj_list[u]:
                v = neighbor['to']
                weight = neighbor['weight']
                matrix[node_to_idx[str(u)]][node_to_idx[str(v)]] = weight
                
        return {'matrix': matrix, 'nodes': nodes, 'directed': is_directed}

    elif to_type == 'edges':
        edge_list = []
        seen_edges = set() # tránh lặp cạnh nếu là đồ thị vô hướng
        
        for u in adj_list:
            for neighbor in adj_list[u]:
                v = neighbor['to']
                w = neighbor['weight']
                
                if not is_directed:
                    # Sắp xếp u, v để tạo định danh duy nhất cho cạnh vô hướng
                    try:
                        edge_id = tuple(sorted((u, v), key=lambda x: int(x)))
                    except (ValueError, TypeError):
                        edge_id = tuple(sorted((u, v)))
                    if edge_id not in seen_edges:
                        edge_list.append({'from': u, 'to': v, 'weight': w})
                        seen_edges.add(edge_id)
                else:
                    edge_list.append({'from': u, 'to': v, 'weight': w})
                    
        return {'edges': edge_list, 'directed': is_directed}


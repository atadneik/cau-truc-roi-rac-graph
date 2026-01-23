"""
Thuật toán kiểm tra đồ thị hai phía (Bipartite Graph Check).
"""
from collections import deque, defaultdict


def check_bipartite(graph):
    """Kiểm tra xem đồ thị có phải là hai phía không và trả về cách tô màu."""
    # Xây dựng danh sách kề (vô hướng)
    adj = defaultdict(list)
    nodes = set()
    
    # Lấy tất cả các đỉnh trước
    for node in graph['nodes']:
        nodes.add(node['id'])
        
    for edge in graph['edges']:
        u, v = edge['from'], edge['to']
        adj[u].append(v)
        adj[v].append(u)
        # Đảm bảo các đỉnh trong cạnh có trong tập hợp đỉnh (đề phòng trường hợp thiếu)
        nodes.add(u)
        nodes.add(v)
        
    coloring = {} # node_id -> 0 hoặc 1
    is_bipartite = True
    
    # Duyệt qua tất cả các đỉnh để xử lý các thành phần liên thông rời rạc
    for start_node in nodes:
        if start_node in coloring:
            continue
            
        # Bắt đầu BFS cho thành phần này
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
                    # Phát hiện xung đột: hai đỉnh kề nhau có cùng màu.
                    # Kết luận ngay đây không phải là đồ thị hai phía và dừng xử lý.
                    break
            if not is_bipartite:
                break
        
        if not is_bipartite:
            break
            
    # Nhóm các đỉnh theo màu
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

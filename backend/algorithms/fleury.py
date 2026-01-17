"""
Thuật toán Fleury cho Đường đi/Chu trình Euler.
"""
import sys
import copy
from collections import deque


def bfs_count_reachable(start_node, adj):
    """Đếm số đỉnh có thể đi tới từ start_node bằng BFS."""
    count = 0
    visited = set()
    queue = deque([start_node])
    visited.add(start_node)
    count += 1

    while queue:
        u = queue.popleft()
        for v in adj[u]:
            if v not in visited:
                visited.add(v)
                count += 1
                queue.append(v)
    return count

def is_valid_next_edge(u, v, adj, is_directed):
    """Kiểm tra xem cạnh (u, v) có hợp lệ để đi tiếp không (không phải là cầu trừ khi cần thiết)."""
    # 1. Nếu chỉ còn 1 cạnh nối từ u, bắt buộc phải đi
    if len(adj[u]) == 1:
        return True

    # 2. Kiểm tra xem (u, v) có phải là cầu không
    # a) Đếm số đỉnh tới được trước khi xóa cạnh
    count_before = bfs_count_reachable(u, adj)

    # b) Xóa tạm thời cạnh (u, v)
    adj[u].remove(v)
    if not is_directed:
        adj[v].remove(u)

    # c) Đếm số đỉnh tới được sau khi xóa
    count_after = bfs_count_reachable(u, adj)

    # d) Thêm lại cạnh (Backtrack)
    adj[u].append(v)
    if not is_directed:
        adj[v].append(u)

    # Nếu số đỉnh tới được giảm đi -> Cạnh là cầu -> Tránh đi (trừ khi không còn đường nào khác)
    # Tuy nhiên ở bước 1 ta đã check len == 1, nên nếu xuống đây mà count giảm thì return False.
    return count_before <= count_after

def check_connectivity(nodes, adj):
    """Kiểm tra xem tất cả các cạnh có thuộc cùng một thành phần liên thông không."""
    # Tìm một đỉnh bất kỳ có bậc > 0 để bắt đầu duyệt
    start_node = -1
    non_isolated_nodes = 0
    
    # Tính bậc của mỗi đỉnh (coi như vô hướng)
    degrees = [0] * len(nodes)
    for u in range(len(adj)):
        degrees[u] += len(adj[u])
        for v in adj[u]:
            degrees[v] += 1
            
    for i in range(len(nodes)):
        if degrees[i] > 0:
            non_isolated_nodes += 1
            if start_node == -1:
                start_node = i
    
    if start_node == -1:
        return True # Đồ thị rỗng coi như liên thông

    # Đếm số đỉnh đi tới được từ start_node
    reachable_count = bfs_count_reachable(start_node, adj)
    
    # Nếu số đỉnh duyệt được < tổng số đỉnh có cạnh -> Đồ thị không liên thông
    return reachable_count == non_isolated_nodes

def find_start_node(n, adj, is_directed):
    """Tìm đỉnh bắt đầu hợp lệ cho đường đi/chu trình Euler."""
    start_node = 0
    
    if not is_directed:
        # Vô hướng: Đếm số đỉnh bậc lẻ
        odd_degree_nodes = []
        for i in range(n):
            if len(adj[i]) % 2 != 0:
                odd_degree_nodes.append(i)
        
        # Điều kiện Euler: 0 hoặc 2 đỉnh bậc lẻ
        if len(odd_degree_nodes) == 0:
            # Chu trình Euler: Bắt đầu tại đỉnh bất kỳ có bậc > 0
            for i in range(n):
                if len(adj[i]) > 0: return i
            return 0
        elif len(odd_degree_nodes) == 2:
            # Đường đi Euler: Bắt đầu tại một trong hai đỉnh bậc lẻ
            return odd_degree_nodes[0]
        else:
            return -1 # Không tồn tại
    else:
        # Có hướng: Tính bán bậc ra - bán bậc vào
        in_degree = [0] * n
        out_degree = [0] * n
        for u in range(n):
            out_degree[u] = len(adj[u])
            for v in adj[u]:
                in_degree[v] += 1
        
        start_nodes = []
        end_nodes = []
        
        for i in range(n):
            diff = out_degree[i] - in_degree[i]
            if diff == 1:
                start_nodes.append(i)
            elif diff == -1:
                end_nodes.append(i)
            elif diff != 0:
                return -1 # Không thỏa mãn cân bằng
        
        if len(start_nodes) == 0 and len(end_nodes) == 0:
            # Chu trình Euler: Bắt đầu bất kỳ đỉnh nào có cạnh
            for i in range(n):
                if out_degree[i] > 0 or in_degree[i] > 0: return i
            return 0
        elif len(start_nodes) == 1 and len(end_nodes) == 1:
            # Đường đi Euler
            return start_nodes[0]
        else:
            return -1

def find_euler_path(graph, start_node_id=None):
    """Tìm đường đi Euler sử dụng thuật toán Fleury."""

    # 1. Map ID sang index 0..n-1
    node_id_to_idx = {n['id']: i for i, n in enumerate(nodes_data)}
    idx_to_node_id = {i: n['id'] for i, n in enumerate(nodes_data)}
    n = len(nodes_data)

    # 2. Xây dựng danh sách kề (Adjacency List)
    # Lưu ý: Với đồ thị vô hướng, cạnh (u, v) được thêm vào cả adj[u] và adj[v]
    adj = [[] for _ in range(n)]
    total_edges_count = 0
    
    for edge in edges_data:
        u_id = edge['from']
        v_id = edge['to']
        if u_id not in node_id_to_idx or v_id not in node_id_to_idx:
            continue
        
        u = node_id_to_idx[u_id]
        v = node_id_to_idx[v_id]
        
        adj[u].append(v)
        if not is_directed:
            adj[v].append(u)
        
        total_edges_count += 1

    # 3. Kiểm tra tính liên thông (Bắt buộc)
    if not check_connectivity(nodes_data, adj):
         return {'path': [], 'exists': False, 'length': 0, 'steps': ["Đồ thị không liên thông."]}

    # 4. Tìm đỉnh xuất phát
    curr = find_start_node(n, adj, is_directed)
    
    # Nếu người dùng chỉ định đỉnh bắt đầu, ta kiểm tra xem nó có hợp lệ không
    # (Logic này mở rộng thêm, ưu tiên thuật toán tự tìm)
    if start_node_id is not None and start_node_id in node_id_to_idx:
        # Nếu đồ thị có chu trình Euler (bắt đầu đâu cũng được), ta chiều ý người dùng
        # Nếu đồ thị chỉ có đường đi Euler, bắt buộc phải theo find_start_node
        pass 

    if curr == -1:
        return {'path': [], 'exists': False, 'length': 0, 'steps': ["Không thỏa mãn điều kiện bậc của đỉnh."]}

    # 5. Thuật toán Fleury
    res_path_indices = [curr]
    steps = []
    
    # Copy adj để thao tác xóa cạnh
    temp_adj = [list(neighbors) for neighbors in adj]
    
    # Tổng số cạnh cần đi qua
    edges_to_visit = total_edges_count
    
    while edges_to_visit > 0:
        found_next_step = False
        
        # Lấy danh sách các đỉnh kề hiện tại
        # Sắp xếp để đảm bảo thứ tự duyệt nhất quán (ví dụ ưu tiên đỉnh có index nhỏ)
        neighbors = sorted(temp_adj[curr])
        
        for v in neighbors:
            # Kiểm tra xem đi qua cạnh (curr, v) có hợp lệ không
            if is_valid_next_edge(curr, v, temp_adj, is_directed):
                u_real = idx_to_node_id[curr]
                v_real = idx_to_node_id[v]
                steps.append(f"Đi từ {u_real} đến {v_real}")
                
                # Xóa cạnh đã đi
                temp_adj[curr].remove(v)
                if not is_directed:
                    temp_adj[v].remove(curr)
                
                curr = v
                res_path_indices.append(curr)
                edges_to_visit -= 1
                found_next_step = True
                
                # TỐI ƯU: Tìm được cạnh hợp lệ là đi luôn, không cần check cạnh khác
                break
        
        if not found_next_step:
            # Bị kẹt (không còn cạnh đi tiếp dù chưa hết cạnh)
            break

    # 6. Kết quả
    res_path = [idx_to_node_id[i] for i in res_path_indices]
    exists = (len(res_path) == total_edges_count + 1)

    return {
        'path': res_path,
        'exists': exists,
        'length': len(res_path) - 1 if len(res_path) > 0 else 0,
        'steps': steps
    }
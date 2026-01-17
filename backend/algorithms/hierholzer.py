"""
Thuật toán Hierholzer cho Đường đi/Chu trình Euler.

MỤC ĐÍCH:
Tìm chu trình hoặc đường đi Euler trong đồ thị có hướng hoặc vô hướng.
Hierholzer hiệu quả hơn Fleury (O(E) so với O(E^2)) vì không cần kiểm tra cầu.

CẢI TIẾN:
1. Kiểm tra tính liên thông (Connectivity Check).
2. Kiểm tra điều kiện bậc (Degree Check) để xác định có Euler Path/Circuit không.
3. Sử dụng Stack để tìm đường đi (Iterative DFS) -> Tránh đệ quy sâu.
4. Xử lý đúng cạnh song song (Parallel Edges).
5. Trả về kết quả chi tiết kèm các bước thực hiện (steps).
"""
import sys
import copy
from collections import deque, defaultdict

def bfs_check_connectivity(nodes, adj):
    """
    Kiểm tra xem tất cả các cạnh có thuộc cùng một thành phần liên thông không.
    (Bỏ qua các đỉnh cô lập).
    """
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
        return True # Đồ thị rỗng hoặc toàn đỉnh cô lập

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
    
    # Nếu số đỉnh duyệt được < tổng số đỉnh có cạnh -> Không liên thông
    return count == non_isolated_nodes

def get_degrees(n, adj, is_directed):
    """
    Tính bậc của các đỉnh.
    """
    if not is_directed:
        # Vô hướng: Bậc = số cạnh nối với đỉnh
        degree = [len(adj[i]) for i in range(n)]
        return degree, degree # In/Out giống nhau
    else:
        # Có hướng: Tính In-degree và Out-degree
        out_degree = [len(adj[i]) for i in range(n)]
        in_degree = [0] * n
        for u in range(n):
            for v in adj[u]:
                in_degree[v] += 1
        return in_degree, out_degree

def find_start_node_hierholzer(n, adj, is_directed):
    """
    Xác định điểm bắt đầu và loại đường đi (Cycle hay Path).
    Returns: (start_node, type_str) hoặc (-1, error_msg)
    """
    in_degree, out_degree = get_degrees(n, adj, is_directed)
    
    if not is_directed:
        # Vô hướng
        odd_nodes = [i for i in range(n) if out_degree[i] % 2 != 0]
        if len(odd_nodes) == 0:
            # Tìm đỉnh đầu tiên có cạnh để bắt đầu
            for i in range(n):
                if out_degree[i] > 0: return i, "Cycle"
            return 0, "Cycle" # Đồ thị rỗng
        elif len(odd_nodes) == 2:
            return odd_nodes[0], "Path"
        else:
            return -1, "Không thỏa mãn điều kiện bậc (số đỉnh bậc lẻ phải là 0 hoặc 2)."
    else:
        # Có hướng
        start_nodes = []
        end_nodes = []
        balanced_nodes = 0
        
        for i in range(n):
            diff = out_degree[i] - in_degree[i]
            if diff == 1:
                start_nodes.append(i)
            elif diff == -1:
                end_nodes.append(i)
            elif diff == 0:
                balanced_nodes += 1
            else:
                return -1, "Không thỏa mãn điều kiện cân bằng bậc."
        
        if len(start_nodes) == 0 and len(end_nodes) == 0:
             # Tìm đỉnh đầu tiên có cạnh
            for i in range(n):
                if out_degree[i] > 0 or in_degree[i] > 0: return i, "Cycle"
            return 0, "Cycle"
        elif len(start_nodes) == 1 and len(end_nodes) == 1:
            return start_nodes[0], "Path"
        else:
            return -1, "Không thỏa mãn điều kiện đầu/cuối của đường đi Euler."

def find_euler_circuit(graph):
    """
    Hàm chính tìm chu trình/đường đi Euler bằng thuật toán Hierholzer.
    """
    nodes_data = graph.get('nodes', [])
    edges_data = graph.get('edges', [])
    is_directed = graph.get('directed', False)

    if not nodes_data:
        return {'path': [], 'exists': False, 'length': 0, 'steps': []}

    # 1. Map ID
    node_id_to_idx = {n['id']: i for i, n in enumerate(nodes_data)}
    idx_to_node_id = {i: n['id'] for i, n in enumerate(nodes_data)}
    n = len(nodes_data)

    # 2. Build Adjacency List
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

    # 3. Check Connectivity
    if not bfs_check_connectivity(nodes_data, adj):
        return {'path': [], 'exists': False, 'length': 0, 'steps': ["Đồ thị không liên thông."]}

    # 4. Find Start Node & Check Conditions
    start_node, msg = find_start_node_hierholzer(n, adj, is_directed)
    
    if start_node == -1:
        return {'path': [], 'exists': False, 'length': 0, 'steps': [msg]}

    # 5. Hierholzer Algorithm
    # Sử dụng Stack để tìm đường
    # adj sẽ bị thay đổi (xóa cạnh dần)
    
    # Copy adj để không làm hỏng dữ liệu gốc (nếu cần dùng lại sau này)
    # Tuy nhiên ở đây ta build adj cục bộ nên có thể sửa trực tiếp.
    # Để xử lý cạnh song song và xóa nhanh:
    # Với Python list, remove(v) tốn O(deg(u)). Tổng cộng O(E * max_deg).
    # Để tối ưu O(E), ta có thể dùng pop() từ cuối list, nhưng cần swap v với phần tử cuối.
    # Hoặc đơn giản dùng list.pop() nếu thứ tự không quan trọng.
    # Để đảm bảo thứ tự (ví dụ ưu tiên đỉnh nhỏ), ta cần sort trước.
    
    for i in range(n):
        adj[i].sort(reverse=True) # Sort reverse để pop() lấy phần tử nhỏ nhất ra trước
    
    curr_path = [start_node] # Stack
    circuit = [] # Kết quả (ngược)
    steps = []
    
    steps.append(f"Bắt đầu tại đỉnh {idx_to_node_id[start_node]}")

    while curr_path:
        u = curr_path[-1] # Peek
        
        if adj[u]:
            # Còn cạnh để đi
            v = adj[u].pop() # Lấy cạnh (u, v) và xóa khỏi danh sách
            
            # Nếu vô hướng, phải xóa cả (v, u)
            if not is_directed:
                # Xóa u trong adj[v]. Lưu ý: adj[v] đã sort reverse.
                # Việc tìm và xóa u trong adj[v] tốn thời gian.
                # Để tối ưu O(1) xóa, cần cấu trúc phức tạp hơn (như set hoặc dict đếm).
                # Với giới hạn bài tập nhỏ, list.remove() chấp nhận được.
                if u in adj[v]:
                    adj[v].remove(u)
            
            curr_path.append(v)
            # steps.append(f"Đi tới {idx_to_node_id[v]}") 
        else:
            # Hết đường, quay lui và thêm vào mạch
            finished_node = curr_path.pop()
            circuit.append(finished_node)
            # steps.append(f"Backtrack từ {idx_to_node_id[finished_node]}")

    # Kết quả là circuit đảo ngược
    circuit.reverse()
    
    # Map back to IDs
    res_path = [idx_to_node_id[i] for i in circuit]
    
    # Kiểm tra xem đã đi hết cạnh chưa (phòng trường hợp đồ thị có nhiều thành phần liên thông có cạnh)
    # Tuy nhiên bước check_connectivity ở trên đã lo việc này.
    # Nhưng cẩn thận: check_connectivity chỉ check các đỉnh CÓ CẠNH.
    # Nếu Hierholzer chạy xong mà độ dài đường đi (số cạnh) != tổng số cạnh -> Fail.
    
    path_edges_count = len(res_path) - 1
    if path_edges_count != total_edges_count:
         return {
            'path': [], 
            'exists': False, 
            'length': 0, 
            'steps': ["Không đi qua hết tất cả các cạnh (Đồ thị có thể bị ngắt quãng)."]
        }

    return {
        'path': res_path,
        'exists': True,
        'length': path_edges_count,
        'steps': steps # Hierholzer ít steps chi tiết hơn Fleury vì nó backtrack
    }

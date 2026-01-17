# Báo Cáo Bài Tập Lớn: Ứng Dụng Trực Quan Hóa Đồ Thị (Graph Visualization)

## 1. Giới Thiệu Đề Tài
Trong khoa học máy tính, Đồ thị (Graph) là một cấu trúc dữ liệu nền tảng với vô vàn ứng dụng thực tế như định tuyến mạng, bản đồ số, mạng xã hội, và lập lịch dự án. Tuy nhiên, việc học và hiểu các thuật toán đồ thị chỉ qua lý thuyết thường gặp nhiều khó khăn do tính trừu tượng cao.

**Mục tiêu của dự án** là xây dựng một ứng dụng web trực quan, cho phép người dùng tương tác trực tiếp để tạo đồ thị và quan sát từng bước chạy của các thuật toán. Điều này giúp sinh viên và giảng viên có một công cụ đắc lực trong việc học tập và giảng dạy môn Cấu trúc Dữ liệu và Giải thuật.

## 2. Các Tính Năng Chi Tiết

### 2.1. Tương Tác & Thao Tác Đồ Thị (Graph Manipulation)
Hệ thống cung cấp một giao diện Canvas tương tác cao:
- **Vẽ Đỉnh (Add Vertex)**: Người dùng click chuột trái vào vùng trống trên Canvas để tạo đỉnh mới. Các đỉnh được tự động đánh số thứ tự (0, 1, 2...).
- **Vẽ Cạnh (Add Edge)**:
    - Chọn chế độ "Nối đỉnh", click vào đỉnh nguồn và kéo đến đỉnh đích.
    - Hộp thoại (Modal) xuất hiện cho phép nhập **Trọng số (Weight)** và chọn loại cạnh (**Có hướng** hoặc **Vô hướng**).
    - Hỗ trợ đồ thị hỗn hợp (Mixed Graph) chứa cả cạnh có hướng và vô hướng.
- **Di Chuyển & Chỉnh Sửa**:
    - Tính năng **Drag & Drop** cho phép kéo thả các đỉnh để thay đổi bố cục đồ thị tùy ý.
    - Click chuột phải (hoặc chọn công cụ xóa) để xóa đỉnh hoặc cạnh.
- **Quản Lý Dữ Liệu**:
    - **Export JSON**: Xuất cấu trúc đồ thị hiện tại ra file `.json` để lưu trữ.
    - **Import JSON**: Tải lại đồ thị đã lưu để tiếp tục làm việc.
    - **Clear All**: Xóa trắng toàn bộ Canvas để bắt đầu lại.

### 2.2. Chuyển Đổi Biểu Diễn (Representation Conversion)
Hệ thống tự động đồng bộ và hiển thị dữ liệu đồ thị dưới 3 dạng biểu diễn kinh điển trong thời gian thực:
1.  **Ma trận kề (Adjacency Matrix)**: Hiển thị lưới $N \times N$ với trọng số giữa các đỉnh.
2.  **Danh sách kề (Adjacency List)**: Liệt kê các đỉnh kề và trọng số tương ứng cho từng đỉnh.
3.  **Danh sách cạnh (Edge List)**: Liệt kê toàn bộ các cạnh dưới dạng `(u, v, w)`.

### 2.3. Mô Phỏng Thuật Toán (Algorithm Visualization)
Ứng dụng không chỉ trả về kết quả cuối cùng mà còn trả về **các bước thực hiện (steps)**, giúp Frontend hiển thị hoạt hình (animation) quá trình duyệt:

#### A. Tìm Đường Đi Ngắn Nhất (Shortest Path)
- **Dijkstra**: Sử dụng hàng đợi ưu tiên (Priority Queue). Thuật toán tối ưu cho đồ thị có trọng số không âm.
    - *Hiển thị*: Tô màu các đỉnh đã duyệt, đỉnh đang xét, và đường đi ngắn nhất cuối cùng.
- **Bellman-Ford**: Xử lý được đồ thị có trọng số âm.
    - *Tính năng*: Phát hiện và cảnh báo nếu đồ thị chứa **chu trình âm** (Negative Cycle).

#### B. Duyệt Đồ Thị (Traversal)
- **BFS (Breadth-First Search)**: Duyệt theo chiều rộng, sử dụng hàng đợi (Queue).
    - *Ứng dụng*: Tìm đường đi ngắn nhất trên đồ thị không trọng số.
- **DFS (Depth-First Search)**: Duyệt theo chiều sâu, sử dụng ngăn xếp (Stack) hoặc đệ quy.
    - *Ứng dụng*: Kiểm tra tính liên thông, phát hiện chu trình.

#### C. Cây Khung Nhỏ Nhất (Minimum Spanning Tree - MST)
- **Prim**: Thuật toán tham lam (Greedy), phát triển cây từ một đỉnh xuất phát bằng cách chọn cạnh nhỏ nhất kết nối với tập đỉnh đã có.
- **Kruskal**: Sắp xếp các cạnh theo trọng số tăng dần, lần lượt chọn cạnh nếu không tạo thành chu trình (sử dụng cấu trúc dữ liệu **Disjoint Set / Union-Find**).

#### D. Luồng Cực Đại (Maximum Flow)
- **Ford-Fulkerson (Edmonds-Karp)**: Tìm đường tăng luồng (Augmenting Path) trên đồ thị thặng dư bằng BFS cho đến khi không còn đường đi từ nguồn (Source) đến đích (Sink).

#### E. Chu Trình & Đường Đi Euler
- **Fleury**: Tìm đường đi Euler bằng cách ưu tiên đi qua cạnh không phải là cầu (Bridge).
- **Hierholzer**: Thuật toán hiệu quả hơn ($O(E)$) để tìm chu trình Euler trên đồ thị liên thông.

#### F. Kiểm Tra Tính Chất
- **Bipartite Check**: Sử dụng BFS/DFS để tô màu đồ thị bằng 2 màu. Nếu không có hai đỉnh kề nhau cùng màu, đồ thị là đồ thị hai phía.

## 3. Kiến Trúc Hệ Thống & Công Nghệ

### 3.1. Backend (Python Flask)
Backend đóng vai trò là "bộ não" xử lý logic thuật toán.
- **Framework**: Flask (Microframework nhẹ, linh hoạt).
- **Thư viện chính**:
    - `networkx`: Hỗ trợ mạnh mẽ các cấu trúc dữ liệu đồ thị và một số thuật toán phức tạp.
    - `flask-cors`: Xử lý vấn đề Cross-Origin Resource Sharing khi Frontend và Backend chạy khác domain.
- **Luồng xử lý**:
    1.  Nhận request JSON từ Frontend chứa danh sách đỉnh (`nodes`) và cạnh (`edges`).
    2.  Xây dựng lại cấu trúc đồ thị (Adjacency List/Matrix) trong Python.
    3.  Thực thi thuật toán.
    4.  Ghi lại từng bước thực hiện (visited nodes, path updates) vào danh sách `steps`.
    5.  Trả về JSON chứa kết quả cuối cùng và danh sách `steps`.

### 3.2. Frontend (HTML/CSS/JS)
Frontend đảm nhiệm vai trò hiển thị và tương tác.
- **HTML5 Canvas**: Được sử dụng để vẽ đồ họa 2D hiệu năng cao.
- **Vanilla JavaScript (ES6+)**:
    - Class `Graph`: Quản lý trạng thái dữ liệu (CRUD đỉnh/cạnh).
    - Class `GraphCanvas`: Chuyên trách việc vẽ (Render loop, xử lý sự kiện chuột).
    - Class `API`: Wrapper cho các gọi `fetch` đến Backend.
    - Class `UI`: Quản lý logic giao diện, modal, và kết nối các thành phần.
- **CSS3**: Thiết kế giao diện hiện đại, Responsive (bố cục 3 cột).

### 3.3. Hạ Tầng & Triển Khai (DevOps)
- **Docker**:
    - `Dockerfile`: Đóng gói môi trường Python 3.9 cho Backend.
    - `nginx.conf`: Cấu hình Nginx làm Web Server và Reverse Proxy.
    - `docker-compose.yml`: Định nghĩa và chạy đa dịch vụ (Backend + Frontend) chỉ với 1 lệnh.
- **Cloud Deployment**:
    - Triển khai thành công trên **Render.com**.
    - Backend chạy dưới dạng Web Service (Docker).
    - Frontend chạy dưới dạng Static Site, kết nối với Backend qua biến môi trường `API_URL`.

## 4. Thách Thức & Giải Pháp

| Thách Thức | Giải Pháp |
| :--- | :--- |
| **Đồ thị hỗn hợp (Mixed Graph)** | Backend xử lý logic riêng cho cạnh có hướng và vô hướng. Khi xây dựng danh sách kề, cạnh vô hướng được thêm 2 chiều `u->v` và `v->u`. |
| **Trực quan hóa (Animation)** | Backend không chỉ trả về kết quả mà trả về một mảng `steps`. Frontend sử dụng `setTimeout` hoặc `requestAnimationFrame` để "phát lại" từng bước này. |
| **CORS Error** | Cấu hình `flask-cors` cho phép mọi origin (`*`) và cấu hình Nginx Proxy trong môi trường Docker để Frontend gọi API cùng domain. |
| **Triển khai Cloud** | Tách biệt Frontend và Backend thành 2 service trên Render. Sử dụng biến `window.API_URL` để Frontend biết địa chỉ Backend động. |

## 5. Hướng Phát Triển
- [ ] **Lưu lịch sử**: Cho phép Undo/Redo các thao tác vẽ.
- [ ] **Thuật toán nâng cao**: A* Search, Topological Sort, Strongly Connected Components (Tarjan/Kosaraju).
- [ ] **Hiệu năng**: Tối ưu hóa Canvas cho đồ thị cực lớn (>1000 đỉnh) sử dụng WebGL hoặc thư viện như D3.js/Vis.js (hiện tại đang tự viết engine vẽ để hiểu sâu nguyên lý).

## 6. Kết Luận
Dự án đã hoàn thành tốt các mục tiêu đề ra, cung cấp một công cụ trực quan hóa mạnh mẽ, chính xác và dễ sử dụng. Việc áp dụng Docker và quy trình triển khai chuẩn giúp dự án dễ dàng mở rộng và bảo trì trong tương lai.

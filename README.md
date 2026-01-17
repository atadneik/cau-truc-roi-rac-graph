# Ứng Dụng Trực Quan Hóa Đồ Thị (Graph Visualization)

Dự án này là một ứng dụng web tương tác giúp trực quan hóa các thuật toán đồ thị phổ biến. Ứng dụng được xây dựng với mục đích hỗ trợ học tập và giảng dạy môn Cấu trúc Dữ liệu & Giải thuật, cho phép người dùng vẽ đồ thị, chạy thuật toán từng bước và quan sát kết quả trực quan.

## 🚀 Tính Năng Đã Thực Hiện

### 1. Thao Tác Đồ Thị (Graph Manipulation)
- **Vẽ Đồ Thị Tương Tác**:
  - Thêm đỉnh (Vertex) bằng cách click chuột.
  - Thêm cạnh (Edge) bằng cách nối hai đỉnh.
  - Hỗ trợ cả đồ thị **Có hướng (Directed)** và **Vô hướng (Undirected)**.
  - Tùy chỉnh trọng số (Weight) cho từng cạnh.
  - Di chuyển đỉnh (Drag & Drop) để chỉnh sửa bố cục.
  - Xóa đỉnh và cạnh.
- **Quản Lý Dữ Liệu**:
  - **Lưu Đồ Thị**: Xuất cấu trúc đồ thị hiện tại ra file JSON.
  - **Tải Đồ Thị**: Nhập dữ liệu đồ thị từ file JSON đã lưu.
  - **Xóa Trắng**: Tạo mới đồ thị.
- **Chuyển Đổi Biểu Diễn**:
  - Tự động chuyển đổi và hiển thị đồ thị dưới các dạng:
    - **Ma trận kề (Adjacency Matrix)**
    - **Danh sách kề (Adjacency List)**
    - **Danh sách cạnh (Edge List)**

### 2. Thuật Toán Cơ Bản
- **Tìm Đường Đi Ngắn Nhất (Shortest Path)**:
  - **Dijkstra**: Tìm đường đi ngắn nhất từ một đỉnh đến các đỉnh khác (trọng số không âm).
  - **Bellman-Ford**: Hỗ trợ đồ thị có trọng số âm và phát hiện chu trình âm.
  - *Cập nhật mới*: Đã hỗ trợ xử lý đúng cho đồ thị hỗn hợp (có cả cạnh có hướng và vô hướng).
- **Duyệt Đồ Thị (Traversal)**:
  - **BFS (Breadth-First Search)**: Duyệt theo chiều rộng, hiển thị thứ tự duyệt và cây BFS.
  - **DFS (Depth-First Search)**: Duyệt theo chiều sâu, hiển thị thứ tự duyệt.
- **Kiểm Tra Tính Chất**:
  - **Bipartite Graph Check**: Kiểm tra đồ thị hai phía và tô màu phân loại đỉnh.

### 3. Thuật Toán Nâng Cao
- **Cây Khung Nhỏ Nhất (Minimum Spanning Tree - MST)**:
  - **Prim**: Thuật toán tham lam phát triển cây khung từ một đỉnh.
  - **Kruskal**: Thuật toán tham lam chọn cạnh có trọng số nhỏ nhất và sử dụng Union-Find để tránh chu trình.
- **Luồng Cực Đại (Maximum Flow)**:
  - **Ford-Fulkerson**: Sử dụng phương pháp đường tăng (Augmenting Path) trên đồ thị thặng dư (Residual Graph) để tìm luồng cực đại từ nguồn (Source) đến đích (Sink).
- **Chu Trình & Đường Đi Euler**:
  - **Fleury**: Tìm đường đi Euler bằng cách tránh đi qua cầu (Bridge) nếu có thể.
  - **Hierholzer**: Tìm chu trình Euler hiệu quả hơn cho đồ thị liên thông.

## 🛠️ Cách Hoạt Động

### Backend (Python/Flask)
Backend đóng vai trò là bộ xử lý thuật toán.
- **API Endpoints**: Cung cấp các RESTful API (ví dụ: `/api/shortest-path`, `/api/bfs`) nhận dữ liệu đồ thị từ frontend.
- **Xử Lý Logic**: Các thuật toán được cài đặt độc lập trong thư mục `algorithms/`.
- **Dữ Liệu**: Nhận input là danh sách đỉnh/cạnh và trả về kết quả chi tiết (đường đi, các bước thực hiện, màu sắc đỉnh...) để frontend hiển thị animation.

### Frontend (HTML/CSS/JS)
Frontend đảm nhiệm việc hiển thị và tương tác người dùng.
- **Canvas API**: Sử dụng HTML5 Canvas để vẽ các đỉnh, cạnh và hiệu ứng hoạt hình (animation) mượt mà.
- **Quản Lý State**: Class `Graph` quản lý trạng thái logic của đồ thị, trong khi `GraphCanvas` xử lý việc vẽ.
- **Tương Tác API**: Gửi request chứa cấu trúc đồ thị về backend và nhận kết quả để hiển thị từng bước chạy của thuật toán.

## 📦 Cấu Trúc Dự Án

```
cautrucroirac/
├── backend/
│   ├── app.py                # Server Flask chính
│   └── algorithms/           # Cài đặt các thuật toán (Python)
│       ├── shortest_path.py  # Dijkstra, Bellman-Ford
│       ├── traversal.py      # BFS, DFS
│       ├── prim.py           # Prim MST
│       ├── kruskal.py        # Kruskal MST
│       ├── ...               # Các thuật toán khác
└── frontend/
    ├── index.html            # Giao diện chính
    ├── css/                  # Stylesheet
    └── js/                   # Mã nguồn JavaScript
        ├── graph.js          # Class Graph
        ├── canvas.js         # Xử lý vẽ Canvas
        ├── ui.js             # Xử lý sự kiện UI
        └── api.js            # Gọi API Backend
```

## 👨‍💻 Tác Giả
Bài tập lớn môn Cấu trúc Dữ liệu & Giải thuật.

# Ứng Dụng Trực Quan Hóa Đồ Thị
## Graph Visualization Application

Ứng dụng web để vẽ và trực quan hóa đồ thị với đầy đủ các thuật toán cơ bản và nâng cao.

### 🎯 Chức năng

#### Phần Cơ Bản:
1. ✅ Vẽ đồ thị trực quan (Canvas)
2. ✅ Lưu/tải đồ thị (JSON)
3. ✅ Tìm đường đi ngắn nhất (Dijkstra, Bellman-Ford)
4. ✅ Duyệt đồ thị (BFS & DFS)
5. ✅ Kiểm tra đồ thị 2 phía (Bipartite)
6. ✅ Chuyển đổi biểu diễn (Ma trận kề ↔ Danh sách kề ↔ Danh sách cạnh)

#### Phần Nâng Cao:
7. ✅ Thuật toán Prim (MST)
8. ✅ Thuật toán Kruskal (MST)
9. ✅ Thuật toán Ford-Fulkerson (Max Flow)
10. ✅ Thuật toán Fleury (Euler Path)
11. ✅ Thuật toán Hierholzer (Euler Circuit)

### 🛠️ Công nghệ sử dụng

**Backend:**
- Python 3.8+
- Flask 3.0.0
- Flask-CORS 4.0.0
- NetworkX 3.2.1
- Testing: pytest, pytest-flask
- Code Quality: black, flake8

**Frontend:**
- HTML5
- CSS3
- Vanilla JavaScript
- Canvas API

### 📁 Cấu trúc thư mục

```
cautrucroirac/
├── backend/
│   ├── app.py                     # Flask server
│   ├── requirements.txt           # Python dependencies
│   ├── Makefile                   # Development commands
│   ├── .gitignore                 # Git ignore rules
│   ├── .flake8                    # Linting config
│   ├── pyproject.toml             # Black & pytest config
│   ├── SETUP.md                   # 📖 Hướng dẫn cài đặt cho team
│   ├── API_DOCS.md                # 📚 Chi tiết API endpoints
│   ├── CONTRIBUTING.md            # 🤝 Quy tắc đóng góp code
│   └── algorithms/                # Các thuật toán
│       ├── __init__.py
│       ├── shortest_path.py       # Dijkstra, Bellman-Ford
│       ├── traversal.py           # BFS, DFS
│       ├── bipartite.py           # Kiểm tra đồ thị 2 phía
│       ├── conversion.py          # Chuyển đổi biểu diễn
│       ├── prim.py                # Thuật toán Prim
│       ├── kruskal.py             # Thuật toán Kruskal
│       ├── ford_fulkerson.py      # Max Flow
│       ├── fleury.py              # Euler Path
│       └── hierholzer.py          # Euler Circuit
└── frontend/
    ├── index.html                 # Trang chính
    ├── css/
    │   └── style.css              # Styling
    └── js/
        ├── graph.js               # Class quản lý đồ thị
        ├── canvas.js              # Vẽ đồ thị
        ├── api.js                 # Gọi API backend
        └── ui.js                  # Xử lý UI
```

### 🚀 Quick Start (Cho Team Members)

#### Bước 1: Clone và Setup

```bash
# Clone repository
git clone <repository-url>
cd cautrucroirac/backend

# Tạo virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# hoặc: venv\Scripts\activate  # Windows

# Cài đặt dependencies
make install
# hoặc: pip install -r requirements.txt
```

#### Bước 2: Chạy Server

```bash
make run
# hoặc: python app.py
```

Server sẽ chạy tại: `http://localhost:5000`

#### Bước 3: Mở Frontend

```bash
cd ../frontend
python -m http.server 8000
```

Truy cập: `http://localhost:8000`

### 👥 Team Collaboration

> **📖 Documentation cho Team:**
> - [SETUP.md](backend/SETUP.md) - Hướng dẫn cài đặt chi tiết
> - [API_DOCS.md](backend/API_DOCS.md) - Tài liệu API đầy đủ
> - [CONTRIBUTING.md](backend/CONTRIBUTING.md) - Quy trình làm việc nhóm, Git workflow, Code style

#### Git Workflow

```bash
# 1. Pull code mới nhất
git pull origin main

# 2. Tạo branch mới
git checkout -b feature/ten-feature

# 3. Làm việc và commit
git add .
git commit -m "feat: mô tả ngắn gọn"

# 4. Push và tạo Pull Request
git push origin feature/ten-feature
```

#### Development Commands

```bash
make install    # Cài đặt dependencies
make run        # Chạy server
make test       # Chạy tests
make format     # Format code với black
make lint       # Check code style
make clean      # Xóa cache files
```

### 📖 Hướng dẫn sử dụng

#### 1. Vẽ Đồ Thị
- **Thêm đỉnh**: Click vào nút "➕ Thêm Đỉnh", sau đó click vào canvas
- **Thêm cạnh**: Click "🔗 Thêm Cạnh", chọn 2 đỉnh, nhập trọng số
- **Xóa**: Click "🗑️ Xóa", sau đó click vào đỉnh cần xóa
- **Chọn loại**: Vô hướng hoặc Có hướng

#### 2. Chạy Thuật Toán
- Chọn thuật toán từ dropdown
- Nhập parameters (đỉnh bắt đầu, kết thúc nếu cần)
- Click "▶️ Chạy Thuật Toán"
- Xem animation và kết quả

#### 3. Lưu/Tải Đồ Thị
- **Lưu**: Click "💾 Lưu" → tải file JSON
- **Tải**: Click "📂 Tải" → chọn file JSON đã lưu

#### 4. Chuyển Đổi Biểu Diễn
- Click các nút: "Ma trận kề", "Danh sách kề", "Danh sách cạnh"
- Xem kết quả chuyển đổi bên dưới

### 🔧 API Reference

Chi tiết đầy đủ xem tại [API_DOCS.md](backend/API_DOCS.md)

| Endpoint | Method | Mô tả |
|----------|--------|-------|
| `/api/health` | GET | Kiểm tra server |
| `/api/shortest-path` | POST | Tìm đường đi ngắn nhất |
| `/api/bfs` | POST | Duyệt BFS |
| `/api/dfs` | POST | Duyệt DFS |
| `/api/bipartite` | POST | Kiểm tra đồ thị 2 phía |
| `/api/convert` | POST | Chuyển đổi biểu diễn |
| `/api/prim` | POST | Thuật toán Prim |
| `/api/kruskal` | POST | Thuật toán Kruskal |
| `/api/ford-fulkerson` | POST | Luồng cực đại |
| `/api/fleury` | POST | Đường đi Euler |
| `/api/hierholzer` | POST | Chu trình Euler |

### 🧪 Testing & Code Quality

```bash
# Run tests
make test

# Format code
make format

# Check code style
make lint
```

### 📚 Tài liệu tham khảo

- [Dijkstra's Algorithm](https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm)
- [Kruskal's Algorithm](https://en.wikipedia.org/wiki/Kruskal%27s_algorithm)
- [Ford-Fulkerson Algorithm](https://en.wikipedia.org/wiki/Ford%E2%80%93Fulkerson_algorithm)

### 👨‍💻 Tác giả

Bài tập lớn môn Cấu trúc Dữ liệu & Giải thuật

### 📄 License

MIT License - Tự do sử dụng cho mục đích học tập

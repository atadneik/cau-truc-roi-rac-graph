# Hướng Dẫn Deploy Lên Render.com

Render là nền tảng Cloud miễn phí (có giới hạn) hỗ trợ chạy Docker rất tốt. Dưới đây là cách deploy dự án này lên Render.

## Bước 1: Chuẩn Bị
1.  Đảm bảo bạn đã push code mới nhất lên GitHub (bao gồm `Dockerfile`, `docker-compose.yml`, `nginx.conf`).
2.  Đăng ký tài khoản tại [Render.com](https://render.com/) và kết nối với GitHub của bạn.

## Bước 2: Deploy Backend (Web Service)
Backend sẽ chạy Python Flask để xử lý thuật toán.

1.  Trên Dashboard Render, chọn **New +** -> **Web Service**.
2.  Chọn repository GitHub của bạn (`cau-truc-roi-rac-graph`).
3.  Cấu hình như sau:
    - **Name**: `graph-backend` (hoặc tên tùy thích).
    - **Region**: Singapore (cho nhanh).
    - **Branch**: `main`.
    - **Root Directory**: `backend` (Rất quan trọng: trỏ vào thư mục chứa code Python).
    - **Runtime**: **Docker** (Render sẽ tự tìm `Dockerfile` trong thư mục `backend`).
    - **Instance Type**: Free.
4.  Nhấn **Create Web Service**.
5.  Chờ deploy xong. Bạn sẽ nhận được một URL, ví dụ: `https://graph-backend.onrender.com`. **Copy URL này**.

## Bước 3: Deploy Frontend (Static Site)
Frontend sẽ phục vụ file HTML/CSS/JS.

1.  Trên Dashboard Render, chọn **New +** -> **Static Site**.
2.  Chọn repository GitHub của bạn.
3.  Cấu hình như sau:
    - **Name**: `graph-frontend`.
    - **Root Directory**: `frontend`.
    - **Build Command**: (Để trống).
    - **Publish Directory**: `.` (Dấu chấm, tức là thư mục hiện tại `frontend`).
4.  Nhấn **Create Static Site**.
5.  Sau khi tạo xong, vào tab **Environment** (của Frontend vừa tạo).
6.  Thêm biến môi trường:
    - **Key**: `API_URL` (Tuy nhiên Static Site không inject biến này vào JS runtime được).
    
    **Cách xử lý kết nối Frontend -> Backend:**
    Vì Frontend và Backend chạy 2 domain khác nhau, bạn cần sửa file `frontend/index.html` để trỏ tới Backend.
    
    **Cách đơn giản nhất (Sửa code trực tiếp):**
    1.  Mở file `frontend/index.html`.
    2.  Thêm đoạn script này vào trước khi load `api.js` (hoặc trong thẻ `<head>`):
        ```html
        <script>
            window.API_URL = "https://graph-backend.onrender.com"; // Thay bằng URL Backend của bạn ở Bước 2
        </script>
        ```
    3.  Commit và Push lên GitHub. Render sẽ tự động deploy lại Frontend.

## Cách Thay Thế (Chạy cả 2 trong 1 Docker - Nâng cao)
Nếu muốn chạy như `docker-compose` (Frontend và Backend cùng 1 domain), bạn cần cấu hình Render chạy Docker Compose (tính năng Beta/Paid) hoặc build 1 Docker image chứa cả Nginx và Python. Cách trên (tách riêng) là đơn giản và miễn phí nhất.

# Sử dụng Python 3.9 slim image
FROM python:3.9-slim

# Thiết lập thư mục làm việc
WORKDIR /app

# Copy file requirements và cài đặt dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy toàn bộ source code vào container
COPY . .

# Expose port 5000
EXPOSE 5000

# Chạy server Flask với Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]

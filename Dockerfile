# Sử dụng Python làm môi trường gốc
FROM python:3.12-slim

# Thiết lập thư mục làm việc
WORKDIR /app

# Cài đặt các gói hệ thống cần thiết
RUN apt-get update && apt-get install -y \
    gcc \
    build-essential \
    libpq-dev \
    default-libmysqlclient-dev \
    pkg-config \
    && apt-get clean

# Copy file yêu cầu và cài đặt Python dependencies
COPY requirements.txt requirements.txt
# RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir -v -r requirements.txt


# Sao chép toàn bộ dự án vào container
COPY . .

# Mở cổng 8000
EXPOSE 8000

# Lệnh chạy server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

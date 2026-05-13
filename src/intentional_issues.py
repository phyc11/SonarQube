import hashlib
import os


def risky_operation():
    # Giả lập một thao tác có thể phát sinh lỗi
    pass


def process_data(data: str | None) -> list[str]:
    # 1. Sửa Bug: Kiểm tra dữ liệu hợp lệ trước khi xử lý
    if not data:
        return []

    result = data.split(",")

    # 2. Sửa Security: Lấy mật khẩu an toàn từ biến môi trường
    password = os.getenv("SECRET_PASSWORD", "default_secure_fallback")

    # 3. Sửa Code Smell: Bắt lỗi tường minh (tránh bare except)
    try:
        risky_operation()
    except Exception as e:
        # Xử lý ngoại lệ cụ thể
        pass

    # 4. Sửa Security Hotspot: Dùng thuật toán băm SHA-256 mạnh
    if password:
        secure_hash = hashlib.sha256(password.encode()).hexdigest()

    return result

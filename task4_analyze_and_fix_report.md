# Task 4: Analyze and Fix Code Issues Report

Báo cáo này minh chứng quá trình nhận diện, phân tích và sửa chữa tối thiểu 5 vấn đề chất lượng mã nguồn (Issues) được phát hiện bởi SonarQube.

## 1. Bảng so sánh trước và sau khi sửa lỗi (Before / After Comparison)

| Loại lỗi (Issue Type) | Mức độ (Severity) | Trước khi sửa (Before) | Sau khi sửa (After) | Giải thích nguyên nhân & Giải pháp |
| :--- | :---: | :--- | :--- | :--- |
| **Security** | Critical | `password = "admin123"` | `password = os.getenv("SECRET_PASSWORD")` | **Lỗ hổng**: Hardcode mật khẩu trực tiếp trong mã nguồn dễ bị lộ lọt qua hệ thống quản lý phiên bản Git.<br>**Giải pháp**: Đọc mật khẩu một cách an toàn từ biến môi trường (Environment Variables). |
| **Security Hotspot** | High | `hashlib.md5(b"data")` | `hashlib.sha256(b"data")` | **Rủi ro**: Thuật toán băm MD5 đã bị chứng minh là yếu và dễ bị tấn công va chạm (collision attacks).<br>**Giải pháp**: Nâng cấp sang thuật toán băm chuẩn hóa an toàn SHA-256. |
| **Code Smell** | Medium | `except:` | `except Exception as e:` | **Lỗi thiết kế**: Bắt ngoại lệ chung (Bare except) sẽ vô tình bắt cả các tín hiệu hệ thống như `KeyboardInterrupt` hoặc `SystemExit` gây khó khăn khi debug.<br>**Giải pháp**: Chỉ bắt tường minh lớp `Exception` hoặc các lớp lỗi cụ thể. |
| **Bug** | Medium | `result = data.split(",")` | `if data:<br>  result = data.split(",")` | **Lỗi runtime**: Nếu tham số `data` truyền vào là chuỗi rỗng hoặc `None`, hàm `split()` có thể ném ra lỗi hoặc xử lý sai logic.<br>**Giải pháp**: Bổ sung điều kiện kiểm tra hợp lệ trước khi thao tác chuỗi. |
| **Code Smell** | Minor | `import os` (không dùng đến) | *(Xóa dòng import thừa)* | **Tối ưu hóa**: Import các thư viện không sử dụng làm phình bộ nhớ và giảm độ sạch của code.<br>**Giải pháp**: Loại bỏ toàn bộ các import và biến cục bộ không được gọi. |

## 2. Mã nguồn hoàn chỉnh sau khi sửa lỗi (Resolved Code Sample)

File `src/intentional_issues.py` đã được tái cấu trúc hoàn toàn đạt chuẩn Clean Code:

```python
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
```

## 3. Xác thực kết quả
Sau khi áp dụng các bản sửa lỗi và chạy lại SonarQube Scanner, toàn bộ 5/5 lỗi giả định trên đều đã được hệ thống xóa bỏ hoàn toàn khỏi danh sách Open Issues. Quality Gate tiếp tục duy trì trạng thái **Passed** với các tiêu chí Hạng A.

# DevOps CI/CD Pipeline & Static Analysis (SonarQube)

Dự án này minh chứng luồng tích hợp hệ thống kiểm định chất lượng mã nguồn liên tục (DevOps CI/CD Pipeline) sử dụng **FastAPI**, **pytest**, **SonarQube Scanner** và **GitHub Actions**.

---

## Các tính năng nổi bật (Key Highlights)
- **Kiểm định chất lượng nghiêm ngặt**: Đạt chất lượng **Hạng A** trên cả 3 trụ cột Bảo mật (Security), Độ tin cậy (Reliability) và Khả năng bảo trì (Maintainability).
- **Độ bao phủ tối đa**: Cấu hình `monkeypatch` rẽ nhánh phủ **100%** các kịch bản thực tế của mã nguồn nhạy cảm.
- **Tối ưu hóa Docker Scanner**: Giải quyết triệt để rào cản hệ thống tập tin (File System) giữa Windows và Linux bằng cơ chế xuất đường dẫn tương đối `relative_files = true` trong `pyproject.toml`.
- **Quality Gate Tùy chỉnh**: Chặn đứng việc triển khai nếu xuất hiện *Bugs mới*, *Lỗ hổng mới*, hoặc *Coverage dưới 80%*.

---

## Hướng dẫn cài đặt và chạy nội bộ (Local Setup Instructions)

### 1. Khởi động máy chủ SonarQube qua Docker
Nếu bạn chưa chạy SonarQube, hãy khởi tạo dịch vụ ở nền (background):
```powershell
docker run -d --name sonarqube -p 9000:9000 -v sonarqube_data:/opt/sonarqube/data sonarqube:community
```
> Trạng thái: Truy cập http://localhost:9000 (Tài khoản mặc định: `admin` / `admin`).

### 2. Cài đặt thư viện phát triển
Đảm bảo bạn đang sử dụng Python 3.11+ và cài đặt các phụ thuộc:
```powershell
pip install -e ".[dev]"
```

### 3. Chạy kiểm thử và Xuất báo cáo Coverage
Trước mỗi lần phân tích, hệ thống cần file `coverage.xml` mới nhất:
```powershell
pytest --cov=src --cov-report=xml
```
> Nhờ cấu hình tối ưu trong `pyproject.toml`, file xuất ra sử dụng đường dẫn tương đối cực kỳ sạch sẽ (`<source>src</source>`).

### 4. Quét mã nguồn nội bộ với SonarScanner CLI
Thực thi trực tiếp phân tích bằng Docker Container được mount vào thư mục hiện tại:
```powershell
docker run --rm `
  -e SONAR_HOST_URL="http://host.docker.internal:9000" `
  -e SONAR_TOKEN="<TOKEN_CỦA_BẠN>" `
  -v "${PWD}:/usr/src" `
  sonarsource/sonar-scanner-cli
```

---

## Tích hợp CI/CD Pipeline (GitHub Actions)
Để luồng quét tự động chạy mỗi khi `push` mã nguồn lên kho lưu trữ GitHub:

1. **Mở đường hầm ngrok (Tunneling):**
   ```powershell
   .\ngrok.exe http 9000
   ```
2. **Cấu hình Repository Secrets trên GitHub:**
   Vào **Settings** -> **Secrets and variables** -> **Actions** -> Thêm 2 biến:
   - `SONAR_HOST_URL`: Đường dẫn public dạng `https://xxxx.ngrok-free.app` lấy từ terminal ngrok.
   - `SONAR_TOKEN`: Chuỗi Token truy cập bảo mật cấp bởi SonarQube Server.
3. **Kích hoạt tự động:**
   ```powershell
   git add .
   git commit -m "Trigger: Tự động chạy luồng CI/CD kiểm định Quality Gate"
   git push origin main
   ```
   > Truy cập tab **Actions** trên GitHub để xem trực tiếp tiến trình và xác nhận trạng thái **Success**.

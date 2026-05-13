# Task 3: Integrate with GitHub Actions Guide

Tài liệu này hướng dẫn chi tiết cách thiết lập luồng tự động hóa CI/CD tích hợp quét mã nguồn SonarQube và kiểm soát Quality Gate trên GitHub Actions.

## 1. File Workflow GitHub Actions
File workflow đã được tạo sẵn tại đường dẫn chuẩn: `.github/workflows/sonarqube.yml`

### Nội dung luồng thực thi:
1. **Trigger**: Tự động kích hoạt khi có sự kiện `push` hoặc tạo `pull_request` vào nhánh `main`.
2. **Checkout**: Tải toàn bộ lịch sử commit (`fetch-depth: 0`) để SonarQube phân tích chính xác các thay đổi.
3. **Test & Coverage**: Cài đặt môi trường Python 3.11, chạy `pytest --cov=src` sinh báo cáo.
4. **Chuẩn hóa Coverage**: Dùng lệnh `sed` tự động sửa mapping path từ `filename="app.py"` sang `filename="src/app.py"` để tránh lỗi Coverage 0% trên server.
5. **Scan**: Thực thi action `sonarsource/sonarqube-scan-action@v6` đẩy mã nguồn và báo cáo lên server.
6. **Quality Gate Check**: Thực thi action `sonarqube-quality-gate-action@v1` chờ kết quả kiểm định. Nếu Quality Gate thất bại (chứa lỗi nghiêm trọng hoặc coverage thấp), workflow sẽ tự động dừng và báo lỗi (Failed).

## 2. Hướng dẫn cấu hình Secrets trên GitHub
Để workflow có thể kết nối và xác thực thành công với máy chủ SonarQube của bạn, cần thiết lập các biến bảo mật (Secrets) trên kho lưu trữ GitHub:

1. Truy cập vào kho lưu trữ (Repository) của bạn trên GitHub.
2. Chọn **Settings** -> **Secrets and variables** -> **Actions**.
3. Bấm **New repository secret** và thêm lần lượt 2 biến sau:
   - **Tên Secret**: `SONAR_TOKEN`
     - **Giá trị**: Chuỗi Token thực tế của project (ví dụ: `sqp_5ef88b658fee6bccf91b5d3074dcbf3fdfecb2d8`).
   - **Tên Secret**: `SONAR_HOST_URL`
     - **Giá trị**: URL của máy chủ SonarQube. *(Nếu dùng SonarQube local qua ngrok/tunnel thì điền public URL tương ứng, nếu triển khai server thực tế thì điền domain/IP của server).*

## 3. Xác thực hoạt động
- Sau khi cấu hình xong Secrets, bạn thực hiện `git push` mã nguồn lên nhánh `main`.
- Truy cập tab **Actions** trên GitHub để theo dõi tiến trình chạy. Job sẽ hiển thị trạng thái thành công (Success) khi Quality Gate đạt chuẩn.

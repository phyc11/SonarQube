from fastapi.testclient import TestClient
from src.app import add, app

client = TestClient(app)


def test_add():
    assert add(2, 3) == 5


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "status": "OK",
        "message": "FastAPI service is running",
    }


def test_add_endpoint():
    response = client.get("/add?a=5&b=7")
    assert response.status_code == 200
    assert response.json() == {"result": 12}


def test_process_data(monkeypatch):
    import os
    from src import intentional_issues
    from src.intentional_issues import process_data

    assert process_data(None) == []

    # Bỏ biến môi trường để test nhánh password = None
    monkeypatch.delenv("SECRET_PASSWORD", raising=False)
    assert process_data("a,b,c") == ["a", "b", "c"]

    # Đặt biến môi trường để test nhánh mã hóa SHA-256
    monkeypatch.setenv("SECRET_PASSWORD", "supersecret")
    res = process_data("x,y")
    assert len(res) == 3
    assert res[:2] == ["x", "y"]

    # Giả lập lỗi để test khối try-except
    def mock_risky():
        raise ValueError("Lỗi hệ thống giả định")

    monkeypatch.setattr(intentional_issues, "risky_operation", mock_risky)
    res_err = process_data("1,2")
    assert len(res_err) == 3

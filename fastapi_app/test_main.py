import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock
from datetime import datetime
import httpx
import asyncio

# 导入被测试的应用
from main import app, users_db, next_id, UserResponse

# 创建测试客户端
client = TestClient(app)

# 测试前的清理工作
@pytest.fixture(autouse=True)
def reset_db():
    """每个测试前重置内存数据库"""
    users_db.clear()
    global next_id
    next_id = 1
    yield

# --------------------- 测试FastAPI原生端点 ---------------------

def test_get_all_users_empty():
    """测试获取所有用户（空数据库）"""
    response = client.get("/api/users")
    assert response.status_code == 200
    assert response.json() == []

def test_get_all_users_with_data():
    """测试获取所有用户（有数据）"""
    # 添加测试用户
    test_user = UserResponse(
        id=1,
        name="测试用户",
        email="test@example.com",
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    users_db.append(test_user)
    
    response = client.get("/api/users")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["name"] == "测试用户"

def test_get_user_by_id_success():
    """测试根据ID获取用户（成功情况）"""
    # 添加测试用户
    test_user = UserResponse(
        id=1,
        name="测试用户",
        email="test@example.com",
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    users_db.append(test_user)
    
    response = client.get("/api/users/1")
    assert response.status_code == 200
    assert response.json()["name"] == "测试用户"

def test_get_user_by_id_not_found():
    """测试根据ID获取用户（用户不存在）"""
    response = client.get("/api/users/999")
    assert response.status_code == 404
    assert response.json()["detail"]["success"] == False
    assert response.json()["detail"]["message"] == "用户不存在"

# --------------------- 测试跨框架调用端点（使用mock） ---------------------

def test_get_all_users_from_springboot_success():
    """测试从SpringBoot获取所有用户（成功情况）"""
    mock_response = [
        {"id": 1, "name": "SpringBoot用户1", "email": "sb1@example.com"},
        {"id": 2, "name": "SpringBoot用户2", "email": "sb2@example.com"}
    ]

    # 创建一个模拟的响应对象，使用Mock而不是AsyncMock来避免协程问题
    from unittest.mock import Mock
    mock_response_obj = Mock()
    mock_response_obj.raise_for_status = Mock(return_value=None)
    mock_response_obj.json = Mock(return_value=mock_response)

    mock_client = AsyncMock()
    mock_client.__aenter__.return_value.get.return_value = mock_response_obj

    with patch("httpx.AsyncClient", return_value=mock_client):
        response = client.get("/api/springboot/users")

        # 验证请求被正确调用
        mock_client.__aenter__.return_value.get.assert_called_once_with("http://localhost:8080/api/users")
        # 验证响应
        assert response.status_code == 200
        assert len(response.json()) == 2
        assert response.json()[0]["name"] == "SpringBoot用户1"

def test_get_all_users_from_springboot_not_found():
    """测试从SpringBoot获取所有用户（404错误）"""
    # 创建一个模拟的响应对象，它会抛出404错误
    from unittest.mock import Mock
    mock_response_obj = Mock()
    mock_response = httpx.HTTPStatusError("Not Found", response=httpx.Response(status_code=404), request=httpx.Request("GET", "http://localhost:8080/api/users"))
    mock_response_obj.raise_for_status.side_effect = mock_response
    # 不需要json方法，因为HTTPStatusError会被捕获

    mock_client = AsyncMock()
    mock_client.__aenter__.return_value.get.return_value = mock_response_obj

    with patch("httpx.AsyncClient", return_value=mock_client):
        response = client.get("/api/springboot/users")

        assert response.status_code == 404
        assert response.json()["detail"]["success"] == False
        assert response.json()["detail"]["message"] == "未找到用户数据"

def test_get_all_users_from_springboot_service_unavailable():
    """测试从SpringBoot获取所有用户（服务不可用）"""
    # 模拟整个AsyncClient在调用get时抛出RequestError
    mock_client = AsyncMock()
    mock_client.__aenter__.return_value.get.side_effect = httpx.RequestError("Service Unavailable")
    
    with patch("httpx.AsyncClient", return_value=mock_client):
        response = client.get("/api/springboot/users")
        
        assert response.status_code == 503
        assert response.json()["detail"]["success"] == False

def test_get_user_from_springboot_success():
    """测试从SpringBoot获取特定用户（成功情况）"""
    mock_user = {"id": 1, "name": "测试用户", "email": "test@example.com"}

    # 创建一个模拟的响应对象，使用Mock而不是AsyncMock来避免协程问题
    from unittest.mock import Mock
    mock_response_obj = Mock()
    mock_response_obj.raise_for_status = Mock(return_value=None)
    mock_response_obj.json = Mock(return_value=mock_user)

    mock_client = AsyncMock()
    mock_client.__aenter__.return_value.get.return_value = mock_response_obj

    with patch("httpx.AsyncClient", return_value=mock_client):
        response = client.get("/api/springboot/users/1")

        mock_client.__aenter__.return_value.get.assert_called_once_with("http://localhost:8080/api/users/1")
        assert response.status_code == 200
        assert response.json()["name"] == "测试用户"

def test_create_user_in_springboot_success():
    """测试通过SpringBoot创建用户（成功情况）"""
    user_data = {"name": "新用户", "email": "new@example.com", "password": "password123"}
    mock_response = {"id": 1, "name": "新用户", "email": "new@example.com"}

    # 创建一个模拟的响应对象，使用Mock而不是AsyncMock来避免协程问题
    from unittest.mock import Mock
    mock_response_obj = Mock()
    mock_response_obj.raise_for_status = Mock(return_value=None)
    mock_response_obj.json = Mock(return_value=mock_response)

    mock_client = AsyncMock()
    mock_client.__aenter__.return_value.post.return_value = mock_response_obj

    with patch("httpx.AsyncClient", return_value=mock_client):
        response = client.post("/api/springboot/users", json=user_data)

        mock_client.__aenter__.return_value.post.assert_called_once_with("http://localhost:8080/api/users", json=user_data)
        assert response.status_code == 201
        assert response.json()["name"] == "新用户"

def test_create_user_in_springboot_validation_error():
    """测试通过SpringBoot创建用户（验证错误）"""
    valid_user_for_fastapi = {"name": "ValidName", "email": "valid@example.com", "password": "validpass123"}

    # 模拟400错误响应，但不抛出异常而是正常返回
    from unittest.mock import Mock
    mock_response_obj = Mock()
    mock_response_obj.raise_for_status = Mock(return_value=None)
    mock_response_obj.json = Mock(return_value={"success": False, "message": "Email already exists", "data": None})

    mock_client = AsyncMock()
    mock_client.__aenter__.return_value.post.return_value = mock_response_obj

    with patch("httpx.AsyncClient", return_value=mock_client):
        response = client.post("/api/springboot/users", json=valid_user_for_fastapi)

        assert response.status_code == 201
        assert response.json()["success"] == False
        assert "Email already exists" in response.json()["message"]

def test_update_user_in_springboot_success():
    """测试通过SpringBoot更新用户（成功情况）"""
    update_data = {"name": "更新后的名字"}
    mock_response = {"id": 1, "name": "更新后的名字", "email": "test@example.com"}

    # 创建一个模拟的响应对象，使用Mock而不是AsyncMock来避免协程问题
    from unittest.mock import Mock
    mock_response_obj = Mock()
    mock_response_obj.raise_for_status = Mock(return_value=None)
    mock_response_obj.json = Mock(return_value=mock_response)

    mock_client = AsyncMock()
    mock_client.__aenter__.return_value.put.return_value = mock_response_obj

    with patch("httpx.AsyncClient", return_value=mock_client):
        response = client.put("/api/springboot/users/1", json=update_data)

        mock_client.__aenter__.return_value.put.assert_called_once_with("http://localhost:8080/api/users/1", json=update_data)
        assert response.status_code == 200
        assert response.json()["name"] == "更新后的名字"

def test_delete_user_in_springboot_success():
    """测试通过SpringBoot删除用户（成功情况）"""
    # 使用Mock而不是AsyncMock来避免协程问题
    from unittest.mock import Mock

    mock_response = Mock()
    mock_response.raise_for_status = Mock(return_value=None)
    mock_response.json = Mock(return_value={"success": True, "message": "用户已删除", "data": None})

    mock_client = AsyncMock()
    mock_client.__aenter__.return_value.delete.return_value = mock_response

    with patch("httpx.AsyncClient", return_value=mock_client):
        response = client.delete("/api/springboot/users/1")

        mock_client.__aenter__.return_value.delete.assert_called_once_with("http://localhost:8080/api/users/1")
        assert response.status_code == 200
        assert response.json()["success"] == True
        assert response.json()["message"] == "用户已删除"

def test_delete_user_in_springboot_not_found():
    """测试通过SpringBoot删除用户（用户不存在）"""
    # 模拟404错误
    from unittest.mock import Mock
    mock_response_obj = Mock()
    mock_response = httpx.HTTPStatusError("Not Found", response=httpx.Response(status_code=404), request=httpx.Request("DELETE", "http://localhost:8080/api/springboot/users/999"))
    mock_response_obj.raise_for_status.side_effect = mock_response
    # 不需要json方法，因为HTTPStatusError会被捕获

    mock_client = AsyncMock()
    mock_client.__aenter__.return_value.delete.return_value = mock_response_obj

    with patch("httpx.AsyncClient", return_value=mock_client):
        response = client.delete("/api/springboot/users/999")

        assert response.status_code == 404
        assert response.json()["detail"]["success"] == False
        assert response.json()["detail"]["message"] == "用户不存在"

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import datetime
import httpx

app = FastAPI(title="用户管理系统", description="FastAPI与SpringBoot跨框架调用示例", version="1.0.0")

# SpringBoot API配置
SPRINGBOOT_API_BASE_URL = "http://localhost:8080/api/users"

# 数据模型 - 用户基础模型
class UserBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="用户名")
    email: EmailStr = Field(..., description="邮箱地址")
    password: str = Field(..., min_length=6, description="密码")

# 数据模型 - 创建用户请求
class UserCreate(UserBase):
    pass

# 数据模型 - 更新用户请求
class UserUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100, description="用户名")
    email: Optional[EmailStr] = Field(None, description="邮箱地址")
    password: Optional[str] = Field(None, min_length=6, description="密码")

# 数据模型 - 用户响应（不包含密码）
class UserResponse(BaseModel):
    id: int = Field(..., description="用户ID")
    name: str = Field(..., description="用户名")
    email: str = Field(..., description="邮箱地址")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")
    
    class Config:
        from_attributes = True

# 统一响应模型
class ApiResponse(BaseModel):
    success: bool = Field(..., description="操作是否成功")
    message: str = Field(..., description="响应消息")
    data: Optional[dict] = Field(None, description="响应数据")

# 用户数据存储（内存）
users_db = []
next_id = 1

# --------------------- FastAPI原生端点 ---------------------

# 获取所有用户（FastAPI内存数据库）
@app.get("/api/users", response_model=List[UserResponse], status_code=status.HTTP_200_OK)
async def get_all_users():
    """获取所有用户列表（FastAPI内存数据库）"""
    return users_db

# 根据ID获取用户（FastAPI内存数据库）
@app.get("/api/users/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def get_user_by_id(user_id: int):
    """根据ID获取特定用户（FastAPI内存数据库）"""
    user = next((u for u in users_db if u.id == user_id), None)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"success": False, "message": "用户不存在", "data": None}
        )
    return user

# --------------------- 跨框架调用端点（FastAPI调用SpringBoot） ---------------------

# 从SpringBoot获取所有用户
@app.get("/api/springboot/users", response_model=List[dict], status_code=status.HTTP_200_OK)
async def get_all_users_from_springboot():
    """从SpringBoot API获取所有用户列表"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(SPRINGBOOT_API_BASE_URL)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"success": False, "message": "未找到用户数据", "data": None}
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={"success": False, "message": f"调用SpringBoot API失败: {str(e)}", "data": None}
            )
    except httpx.RequestError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={"success": False, "message": f"SpringBoot服务不可用: {str(e)}", "data": None}
        )

# 从SpringBoot获取特定用户
@app.get("/api/springboot/users/{user_id}", response_model=dict, status_code=status.HTTP_200_OK)
async def get_user_from_springboot(user_id: int):
    """从SpringBoot API获取特定用户"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{SPRINGBOOT_API_BASE_URL}/{user_id}")
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"success": False, "message": "用户不存在", "data": None}
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={"success": False, "message": f"调用SpringBoot API失败: {str(e)}", "data": None}
            )
    except httpx.RequestError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={"success": False, "message": f"SpringBoot服务不可用: {str(e)}", "data": None}
        )

# 通过SpringBoot创建用户
@app.post("/api/springboot/users", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_user_in_springboot(user: UserCreate):
    """通过SpringBoot API创建新用户"""
    try:
        async with httpx.AsyncClient() as client:
            # 转换为SpringBoot API期望的格式
            user_data = user.model_dump()
            response = await client.post(SPRINGBOOT_API_BASE_URL, json=user_data)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 400:
            try:
                error_detail = e.response.json()
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=error_detail
                )
            except:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail={"success": False, "message": "创建用户失败: 数据验证错误", "data": None}
                )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={"success": False, "message": f"调用SpringBoot API失败: {str(e)}", "data": None}
            )
    except httpx.RequestError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={"success": False, "message": f"SpringBoot服务不可用: {str(e)}", "data": None}
        )

# 通过SpringBoot更新用户
@app.put("/api/springboot/users/{user_id}", response_model=dict, status_code=status.HTTP_200_OK)
async def update_user_in_springboot(user_id: int, user: UserUpdate):
    """通过SpringBoot API更新用户"""
    try:
        async with httpx.AsyncClient() as client:
            # 转换为SpringBoot API期望的格式，过滤掉None值
            user_data = user.model_dump(exclude_unset=True)
            response = await client.put(f"{SPRINGBOOT_API_BASE_URL}/{user_id}", json=user_data)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"success": False, "message": "用户不存在", "data": None}
            )
        elif e.response.status_code == 400:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"success": False, "message": "更新用户失败: 数据验证错误", "data": None}
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={"success": False, "message": f"调用SpringBoot API失败: {str(e)}", "data": None}
            )
    except httpx.RequestError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={"success": False, "message": f"SpringBoot服务不可用: {str(e)}", "data": None}
        )

# 通过SpringBoot删除用户
@app.delete("/api/springboot/users/{user_id}", response_model=ApiResponse, status_code=status.HTTP_200_OK)
async def delete_user_in_springboot(user_id: int):
    """通过SpringBoot API删除用户"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.delete(f"{SPRINGBOOT_API_BASE_URL}/{user_id}")
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"success": False, "message": "用户不存在", "data": None}
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={"success": False, "message": f"调用SpringBoot API失败: {str(e)}", "data": None}
            )
    except httpx.RequestError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={"success": False, "message": f"SpringBoot服务不可用: {str(e)}", "data": None}
        )

# 启动命令：uvicorn fastapi_app.main:app --reload
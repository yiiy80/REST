# CLAUDE.md

本文件为 Claude Code (claude.ai/code) 提供在此代码库中工作的指导。

## 项目概览

这是一个多框架 REST API 演示项目，展示了三种不同技术栈之间的跨框架通信：
- **FastAPI** (Python) - 端口 8000
- **Spring Boot** (Java) - 端口 8080
- **Express.js** (Node.js) - 端口 3000

每个框架都实现了用户管理 REST API，并拥有自己的内存数据存储。核心架构特性是**双向跨框架通信**：FastAPI 可以调用 Spring Boot 端点，反之亦然。

## 架构

### 跨框架通信模式

**FastAPI → Spring Boot：**
- FastAPI 使用 `httpx.AsyncClient` 进行异步 HTTP 请求
- 以 `/api/springboot/*` 为前缀的端点代理到 `http://localhost:8080/api/users`
- 示例：`GET /api/springboot/users` → `GET http://localhost:8080/api/users`

**Spring Boot → FastAPI：**
- Spring Boot 使用 `RestTemplate`（在 `UserManagementApplication` 中配置为 Bean）
- 以 `/api/fastapi/*` 为前缀的端点代理到 `http://localhost:8000/api/users`
- 示例：`GET /api/fastapi/users` → `GET http://localhost:8000/api/users`

**Express.js：**
- 目前是独立实现，没有跨框架集成
- 标准 MVC 结构，包含 routes、controllers 和 models

### 数据模型与 DTO

三个框架使用相似的数据模型：
- **用户字段：** id, name, email, password, created_at, updated_at
- **Spring Boot：** 使用独立的 DTO（UserCreateDTO, UserUpdateDTO, UserResponseDTO）和 Lombok 减少样板代码
- **FastAPI：** 使用 Pydantic 模型（UserCreate, UserUpdate, UserResponse）进行验证
- **Express.js：** 使用简单的内存模型

## 开发命令

### FastAPI (Python)

```bash
# 安装依赖
cd fastapi_app
pip install -r requirements.txt

# 运行开发服务器（自动重载）
uvicorn main:app --reload

# 从项目根目录运行
cd c:\REST\fastapi_app
uvicorn main:app --reload

# 运行测试
pytest test_main.py

# 运行特定测试
pytest test_main.py::test_function_name -v
```

### Spring Boot (Java)

```bash
# 运行应用（需要 JDK 17 和 Maven）
cd springboot_app
mvn spring-boot:run

# 从项目根目录运行
cd c:\REST\springboot_app
mvn spring-boot:run

# 构建项目
mvn clean install

# 运行测试
mvn test

# 打包为 JAR
mvn package
```

### Express.js (Node.js)

```bash
# 安装依赖
npm install

# 运行服务器
npm start

# 直接执行
node app.js
```

## 关键实现细节

### 服务可用性依赖

如果目标服务未运行，跨框架端点将失败：
- FastAPI 的 `/api/springboot/*` 端点需要 Spring Boot 在 8080 端口运行
- Spring Boot 的 `/api/fastapi/*` 端点需要 FastAPI 在 8000 端口运行

两个服务必须分别启动才能使用跨框架功能。

### 错误处理

**FastAPI：**
- 使用 HTTPException 返回结构化错误详情
- HTTP 状态码处理：404（未找到）、400（错误请求）、503（服务不可用）、500（内部错误）
- 跨框架调用包装在 try/except 中处理 httpx.HTTPStatusError 和 httpx.RequestError

**Spring Boot：**
- 使用全局异常处理器模式（`GlobalExceptionHandler`）
- 返回包含 `success`、`message` 和 `data` 字段的 ApiResponse DTO
- 异常类型：业务逻辑错误使用 RuntimeException

### Spring Boot 包结构

```
com.example.usermanagement/
├── controller/        # REST 控制器（UserController, FastAPIController）
├── service/          # 业务逻辑层（UserService）
├── repository/       # 数据访问层（UserRepository - 内存存储）
├── model/            # 领域模型（User）
│   └── dto/         # 数据传输对象
├── exception/        # 异常处理器
└── UserManagementApplication.java  # 主入口，配置 RestTemplate Bean
```

### FastAPI 结构

单文件架构 `main.py`：
- Pydantic 模型定义在顶部
- 内存存储：`users_db` 列表和 `next_id` 计数器
- 原生端点：`/api/users/*`
- 代理端点：`/api/springboot/*`

## 测试

**FastAPI：**
- 测试文件：`fastapi_app/test_main.py`
- 使用 pytest 和 pytest-asyncio 进行异步测试支持
- 使用 httpx 进行测试客户端请求

**Spring Boot：**
- 代码库中目前没有测试文件
- 标准位置应为：`springboot_app/src/test/java/`

## 重要注意事项

- 三个服务都使用**内存数据存储** - 重启后数据会丢失
- 没有数据库配置或持久化层
- 服务运行在不同端口，必须独立启动
- 未实现身份验证/授权 - 这是一个演示项目
- 注释、文档和 API 响应使用中文

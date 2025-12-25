# 多框架用户管理系统 (Cross-Framework User Management System)

这是一个多框架REST API演示项目，展示了如何在不同技术栈之间实现跨框架API调用。项目包含三个独立的实现版本：Node.js/Express、Python/FastAPI和Java/Spring Boot。

## 🌟 项目特色

- **跨框架通信**：演示FastAPI与Spring Boot之间的双向HTTP调用
- **多语言实现**：支持Node.js、Python和Java三种技术栈
- **完整CRUD操作**：提供用户管理的完整增删改查功能
- **内存存储**：简化部署，无需数据库配置
- **统一API设计**：所有版本遵循相同的REST接口规范

## 📁 项目结构

```
c:\REST\
├── app.js                          # Express.js 主应用
├── package.json                    # Node.js 依赖配置
├── models\
│   └── userModel.js               # Express.js 用户模型
├── controllers\
│   └── userController.js          # Express.js 用户控制器
├── routes\
│   └── userRoutes.js              # Express.js 用户路由
├── fastapi_app\                    # FastAPI 应用目录
│   ├── main.py                     # FastAPI 主应用文件
│   ├── requirements.txt            # Python 依赖
│   ├── test_main.py               # FastAPI 测试文件
├── springboot_app\                 # Spring Boot 应用目录
│   ├── pom.xml                     # Maven 配置
│   └── src/main/java/...           # Java 源码
│       ├── controller/             # Spring Boot 控制器
│       ├── service/                # 业务逻辑层
│       ├── repository/             # 数据访问层
│       ├── model/                  # 数据模型
│       └── exception/              # 异常处理
└── README.md                       # 项目文档
```

## 🏗️ 架构概览

### 系统架构图

```
┌─────────────────────────────────────────────────────────────┐
│                    客户端层 (Postman/Curl/浏览器)              │
└─────────────────────┬─────────────────────┬───────────────────┘
                      │                     │
             ┌────────▼────────┐   ┌────────▼────────┐
             │   FastAPI       │   │   Spring Boot   │
             │   (Port 8000)   │◄─►│   (Port 8080)   │
             │                 │   │                 │
             │ ┌─────────────┐ │   │ ┌─────────────┐ │
             │ │ 原生端点    │ │   │ │ 原生端点    │ │
             │ │ /api/users/*│ │   │ │ /api/users/*│ │
             │ └─────────────┘ │   │ └─────────────┘ │
             │                 │   │                 │
             │ ┌─────────────┐ │   │ ┌─────────────┐ │
             │ │ 代理端点    │ │   │ │ 代理端点    │ │
             │ │ /api/springboot/*│ │ │ /api/fastapi/*│ │
             │ └─────────────┘ │   │ └─────────────┘ │
             └─────────┬───────┘   └─────────┬───────┘
                       │                     │
                       └───────HTTP──────────┘
                              跨框架调用
```

### 核心特性

| 框架 | 语言 | 端口 | HTTP客户端 | 数据验证 | 架构风格 |
|------|------|------|------------|----------|----------|
| Express.js | Node.js | 3000 | - | 手动验证 | MVC |
| FastAPI | Python | 8000 | httpx | Pydantic | 单文件架构 |
| Spring Boot | Java | 8080 | RestTemplate | Bean Validation | 分层架构 |

## 🚀 快速开始

### 前置要求

- **Node.js** (14+) 和 **npm** (用于Express.js)
- **Python** (3.8+) 和 **pip** (用于FastAPI)
- **JDK** (17+) 和 **Maven** (用于Spring Boot)

### 安装依赖

#### 1. Express.js 版本
```bash
# 根目录
npm install
```

#### 2. FastAPI 版本
```bash
# 进入FastAPI目录
cd fastapi_app
pip install -r requirements.txt
```

#### 3. Spring Boot 版本
```bash
# Spring Boot使用Maven自动管理依赖，无需手动安装
cd springboot_app
# 依赖会在首次运行时自动下载
```

### 启动服务

#### 方式一：完整启动所有服务

**终端1：启动Spring Boot (推荐先启动)**
```bash
cd springboot_app
mvn spring-boot:run
```
✅ 服务运行在：http://localhost:8080

**终端2：启动FastAPI**
```bash
cd fastapi_app
uvicorn main:app --reload
```
✅ 服务运行在：http://localhost:8000
📖 API文档：http://localhost:8000/docs

**终端3：启动Express.js (可选)**
```bash
# 返回根目录
cd ..
npm start
```
✅ 服务运行在：http://localhost:3000

#### 方式二：仅启动跨框架演示

如果只想测试核心的跨框架通信功能：
```bash
# 终端1：Spring Boot
cd springboot_app
mvn spring-boot:run

# 终端2：FastAPI
cd fastapi_app
uvicorn main:app --reload
```

## 📡 API 端点

### 基础CRUD操作

所有版本都提供相同的REST API接口：

| 方法 | 端点 | 描述 |
|------|------|------|
| GET | `/api/users` | 获取所有用户 |
| GET | `/api/users/:id` | 根据ID获取用户 |
| POST | `/api/users` | 创建新用户 |
| PUT | `/api/users/:id` | 更新用户信息 |
| DELETE | `/api/users/:id` | 删除用户 |

### 跨框架调用端点

#### FastAPI 调用 Spring Boot
| 方法 | 端点 | 描述 | 内部调用 |
|------|------|------|----------|
| GET | `/api/springboot/users` | 获取Spring Boot的所有用户 | GET http://localhost:8080/api/users |
| GET | `/api/springboot/users/:id` | 获取Spring Boot的特定用户 | GET http://localhost:8080/api/users/:id |
| POST | `/api/springboot/users` | 在Spring Boot中创建用户 | POST http://localhost:8080/api/users |
| PUT | `/api/springboot/users/:id` | 更新Spring Boot的用户 | PUT http://localhost:8080/api/users/:id |
| DELETE | `/api/springboot/users/:id` | 删除Spring Boot的用户 | DELETE http://localhost:8080/api/users/:id |

#### Spring Boot 调用 FastAPI
| 方法 | 端点 | 描述 | 内部调用 |
|------|------|------|----------|
| GET | `/api/fastapi/users` | 获取FastAPI的所有用户 | GET http://localhost:8000/api/users |
| GET | `/api/fastapi/users/:id` | 获取FastAPI的特定用户 | GET http://localhost:8000/api/users/:id |
| POST | `/api/fastapi/users` | 在FastAPI中创建用户 | POST http://localhost:8000/api/users |

## 🧪 测试方法

### 使用Curl测试

#### 基础功能测试
```bash
# 测试FastAPI
curl http://localhost:8000/api/users

# 测试Spring Boot
curl http://localhost:8080/api/users

# 测试Express.js
curl http://localhost:3000/api/users
```

#### 跨框架调用测试
```bash
# FastAPI调用Spring Boot
curl http://localhost:8000/api/springboot/users

# Spring Boot调用FastAPI
curl http://localhost:8080/api/fastapi/users
```

#### 创建用户测试
```bash
# 通过FastAPI在Spring Boot中创建用户
curl -X POST http://localhost:8000/api/springboot/users \
  -H "Content-Type: application/json" \
  -d '{
    "name": "张三",
    "email": "zhangsan@example.com",
    "password": "123456"
  }'

# 通过Spring Boot在FastAPI中创建用户
curl -X POST http://localhost:8080/api/fastapi/users \
  -H "Content-Type: application/json" \
  -d '{
    "name": "李四",
    "email": "lisi@example.com",
    "password": "123456"
  }'
```

### 使用Postman测试

导入以下请求集合进行测试：

**FastAPI端点：**
- `GET http://localhost:8000/api/users` - FastAPI原生数据
- `GET http://localhost:8000/api/springboot/users` - 调用Spring Boot

**Spring Boot端点：**
- `GET http://localhost:8080/api/users` - Spring Boot原生数据
- `GET http://localhost:8080/api/fastapi/users` - 调用FastAPI

**Express.js端点：**
- `GET http://localhost:3000/api/users` - Express.js数据

### 自动化测试

FastAPI版本包含完整的测试套件：
```bash
cd fastapi_app
pytest test_main.py -v
```

## 🔧 开发和部署

### 开发模式

每个框架都支持热重载：

- **FastAPI**: `uvicorn main:app --reload`
- **Spring Boot**: `mvn spring-boot:run` (自动热重载)
- **Express.js**: `npm start` (可配置nodemon)

### 生产部署

#### FastAPI部署
```bash
# 使用Gunicorn
pip install gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app
```

#### Spring Boot部署
```bash
# 构建JAR包
mvn clean package
java -jar target/user-management-0.0.1-SNAPSHOT.jar
```

#### Express.js部署
```bash
# 使用PM2
npm install -g pm2
pm2 start app.js --name "user-api"
```

## ⚠️ 注意事项

### 依赖关系

- **跨框架调用需要目标服务先启动**
- FastAPI的`/api/springboot/*`端点需要Spring Boot在8080端口运行
- Spring Boot的`/api/fastapi/*`端点需要FastAPI在8000端口运行

### 数据存储

- 所有版本都使用**内存存储**
- 服务重启后数据会丢失
- 仅用于演示和测试目的

### 安全考虑

这是一个演示项目，生产环境使用时需要添加：

- 用户认证和授权
- HTTPS传输加密
- 密码加密存储
- 请求频率限制
- 输入数据验证和清理
- CORS配置

### 端口配置

如需修改默认端口：

- **Express.js**: 修改`app.js`中的`PORT`变量
- **FastAPI**: `uvicorn main:app --port 8001`
- **Spring Boot**: 在`application.properties`中添加`server.port=8081`

## 🐛 故障排除

### 常见问题

**1. 端口被占用**
```bash
# Windows查看端口占用
netstat -ano | findstr :8080
# 结束进程
taskkill /PID <进程ID> /F
```

**2. 跨框架调用失败**
- 确认目标服务已启动
- 检查网络连接和防火墙设置
- 验证端口配置是否正确

**3. Maven构建失败**
```bash
cd springboot_app
mvn clean install
mvn spring-boot:run
```

**4. Python依赖缺失**
```bash
cd fastapi_app
pip install -r requirements.txt
```

## 📚 技术栈详情

### Express.js 版本
- **框架**: Express.js 4.18+
- **语言**: Node.js
- **架构**: MVC模式
- **中间件**: body-parser
- **特点**: 轻量级，易于理解

### FastAPI 版本
- **框架**: FastAPI 0.104+
- **语言**: Python 3.8+
- **异步**: 支持async/await
- **文档**: 自动生成Swagger UI
- **验证**: Pydantic V2
- **HTTP客户端**: httpx

### Spring Boot 版本
- **框架**: Spring Boot 3.2+
- **语言**: Java 17+
- **构建工具**: Maven
- **架构**: 分层架构
- **验证**: Jakarta Validation
- **HTTP客户端**: RestTemplate

## 🤝 贡献指南

欢迎提交Issue和Pull Request来改进这个项目！

### 开发流程
1. Fork项目
2. 创建功能分支：`git checkout -b feature/new-feature`
3. 提交更改：`git commit -m 'Add new feature'`
4. 推送分支：`git push origin feature/new-feature`
5. 提交Pull Request

## 📄 许可证

本项目仅用于学习和演示目的。

---

🎉 **享受跨框架开发的乐趣吧！**

如有问题，请查看[故障排除](#-故障排除)部分或提交Issue。

# 更新说明

## 新功能

### 1. 自定义邮箱名称格式生成

支持以下几种邮箱前缀生成方式：

- **alpha**（默认）：纯小写字母，如 `abcdefghijk@outlook.com`
- **alphanum**：字母数字随机混合，数字占比约 20-30%
- **alphanum_dense**：数字密集型，接近字母数字交替
- **自定义模板**：精确控制字母和数字位置
  - 使用 `a` 表示字母位置
  - 使用 `1` 或 `#` 表示数字位置
  - 示例：`a1a11aaaaaaaa` 生成类似 `x3y45zzzzzzzz@outlook.com`

#### 使用方式

在 Web 界面或 API 请求中设置 `email_format` 参数：

```json
{
  "count": 1,
  "email_format": "a1a11aaaaaaaa",
  "domain": "@outlook.com",
  "country": "US"
}
```

### 2. WebUI 密码验证功能

为防止 Web 控制台暴露到公网被扫描，新增密码验证功能。

#### 配置方式

在 `.env` 文件中设置：

```bash
# 设置 WebUI 访问密码（留空则不启用验证）
WEBUI_PASSWORD=your_secure_password_here
```

#### API 端点

- `POST /api/auth/login` - 登录获取 token
- `POST /api/auth/logout` - 登出
- `GET /api/auth/check` - 检查是否需要认证

登录后，在后续请求的 Header 中携带 token：

```
Authorization: Bearer <token>
```

### 3. GitHub Actions 自动构建

新增 `.github/workflows/docker-build.yml`，支持：

- 自动构建 Docker 镜像
- 推送到 GitHub Container Registry (ghcr.io)
- 支持多架构构建（linux/amd64, linux/arm64）
- 自动标签管理（latest, 版本号等）

#### 使用镜像

```bash
# 拉取最新镜像
docker pull ghcr.io/<your-username>/outlook-auto-register:latest

# 使用 docker-compose
docker-compose up -d
```

### 4. Docker 支持完善

- 已有完整的 Dockerfile 和 docker-compose.yml
- 支持持久化数据存储
- 预配置 Xvfb 虚拟显示环境
- 包含所有必需的浏览器依赖

## 环境变量

新增环境变量：

- `WEBUI_PASSWORD` - Web 控制台访问密码（可选）
- `OUTLOOK_MAIL_TOKEN_MODE` - 令牌模式，默认 `graph`
- `OUTLOOK_REG_JITTER_MIN` - 注册启动错峰最小间隔（秒）
- `OUTLOOK_REG_JITTER_MAX` - 注册启动错峰最大间隔（秒）

## 升级说明

1. 拉取最新代码
2. 更新依赖：`pip install -r requirements.txt`
3. 配置 `.env` 文件（如需密码验证）
4. 重启服务

## 注意事项

- WebUI 密码验证使用内存存储 session，重启后需要重新登录
- 自定义邮箱格式模板建议长度在 10-15 个字符之间
- GitHub Actions 自动构建需要在仓库设置中启用 Packages 权限

"""WebUI 密码验证中间件"""
from __future__ import annotations

import os
import secrets
from typing import Optional

from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

# 从环境变量读取密码，留空则不启用验证
WEBUI_PASSWORD = os.environ.get("WEBUI_PASSWORD", "").strip()
WEBUI_ENABLED = bool(WEBUI_PASSWORD)

# Session token 存储（生产环境建议使用 Redis）
_active_tokens: set[str] = set()


def generate_token() -> str:
    """生成安全的 session token"""
    return secrets.token_urlsafe(32)


def verify_password(password: str) -> bool:
    """验证密码"""
    if not WEBUI_ENABLED:
        return True
    return password == WEBUI_PASSWORD


def create_session() -> str:
    """创建新会话"""
    token = generate_token()
    _active_tokens.add(token)
    return token


def verify_token(token: Optional[str]) -> bool:
    """验证 token"""
    if not WEBUI_ENABLED:
        return True
    return token in _active_tokens if token else False


def revoke_token(token: str) -> None:
    """撤销 token"""
    _active_tokens.discard(token)


class AuthMiddleware(BaseHTTPMiddleware):
    """WebUI 认证中间件"""

    # 无需认证的路径（"/" 为静态页面壳，不含数据；数据接口均需登录）
    EXEMPT_PATHS = {
        "/",
        "/api/ping",
        "/api/health",
        "/api/auth/login",
        "/api/auth/check",
    }

    async def dispatch(self, request: Request, call_next):
        # 未启用密码验证，直接放行
        if not WEBUI_ENABLED:
            return await call_next(request)

        # 豁免路径
        if request.url.path in self.EXEMPT_PATHS:
            return await call_next(request)

        # 检查 Authorization header；EventSource 无法带 header，兼容 ?token= 查询参数
        token: Optional[str] = None
        auth_header = request.headers.get("Authorization", "")
        if auth_header.startswith("Bearer "):
            token = auth_header[7:]
        if not token:
            token = request.query_params.get("token")
        if verify_token(token):
            return await call_next(request)

        # 认证失败
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"error": "未授权访问，请先登录"},
        )

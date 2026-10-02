"""WebUI 认证控制器"""
from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from middleware.auth_middleware import (
    WEBUI_ENABLED,
    create_session,
    revoke_token,
    verify_password,
)

router = APIRouter()


class LoginRequest(BaseModel):
    password: str


class LoginResponse(BaseModel):
    token: str
    message: str


@router.post("/api/auth/login")
def login(req: LoginRequest) -> JSONResponse:
    """登录接口"""
    if not WEBUI_ENABLED:
        return JSONResponse({"error": "密码验证未启用"}, status_code=400)

    if not verify_password(req.password):
        raise HTTPException(status_code=401, detail="密码错误")

    token = create_session()
    return JSONResponse(
        {
            "token": token,
            "message": "登录成功",
        }
    )


@router.post("/api/auth/logout")
def logout(token: Optional[str] = None) -> JSONResponse:
    """登出接口"""
    if token:
        revoke_token(token)
    return JSONResponse({"message": "登出成功"})


@router.get("/api/auth/check")
def check_auth() -> JSONResponse:
    """检查是否需要认证"""
    return JSONResponse(
        {
            "enabled": WEBUI_ENABLED,
            "message": "需要认证" if WEBUI_ENABLED else "无需认证",
        }
    )

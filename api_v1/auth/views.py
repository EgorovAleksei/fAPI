import secrets
import uuid
from typing import Annotated, Any
from time import time

from fastapi import APIRouter, Depends, HTTPException, status, Header, Response, Cookie
from fastapi.security import HTTPBasicCredentials, HTTPBasic

router = APIRouter(prefix="/auth", tags=["Auth"])

security = HTTPBasic()


@router.get("/basic-auth")
def basic_auth(credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
    return {
        "message": "Hello",
        "username": credentials.username,
        "password": credentials.password,
    }


username_to_passwords = {
    "admin": "admin",
    "john": "password",
}

static_auth_token_to_username = {
    "bc8187ce68e1e0591860a671be4b4e65": "admin",
    "094a15075e7d74856055a5dbba6c70d5": "john",
}


def get_auth_user_username(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)]
) -> str:
    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Unauthorized",
        headers={"WWW-Authenticate": "Basic"},
    )
    correct_password = username_to_passwords.get(credentials.username)
    if correct_password is None:
        raise unauthed_exc
    if not secrets.compare_digest(
        credentials.password.encode("utf-8"),
        correct_password.encode("utf-8"),
    ):
        raise unauthed_exc

    return credentials.username


def get_username_by_static_auth_token(
    static_token: str = Header(alias="X-Auth-Token"),
) -> str:
    if username := static_auth_token_to_username.get(static_token):
        return username
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Unauthorized",
    )


@router.get("/basic-auth-username")
def basic_auth_username(
    auth_username: str = Depends(get_auth_user_username),
):
    return {
        "message": "Hello",
        "username": auth_username,
    }


@router.get("/some-http-header-auth")
def basic_auth_some_http_header(
    auth_username: str = Depends(get_username_by_static_auth_token),
):
    return {
        "message": "Hello",
        "username": auth_username,
    }


COOKIES: dict[str, dict[str, Any]] = {}
COOKIE_SESSION_ID_KEY = "web-app-session-id"


def generate_session_id() -> str:
    return uuid.uuid4().hex


def get_session_data(
    session_id: str = Cookie(alias=COOKIE_SESSION_ID_KEY),
) -> dict:
    if session_id not in COOKIES:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized",
        )
    return COOKIES[session_id]


@router.post("/login-cookie")
def auth_login_set_cookie(
    response: Response,
    # auth_username: str = Depends(get_auth_user_username),
    auth_username: str = Depends(get_username_by_static_auth_token),
):
    session_id = generate_session_id()
    COOKIES[session_id] = {
        "username": auth_username,
        "login_at": int(time()),
    }
    response.set_cookie(COOKIE_SESSION_ID_KEY, session_id)
    return {"result": "ok"}


@router.get("/login-cookie")
def auth_check_cookie(
    user_session_data: dict = Depends(get_session_data),
):
    username = user_session_data["username"]
    login_at = user_session_data["login_at"]
    return {
        "message": f"Hello, {username}! Login at: {login_at}",
        **user_session_data,
    }


@router.get("/logout-cookie")
def auth_logout_cookie(
    response: Response,
    session_id: str = Cookie(alias=COOKIE_SESSION_ID_KEY),
    user_session_data: dict = Depends(get_session_data),
):
    COOKIES.pop(session_id)
    response.delete_cookie(COOKIE_SESSION_ID_KEY)
    username = user_session_data["username"]
    login_at = user_session_data["login_at"]
    return {
        "message": f"Bye, {username}! Login at: {login_at}",
    }

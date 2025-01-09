from fastapi import APIRouter, Depends, Form, HTTPException, status
from pydantic import BaseModel
from fastapi.security import (
    HTTPBearer,
)

from api_v1.auth.helpers import (
    create_access_token,
    create_refresh_token,
    REFRESH_TOKEN_TYPE,
)
from api_v1.auth.validation import (
    get_auth_user_rom_token_of_type,
    get_current_auth_user,
    get_current_auth_user_for_refresh,
    get_current_token_payload,
    UserGetterFromToken,
)
from api_v1.auth.crud import users_db
from auth import utils as auth_utils
from users.schemas import UserSchema

http_bearer = HTTPBearer(auto_error=False)


class TokenInfo(BaseModel):
    access_token: str
    refresh_token: str | None = None
    token_type: str = "Bearer"


router = APIRouter(
    prefix="/jwt",
    tags=["JWT"],
    dependencies=[Depends(http_bearer)],
)


async def validate_auth_user(
    username: str = Form(),
    password: str = Form(),
):
    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Unauthorized",
    )
    if not (user := users_db.get(username)):
        raise unauthed_exc
    if not (
        auth_utils.validate_password(
            password=password,
            hashed_password=user.password,
        )
    ):
        raise unauthed_exc
    if not user.active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user",
        )
    return user


async def get_current_active_auth_user(
    user: UserSchema = Depends(get_current_auth_user),
):
    if user.active:
        return user
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="user inactive",
    )


@router.post("/login", response_model=TokenInfo)
async def auth_user_issue_jwt(
    user: UserSchema = Depends(validate_auth_user),
):
    access_token = create_access_token(user)
    refresh_token = create_refresh_token(user)
    return TokenInfo(
        access_token=access_token,
        refresh_token=refresh_token,
    )


@router.post(
    "/refresh",
    response_model=TokenInfo,
    response_model_exclude_none=True,
)
async def auth_refresh_jwt(
    # user: UserSchema = Depends(get_current_auth_user_for_refresh),
    # user: UserSchema = Depends(get_auth_user_rom_token_of_type(REFRESH_TOKEN_TYPE)),
    user: UserSchema = Depends(UserGetterFromToken(REFRESH_TOKEN_TYPE)),
):
    access_token = create_access_token(user)
    return TokenInfo(
        access_token=access_token,
    )


@router.get("/users/me")
async def auth_user_check_self_info(
    payload: dict = Depends(get_current_token_payload),
    user: UserSchema = Depends(get_current_active_auth_user),
):
    iat = payload.get("iat")
    return {
        "username": user.username,
        "email": user.email,
        "logged_in_at": iat,
    }

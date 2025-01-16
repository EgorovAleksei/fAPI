from fastapi import APIRouter, Depends
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
    get_current_active_auth_user,
    get_current_token_payload,
    UserGetterFromToken,
    validate_auth_user,
)
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

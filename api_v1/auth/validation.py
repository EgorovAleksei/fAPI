from fastapi import Depends, Form, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
from starlette import status

from api_v1.auth.crud import users_db
from api_v1.auth.helpers import ACCESS_TOKEN_TYPE, REFRESH_TOKEN_TYPE, TOKEN_TYPE_FIELD
from auth import utils as auth_utils
from users.schemas import UserSchema

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/jwt/login",
)


async def get_current_token_payload(
    # credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
    token: str = Depends(oauth2_scheme),
) -> UserSchema:
    # token = credentials.credentials
    try:
        payload = auth_utils.decode_jwt(token=token)
    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Unauthorized {e}",
        )
    return payload


def validate_token_type(payload: dict, token_type: str) -> bool:
    current_token_type = payload.get(TOKEN_TYPE_FIELD)
    if current_token_type == token_type:
        return True
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"invalid token type {current_token_type!r} expected {token_type!r}",
    )


def get_user_by_token_sub(payload: dict) -> UserSchema:
    username: str | None = payload.get("sub")
    if user := users_db.get(username):
        return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Unauthorized",
    )


def get_auth_user_rom_token_of_type(token_type: str):
    def get_auth_user_rom_token(
        payload: dict = Depends(get_current_token_payload),
    ) -> UserSchema:
        validate_token_type(payload=payload, token_type=token_type)
        return get_user_by_token_sub(payload=payload)

    return get_auth_user_rom_token


class UserGetterFromToken:
    def __init__(self, token_type: str):
        self.token_type = token_type

    def __call__(
        self,
        payload: dict = Depends(get_current_token_payload),
    ):
        validate_token_type(payload=payload, token_type=self.token_type)
        return get_user_by_token_sub(payload=payload)


get_current_auth_user = get_auth_user_rom_token_of_type(ACCESS_TOKEN_TYPE)
get_current_auth_user_for_refresh = UserGetterFromToken(REFRESH_TOKEN_TYPE)


async def get_current_active_auth_user(
    user: UserSchema = Depends(get_current_auth_user),
):
    if user.active:
        return user
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="user inactive",
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

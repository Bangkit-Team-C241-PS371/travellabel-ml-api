import os
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from jwt.exceptions import InvalidTokenError
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

JWT_ACCESS_KEY = os.environ.get('JWT_ACCESS_SECRET')
ALGORITHM='HS256'

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None
    user_id: str | None = None
    email: str | None = None

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid access token",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # validates the token expiry too
        payload = jwt.decode(token, JWT_ACCESS_KEY, algorithms=[ALGORITHM])

        username: str = payload.get("username")
        user_id: str = payload.get("id")
        email: str = payload.get("email")

        if username is None or user_id is None or email is None:
            raise credentials_exception

        token_data = TokenData(username=username, user_id=user_id, email=email)
    except InvalidTokenError as e:
        raise credentials_exception

    # For now, blindly trust that the user exists as long as the token is properly signed
    """ user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception """
    return token_data

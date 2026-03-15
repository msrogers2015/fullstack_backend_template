# utils/Authentication.py

import bcrypt
from fastapi import HTTPException
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordBearer
from custom_cruds import account_crud
from models.Account import Account
from sqlalchemy.orm import Session
import jwt
from jwt.exceptions import InvalidTokenError
from datetime import datetime, timedelta, timezone
from configs.config import JWT_SECRET_KEY, JWT_ALGORITHM, JWT_TOKEN_LIFETIME
from configs.database import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def check_password(username: str, password: str, db: Session) -> bool:
    """Checks if the provided user data is correct for logging in. The username
    and password is passed as an object, the password is hashed and then checked
    against the database.
    Args:
        username: Username formatted using the oauth2 schema.
        password: Passsword formatted usign the oauth2 schema.
        db: Database session object.
    Returns:
        Boolean: True if the provided user data is correct, else false for
            incorrect password or no user account found."""
    user_account = account_crud.get_by_username(db=db, username=username)
    if user_account:
        hashed = user_account.credential.password_hash
        if isinstance(hashed, str):
            hashed = hashed.encode()
        is_valid = bcrypt.checkpw(password.encode(), hashed)
        if is_valid:
            return True
        else:
            return False
    return False


def create_jwt_token(account: Account) -> str:
    expires = datetime.now(timezone.utc) + timedelta(minutes=JWT_TOKEN_LIFETIME)
    payload = {
        "account_id": account.id,
        "username": account.username,
        "email": account.email,
        "last_login": account.last_login.isoformat() if account.last_login else None,
        "token_expires": expires.timestamp(),
    }

    token = jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return token


def check_jwt_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        if payload["account_id"] is None:
            raise HTTPException(status_code=401, detail="Invalid token.")
        return payload
    except InvalidTokenError:
        raise HTTPException(
            status_code=401,
            detail="An error has occurred and the token has been invalidated.",
        )


def check_current_account(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> Account:
    payload = check_jwt_token(token)
    account_id = payload["account_id"]
    account = account_crud.get_by_id(db, account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found.")
    return account

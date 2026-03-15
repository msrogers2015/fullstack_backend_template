# router/Authentication.py

from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from configs.database import get_db
from utils.Authentication import (
    check_password,
    create_jwt_token,
    check_jwt_token,
    oauth2_scheme,
)
from custom_cruds import account_crud

auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.post("/login")
async def login(
    user_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    if not check_password(
        username=user_data.username, password=user_data.password, db=db
    ):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    user_account = account_crud.get_by_username(db=db, username=user_data.username)
    token = create_jwt_token(user_account)
    return {"access_token": token, "token_type": "bearer"}


@auth_router.post("/verify")
async def verify_token(token: str = Depends(oauth2_scheme)):
    account = check_jwt_token(token=token)
    if not account:
        raise HTTPException(status_code=401, detail="Invalid token.")
    return {"valid": True}

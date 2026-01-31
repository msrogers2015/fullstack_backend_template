# router/Authentication.py

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from configs.database import get_db
from schemas.Authentication import Login
from utils.Authentication import (
    check_password,
    create_jwt_token,
    check_current_account,
)
from custom_cruds.Account import AccountCrud, Account

auth = APIRouter(prefix="/auth", tags=["auth"])


account_crud = AccountCrud()


@auth.post("/login")
async def login(user_data: Login, db: Session = Depends(get_db)):
    if not check_password(user_data=user_data, db=db):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user_account = account_crud.get_by_username(db=db, username=user_data.username)
    token = create_jwt_token(user_account)
    return {"token": token, "token_type": "bearer"}


@auth.get("/verify")
async def verify_token(account: Account = Depends(check_current_account)):
    return {"status": "valid"}

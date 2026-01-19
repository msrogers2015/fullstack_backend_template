# router/Authentication.py

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from configs.database import get_db
from schemas.Authentication import Login
from utils.Authentication import check_password, create_jwt_token, check_jwt_token
from custom_cruds.Account import AccountCrud

auth = APIRouter()


account_crud = AccountCrud()


@auth.post("/login")
async def login(user_data: Login, db: Session = Depends(get_db)):
    if not check_password(user_data=user_data, db=db):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user_account = account_crud.get_by_username(db=db, username=user_data.username)
    token = create_jwt_token(user_account)
    return {"token": token, "token_type": "bearer"}


@auth.post("/verify")
async def verify_token(token: str):
    try:
        account = check_jwt_token(token=token)
        if account:
            print("Token verified")
        else:
            raise HTTPException(status_code=401, detail="Invalid token.")
    except Exception:
        raise HTTPException(status_code=401, detail="Unable to validate token.")

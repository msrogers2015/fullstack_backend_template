# router/User.py

from fastapi import APIRouter, Depends
from utils.Authentication import check_current_account
from models.Account import Account


user = APIRouter(
    prefix="/user", tags=["user"], dependencies=[Depends(check_current_account)]
)


@user.get("/me")
async def me(current_user: Account = Depends(check_current_account)):
    return current_user

# custom_crud/Account.py

from configs.crud import BaseCrud
from models.Account import Account
from sqlalchemy.orm import Session


class AccountCrud(BaseCrud):
    def __init__(self):
        super().__init__(Account)

    def get_by_username(self, db: Session, username: str):
        return db.query(self.model).filter(self.model.username == username).first()

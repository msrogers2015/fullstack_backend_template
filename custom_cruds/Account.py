# custom_crud/Account.py
from sqlalchemy.exc import SQLAlchemyError

from configs.crud import BaseCrud
from models import Account
from sqlalchemy.orm import Session


class AccountCrud(BaseCrud):
    def __init__(self):
        super().__init__(Account)

    def get_by_username(self, db: Session, username: str) -> Account | bool:
        """
        Find a user based on the provided username.
        Args:
            db: SQLAlchemy Session
            username: Username to search by.
        """
        try:
            user = db.query(self.model).filter(self.model.username == username).first()
            if user is None:
                return False
            else:
                return user
        except SQLAlchemyError:
            return False

    def get_by_email(self, db: Session, email: str) -> Account | bool:
        """
        Find a user based on the provided email.
        Args:
            db: SQLAlchemy Session
            email: email to search by.
        """
        try:
            user = db.query(self.model).filter(self.model.email == email).first()
            if user is None:
                return False
            else:
                return user
        except SQLAlchemyError:
            return False

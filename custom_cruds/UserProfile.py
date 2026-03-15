# custom_crud/UserProfile.py

from configs.crud import BaseCrud
from models import UserProfile


class UserProfileCrud(BaseCrud):
    def __init__(self):
        super().__init__(UserProfile)

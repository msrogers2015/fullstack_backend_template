# custom_crud/Role.py

from configs.crud import BaseCrud
from models import Role


class RoleCrud(BaseCrud):
    def __init__(self):
        super().__init__(Role)

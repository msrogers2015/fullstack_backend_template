# custom_crud/Credential.py

from configs.crud import BaseCrud
from models.Credential import Credential


class CredentialCrud(BaseCrud):
    def __init__(self):
        super().__init__(Credential)

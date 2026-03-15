from .Role import RoleCrud
from .Account import AccountCrud
from .Credential import CredentialCrud
from .UserProfile import UserProfileCrud

role_crud = RoleCrud()
account_crud = AccountCrud()
credential_crud = CredentialCrud()
user_profile_crud = UserProfileCrud()

__all__ = [
    "role_crud",
    "account_crud",
    "credential_crud",
    "user_profile_crud",
]

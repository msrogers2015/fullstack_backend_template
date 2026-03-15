# tests/test_models.py

import pytest
from sqlalchemy.exc import IntegrityError
from models import *


class TestRole:
    def test_create_role(self, db):
        """Successfully create a new role."""
        role = Role(name="test_role", access_level=1, description="Test role")
        db.add(role)
        db.commit()
        assert role.id is not None

    def test_duplicate_name_rejected(self, db):
        """Reject duplicate role name."""
        role = Role(name="admin", access_level=3, description="Duplicate")
        db.add(role)
        with pytest.raises(IntegrityError):
            db.commit()

    def test_restrict_role_deletion(self, db):
        """Reject deleting a role that is assigned to an account."""
        role = db.query(Role).filter(Role.id == 1).first()
        db.delete(role)
        with pytest.raises(IntegrityError):
            db.commit()


class TestAccount:
    def test_duplicate_username_rejected(self, db):
        """Reject duplicate username."""
        account = Account(username="admin_user", email="unique@example.com")
        db.add(account)
        with pytest.raises(IntegrityError):
            db.commit()

    def test_duplicate_email_rejected(self, db):
        """Reject duplicate email."""
        account = Account(username="unique_user", email="admin@example.com")
        db.add(account)
        with pytest.raises(IntegrityError):
            db.commit()

    def test_invalid_role_id_rejected(self, db):
        """Reject account with non-existent role_id."""
        account = Account(
            username="unique_user", email="unique@example.com", role_id=999
        )
        db.add(account)
        with pytest.raises(IntegrityError):
            db.commit()

    def test_is_active_defaults_true(self, db):
        """is_active should default to True."""
        account = Account(username="new_user", email="new@example.com")
        db.add(account)
        db.commit()
        db.refresh(account)
        assert account.is_active is True


class TestCredential:
    def test_duplicate_account_id_rejected(self, db):
        """Reject duplicate account_id — one credential per account."""
        credential = Credential(account_id=1, password_hash="somehash")
        db.add(credential)
        with pytest.raises(IntegrityError):
            db.commit()

    def test_invalid_account_id_rejected(self, db):
        """Reject credential with non-existent account_id."""
        credential = Credential(account_id=999, password_hash="somehash")
        db.add(credential)
        with pytest.raises(IntegrityError):
            db.commit()

    # noinspection PyTypeChecker
    def test_null_password_hash_rejected(self, db):
        """Reject null password hash."""
        credential = Credential(account_id=2, password_hash=None)
        db.add(credential)
        with pytest.raises(IntegrityError):
            db.commit()

    def test_restrict_account_deletion(self, db):
        """Reject deleting an account that has a credential."""
        account = db.query(Account).filter(Account.id == 1).first()
        db.delete(account)
        with pytest.raises(IntegrityError):
            db.commit()


class TestUserProfile:
    def test_duplicate_account_id_rejected(self, db):
        """Reject duplicate account_id — one profile per account."""
        profile = UserProfile(account_id=1, full_name="Duplicate")
        db.add(profile)
        with pytest.raises(IntegrityError):
            db.commit()

    def test_invalid_account_id_rejected(self, db):
        """Reject profile with non-existent account_id."""
        profile = UserProfile(account_id=999, full_name="Nobody")
        db.add(profile)
        with pytest.raises(IntegrityError):
            db.commit()

    def test_restrict_account_deletion(self, db):
        """Reject deleting an account that has a user profile."""
        account = db.query(Account).filter(Account.id == 1).first()
        db.delete(account)
        with pytest.raises(IntegrityError):
            db.commit()

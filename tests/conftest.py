# tests/conftest.py

import os

os.environ["ENV"] = "tests"
from dotenv import load_dotenv

load_dotenv(".env.tests")


import csv
import bcrypt
import pytest
from alembic import command
from alembic.config import Config
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from configs.database import SessionLocal, get_db
from models import Role, Account, Credential, UserProfile
from main import app
from sqlalchemy import text

# Hard fail if not running in a test environment
assert os.getenv("ENV", "").startswith(
    "test"
), "Tests must be run with ENV=test. Refusing to continue."

FIXTURE_DIR = os.path.join(os.path.dirname(__file__), "fixtures")


def load_csv(filename: str) -> list[dict]:
    """Load a CSV file from the fixtures directory."""
    with open(os.path.join(FIXTURE_DIR, filename), newline="") as f:
        return list(csv.DictReader(f))


def seed_roles(db: Session):
    for row in load_csv("role.csv"):
        db.add(
            Role(
                id=int(row["id"]),
                name=row["name"],
                access_level=int(row["access_level"]),
                description=row["description"],
            )
        )
    db.commit()


def seed_accounts(db: Session):
    for row in load_csv("account.csv"):
        db.add(
            Account(
                id=int(row["id"]),
                username=row["username"],
                email=row["email"],
                role_id=int(row["role_id"]),
                is_active=row["is_active"].lower() == "true",
            )
        )
    db.commit()


def seed_credentials(db: Session):
    for row in load_csv("credential.csv"):
        hashed = bcrypt.hashpw(row["password_hash"].encode(), bcrypt.gensalt())
        db.add(
            Credential(
                id=int(row["id"]),
                account_id=int(row["account_id"]),
                password_hash=hashed.decode(),
            )
        )
    db.commit()


def seed_user_profiles(db: Session):
    for row in load_csv("user_profile.csv"):
        db.add(
            UserProfile(
                id=int(row["id"]),
                account_id=int(row["account_id"]),
                full_name=row["full_name"],
                phone_number=row["phone_number"],
            )
        )
    db.commit()


@pytest.fixture(scope="session")
def alembic_cfg():
    return Config("alembic.ini")


@pytest.fixture(scope="session", autouse=True)
def apply_migrations(alembic_cfg):
    """Run migrations before all tests, tear down after."""
    command.upgrade(alembic_cfg, "head")
    yield
    command.downgrade(alembic_cfg, "base")


def reset_sequences(db: Session):
    db.execute(text("SELECT setval('role_id_seq', (SELECT MAX(id) FROM role))"))
    db.execute(text("SELECT setval('account_id_seq', (SELECT MAX(id) FROM account))"))
    db.execute(
        text("SELECT setval('credential_id_seq', (SELECT MAX(id) FROM credential))")
    )
    db.execute(
        text("SELECT setval('user_profile_id_seq', (SELECT MAX(id) FROM user_profile))")
    )
    db.commit()


@pytest.fixture(scope="session")
def seed_data(apply_migrations):
    """Seed test data once for the entire session."""
    db = SessionLocal()
    try:
        seed_roles(db)
        seed_accounts(db)
        seed_credentials(db)
        seed_user_profiles(db)
        reset_sequences(db)
    finally:
        db.close()


@pytest.fixture(scope="function")
def db(seed_data):
    db = SessionLocal()
    db.begin_nested()
    yield db
    db.rollback()
    db.close()


@pytest.fixture(scope="function")
def client(db):
    """Test client with db dependency overridden."""

    def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()

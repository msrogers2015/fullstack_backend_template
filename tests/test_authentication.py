import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from sqlalchemy import event
import bcrypt
from datetime import datetime

from configs.database import get_db
from main import app
from configs.database_test import engine, SessionLocal
from models.BaseModel import BaseModel
from models.Account import Account
from models.Credential import Credential
from utils.Authentication import create_jwt_token

# Create tables before tests
BaseModel.metadata.create_all(bind=engine)

client = TestClient(app)


@pytest.fixture
def db():
    """Provide a test database session for each test."""

    # Enable foreign keys for SQLite
    @event.listens_for(engine, "connect")
    def set_sqlite_pragma(dbapi_conn, connection_record):
        cursor = dbapi_conn.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

    connection = engine.connect()
    transaction = connection.begin()
    session = SessionLocal(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(autouse=True)
def override_get_db(db: Session):
    """Override the get_db dependency to use test database."""

    def _get_db():
        yield db

    app.dependency_overrides[get_db] = _get_db
    yield
    app.dependency_overrides.clear()


@pytest.fixture
def test_account(db: Session):
    """Create a test account with credentials."""
    # Create account
    account = Account(
        id=1,
        username="testuser",
        email="test@example.com",
        created_at=datetime.now(),
        is_active=True,
    )
    db.add(account)
    db.flush()
    db.refresh(account)

    # Hash password and create credential
    password = "testpassword123"
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt(rounds=12))
    credential = Credential(
        id=1, account_id=1, password_hash=hashed, created_at=datetime.now()
    )
    db.add(credential)
    db.commit()
    return {"account": account, "password": password}


def test_login_success(test_account):
    """Test successful login with correct credentials."""
    response = client.post(
        "/auth/login", json={"username": "testuser", "password": "testpassword123"}
    )

    assert response.status_code == 200
    assert "token" in response.json()
    assert response.json()["token_type"] == "bearer"


def test_login_invalid_password(test_account):
    """Test login with incorrect password."""
    response = client.post(
        "/auth/login", json={"username": "testuser", "password": "wrongpassword"}
    )

    assert response.status_code == 400
    assert "Incorrect username or password" in response.json()["detail"]


def test_login_nonexistent_user():
    """Test login with non-existent username."""
    response = client.post(
        "/auth/login", json={"username": "nonexistentuser", "password": "anypassword"}
    )

    assert response.status_code == 400
    assert "Incorrect username or password" in response.json()["detail"]


def test_verify_token_valid(test_account):
    """Test token verification with valid token."""
    # Create a token
    token = create_jwt_token(test_account["account"])

    response = client.post(
        f"/auth/verify?token={token}",
    )
    assert response.status_code == 200


def test_verify_token_invalid(test_account):
    """Test token verification with valid token."""
    response = client.post(
        "/auth/verify?token=random_string_for_token",
    )
    assert response.status_code == 401

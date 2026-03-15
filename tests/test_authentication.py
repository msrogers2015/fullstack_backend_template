# tests/test_authentication.py

from utils.Authentication import create_jwt_token
from models import Account
from datetime import datetime, timezone, timedelta
import jwt
from configs.config import JWT_SECRET_KEY, JWT_ALGORITHM


class TestLogin:
    def test_login_success(self, client):
        """Successful login returns access_token and token_type."""
        response = client.post(
            "/auth/login",
            data={"username": "admin_user", "password": "AdminPassword123!"},
        )
        assert response.status_code == 200
        assert "access_token" in response.json()
        assert response.json()["token_type"] == "bearer"

    def test_login_wrong_password(self, client):
        """Wrong password returns 401."""
        response = client.post(
            "/auth/login",
            data={"username": "admin_user", "password": "wrongpassword"},
        )
        assert response.status_code == 401
        assert "Incorrect username or password" in response.json()["detail"]

    def test_login_nonexistent_user(self, client):
        """Non-existent username returns 401."""
        response = client.post(
            "/auth/login",
            data={"username": "nobody", "password": "somepassword"},
        )
        assert response.status_code == 401
        assert "Incorrect username or password" in response.json()["detail"]

    def test_login_returns_valid_jwt(self, client):
        """Token returned on login is a valid decodable JWT."""
        response = client.post(
            "/auth/login",
            data={"username": "admin_user", "password": "AdminPassword123!"},
        )
        token = response.json()["access_token"]
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        assert payload["username"] == "admin_user"
        assert payload["account_id"] is not None


class TestVerify:
    def test_verify_valid_token(self, client, db):
        """Valid token returns valid: True."""
        account = db.query(Account).filter(Account.id == 1).first()
        token = create_jwt_token(account)
        response = client.post(
            "/auth/verify",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200
        assert response.json()["valid"] is True

    def test_verify_invalid_token(self, client):
        """Malformed token returns 401."""
        response = client.post(
            "/auth/verify",
            headers={"Authorization": "Bearer this.is.not.a.token"},
        )
        assert response.status_code == 401

    def test_verify_expired_token(self, client, db):
        """Expired token returns 401."""
        account = db.query(Account).filter(Account.id == 1).first()
        expires = datetime.now(timezone.utc) - timedelta(minutes=1)
        payload = {
            "account_id": account.id,
            "username": account.username,
            "email": account.email,
            "last_login": None,
            "exp": expires,
        }
        expired_token = jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
        response = client.post(
            "/auth/verify",
            headers={"Authorization": f"Bearer {expired_token}"},
        )
        assert response.status_code == 401

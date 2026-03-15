# Router

FastAPI route definitions organised by domain. Each file registers an `APIRouter` that is included in `main.py`.

---

## Structure

| File | Prefix | Description |
|---|---|---|
| `Authentication.py` | `/auth` | Login and token verification |

---

## Endpoints

### Authentication `/auth`

| Method | Endpoint | Auth Required | Description |
|---|---|---|---|
| `POST` | `/auth/login` | No | Accepts username and password, returns a bearer token |
| `POST` | `/auth/verify` | Yes | Verifies the provided bearer token is valid |

#### `/auth/login`
Accepts `OAuth2PasswordRequestForm` (form fields, not JSON). Returns an `access_token` on success.

```json
{
  "access_token": "<token>",
  "token_type": "bearer"
}
```

#### `/auth/verify`
Reads the token from the `Authorization: Bearer` header. Returns `{"valid": true}` on success, `401` on failure.

---

## Adding a New Router

1. Create a new file in `router/` following the naming convention `RouterName.py`
2. Define an `APIRouter` with a prefix and tags
3. Register it in `main.py`

### Template

```python
from fastapi import APIRouter, Depends
from utils.Authentication import check_current_account

my_router = APIRouter(prefix="/my-router", tags=["my-router"])


# Unprotected route
@my_router.get("/")
async def my_route():
    return {}


# Protected route
@my_router.get("/protected", dependencies=[Depends(check_current_account)])
async def my_protected_route():
    return {}
```

### Registering in main.py

By updating the router/__init__.py file, main.py automatically handles adding new routers.
```python
from .NewRoute import new_route_router

ROUTERS = [
    ...
    new_route_router,
    ...
]

__all__ = [
    ...
    "new_route_router",
    ...
]
```

---

## Notes

- Protected routes use `check_current_account` from `utils/Authentication.py` as a dependency
- Swagger UI is available at `/docs` — use the Authorize button to set a bearer token for testing protected endpoints
- All authentication logic lives in `utils/Authentication.py`, not in the router
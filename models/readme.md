# Models

SQLAlchemy ORM models representing the database schema. All models inherit from `BaseModel` and are
managed by Alembic. See `alembic/readme.md` for migration workflows.

---

## Structure

| Model | Table | Description                                                                  |
|---|---|------------------------------------------------------------------------------|
| `BaseModel` | — | Shared declarative base for all models.                                      |
| `Role` | `role` | Defines access roles assignable to accounts with easy to use numeric checks. |
| `Account` | `account` | Core authentication entry point. All other models relate back to this.       |
| `Credential` | `credential` | Stores hashed passwords for an account.                                      |
| `UserProfile` | `user_profile` | Stores personal information for an account.                                  |

---

## Adding a New Model

1. Create a new file in `models/` following the naming convention `ModelName.py`
2. Inherit from `BaseModel`
5. Add the import and export to `models/__init__.py`
6. Create a corresponding crud in `custom_cruds/`
7. Run `alembic revision --autogenerate -m "description"` and review before applying

### Template

```python
from sqlalchemy import Column, BigInteger
from .BaseModel import BaseModel

class MyModel(BaseModel):
    __tablename__ = "my_model"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    ### Add other table columns
```

---

## Notes

- `BaseModel` provides a `__repr__` for all models: `<ModelName id=1>`
- Do not store personal data outside of `UserProfile` — keep it as the single source of truth for
erasure requests
- Always reference `account_id` on transaction/audit records rather than storing names directly.
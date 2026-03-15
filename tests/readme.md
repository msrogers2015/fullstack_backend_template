# Tests

Pytest test suite running against a real Postgres database. Tests use Alembic migrations to set up the schema and CSV fixtures for consistent, reproducible test data.

---

## Structure

| File/Folder | Description |
|---|---|
| `conftest.py` | Fixtures, session setup, migrations, seeding, and db session management |
| `fixtures/` | CSV files containing seed data for each model |
| `test_models.py` | Constraint, relationship, and FK restriction tests for all models |

---

## Running Tests

Tests require a Postgres database with a dedicated test schema. The `ENV` variable must start with `test` — the test suite will hard fail if it does not.

```bash
pytest
```

The `conftest.py` forces `ENV=tests` and loads `.env.tests` automatically. No manual environment setup is required.

---

## Environment

Create a `.env.tests` file at the project root based on `.env.example`. Point `DB_SCHEMA` at your
test schema. An example is not provided here as the `.env.example` is meant to be copied and pasted.
Just ensure the schema you use already exist in your database. 

---

## How It Works

**Session setup** — `apply_migrations` runs `alembic upgrade head` before all tests and `alembic downgrade base` after, creating and destroying the schema automatically.

**Seeding** — `seed_data` inserts fixture data once per session after migrations are applied. PK sequences are reset after seeding to avoid conflicts with autoincrement.

**Test isolation** — each test function receives a `db` session wrapped in a savepoint (`begin_nested()`). Changes are rolled back after each test, keeping tests independent without recreating the schema.

---

## Fixtures

Seed data lives in `tests/fixtures/` as CSV files. Data is loaded in FK dependency order:

| File | Description |
|---|---|
| `role.csv` | Three roles: admin, staff, viewer |
| `account.csv` | Four accounts — one per role plus one inactive account |
| `credential.csv` | One credential per account with plain text passwords (hashed on load) |
| `user_profile.csv` | One profile per account |

Passwords in `credential.csv` are plain text for readability — they are bcrypt hashed during fixture load and never stored in plain text.

---

## Adding Tests

1. Create a new file in `tests/` following the naming convention `test_<area>.py`
2. Use the `db` fixture for database access and the `client` fixture for endpoint testing
3. Reference fixture data by its known IDs or values from the CSV files for predictable assertions

### Template

```python
import pytest
from models import MyModel


class TestMyModel:
    def test_example(self, db):
        record = db.query(MyModel).filter(MyModel.id == 1).first()
        assert record is not None
```

---

## Notes

- Never run tests against a development or production schema — the suite will refuse to start if `ENV` does not start with `test`
- The `client` fixture is available for router/endpoint tests — it overrides `get_db` with the test session automatically
- If the test schema has leftover data from a failed run, drop and recreate the schema manually before running again:
```sql
DROP SCHEMA your_test_schema CASCADE;
CREATE SCHEMA your_test_schema;
```
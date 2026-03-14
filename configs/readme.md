# Configs

Core application configuration including database setup, environment variables,
CORS middleware, and shared CRUD logic.

---

## Files

| File | Description |
|---|---|
| `config.py` | Loads environment variables based on the active `ENV` setting |
| `database.py` | Database engine, session factory, and `get_db` dependency |
| `crud.py` | Generic `BaseCrud` class providing shared database operations |
| `middleware.py` | CORS middleware setup |

---

## Environment

The active environment is controlled by the `ENV` variable. A corresponding `.env`
file must be present at the project root. Use the `.env.example` as a base for all
required env files.

| `ENV` Value | File Loaded |
|---|---|
| `development` (default) | `.env.development` |
| `production` | `.env.production` |
| `test*` | `.env.test` |


---

## BaseCrud

`BaseCrud` is a generic class that provides common database operations for any model. All custom cruds should inherit from it.

```python
from configs.crud import BaseCrud
from models.MyModel import MyModel

class MyModelCrud(BaseCrud):
    def __init__(self):
        super().__init__(MyModel)
```

### Methods

| Method | Description |
|---|---|
| `get_records(db, filters, skip, total_records)` | Returns a list of records, with optional filtering and pagination |
| `get_by_id(db, record_id)` | Returns a single record by its integer primary key |
| `new_record(db, data, commit, return_record)` | Inserts a new record |
| `update_record(db, record_id, new_data, commit)` | Updates an existing record by its integer primary key |
| `remove_records(db, record_id, deactivate, col)` | Deletes or deactivates a record |

### Notes
- `get_by_id` expects an autoincremented integer PK. For other lookup types (e.g. username, email,
UUID), add a custom method in the model's custom crud. See `custom_cruds/`.
- `remove_records` requires a `col` argument when `deactivate=True` to specify which boolean column
to set to `False`. If a hard delete (record being removed from the database instead of being
deactivated) set deactivate to `False`. This is a data protection workflow to avoid accidental deletion.

---

## Notes

- `allow_methods` and `allow_headers` in `middleware.py` should be restricted before deploying to production.
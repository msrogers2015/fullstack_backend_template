# Custom Cruds

Model-specific database operations that extend `BaseCrud`. Each model has a corresponding crud class that inherits shared functionality from `BaseCrud` and adds custom query methods as needed. See `configs/readme.md` for `BaseCrud` documentation.

---

## Structure

| File | Model |
|---|---|
| `Account.py` | `Account` |
| `Credential.py` | `Credential` |
| `Role.py` | `Role` | Base only |
| `UserProfile.py` | `UserProfile` |

---

## Adding a New Crud

1. Create a new file in `custom_cruds/` following the naming convention `ModelName.py`
2. Inherit from `BaseCrud` and pass the model to `super().__init__()`
3. Add the import, instantiation, and export to `custom_cruds/__init__.py`

---

### Updating Init File

The custom crud must be added to the init file as well as initialized for actual use within the
project.
```py
...
from .NewCrud import MyCrud
...

...
new_crud = MyCrud()
...

__all__ = [
    ...
    "new_crud",
    ...
]
```

---

### Template

```python
from configs.crud import BaseCrud
from models import MyModel


class MyModelCrud(BaseCrud):
    def __init__(self):
        super().__init__(MyModel)
```

### Adding Custom Methods

Custom methods should be added when a lookup cannot be performed by `BaseCrud.get_by_id()` — for example, querying by a non-integer field like username, email, or a unique string identifier.

```python
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

class MyModelCrud(BaseCrud):
    def __init__(self):
        super().__init__(MyModel)

    def get_by_name(self, db: Session, name: str):
        try:
            record = db.query(self.model).filter(self.model.name == name).first()
            if record is None:
                return False
            else:
                return record
        except SQLAlchemyError:
            return False
```

---

## Notes

- Crud instances are instantiated in `__init__.py` — import the instance, not the class:
```python
# Correct
from custom_cruds import account_crud

# Avoid
from custom_cruds.Account import AccountCrud
account_crud = AccountCrud()
```
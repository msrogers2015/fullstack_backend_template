# Alembic

Database migration management for the project. Alembic tracks schema changes as versioned migration files, allowing all environments to be brought to the same schema state with a single command.

---

## Structure

| File/Folder | Description |
|---|---|
| `env.py` | Connects Alembic to the project database and models |
| `script.py.mako` | Template used to generate new migration files |
| `versions/` | Contains all migration files in order |

---

## Commands

| Command | Description                                                                               |
|---|-------------------------------------------------------------------------------------------|
| `alembic upgrade head` | Apply all pending migrations                                                              |
| `alembic downgrade -1` | Roll back the most recent migration                                                       |
| `alembic current` | Show the current migration revision of the database                                       |
| `alembic history` | Show the full migration chain                                                             |
| `alembic revision --autogenerate -m "description"` | Generate a new migration from model changes. The -m is a flag for the message to be added |
| `alembic upgrade head --sql` | Preview the SQL that would be executed without applying it                                |

---

## Workflow

Follow this process for every model change:

1. Make the change in the model file
2. Run `alembic revision --autogenerate -m "description"`
3. Review the generated file in `versions/` before applying
4. Run `alembic upgrade head`
5. Commit both the model change and the migration file in the same PR

---

## Reviewing Migrations

Always review the generated migration file before applying. Autogenerate is reliable for most changes but can miss:

- Custom constraints or indexes
- Server-side defaults
- Schema-level changes

Watch for destructive operations in the `upgrade()` function such as `op.drop_table()` or `op.drop_column()` — these should be intentional and never appear in a migration unexpectedly.

---

## Environments

Alembic uses the database connection from `configs/database.py` and the active `.env` file based on the `ENV` variable. Ensure the correct environment is set before running migrations.

```bash
# Development (default)
alembic upgrade head

# Production
ENV=production alembic upgrade head
```

---

## Notes

- Migration files in `versions/` are committed to Git — every environment applies the same migrations
- The `alembic_version` table is managed automatically and should never be edited manually
- `downgrade()` is generated automatically — review it to ensure it correctly reverses the upgrade
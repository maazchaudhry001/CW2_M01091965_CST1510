# Project quick commands

This repository contains simple Vehicle/Car models and a tiny SQLite demo used
for workshop activities.

Quick commands (run from the project root):

- Run tests (uses pytest if installed):

```bash
pytest -q
```

- Reset the persistent dev DB (recreates `data/dev.db` and inserts sample rows):

```bash
python3 scripts/reset_db.py
```

- Run the in-memory smoke test (prints seeded rows):

```bash
python3 scripts/test_models_db.py
```

- Lightweight test runner (no pytest required):

```bash
python3 scripts/run_tests.py
```

Files of interest:
- `models/vehicle.py` — Vehicle and Car classes
- `database/schema.py` — sqlite helpers
- `database/seed_data.py` — seeding helpers (includes `seed_file`)
- `database/loader.py` — load DB rows into model objects
- `scripts/reset_db.py` — helper to recreate `data/dev.db`
- `scripts/test_models_db.py` — smoke test

If you'd like, I can add CI, more tests, or update service modules to use the seeded DB.

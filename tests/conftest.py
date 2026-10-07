"""Test session for the CRM demo: a disposable database, every extension installed for real.

The database is a fresh SQLite file per session (or a disposable PostgreSQL
database with `CRM_TEST_DB=pgsql`), so the demo's own data is never touched. Extensions are installed and activated through the
engine's `ExtensionManager`, exactly as an operator would.
"""

import os
import tempfile
from collections.abc import Generator
from typing import Any

import pytest

#: `CRM_TEST_DB=pgsql` runs the suite on the PostgreSQL server named by the
#: DB_* variables, which must point at a disposable database; anything else
#: uses a fresh SQLite file.
if os.environ.get("CRM_TEST_DB") != "pgsql":
    os.environ["DB_CONNECTION"] = "sqlite"
    os.environ["DB_DATABASE"] = os.path.join(tempfile.mkdtemp(prefix="crm_demo_test_"), "crm.sqlite")

import engine  # noqa: E402,F401  installs the `craft.*` import alias, as bootstrap/app.py does

#: Install order follows the dependencies declared in each manifest.
EXTENSIONS = ("companies", "contacts", "deals", "activities", "dashboard", "posts", "pages", "users", "media", "audit_log", "harbor", "extension_manager",
              "tickets", "invoices", "activity_digest", "midnight", "outbound_webhooks")


@pytest.fixture(scope="session", autouse=True)
def crm() -> Generator[Any, None, None]:
    """Boot the CRM on a fresh database with every extension active."""
    from bootstrap.app import app
    from craft.migrations.migrator import Migrator

    Migrator(app).run()
    manager = app.make("extensions")
    for slug in EXTENSIONS:
        manager.install(slug)
        manager.activate(slug)
    yield app

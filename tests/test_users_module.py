"""Slice 5 of the WordPress-style admin: the users module (list, add, roles)."""

import os
import re
import subprocess
import sys
from typing import Any

import pytest

from craft.facades import DB

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EMAIL = "users@crm.admin.test"
PASSWORD = "s3cret-Passw0rd!"
NEW_EMAIL = "editor@crm.test"


def _token(html: str) -> str:
    found = re.search(r'name="_token" value="([^"]+)"', html)
    return found.group(1) if found else ""


def _client() -> Any:
    from starlette.testclient import TestClient

    from bootstrap.app import app, asgi_app

    base_url = str(app.make("config").get("app.APP_URL", "http://testserver") or "http://testserver").rstrip("/")
    return TestClient(asgi_app, follow_redirects=False, base_url=base_url)


def _register(client: Any, email: str, name: str) -> None:
    page = client.get("/register")
    registered = client.post("/register", data={
        "_token": _token(page.text), "name": name, "email": email,
        "password": PASSWORD, "password_confirmation": PASSWORD,
    })
    assert registered.status_code in (302, 303), registered.text[:300]


@pytest.fixture(scope="module")
def admin(crm: Any) -> Any:
    """A signed-in administrator, registered through the real form."""
    client = _client()
    _register(client, EMAIL, "User Admin")
    assigned = subprocess.run([sys.executable, "dev.py", "user", "assign-role", EMAIL, "admin"], cwd=ROOT, capture_output=True, text=True)
    assert assigned.returncode == 0, assigned.stdout + assigned.stderr
    return client


class TestUsers:
    def test_the_users_screen_renders_for_an_admin(self, admin: Any) -> None:
        page = admin.get("/admin/users")
        assert page.status_code == 200
        assert "/extensions/harbor/css/harbor.css" in page.text

    def test_a_guest_is_sent_to_sign_in(self, crm: Any) -> None:
        assert _client().get("/admin/users").status_code in (302, 303)

    def test_a_plain_user_cannot_reach_the_screen(self, crm: Any) -> None:
        client = _client()
        _register(client, "plain@crm.test", "Plain User")
        assert client.get("/admin/users").status_code != 200

    def test_an_admin_adds_a_user_with_a_role(self, admin: Any) -> None:
        role_id = DB.table("roles").where("slug", "admin").first()["id"]
        created = admin.post("/admin/users", data={
            "_token": _token(admin.get("/admin/users/create").text), "name": "Novo Editor",
            "email": NEW_EMAIL, "password": PASSWORD, "password_confirmation": PASSWORD, "role_id": str(role_id),
        })
        assert created.status_code in (302, 303), created.text[:300]
        row = DB.table("users").where("email", NEW_EMAIL).first()
        assert row is not None
        assigned = DB.table("role_user").where("user_id", row["id"]).first()
        assert assigned is not None and str(assigned["role_id"]) == str(role_id)

    def test_a_duplicate_email_is_refused(self, admin: Any) -> None:
        before = DB.table("users").count()
        refused = admin.post("/admin/users", data={
            "_token": _token(admin.get("/admin/users/create").text), "name": "Repetido",
            "email": NEW_EMAIL, "password": PASSWORD, "password_confirmation": PASSWORD, "role_id": "",
        })
        assert refused.status_code in (302, 303)
        assert DB.table("users").count() == before

    def test_the_copy_is_translated_not_raw_keys(self, admin: Any) -> None:
        page = admin.get("/admin/users").text
        assert "users.field." not in page

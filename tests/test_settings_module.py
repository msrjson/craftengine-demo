"""Slice 7 of the WordPress-style admin: Menus and Settings."""

import os
import re
import subprocess
import sys
from typing import Any

import pytest

from craft.facades import DB

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EMAIL = "settings@crm.admin.test"
PASSWORD = "s3cret-Passw0rd!"
SITE_NAME = "Craft CRM Demo"


def _token(html: str) -> str:
    found = re.search(r'name="_token" value="([^"]+)"', html)
    return found.group(1) if found else ""


def _menu(html: str) -> str:
    found = re.search(r'<nav id="admin-menu".*?</nav>', html, re.S)
    return found.group(0) if found else ""


@pytest.fixture(scope="module")
def admin(crm: Any) -> Any:
    """A signed-in administrator, registered through the real form."""
    from starlette.testclient import TestClient

    from bootstrap.app import app, asgi_app

    base_url = str(app.make("config").get("app.APP_URL", "http://testserver") or "http://testserver").rstrip("/")
    client = TestClient(asgi_app, follow_redirects=False, base_url=base_url)
    page = client.get("/register")
    registered = client.post("/register", data={
        "_token": _token(page.text), "name": "Settings Admin", "email": EMAIL,
        "password": PASSWORD, "password_confirmation": PASSWORD,
    })
    assert registered.status_code in (302, 303), registered.text[:300]
    assigned = subprocess.run([sys.executable, "dev.py", "user", "assign-role", EMAIL, "admin"], cwd=ROOT, capture_output=True, text=True)
    assert assigned.returncode == 0, assigned.stdout + assigned.stderr
    return client


class TestSettings:
    def test_the_settings_screen_renders_for_an_admin(self, admin: Any) -> None:
        page = admin.get("/admin/settings")
        assert page.status_code == 200
        assert "/extensions/harbor/css/harbor.css" in page.text
        assert 'name="site_name"' in page.text

    def test_a_guest_is_sent_to_sign_in(self, crm: Any) -> None:
        from starlette.testclient import TestClient

        from bootstrap.app import app, asgi_app

        base_url = str(app.make("config").get("app.APP_URL", "http://testserver") or "http://testserver").rstrip("/")
        assert TestClient(asgi_app, follow_redirects=False, base_url=base_url).get("/admin/settings").status_code in (302, 303)

    def test_saving_the_site_name_persists_and_shows_on_the_admin_bar(self, admin: Any) -> None:
        saved = admin.post("/admin/settings", data={
            "_token": _token(admin.get("/admin/settings").text),
            "site_name": SITE_NAME, "site_tagline": "CRM de demonstracao", "posts_per_page": "10",
        })
        assert saved.status_code in (302, 303), saved.text[:300]
        row = DB.table("settings").where("key", "site_name").first()
        assert row is not None and SITE_NAME in str(row["value"])
        assert SITE_NAME in admin.get("/overview").text

    def test_the_settings_copy_is_translated_not_raw_keys(self, admin: Any) -> None:
        page = admin.get("/admin/settings").text
        assert "settings.field." not in page

    def test_hiding_a_menu_entry_removes_it_from_the_menu(self, admin: Any) -> None:
        menus = admin.get("/admin/menus")
        assert menus.status_code == 200
        routes = re.findall(r'name="hidden__([^"]+)"', menus.text)
        assert "companies.index" in routes

        visible = {f"hidden__{route}": "1" for route in routes if route != "companies.index"}
        admin.post("/admin/menus", data={"_token": _token(admin.get("/admin/menus").text), **visible})
        try:
            assert 'href="/companies"' not in _menu(admin.get("/overview").text)
        finally:
            restore = {f"hidden__{route}": "1" for route in routes}
            admin.post("/admin/menus", data={"_token": _token(admin.get("/admin/menus").text), **restore})
        assert 'href="/companies"' in _menu(admin.get("/overview").text)

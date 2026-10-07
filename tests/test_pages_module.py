"""Slice 4 of the WordPress-style admin: the pages module (list + editor)."""

import os
import re
import subprocess
import sys
from typing import Any

import pytest

from craft.facades import DB

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EMAIL = "pages@crm.admin.test"
PASSWORD = "s3cret-Passw0rd!"
TITLE = "Pagina de teste"


def _token(html: str) -> str:
    found = re.search(r'name="_token" value="([^"]+)"', html)
    return found.group(1) if found else ""


@pytest.fixture(scope="module")
def admin(crm: Any) -> Any:
    """A signed-in administrator, registered through the real form."""
    from starlette.testclient import TestClient

    from bootstrap.app import app, asgi_app

    base_url = str(app.make("config").get("app.APP_URL", "http://testserver") or "http://testserver").rstrip("/")
    client = TestClient(asgi_app, follow_redirects=False, base_url=base_url)
    page = client.get("/register")
    registered = client.post("/register", data={
        "_token": _token(page.text), "name": "Page Admin", "email": EMAIL,
        "password": PASSWORD, "password_confirmation": PASSWORD,
    })
    assert registered.status_code in (302, 303), registered.text[:300]
    assigned = subprocess.run([sys.executable, "dev.py", "user", "assign-role", EMAIL, "admin"], cwd=ROOT, capture_output=True, text=True)
    assert assigned.returncode == 0, assigned.stdout + assigned.stderr
    return client


class TestPages:
    def test_the_pages_screen_renders_with_the_theme(self, admin: Any) -> None:
        page = admin.get("/pages")
        assert page.status_code == 200
        assert "/extensions/harbor/css/harbor.css" in page.text

    def test_the_editor_renders_title_and_body(self, admin: Any) -> None:
        page = admin.get("/pages/create")
        assert page.status_code == 200
        assert 'name="title"' in page.text and 'name="body"' in page.text

    def test_the_copy_is_translated_not_raw_keys(self, admin: Any) -> None:
        page = admin.get("/pages").text
        assert "pages.field." not in page and "pages.status." not in page

    def test_a_page_is_created_as_a_draft_then_published_and_unpublished(self, admin: Any) -> None:
        created = admin.post("/pages", data={
            "_token": _token(admin.get("/pages/create").text), "title": TITLE, "body": "Um corpo qualquer.",
        })
        assert created.status_code in (302, 303), created.text[:300]
        row = DB.table("crm_pages").where("title", TITLE).first()
        assert row["status"] == "draft"
        assert TITLE in admin.get("/pages").text

        published = admin.post(f"/pages/{row['id']}/publish", data={"_token": _token(admin.get("/pages").text), "action": "publish"})
        assert published.status_code in (302, 303)
        assert DB.table("crm_pages").where("title", TITLE).first()["status"] == "published"

        back = admin.post(f"/pages/{row['id']}/publish", data={"_token": _token(admin.get("/pages").text), "action": "draft"})
        assert back.status_code in (302, 303)
        assert DB.table("crm_pages").where("title", TITLE).first()["status"] == "draft"

    def test_a_blank_page_is_refused(self, admin: Any) -> None:
        refused = admin.post("/pages", data={"_token": _token(admin.get("/pages/create").text), "title": "", "body": ""})
        assert refused.status_code in (302, 303)
        assert DB.table("crm_pages").where("title", "").first() is None

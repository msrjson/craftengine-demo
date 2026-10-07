"""Slice 6 of the WordPress-style admin: the media library (upload + browse)."""

import base64
import os
import re
import subprocess
import sys
from typing import Any

import pytest

from craft.facades import DB

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EMAIL = "media@crm.admin.test"
PASSWORD = "s3cret-Passw0rd!"
#: A real 1x1 PNG, so the browser can render the thumbnail.
PNG = base64.b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAAC0lEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=="
)


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
        "_token": _token(page.text), "name": "Media Admin", "email": EMAIL,
        "password": PASSWORD, "password_confirmation": PASSWORD,
    })
    assert registered.status_code in (302, 303), registered.text[:300]
    assigned = subprocess.run([sys.executable, "dev.py", "user", "assign-role", EMAIL, "admin"], cwd=ROOT, capture_output=True, text=True)
    assert assigned.returncode == 0, assigned.stdout + assigned.stderr
    return client


class TestMedia:
    def test_the_library_renders_with_the_theme(self, admin: Any) -> None:
        page = admin.get("/media")
        assert page.status_code == 200
        assert "/extensions/harbor/css/harbor.css" in page.text
        assert 'enctype="multipart/form-data"' in page.text

    def test_an_image_is_stored_shown_and_served(self, admin: Any) -> None:
        uploaded = admin.post(
            "/media",
            data={"_token": _token(admin.get("/media").text)},
            files={"file": ("shot.png", PNG, "image/png")},
        )
        assert uploaded.status_code in (302, 303), uploaded.text[:300]
        row = DB.table("crm_media").where("original_name", "shot.png").first()
        assert row is not None and row["size"] == len(PNG)
        assert "shot.png" in admin.get("/media").text

        served = admin.get(f"/media/{row['id']}/file")
        assert served.status_code == 200
        assert served.headers["content-type"].startswith("image/png")
        assert served.content == PNG

    def test_a_disallowed_type_is_refused(self, admin: Any) -> None:
        before = DB.table("crm_media").count()
        refused = admin.post(
            "/media",
            data={"_token": _token(admin.get("/media").text)},
            files={"file": ("payload.exe", b"MZ\x90\x00", "application/octet-stream")},
        )
        assert refused.status_code in (302, 303)
        assert DB.table("crm_media").count() == before

    def test_a_guest_cannot_upload(self, crm: Any) -> None:
        from starlette.testclient import TestClient

        from bootstrap.app import app, asgi_app

        base_url = str(app.make("config").get("app.APP_URL", "http://testserver") or "http://testserver").rstrip("/")
        guest = TestClient(asgi_app, follow_redirects=False, base_url=base_url)
        assert guest.get("/media").status_code in (302, 303)

    def test_the_copy_is_translated_not_raw_keys(self, admin: Any) -> None:
        page = admin.get("/media").text
        assert "media.field." not in page and "media.error." not in page

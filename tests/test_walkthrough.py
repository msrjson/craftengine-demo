"""Walk the CRM as a person would: register, become admin, use every screen.

Needs the login and the admin panel generated (`dev.py make auth`, `dev.py
make admin`); until they are, the walkthrough is skipped with that reason.
"""

import os
import re
import subprocess
import sys
from typing import Any

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCAFFOLDED = all(
    os.path.exists(os.path.join(ROOT, *path))
    for path in (("app", "Http", "Controllers", "Auth", "AuthController.py"), ("app", "Http", "Controllers", "Admin", "HomeController.py"))
)
pytestmark = pytest.mark.skipif(not SCAFFOLDED, reason="run `dev.py make auth` and `dev.py make admin` first")

EMAIL = "admin@crm.test"
PASSWORD = "s3cret-Passw0rd!"


def _token(html: str) -> str:
    found = re.search(r'name="_token" value="([^"]+)"', html)
    return found.group(1) if found else ""


@pytest.fixture(scope="module")
def admin(crm: Any) -> Any:
    """A signed-in administrator, registered through the real form."""
    from starlette.testclient import TestClient

    from bootstrap.app import app, asgi_app

    # The browser's view: requests and Referer carry the configured APP_URL,
    # which is what the CSRF origin check compares against.
    base_url = str(app.make("config").get("app.APP_URL", "http://testserver") or "http://testserver").rstrip("/")
    client = TestClient(asgi_app, follow_redirects=False, base_url=base_url)
    page = client.get("/register")
    assert page.status_code == 200
    registered = client.post("/register", data={
        "_token": _token(page.text), "name": "Admin", "email": EMAIL,
        "password": PASSWORD, "password_confirmation": PASSWORD,
    })
    assert registered.status_code in (302, 303), registered.text[:300]
    assigned = subprocess.run([sys.executable, "dev.py", "user", "assign-role", EMAIL, "admin"], cwd=ROOT, capture_output=True, text=True)
    assert assigned.returncode == 0, assigned.stdout + assigned.stderr
    return client


def _post(client: Any, form_url: str, url: str, data: dict) -> Any:
    return client.post(url, data={"_token": _token(client.get(form_url).text), **data})


@pytest.mark.parametrize("url", [
    "/overview", "/companies", "/companies/create", "/contacts", "/contacts/create", "/deals",
    "/deals/create", "/activities", "/activities/create", "/posts", "/posts/create", "/pages", "/pages/create", "/media", "/admin/users", "/admin/users/create", "/admin/extensions", "/admin/audit",
])
def test_every_screen_renders_with_the_theme(admin: Any, url: str) -> None:
    response = admin.get(url)
    assert response.status_code == 200, f"{response.status_code} {response.headers.get('location', '')}"
    assert "/extensions/harbor/css/harbor.css" in response.text


def test_the_sales_flow(admin: Any) -> None:
    assert _post(admin, "/companies/create", "/companies", {"name": "Acme Ltda", "industry": "retail"}).status_code in (302, 303)
    assert "Acme Ltda" in admin.get("/companies").text
    assert _post(admin, "/contacts/create", "/contacts", {"first_name": "Ana", "last_name": "Souza", "company_id": "1"}).status_code in (302, 303)
    assert "Acme Ltda" in admin.get("/contacts").text
    created = _post(admin, "/deals/create", "/deals", {"title": "Annual plan", "contact_id": "1", "amount": "1500,90", "currency": "BRL"})
    assert created.status_code in (302, 303), created.text[:300]
    assert "Annual plan" in admin.get("/deals").text
    won = _post(admin, "/deals", "/deals/1/stage", {"stage": "won"})
    assert won.status_code in (302, 303), won.text[:300]
    assert admin.get("/activities").text.count("activities.source.deal_won") == 0
    assert "deal_won" not in admin.get("/activities").text


def test_an_invalid_form_returns_to_it(admin: Any) -> None:
    referer = str(admin.base_url).rstrip("/") + "/companies/create"
    response = admin.post("/companies", data={"_token": _token(admin.get("/companies/create").text), "name": ""}, headers={"referer": referer})
    assert response.status_code in (302, 303)
    assert response.headers["location"].endswith("/companies/create")


def test_the_panel_explains_a_refusal(admin: Any) -> None:
    response = _post(admin, "/admin/extensions", "/admin/extensions/companies/deactivate", {})
    assert response.status_code in (302, 303)
    page = admin.get("/admin/extensions").text
    assert 'role="alert"' in page and "contacts" in page


def test_the_panel_switches_a_module_off_and_on(admin: Any) -> None:
    assert _post(admin, "/admin/extensions", "/admin/extensions/dashboard/deactivate", {}).status_code in (302, 303)
    try:
        assert 'href="/overview"' not in admin.get("/companies").text
        assert admin.get("/overview").status_code == 404
    finally:
        _post(admin, "/admin/extensions", "/admin/extensions/dashboard/activate", {})
    assert admin.get("/overview").status_code == 200

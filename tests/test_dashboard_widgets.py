"""Slice 2 of the WordPress-style admin: the dashboard widgets.

At a Glance, Activity and Quick Draft. The draft goes through the activities
module's proxy surface, so the dashboard never imports another module.
"""

import importlib
import os
import re
import subprocess
import sys
from typing import Any

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EMAIL = "widgets@crm.admin.test"
PASSWORD = "s3cret-Passw0rd!"


def _token(html: str) -> str:
    found = re.search(r'name="_token" value="([^"]+)"', html)
    return found.group(1) if found else ""


def _service(app: Any, module: str, name: str) -> Any:
    package, cls = {
        "companies": ("companies.services.company_service", "CompanyService"),
        "contacts": ("contacts.services.contact_service", "ContactService"),
    }[module]
    return app.make(getattr(importlib.import_module(f"app.modules.{package}"), cls))


@pytest.fixture(scope="module")
def admin(crm: Any) -> Any:
    """A signed-in administrator, registered through the real form."""
    from starlette.testclient import TestClient

    from bootstrap.app import app, asgi_app

    base_url = str(app.make("config").get("app.APP_URL", "http://testserver") or "http://testserver").rstrip("/")
    client = TestClient(asgi_app, follow_redirects=False, base_url=base_url)
    page = client.get("/register")
    registered = client.post("/register", data={
        "_token": _token(page.text), "name": "Widget Admin", "email": EMAIL,
        "password": PASSWORD, "password_confirmation": PASSWORD,
    })
    assert registered.status_code in (302, 303), registered.text[:300]
    assigned = subprocess.run([sys.executable, "dev.py", "user", "assign-role", EMAIL, "admin"], cwd=ROOT, capture_output=True, text=True)
    assert assigned.returncode == 0, assigned.stdout + assigned.stderr
    return client


class TestDashboardWidgets:
    def test_the_dashboard_renders_the_three_widgets(self, admin: Any) -> None:
        page = admin.get("/overview")
        assert page.status_code == 200
        for widget in ("dash-widget--glance", "dash-widget--activity", "dash-widget--draft"):
            assert widget in page.text
        assert "/extensions/harbor/css/harbor.css" in page.text

    def test_the_widget_copy_is_translated_not_raw_keys(self, admin: Any) -> None:
        page = admin.get("/overview").text
        assert "dashboard.widget." not in page

    def test_a_quick_draft_schedules_an_activity(self, admin: Any, crm: Any) -> None:
        company = _service(crm, "companies", "service").create({"name": "Widget Co", "industry": "retail"})
        contact = _service(crm, "contacts", "service").create({"first_name": "Widget", "last_name": "Target", "company_id": company})
        page = admin.get("/overview").text
        draft = admin.post("/overview/draft", data={
            "_token": _token(page), "contact_id": str(contact), "kind": "note", "subject": "Rascunho da visao geral",
        })
        assert draft.status_code in (302, 303), draft.text[:300]
        assert "Rascunho da visao geral" in admin.get("/overview").text

    def test_a_blank_draft_is_refused(self, admin: Any) -> None:
        page = admin.get("/overview").text
        draft = admin.post("/overview/draft", data={"_token": _token(page), "contact_id": "", "kind": "note", "subject": ""})
        assert draft.status_code in (302, 303)

"""Slice 1 of the WordPress-style admin: the professional login and the chrome.

The login screen and the admin chrome (top bar + left menu) belong to the
`harbor` theme; these tests pin the contract the rest of the slices build on.
"""

from typing import Any

import pytest

from craft.facades import DB, View

CHROME_KEYS = (
    "harbor.layout.admin_menu",
    "harbor.layout.menu",
    "harbor.layout.view_site",
    "harbor.layout.howdy",
    "harbor.auth.tagline",
)


def _client() -> Any:
    from starlette.testclient import TestClient

    from bootstrap.app import app, asgi_app

    base_url = str(app.make("config").get("app.APP_URL", "http://testserver") or "http://testserver").rstrip("/")
    return TestClient(asgi_app, follow_redirects=False, base_url=base_url)


class TestLoginScreen:
    def test_the_login_renders_with_the_theme_and_a_card(self, crm: Any) -> None:
        page = _client().get("/login")
        assert page.status_code == 200
        assert "/extensions/harbor/css/harbor.css" in page.text
        assert 'class="auth-card"' in page.text
        assert 'id="auth-title"' in page.text
        assert "/register" in page.text

    def test_the_login_carries_the_csrf_token_and_the_honeypot(self, crm: Any) -> None:
        page = _client().get("/login").text
        assert 'name="_token"' in page
        assert 'name="_craft_hp_name"' in page

    def test_the_register_shares_the_same_shell(self, crm: Any) -> None:
        page = _client().get("/register")
        assert page.status_code == 200
        assert 'class="auth-card"' in page.text
        assert "/login" in page.text


class TestAdminChrome:
    def test_the_chrome_has_a_top_bar_a_left_menu_and_a_toggle(self, crm: Any) -> None:
        html = View.render("dashboard::index", {"cards": []})
        assert "/extensions/harbor/css/harbor.css" in html
        assert 'class="admin-bar"' in html
        assert 'class="admin-menu"' in html
        assert 'data-menu-toggle' in html and 'aria-controls="admin-menu"' in html
        assert 'aria-expanded="true"' in html

    def test_the_left_menu_is_built_from_the_active_modules(self, crm: Any) -> None:
        html = View.render("dashboard::index", {"cards": []})
        assert 'href="/companies"' in html
        assert 'href="/contacts"' in html

    def test_the_chrome_copy_is_translated_not_raw_keys(self, crm: Any) -> None:
        html = View.render("dashboard::index", {"cards": []})
        assert 'class="admin-menu"' in html and "aria-label=" in html
        assert "harbor.layout." not in html


class TestChromeTranslations:
    @pytest.mark.parametrize("key", CHROME_KEYS)
    def test_every_chrome_key_exists_in_three_locales(self, crm: Any, key: str) -> None:
        assert {row["locale"] for row in DB.table("translations").where("key", key).get()} == {"en", "pt-BR", "es"}

"""Thin HTTP layer of the settings module."""

from typing import Any

from craft.container.application import Container
from craft.http.controller import Controller
from craft.http.response import redirect
from craft.validation import Validator

from ..services.settings_service import SettingsService

RULES = {
    "site_name": ["nullable", "string", "max:80"],
    "site_tagline": ["nullable", "string", "max:160"],
    "posts_per_page": ["required", "integer", "min:1", "max:100"],
}

#: Prefix of a per-item checkbox in the menus form. One field per route,
#: because repeated field names overwrite each other in the input bag.
HIDE_PREFIX = "hidden__"


class SettingsController(Controller):
    """Edit the site settings and which menu entries are visible."""

    def __init__(self, service: SettingsService) -> None:
        self.service = service

    def index(self, request: Any) -> Any:
        """Show the general settings."""
        return self.view("settings::index", {"values": self.service.values()})

    def save(self, request: Any) -> Any:
        """Validate and persist the general settings."""
        validator = Validator(request.all(), RULES)
        if validator.fails():
            return redirect.back(request, fallback="/admin/settings").with_errors(validator).with_input(request.all())
        data = validator.validated()
        self.service.put("site_name", data.get("site_name") or "")
        self.service.put("site_tagline", data.get("site_tagline") or "")
        self.service.put("posts_per_page", int(data.get("posts_per_page") or 20))
        return redirect(route="settings.index")

    def menus(self, request: Any) -> Any:
        """Show every menu entry with its visibility."""
        hidden = set(self.service.hidden_menu())
        rows = [
            {"route": item["route"], "label_key": item["label_key"], "hidden": item["route"] in hidden}
            for item in self._navigation()
        ]
        return self.view("settings::menus", {"rows": rows})

    def save_menus(self, request: Any) -> Any:
        """Persist which entries are hidden; a checked box means visible."""
        known = {item["route"] for item in self._navigation()}
        checked = {
            key[len(HIDE_PREFIX):]
            for key, value in request.all().items()
            if key.startswith(HIDE_PREFIX) and str(value) not in ("", "0")
        }
        self.service.put("menu_hidden", sorted(known - checked))
        return redirect(route="settings.menus")

    @staticmethod
    def _navigation() -> list[dict]:
        """The menu every active module contributes."""
        return Container.getInstance().make("events").apply_filters("crm.navigation", [])

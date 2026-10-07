"""The CRM's own settings, on the engine's settings store.

Only the keys listed here are editable from the panel; anything else is the
engine's own configuration and is not touched by a form.
"""

from typing import Any

from craft.support.settings import SettingManager, setting

#: The setting keys this module owns, with their default value.
DEFAULTS = {
    "site_name": "",
    "site_tagline": "",
    "posts_per_page": 20,
    "menu_hidden": [],
}


class SettingsService:
    """A thin layer over `SettingManager` for the keys the panel edits."""

    def get(self, key: str, default: Any = None) -> Any:
        """Read one setting, falling back to this module's default."""
        return setting(key, DEFAULTS.get(key) if default is None else default)

    def put(self, key: str, value: Any) -> bool:
        """Persist one setting; False when it could not reach the database."""
        return SettingManager.set(key, value)

    def values(self) -> dict:
        """Every editable setting with its effective value."""
        return {key: self.get(key, default) for key, default in DEFAULTS.items()}

    def hidden_menu(self) -> list:
        """The menu routes the admin has hidden."""
        value = setting("menu_hidden", [])
        return list(value) if isinstance(value, list) else []

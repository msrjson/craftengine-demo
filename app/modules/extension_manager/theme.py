"""The theme chosen in the panel, persisted as a setting and cached briefly."""

import time
from typing import Any

#: Setting holding the chosen theme slug.
SETTING = "crm.theme"
#: Seconds a resolved theme is reused before the setting is read again.
CACHE_SECONDS = 5.0


class ThemeChoice:
    """Resolve the active theme: the panel's choice, else `view.theme` from config.

    Args:
        app: The application container.
    """

    def __init__(self, app: Any) -> None:
        self._app = app
        self._cached: tuple[float, str | None] | None = None

    def __call__(self) -> str | None:
        """Return the theme for this render (the view resolver contract)."""
        if self._cached and time.monotonic() - self._cached[0] < CACHE_SECONDS:
            return self._cached[1]
        chosen = self._app.make("setting").get(SETTING) or self._app.make("config").get("view.theme") or None
        self._cached = (time.monotonic(), chosen)
        return chosen

    def choose(self, slug: str) -> None:
        """Persist the chosen theme and use it from the next render."""
        self._app.make("setting").set(SETTING, slug, global_scope=True)
        self._cached = None

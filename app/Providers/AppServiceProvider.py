"""Application service provider.

The CRM itself lives in extensions (`app/modules`, `app/plugins`,
`app/themes`). This provider only offers the layout what every screen shares:
the menu, which each module contributes to through the `crm.navigation`
filter, so a deactivated module disappears from it without anyone editing the
layout.
"""

from typing import Any

from craft.providers import ServiceProvider
from craft.support.settings import setting


class AppServiceProvider(ServiceProvider):
    """Registers and boots this application's services."""

    def register(self) -> None:
        """Bind services into the container."""

    def boot(self) -> None:
        """Share the extension-built menu, honouring the hidden entries, with every template."""
        events = self.app.make("events")

        def navigation() -> list[dict[str, Any]]:
            hidden = set(setting("menu_hidden", []) or [])
            return [item for item in events.apply_filters("crm.navigation", []) if item.get("route") not in hidden]

        view = self.app.make("view")
        view.share("navigation", navigation)
        view.share("setting", setting)

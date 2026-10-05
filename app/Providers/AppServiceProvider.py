"""Application service provider.

The CRM itself lives in extensions (`app/modules`, `app/plugins`,
`app/themes`). This provider only offers the layout what every screen shares:
the menu, which each module contributes to through the `crm.navigation`
filter, so a deactivated module disappears from it without anyone editing the
layout.
"""

from typing import Any

from craft.providers import ServiceProvider


class AppServiceProvider(ServiceProvider):
    """Registers and boots this application's services."""

    def register(self) -> None:
        """Bind services into the container."""

    def boot(self) -> None:
        """Share the extension-built menu with every template."""
        events = self.app.make("events")

        def navigation() -> list[dict[str, Any]]:
            return events.apply_filters("crm.navigation", [])

        self.app.make("view").share("navigation", navigation)

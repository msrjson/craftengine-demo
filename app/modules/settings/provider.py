"""Wire the settings module into the CRM through the engine's seams only."""

from .services.settings_service import SettingsService


def register(context: object) -> None:
    """Bind the service and add the menu entries."""
    context.app.singleton(SettingsService, lambda c: SettingsService())
    context.filter("crm.navigation", lambda items: [*items, {"route": "settings.menus", "label_key": "settings.menus.nav"}], priority=97)
    context.filter("crm.navigation", lambda items: [*items, {"route": "settings.index", "label_key": "settings.nav.label"}], priority=99)

"""Wire the extension manager panel and the theme chosen in it."""

from .theme import ThemeChoice


def register(context: object) -> None:
    """Install the theme resolver and add the panel to the menu."""
    choice = ThemeChoice(context.app)
    context.app.instance("extension_manager.theme", choice)
    view = context.app.make("view")
    view.set_theme_resolver(choice)
    context.on_unload(lambda: view.set_theme_resolver(None))
    context.filter("crm.navigation", lambda items: [*items, {"route": "extension_manager.index", "label_key": "extension_manager.nav.label", "icon": "extensions"}], priority=90)

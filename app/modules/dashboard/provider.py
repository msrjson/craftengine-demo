"""Wire the dashboard into the menu."""


def register(context: object) -> None:
    """Add the dashboard as the first menu entry."""
    context.filter("crm.navigation", lambda items: [{"route": "dashboard.index", "label_key": "dashboard.nav.label", "icon": "dashboard"}, *items], priority=10)

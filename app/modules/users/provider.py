"""Wire the users module into the CRM through the engine's seams only."""

from .services.user_service import UserService


def register(context: object) -> None:
    """Bind the service and add the menu entry and dashboard card."""
    context.app.singleton(UserService, lambda c: UserService())
    context.filter("crm.navigation", lambda items: [*items, {"route": "users.index", "label_key": "users.nav.label"}], priority=95)
    context.filter(
        "crm.dashboard.cards",
        lambda cards: [*cards, {"label_key": "users.card.total", "value": context.app.make(UserService).count(), "route": "users.index"}],
        priority=95,
    )

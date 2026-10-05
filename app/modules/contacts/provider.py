"""Wire the contacts module into the CRM through the engine's seams only."""

from .repositories.contact_repository import ContactRepository
from .services.contact_service import ContactService


def register(context: object) -> None:
    """Bind the service, expose it, and add the menu entry and dashboard card."""
    context.app.singleton(ContactRepository, lambda c: ContactRepository())
    context.app.singleton(ContactService, lambda c: ContactService(c.make(ContactRepository)))
    context.expose("contacts", ContactService, {"names", "options", "exists", "count"})
    context.filter("crm.navigation", lambda items: [*items, {"route": "contacts.index", "label_key": "contacts.nav.label"}], priority=30)
    context.filter(
        "crm.dashboard.cards",
        lambda cards: [*cards, {"label_key": "contacts.card.label", "value": context.app.make(ContactService).count(), "route": "contacts.index"}],
        priority=30,
    )

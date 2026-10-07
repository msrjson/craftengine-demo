"""Wire the pages module into the CRM through the engine's seams only."""

from .repositories.page_repository import PageRepository
from .services.page_service import PageService


def register(context: object) -> None:
    """Bind the service, expose it, and add the menu entry and dashboard card."""
    context.app.singleton(PageRepository, lambda c: PageRepository())
    context.app.singleton(PageService, lambda c: PageService(c.make(PageRepository)))
    context.expose("pages", PageService, {"publish", "unpublish", "count_published"})
    context.filter("crm.navigation", lambda items: [*items, {"route": "pages.index", "label_key": "pages.nav.label"}], priority=16)
    context.filter(
        "crm.dashboard.cards",
        lambda cards: [*cards, {"label_key": "pages.card.published", "value": context.app.make(PageService).count_published(), "route": "pages.index"}],
        priority=16,
    )

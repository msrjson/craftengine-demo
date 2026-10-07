"""Wire the media module into the CRM through the engine's seams only."""

from .repositories.media_repository import MediaRepository
from .services.media_service import MediaService


def register(context: object) -> None:
    """Bind the service and add the menu entry and dashboard card."""
    context.app.singleton(MediaRepository, lambda c: MediaRepository())
    context.app.singleton(MediaService, lambda c: MediaService(c.make(MediaRepository)))
    context.filter("crm.navigation", lambda items: [*items, {"route": "media.index", "label_key": "media.nav.label", "icon": "media"}], priority=91)
    context.filter(
        "crm.dashboard.cards",
        lambda cards: [*cards, {"label_key": "media.card.total", "value": context.app.make(MediaService).count(), "route": "media.index"}],
        priority=91,
    )

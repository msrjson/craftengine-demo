"""Wire the posts module into the CRM through the engine's seams only."""

from .repositories.post_repository import PostRepository
from .services.post_service import PostService


def register(context: object) -> None:
    """Bind the service, expose it, and add the menu entry and dashboard card."""
    context.app.singleton(PostRepository, lambda c: PostRepository())
    context.app.singleton(PostService, lambda c: PostService(c.make(PostRepository)))
    context.expose("posts", PostService, {"draft", "publish", "unpublish", "count_published"})
    context.filter("crm.navigation", lambda items: [*items, {"route": "posts.index", "label_key": "posts.nav.label"}], priority=15)
    context.filter(
        "crm.dashboard.cards",
        lambda cards: [*cards, {"label_key": "posts.card.published", "value": context.app.make(PostService).count_published(), "route": "posts.index"}],
        priority=15,
    )

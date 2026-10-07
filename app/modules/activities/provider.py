"""Wire the activities module into the CRM through the engine's seams only."""

from .repositories.activity_repository import ActivityRepository
from .services.activity_service import ActivityService


def register(context: object) -> None:
    """Bind the service, react to won deals, add the menu entry and dashboard card."""
    context.app.singleton(ActivityRepository, lambda c: ActivityRepository())
    context.app.singleton(ActivityService, lambda c: ActivityService(c.make(ActivityRepository)))
    context.expose("activities", ActivityService, {"agenda", "contact_options", "schedule"})
    context.listen("crm.deal.won", lambda event: context.app.make(ActivityService).follow_up_won_deal(event))
    context.filter("crm.navigation", lambda items: [*items, {"route": "activities.index", "label_key": "activities.nav.label", "icon": "activities"}], priority=50)
    context.filter(
        "crm.dashboard.cards",
        lambda cards: [*cards, {"label_key": "activities.card.pending", "value": context.app.make(ActivityService).count_pending(), "route": "activities.index"}],
        priority=50,
    )

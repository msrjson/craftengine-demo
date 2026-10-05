"""Business rules of the activities module."""

from datetime import UTC, datetime, timedelta

from craft.container.internal_proxy import InternalProxyError
from craft.facades import Proxy

from ..repositories.activity_repository import ActivityRepository

#: Days after a deal is won before the follow-up call is due.
FOLLOW_UP_AFTER_DAYS = 2


class ActivityService:
    """Schedule, list and complete activities."""

    def __init__(self, repository: ActivityRepository) -> None:
        self.repository = repository

    def schedule(self, data: dict) -> int:
        """Create an activity from validated data and return its id."""
        return self.repository.create(data).get_attribute("id")

    def follow_up_won_deal(self, event: object) -> None:
        """Listener of `crm.deal.won`: schedule one follow-up call, never two."""
        deal_id = int(getattr(event, "deal_id"))
        if self.repository.follow_up_exists(deal_id):
            return
        due_at = (datetime.now(UTC) + timedelta(days=FOLLOW_UP_AFTER_DAYS)).isoformat()
        self.repository.create({
            "contact_id": int(getattr(event, "contact_id")), "deal_id": deal_id,
            "kind": "call", "source": "deal_won", "due_at": due_at,
        })

    def agenda(self) -> list[dict]:
        """Return the agenda with each activity's contact name."""
        activities = self.repository.agenda()
        names = _ask("contacts", "names", [a.get_attribute("contact_id") for a in activities], default={})
        return [{"activity": a, "contact": names.get(a.get_attribute("contact_id"), "")} for a in activities]

    def contact_options(self) -> list[dict]:
        """Return the contacts an activity may be about."""
        return _ask("contacts", "options", default=[])

    def complete(self, activity_id: int) -> bool:
        """Mark an activity done."""
        return self.repository.complete(activity_id)

    def count_pending(self) -> int:
        """Return the number of pending activities, for the dashboard."""
        return self.repository.count_pending()


def _ask(alias: str, method: str, *args: object, default: object) -> object:
    """Call another module through the proxy, degrading when it cannot serve.

    A module that is deactivated or out of service must not take this screen
    down with it: the screen renders without that module's data instead.
    """
    try:
        return Proxy.call(alias, method, *args)
    except InternalProxyError:
        return default

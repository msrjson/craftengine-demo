"""Every query of the activities module."""

from datetime import UTC, datetime

from ..models import Activity


class ActivityRepository:
    """Read and write activities; nothing else touches `crm_activities`."""

    def agenda(self) -> list[Activity]:
        """Return pending activities by due date, then the latest done ones."""
        pending = Activity.query().where("done_at", None).order_by("due_at").limit(100).get()
        done = Activity.query().where("done_at", "!=", None).order_by_desc("done_at").limit(20).get()
        return [*pending, *done]

    def create(self, data: dict) -> Activity:
        """Persist a new activity."""
        return Activity.create(data)

    def complete(self, activity_id: int) -> bool:
        """Stamp `done_at`; return False when the activity does not exist."""
        activity = Activity.find(activity_id)
        if activity is None:
            return False
        activity.update({"done_at": datetime.now(UTC).isoformat()})
        return True

    def follow_up_exists(self, deal_id: int) -> bool:
        """Return whether a won-deal follow-up was already scheduled."""
        return Activity.query().where("deal_id", deal_id).where("source", "deal_won").count() > 0

    def count_pending(self) -> int:
        """Return how many activities are still to do."""
        return Activity.query().where("done_at", None).count()

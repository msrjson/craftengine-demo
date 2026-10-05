"""Every query of the deals module."""

from datetime import UTC, datetime

from ..models import Deal


class DealRepository:
    """Read and write deals; nothing else touches `crm_deals`."""

    def all_open_and_recent(self) -> list[Deal]:
        """Return the deals the pipeline board shows, newest first."""
        return list(Deal.query().order_by_desc("id").limit(200).get())

    def create(self, data: dict) -> Deal:
        """Persist a new deal from validated data."""
        return Deal.create(data)

    def find(self, deal_id: int) -> Deal | None:
        """Return one deal, or None."""
        return Deal.find(deal_id)

    def move(self, deal: Deal, stage: str) -> Deal:
        """Set the deal's stage, stamping `won_at` when it is won."""
        changes = {"stage": stage}
        if stage == "won":
            changes["won_at"] = datetime.now(UTC).isoformat()
        deal.update(changes)
        return deal

    def won_total_cents(self, currency: str) -> int:
        """Return the sum of won deals in one currency."""
        return sum(int(d.get_attribute("amount_cents") or 0) for d in Deal.query().where("stage", "won").where("currency", currency).get())

    def count_open(self) -> int:
        """Return how many deals are still in the pipeline."""
        return Deal.query().where_in("stage", ["lead", "qualified", "proposal"]).count()

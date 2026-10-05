"""Events the deals module emits. Listeners match them by `name`, never by import."""

from dataclasses import dataclass


@dataclass(frozen=True)
class DealWon:
    """A deal reached the `won` stage.

    Attributes:
        deal_id: The deal.
        contact_id: Its contact, so a follow-up can be scheduled.
    """

    deal_id: int
    contact_id: int
    name: str = "crm.deal.won"

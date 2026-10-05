"""Business rules of the deals module; exposed on the proxy as `deals`."""

from decimal import Decimal, InvalidOperation

from craft.container.internal_proxy import InternalProxyError
from craft.facades import Proxy

from ..events import DealWon
from ..models import STAGES
from ..repositories.deal_repository import DealRepository


class InvalidAmountError(ValueError):
    """The amount is not a non-negative number with at most two decimals."""

    status_code = 422
    code = "DEALS_AMOUNT_INVALID"
    message_key = "deals.error.amount"


class UnknownDealError(LookupError):
    """The deal does not exist (or was deleted)."""

    status_code = 404
    code = "DEALS_DEAL_UNKNOWN"
    message_key = "deals.error.unknown"


class DealService:
    """Deals as the rest of the CRM sees them."""

    def __init__(self, repository: DealRepository, events: object) -> None:
        self.repository = repository
        self.events = events

    def create(self, data: dict) -> int:
        """Create a deal from form data (amount as a decimal string) and return its id."""
        record = {key: value for key, value in data.items() if key != "amount"}
        record["amount_cents"] = to_cents(str(data.get("amount", "0")))
        return self.repository.create(record).get_attribute("id")

    def move(self, deal_id: int, stage: str) -> None:
        """Move a deal to `stage`; announce it when the deal is won."""
        if stage not in STAGES:
            raise ValueError(stage)
        deal = self.repository.find(deal_id)
        if deal is None:
            raise UnknownDealError(deal_id)
        was_won = deal.get_attribute("stage") == "won"
        self.repository.move(deal, stage)
        if stage == "won" and not was_won:
            self.events.dispatch(DealWon(deal_id=int(deal_id), contact_id=int(deal.get_attribute("contact_id"))))

    def board(self) -> dict[str, list[dict]]:
        """Return the pipeline: each stage with its deals and their contact names."""
        deals = self.repository.all_open_and_recent()
        names = _ask("contacts", "names", [d.get_attribute("contact_id") for d in deals], default={})
        columns: dict[str, list[dict]] = {stage: [] for stage in STAGES}
        for deal in deals:
            columns[deal.get_attribute("stage")].append({"deal": deal, "contact": names.get(deal.get_attribute("contact_id"), "")})
        return columns

    def contact_options(self) -> list[dict]:
        """Return the contacts a deal may belong to."""
        return _ask("contacts", "options", default=[])

    def summary(self) -> dict:
        """Return the open count and the won total per currency, for the dashboard."""
        return {"open": self.repository.count_open(), "won_brl_cents": self.repository.won_total_cents("BRL")}


def to_cents(amount: str) -> int:
    """Turn `1234.5` / `1234,50` into integer cents; never a float.

    Raises:
        InvalidAmountError: Not a non-negative number with at most two decimals.
    """
    try:
        value = Decimal(amount.strip().replace(",", "."))
    except InvalidOperation as error:
        raise InvalidAmountError(amount) from error
    if value < 0 or value != value.quantize(Decimal("0.01")):
        raise InvalidAmountError(amount)
    return int(value * 100)


def _ask(alias: str, method: str, *args: object, default: object) -> object:
    """Call another module through the proxy, degrading when it cannot serve.

    A module that is deactivated or out of service must not take this screen
    down with it: the screen renders without that module's data instead.
    """
    try:
        return Proxy.call(alias, method, *args)
    except InternalProxyError:
        return default

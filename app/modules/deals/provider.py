"""Wire the deals module into the CRM through the engine's seams only."""

from craft.view.forge import active_locale

from .presenters import money
from .repositories.deal_repository import DealRepository
from .services.deal_service import DealService


def register(context: object) -> None:
    """Bind the service, expose it, and add the menu entry and dashboard cards."""
    context.app.singleton(DealRepository, lambda c: DealRepository())
    context.app.singleton(DealService, lambda c: DealService(c.make(DealRepository), c.make("events")))
    context.expose("deals", DealService, {"summary"})
    context.filter("crm.navigation", lambda items: [*items, {"route": "deals.index", "label_key": "deals.nav.label"}], priority=40)
    context.filter("crm.dashboard.cards", lambda cards: [*cards, *_cards(context)], priority=40)


def _cards(context: object) -> list[dict]:
    """Return the open-deals and won-revenue cards."""
    summary = context.app.make(DealService).summary()
    return [
        {"label_key": "deals.card.open", "value": summary["open"], "route": "deals.index"},
        {"label_key": "deals.card.won", "value": money(summary["won_brl_cents"], "BRL", active_locale()), "route": "deals.index"},
    ]

"""Wire the companies module into the CRM through the engine's seams only."""

from .repositories.company_repository import CompanyRepository
from .services.company_service import CompanyService


def register(context: object) -> None:
    """Bind the service, expose it, and add the menu entry and dashboard card."""
    context.app.singleton(CompanyRepository, lambda c: CompanyRepository())
    context.app.singleton(CompanyService, lambda c: CompanyService(c.make(CompanyRepository)))
    context.expose("companies", CompanyService, {"names", "options", "count"})
    context.filter("crm.navigation", _navigation, priority=20)
    context.filter("crm.dashboard.cards", lambda cards: [*cards, _card(context)], priority=20)


def _navigation(items: list) -> list:
    """Add the companies entry to the menu."""
    return [*items, {"route": "companies.index", "label_key": "companies.nav.label", "icon": "companies"}]


def _card(context: object) -> dict:
    """Return the dashboard card counting companies."""
    count = context.app.make(CompanyService).count()
    return {"label_key": "companies.card.label", "value": count, "route": "companies.index"}

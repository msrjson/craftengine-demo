"""Thin HTTP layer of the deals module."""

from typing import Any

from craft.http.controller import Controller
from craft.http.response import redirect
from craft.validation import Validator
from craft.view.forge import active_locale

from ..models import CURRENCIES, STAGES
from ..presenters import money
from ..services.deal_service import DealService

RULES = {
    "title": ["required", "string", "max:160"],
    "contact_id": ["required", "integer"],
    "amount": ["required", "regex:^[0-9]+([.,][0-9]{1,2})?$"],
    "currency": ["required", "in:" + ",".join(CURRENCIES)],
}


class DealController(Controller):
    """Show the pipeline, create deals and move them between stages."""

    def __init__(self, service: DealService) -> None:
        self.service = service

    def index(self, request: Any) -> Any:
        """Show the pipeline board."""
        locale = active_locale()
        board = {
            stage: [{**card, "amount": money(card["deal"].get_attribute("amount_cents"), card["deal"].get_attribute("currency"), locale)} for card in cards]
            for stage, cards in self.service.board().items()
        }
        return self.view("deals::index", {"board": board, "stages": STAGES})

    def create(self, request: Any) -> Any:
        """Show the new-deal form."""
        return self.view("deals::create", {"contacts": self.service.contact_options(), "currencies": CURRENCIES})

    def store(self, request: Any) -> Any:
        """Validate and save a deal, or return to the form with errors."""
        validator = Validator(request.all(), RULES)
        if validator.fails():
            return redirect.back(request).with_errors(validator).with_input(request.all())
        self.service.create(dict(validator.validated()))
        return redirect(route="deals.index")

    def move(self, request: Any, deal: int) -> Any:
        """Move a deal to the stage chosen on the board."""
        validator = Validator(request.all(), {"stage": ["required", "in:" + ",".join(STAGES)]})
        if validator.fails():
            return redirect.back(request).with_errors(validator)
        self.service.move(int(deal), validator.validated()["stage"])
        return redirect(route="deals.index")

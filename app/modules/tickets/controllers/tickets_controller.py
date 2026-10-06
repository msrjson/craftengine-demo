"""Thin HTTP controller of the tickets module."""

from craft.http.controller import Controller

from ..services.tickets_service import TicketsService


class TicketsController(Controller):
    """Translate HTTP into calls on `TicketsService` and back."""

    def __init__(self, service: TicketsService) -> None:
        self.service = service

    def index(self, request: object) -> object:
        """Render the module's start screen."""
        return self.view("tickets::index", {"summary": self.service.summary()})

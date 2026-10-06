"""Thin HTTP controller of the invoices module."""

from craft.http.controller import Controller

from ..services.invoices_service import InvoicesService


class InvoicesController(Controller):
    """Translate HTTP into calls on `InvoicesService` and back."""

    def __init__(self, service: InvoicesService) -> None:
        self.service = service

    def index(self, request: object) -> object:
        """Render the module's start screen."""
        return self.view("invoices::index", {"summary": self.service.summary()})

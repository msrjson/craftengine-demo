"""Wire the tickets module: bindings, listeners, filters and proxy exposures.

Everything goes through `context`, so deactivating the module undoes it in the
running process (ADR 0004).
"""

from .services.tickets_service import TicketsService


def register(context: object) -> None:
    """Bind the module's service and expose it to other modules.

    Args:
        context: The module's `ExtensionContext`.
    """
    context.app.singleton(TicketsService, lambda container: TicketsService())
    context.expose("tickets", TicketsService, {"summary", "open"})

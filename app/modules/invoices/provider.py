"""Wire the invoices module: bindings, listeners, filters and proxy exposures.

Everything goes through `context`, so deactivating the module undoes it in the
running process (ADR 0004).
"""

from .services.invoices_service import InvoicesService


def register(context: object) -> None:
    """Bind the module's service and expose it to other modules.

    Args:
        context: The module's `ExtensionContext`.
    """
    context.app.singleton(InvoicesService, lambda container: InvoicesService())
    context.expose("invoices", InvoicesService, {"summary", "issue"})

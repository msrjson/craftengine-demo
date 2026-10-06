"""HTTP routes of the invoices module; the engine tags each with the module's slug."""

from .controllers.invoices_controller import InvoicesController


def register(router: object) -> None:
    """Register the module's routes.

    Args:
        router: The application router.
    """
    router.get("/invoices", [InvoicesController, "index"]).name("invoices.index")
    # make:screen adds routes above this line.

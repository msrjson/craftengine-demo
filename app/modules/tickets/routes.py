"""HTTP routes of the tickets module; the engine tags each with the module's slug."""

from .controllers.tickets_controller import TicketsController


def register(router: object) -> None:
    """Register the module's routes.

    Args:
        router: The application router.
    """
    router.get("/tickets", [TicketsController, "index"]).name("tickets.index").middleware("auth")
    # make:screen adds routes above this line.

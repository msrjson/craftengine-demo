"""Routes of the deals module; the engine tags each with the slug."""

from .controllers.deal_controller import DealController


def register(router: object) -> None:
    """Register the module's screens, all behind sign-in."""
    router.get("/deals", [DealController, "index"]).name("deals.index").middleware("auth")
    router.get("/deals/create", [DealController, "create"]).name("deals.create").middleware("auth")
    router.post("/deals", [DealController, "store"]).name("deals.store").middleware("auth")
    router.post("/deals/{deal}/stage", [DealController, "move"]).name("deals.move").middleware("auth")

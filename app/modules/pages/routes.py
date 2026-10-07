"""Routes of the pages module; the engine tags each with the slug."""

from .controllers.page_controller import PageController


def register(router: object) -> None:
    """Register the module's screens, all behind sign-in."""
    router.get("/pages", [PageController, "index"]).name("pages.index").middleware("auth")
    router.get("/pages/create", [PageController, "create"]).name("pages.create").middleware("auth")
    router.post("/pages", [PageController, "store"]).name("pages.store").middleware("auth")
    router.get("/pages/{page}/edit", [PageController, "edit"]).name("pages.edit").middleware("auth")
    router.post("/pages/{page}", [PageController, "update"]).name("pages.update").middleware("auth")
    router.post("/pages/{page}/publish", [PageController, "publish"]).name("pages.publish").middleware("auth")

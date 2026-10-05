"""Routes of the activities module; the engine tags each with the slug."""

from .controllers.activity_controller import ActivityController


def register(router: object) -> None:
    """Register the module's screens, all behind sign-in."""
    router.get("/activities", [ActivityController, "index"]).name("activities.index").middleware("auth")
    router.get("/activities/create", [ActivityController, "create"]).name("activities.create").middleware("auth")
    router.post("/activities", [ActivityController, "store"]).name("activities.store").middleware("auth")
    router.post("/activities/{activity}/done", [ActivityController, "complete"]).name("activities.complete").middleware("auth")

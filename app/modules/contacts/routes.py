"""Routes of the contacts module; the engine tags each with the slug."""

from .controllers.contact_controller import ContactController


def register(router: object) -> None:
    """Register the module's screens, all behind sign-in."""
    router.get("/contacts", [ContactController, "index"]).name("contacts.index").middleware("auth")
    router.get("/contacts/create", [ContactController, "create"]).name("contacts.create").middleware("auth")
    router.post("/contacts", [ContactController, "store"]).name("contacts.store").middleware("auth")

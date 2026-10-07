"""Routes of the media module; the engine tags each with the slug."""

from .controllers.media_controller import MediaController


def register(router: object) -> None:
    """Register the module's screens, all behind sign-in."""
    router.get("/media", [MediaController, "index"]).name("media.index").middleware("auth")
    router.post("/media", [MediaController, "store"]).name("media.store").middleware("auth")
    router.get("/media/{media}/file", [MediaController, "show"]).name("media.file").middleware("auth")

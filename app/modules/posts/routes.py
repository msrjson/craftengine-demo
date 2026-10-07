"""Routes of the posts module; the engine tags each with the slug."""

from .controllers.post_controller import PostController


def register(router: object) -> None:
    """Register the module's screens, all behind sign-in."""
    router.get("/posts", [PostController, "index"]).name("posts.index").middleware("auth")
    router.get("/posts/create", [PostController, "create"]).name("posts.create").middleware("auth")
    router.post("/posts", [PostController, "store"]).name("posts.store").middleware("auth")
    router.get("/posts/{post}/edit", [PostController, "edit"]).name("posts.edit").middleware("auth")
    router.post("/posts/{post}", [PostController, "update"]).name("posts.update").middleware("auth")
    router.post("/posts/{post}/publish", [PostController, "publish"]).name("posts.publish").middleware("auth")

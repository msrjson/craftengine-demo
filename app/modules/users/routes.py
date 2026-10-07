"""Routes of the users module; administrators only."""

from .controllers.user_controller import UserController


def register(router: object) -> None:
    """Register the module's screens behind sign-in and the admin role."""
    router.get("/admin/users", [UserController, "index"]).name("users.index").middleware("auth", "role:admin")
    router.get("/admin/users/create", [UserController, "create"]).name("users.create").middleware("auth", "role:admin")
    router.post("/admin/users", [UserController, "store"]).name("users.store").middleware("auth", "role:admin")
    router.post("/admin/users/{user}/role", [UserController, "assign_role"]).name("users.role").middleware("auth", "role:admin")

"""Routes of the extension manager panel: administrators only."""

from .controllers.manager_controller import ManagerController


def register(router: object) -> None:
    """Register the panel behind sign-in and the admin role."""
    router.get("/admin/extensions", [ManagerController, "index"]).name("extension_manager.index").middleware("auth", "role:admin")
    router.post("/admin/extensions/theme", [ManagerController, "choose_theme"]).name("extension_manager.theme").middleware("auth", "role:admin")
    router.post("/admin/extensions/{slug}/{action}", [ManagerController, "act"]).name("extension_manager.act").middleware("auth", "role:admin")

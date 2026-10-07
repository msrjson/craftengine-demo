"""Routes of the settings module; administrators only."""

from .controllers.settings_controller import SettingsController


def register(router: object) -> None:
    """Register the module's screens behind sign-in and the admin role."""
    router.get("/admin/settings", [SettingsController, "index"]).name("settings.index").middleware("auth", "role:admin")
    router.post("/admin/settings", [SettingsController, "save"]).name("settings.save").middleware("auth", "role:admin")
    router.get("/admin/menus", [SettingsController, "menus"]).name("settings.menus").middleware("auth", "role:admin")
    router.post("/admin/menus", [SettingsController, "save_menus"]).name("settings.menus.save").middleware("auth", "role:admin")

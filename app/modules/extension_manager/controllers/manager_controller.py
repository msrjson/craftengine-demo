"""The extension manager panel: list, install, activate, deactivate, uninstall, choose a theme."""

from typing import Any

from craft.extensions.errors import ExtensionError
from craft.http.controller import Controller
from craft.http.response import redirect

#: Lifecycle actions the panel offers, mapped to the manager's methods.
ACTIONS = ("install", "activate", "deactivate", "uninstall")

#: The kinds the panel groups by, in the order it renders them.
KINDS = ("module", "plugin", "theme", "connector")


class ManagerController(Controller):
    """Thin HTTP layer over the engine's `ExtensionManager`."""

    def index(self, request: Any) -> Any:
        """Show every extension with its kind, version, state and health."""
        manager = self._manager()
        rows = manager.status()
        return self.view("extension_manager::index", {
            "groups": {kind: [row for row in rows if row["kind"] == kind] for kind in KINDS},
            "kinds": KINDS,
            "refused": [{"path": path, "code": error.code} for path, error in manager.discovery_errors.items()],
            "theme": self._theme()(),
        })

    def act(self, request: Any, slug: str, action: str) -> Any:
        """Run one lifecycle action; a refusal comes back as a translated reason."""
        if action not in ACTIONS:
            return redirect(route="extension_manager.index")
        try:
            getattr(self._manager(), action)(slug)
        except ExtensionError as refused:
            return redirect(route="extension_manager.index").with_errors({"extension": [refused.message_key], "slug": [slug], "detail": [refused.detail]})
        return redirect(route="extension_manager.index")

    def choose_theme(self, request: Any) -> Any:
        """Select an active theme as the CRM's look."""
        slug = str(request.input("theme", ""))
        themes = {row["slug"] for row in self._manager().status() if row["kind"] == "theme" and row["availability"] == "serving"}
        if slug in themes:
            self._theme().choose(slug)
        return redirect(route="extension_manager.index")

    def _manager(self) -> Any:
        from craft.container.application import Container

        return Container.getInstance().make("extensions")

    def _theme(self) -> Any:
        from craft.container.application import Container

        return Container.getInstance().make("extension_manager.theme")

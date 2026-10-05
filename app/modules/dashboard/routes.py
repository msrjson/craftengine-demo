"""Route of the dashboard module."""

from typing import Any

from craft.facades import View
from craft.http.response import Response


def show(request: Any) -> Response:
    """Render the cards every active module contributed."""
    from craft.container.application import Container

    cards = Container.getInstance().make("events").apply_filters("crm.dashboard.cards", [])
    return Response(View.render("dashboard::index", {"cards": cards}))


def register(router: object) -> None:
    """Register the dashboard, behind sign-in."""
    router.get("/dashboard", show).name("dashboard.index").middleware("auth")

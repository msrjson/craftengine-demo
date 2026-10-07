"""Routes of the dashboard module: the widgets and the quick draft."""

from typing import Any

from craft.container.internal_proxy import InternalProxyError
from craft.facades import Proxy, View
from craft.http.response import Response, redirect
from craft.validation import Validator

#: The kinds a quick draft may become, matching the activities module.
QUICK_DRAFT_KINDS = ("note", "call", "email", "meeting")

RULES = {
    "contact_id": ["required", "integer"],
    "kind": ["required", "in:" + ",".join(QUICK_DRAFT_KINDS)],
    "subject": ["required", "string", "min:2", "max:160"],
}


def show(request: Any) -> Response:
    """Render the widgets: module counts, the agenda and a quick draft."""
    from craft.container.application import Container

    cards = Container.getInstance().make("events").apply_filters("crm.dashboard.cards", [])
    return Response(View.render("dashboard::index", {
        "cards": cards,
        "activity": _ask("agenda", default=[]),
        "contacts": _ask("contact_options", default=[]),
        "kinds": QUICK_DRAFT_KINDS,
    }))


def save_draft(request: Any) -> Any:
    """Schedule a quick draft as an activity on the chosen contact."""
    validator = Validator(request.all(), RULES)
    if validator.fails():
        return redirect(route="dashboard.index").with_errors(validator).with_input(request.all())
    _ask("schedule", {k: v for k, v in validator.validated().items() if v not in ("", None)}, default=None)
    return redirect(route="dashboard.index")


def register(router: object) -> None:
    """Register the dashboard and its quick-draft action, behind sign-in."""
    router.get("/overview", show).name("dashboard.index").middleware("auth")
    router.post("/overview/draft", save_draft).name("dashboard.draft").middleware("auth")


def _ask(method: str, *args: Any, default: Any) -> Any:
    """Call the activities module through the proxy, degrading when it cannot serve.

    The dashboard shows whatever module can answer; a module that is off must
    not take the overview down.
    """
    try:
        return Proxy.call("activities", method, *args)
    except InternalProxyError:
        return default

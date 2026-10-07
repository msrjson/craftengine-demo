"""Routes of the dashboard module: the widgets and the quick draft."""

from typing import Any

from craft.container.internal_proxy import InternalProxyError
from craft.facades import Proxy, View
from craft.http.response import Response, redirect
from craft.validation import Validator

#: A quick draft becomes a post, exactly as WordPress's Quick Draft widget does.
RULES = {
    "title": ["required", "string", "min:2", "max:160"],
    "body": ["nullable", "string", "max:20000"],
}


def show(request: Any) -> Response:
    """Render the widgets: module counts, the agenda and a quick draft."""
    from craft.container.application import Container

    cards = Container.getInstance().make("events").apply_filters("crm.dashboard.cards", [])
    return Response(View.render("dashboard::index", {
        "cards": cards,
        "activity": _ask("activities", "agenda", default=[]),
        "drafts_ready": _probe("posts", "count_published") is not None,
    }))


def save_draft(request: Any) -> Any:
    """Save a quick draft as a post's draft, or return with the errors."""
    validator = Validator(request.all(), RULES)
    if validator.fails():
        return redirect(route="dashboard.index").with_errors(validator).with_input(request.all())
    validated = validator.validated()
    saved = _ask("posts", "draft", validated.get("title") or "", validated.get("body") or "", default=None)
    return redirect(route="posts.index") if saved is not None else redirect(route="dashboard.index")


def register(router: object) -> None:
    """Register the dashboard and its quick-draft action, behind sign-in."""
    router.get("/overview", show).name("dashboard.index").middleware("auth")
    router.post("/overview/draft", save_draft).name("dashboard.draft").middleware("auth")


def _ask(alias: str, method: str, *args: Any, default: Any) -> Any:
    """Call another module through the proxy, degrading when it cannot serve.

    The dashboard shows whatever module can answer; a module that is off must
    not take the overview down.
    """
    try:
        return Proxy.call(alias, method, *args)
    except InternalProxyError:
        return default


def _probe(alias: str, method: str) -> Any:
    """Return the call's result, or None when the module cannot serve."""
    return _ask(alias, method, default=None)

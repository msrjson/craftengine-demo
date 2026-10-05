"""The audit trail screen, for administrators only."""

from typing import Any

from craft.facades import DB, View
from craft.http.response import Response


def index(request: Any) -> Response:
    """Show the latest audit entries."""
    entries = DB.table("crm_audit_entries").order_by("id", "desc").limit(100).get()
    return Response(View.render("audit_log::index", {"entries": entries}))


def register(router: object) -> None:
    """Register the screen behind sign-in and the admin role."""
    router.get("/admin/audit", index).name("audit_log.index").middleware("auth", "role:admin")

"""Audit trail plugin: records who wrote what, as identifiers only.

Formerly the framework's bundled `plugins/audit-log`; moved to the demo as a
plugin extension. It stores the table, the record id and the acting user's id
- never an email or a payload - so the trail itself holds no personal data.
A failure to write an entry is contained by the extension's error boundary:
the business write that triggered it is never affected.
"""

from typing import Any

from craft.facades import DB

#: Its own table is never audited: auditing it would recurse forever.
IGNORED_TABLES = {"crm_audit_entries", "sessions", "translations", "extensions", "migrations"}


def register(context: Any) -> None:
    """Listen to model writes and authentication events."""
    for verb in ("created", "updated", "deleted"):
        context.listen(f"model.{verb}", _model_listener(context, verb))
    for name in ("auth.login", "auth.logout", "auth.failed"):
        context.listen(name, _auth_listener(context, name))


def _model_listener(context: Any, verb: str) -> Any:
    def record(event: Any) -> None:
        table = getattr(event, "table", None)
        if table in IGNORED_TABLES:
            return
        model = event.model
        _write(context, f"model.{verb}", table, model.get_attribute(model.primary_key))

    return record


def _auth_listener(context: Any, name: str) -> Any:
    def record(event: Any) -> None:
        user = getattr(event, "user", None)
        _write(context, name, "users", user.get_attribute(user.primary_key) if user is not None else None)

    return record


def _write(context: Any, event: str, table: str | None, record_id: Any) -> None:
    """Insert one entry; the error boundary contains any failure."""
    from datetime import UTC, datetime

    now = datetime.now(UTC).isoformat()
    DB.table("crm_audit_entries").insert({
        "event": event, "table_name": table, "record_id": None if record_id is None else str(record_id),
        "actor_id": _actor(context), "created_at": now, "updated_at": now,
    })


def _actor(context: Any) -> str | None:
    """Return the signed-in user's id, or None outside a signed-in request."""
    auth = context.app.make("auth")
    actor = auth.id() if auth.check() else None
    return None if actor is None else str(actor)

"""Activity digest plugin: counts the records other extensions create, without importing them.

It reacts to model events only, so it knows no module by name: a new module
that writes a `*_records` table is counted the moment it is active.
"""

from typing import Any


class Digest:
    """Per-table count of records created since the process started."""

    def __init__(self) -> None:
        self.counts: dict[str, int] = {}

    def note(self, table: str) -> None:
        """Count one created record of `table`."""
        self.counts[table] = self.counts.get(table, 0) + 1

    def snapshot(self) -> dict[str, int]:
        """Return a copy of the counts."""
        return dict(self.counts)


def register(context: Any) -> None:
    """Listen to created records and expose the digest on the internal proxy.

    Args:
        context: The plugin's `ExtensionContext`.
    """
    digest = Digest()
    context.app.instance(Digest, digest)

    def on_created(event: Any) -> None:
        table = getattr(event, "table", "")
        if table.endswith("_records"):
            digest.note(table)

    context.listen("model.created", on_created)
    context.expose("activity_digest", Digest, {"snapshot"})

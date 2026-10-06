"""Create the invoices records table (forward-only; rows are soft-deleted, never removed)."""

from craft.migrations import Schema


def up():
    Schema.create_table("invoices_records", lambda t: (
        t.id(),
        t.string("name"),
        t.timestamps(),
        t.soft_deletes(),
    ))

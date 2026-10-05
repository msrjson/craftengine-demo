"""Create the companies table (forward-only; rows are soft-deleted, never removed)."""

from craft.migrations import Schema


def up():
    Schema.create_table("crm_companies", lambda t: (
        t.id(),
        t.string("name"),
        t.string("website").nullable(),
        t.string("industry", 32).nullable(),
        t.timestamps(),
        t.soft_deletes(),
    ))

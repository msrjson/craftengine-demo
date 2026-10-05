"""Create the activities table (forward-only; rows are soft-deleted, never removed)."""

from craft.migrations import Schema


def up():
    Schema.create_table("crm_activities", lambda t: (
        t.id(),
        t.integer("contact_id"),
        t.integer("deal_id").nullable(),
        t.string("kind", 16),
        t.string("subject", 160).nullable(),
        t.string("source", 32).nullable(),
        t.timestamp("due_at").nullable(),
        t.timestamp("done_at").nullable(),
        t.timestamps(),
        t.soft_deletes(),
    ))

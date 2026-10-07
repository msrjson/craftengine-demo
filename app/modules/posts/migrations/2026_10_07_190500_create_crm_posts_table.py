"""Create the posts table (forward-only; rows are soft-deleted, never removed)."""

from craft.migrations import Schema


def up():
    Schema.create_table("crm_posts", lambda t: (
        t.id(),
        t.string("title", 160),
        t.text("body").nullable(),
        t.string("status", 16),
        t.integer("author_id").nullable(),
        t.timestamp("published_at").nullable(),
        t.timestamps(),
        t.soft_deletes(),
    ))

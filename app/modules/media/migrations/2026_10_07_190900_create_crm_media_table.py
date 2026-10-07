"""Create the media table (forward-only; rows are soft-deleted, never removed)."""

from craft.migrations import Schema


def up():
    Schema.create_table("crm_media", lambda t: (
        t.id(),
        t.string("name", 160),
        t.string("original_name", 200),
        t.string("mime", 100).nullable(),
        t.integer("size"),
        t.string("disk", 32),
        t.string("path", 255),
        t.integer("uploaded_by").nullable(),
        t.timestamps(),
        t.soft_deletes(),
    ))

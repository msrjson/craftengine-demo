"""Create the contacts table (forward-only; rows are soft-deleted, never removed)."""

from craft.migrations import Schema


def up():
    Schema.create_table("crm_contacts", lambda t: (
        t.id(),
        t.integer("company_id").nullable(),
        t.string("first_name", 80),
        t.string("last_name", 80),
        t.string("email").nullable(),
        t.string("phone", 40).nullable(),
        t.timestamps(),
        t.soft_deletes(),
    ))

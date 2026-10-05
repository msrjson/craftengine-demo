"""Create the deals table: money as integer minor units plus an ISO-4217 code."""

from craft.migrations import Schema


def up():
    Schema.create_table("crm_deals", lambda t: (
        t.id(),
        t.integer("contact_id"),
        t.string("title", 160),
        t.big_integer("amount_cents").default(0),
        t.char("currency", 3).default("BRL"),
        t.string("stage", 16).default("lead"),
        t.timestamp("won_at").nullable(),
        t.timestamps(),
        t.soft_deletes(),
    ))

"""Create the outbound_webhooks delivery log (forward-only; append-only rows)."""

from craft.migrations import Schema


def up():
    Schema.create_table("outbound_webhooks_deliveries", lambda t: (
        t.id(),
        t.string("event"),
        t.string("status", 32),
        t.timestamps(),
    ))

"""Create the audit trail table: identifiers only, never personal data (LGPD/GDPR)."""

from craft.migrations import Schema


def up():
    Schema.create_table("crm_audit_entries", lambda t: (
        t.id(),
        t.string("event", 32),
        t.string("table_name", 64).nullable(),
        t.string("record_id", 64).nullable(),
        t.string("actor_id", 64).nullable(),
        t.timestamps(),
    ))

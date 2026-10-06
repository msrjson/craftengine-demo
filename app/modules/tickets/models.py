"""The record of the tickets module."""

from craft.orm import Model, SoftDeletes


class TicketsRecord(SoftDeletes, Model):
    """A row of `tickets_records`. Deleting it only stamps `deleted_at`."""

    __table__ = "tickets_records"
    fillable = ["name"]

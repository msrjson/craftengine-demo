"""The record of the invoices module."""

from craft.orm import Model, SoftDeletes


class InvoicesRecord(SoftDeletes, Model):
    """A row of `invoices_records`. Deleting it only stamps `deleted_at`."""

    __table__ = "invoices_records"
    fillable = ["name"]

"""The contact record of the contacts module."""

from craft.orm import Model, SoftDeletes


class Contact(SoftDeletes, Model):
    """A person the sales team talks to. Deleting it only stamps `deleted_at`."""

    __table__ = "crm_contacts"
    fillable = ["company_id", "first_name", "last_name", "email", "phone"]

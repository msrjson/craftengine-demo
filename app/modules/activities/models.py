"""The activity record of the activities module."""

from craft.orm import Model, SoftDeletes

#: Activity kinds; persisted values, labels are `activities.kind.<value>`.
KINDS = ("call", "email", "meeting", "note")


class Activity(SoftDeletes, Model):
    """Something to do with a contact. Deleting it only stamps `deleted_at`."""

    __table__ = "crm_activities"
    fillable = ["contact_id", "deal_id", "kind", "subject", "source", "due_at"]

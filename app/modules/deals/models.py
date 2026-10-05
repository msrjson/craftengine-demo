"""The deal record and the pipeline it moves through."""

from craft.orm import Model, SoftDeletes

#: Pipeline stages, in order; persisted values, labels are `deals.stage.<value>`.
STAGES = ("lead", "qualified", "proposal", "won", "lost")

#: Currencies a deal may be priced in (ISO 4217).
CURRENCIES = ("BRL", "USD", "EUR")


class Deal(SoftDeletes, Model):
    """A sales opportunity with one contact. Deleting it only stamps `deleted_at`."""

    __table__ = "crm_deals"
    fillable = ["contact_id", "title", "amount_cents", "currency", "stage"]

"""The delivery log of the outbound_webhooks connector."""

from craft.orm import Model


class OutboundWebhooksDelivery(Model):
    """One attempt to deliver an event; rows are append-only."""

    __table__ = "outbound_webhooks_deliveries"
    fillable = ["event", "status"]

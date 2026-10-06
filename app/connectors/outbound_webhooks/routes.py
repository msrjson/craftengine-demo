"""Inbound side of the outbound_webhooks connector: the receiver acknowledges deliveries.

Under `api/` so the CSRF check, meant for browser forms, does not apply.
"""


def register(router: object) -> None:
    """Register the acknowledgement endpoint.

    Args:
        router: The application router.
    """
    router.post("/api/webhooks/outbound-webhooks/ack", lambda: {"acknowledged": True}).name("outbound_webhooks.ack")

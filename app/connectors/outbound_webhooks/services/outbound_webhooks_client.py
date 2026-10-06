"""The outbound side of the outbound_webhooks connector."""

from collections.abc import Callable
from typing import Any

from ..models import OutboundWebhooksDelivery

Transport = Callable[[str, dict[str, Any]], dict[str, Any]]


def _not_configured(event: str, payload: dict[str, Any]) -> dict[str, Any]:
    """Default transport: talks to nobody, so a fresh connector never reaches the network."""
    return {"status": "not_configured"}


class OutboundWebhooksClient:
    """Delivers events to the outside service and records every attempt.

    Args:
        transport: Callable doing the actual call. Inject a real one at boot
            (through the provider) and a fake in tests.
    """

    def __init__(self, transport: Transport = _not_configured) -> None:
        self._transport = transport

    def deliver(self, event: str, payload: dict[str, Any]) -> dict[str, Any]:
        """Send one event and log the outcome in `outbound_webhooks_deliveries`.

        Args:
            event: Machine name of the event, e.g. `order.paid`.
            payload: Data to send; never a rendered sentence.

        Returns:
            The transport's answer, always carrying a `status`.
        """
        answer = self._transport(event, payload)
        OutboundWebhooksDelivery.create({"event": event, "status": str(answer.get("status", "unknown"))})
        return answer

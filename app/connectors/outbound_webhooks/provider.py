"""Wire the outbound_webhooks connector: it forwards created records to the outside.

The client has no network transport until the application injects one, so a
fresh install never reaches out. Reactions go through model events; no module
is imported.
"""

from typing import Any

from .services.outbound_webhooks_client import OutboundWebhooksClient


def register(context: Any) -> None:
    """Bind the client, forward created records and expose `deliver`.

    Args:
        context: The connector's `ExtensionContext`.
    """
    client = OutboundWebhooksClient()
    context.app.instance(OutboundWebhooksClient, client)

    def on_created(event: Any) -> None:
        table = getattr(event, "table", "")
        if table.endswith("_records"):
            client.deliver("record.created", {"table": table})

    context.listen("model.created", on_created)
    context.expose("outbound_webhooks", OutboundWebhooksClient, {"deliver"})

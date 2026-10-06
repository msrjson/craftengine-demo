"""Business rules of the tickets module."""

from ..models import TicketsRecord


class TicketsService:
    """The module's domain logic; exposed on the internal proxy as `tickets`."""

    def open(self, name: str) -> int:
        """Create one record and return its id.

        Args:
            name: Short title of the record.

        Returns:
            The new record's id.

        Raises:
            ValueError: `name` is blank.
        """
        if not name.strip():
            raise ValueError("tickets_name_required")
        return int(TicketsRecord.create({"name": name.strip()}).get_attribute("id"))

    def summary(self) -> dict:
        """Return the data the start screen shows.

        Returns:
            A mapping the view renders; never a rendered sentence.
        """
        return {"items": TicketsRecord.query().count()}

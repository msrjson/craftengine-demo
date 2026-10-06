"""Business rules of the invoices module."""

from ..models import InvoicesRecord


class InvoicesService:
    """The module's domain logic; exposed on the internal proxy as `invoices`."""

    def issue(self, name: str) -> int:
        """Create one record and return its id.

        Args:
            name: Short title of the record.

        Returns:
            The new record's id.

        Raises:
            ValueError: `name` is blank.
        """
        if not name.strip():
            raise ValueError("invoices_name_required")
        return int(InvoicesRecord.create({"name": name.strip()}).get_attribute("id"))

    def summary(self) -> dict:
        """Return the data the start screen shows.

        Returns:
            A mapping the view renders; never a rendered sentence.
        """
        return {"items": InvoicesRecord.query().count()}

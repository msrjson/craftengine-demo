"""Every query of the contacts module."""

from typing import Any

from ..models import Contact


class ContactRepository:
    """Read and write contacts; nothing else touches `crm_contacts`."""

    def paginate(self, page: int) -> Any:
        """Return one page of contacts, newest first."""
        return Contact.query().order_by_desc("id").paginate(per_page=20, page=page)

    def create(self, data: dict) -> Contact:
        """Persist a new contact from validated data."""
        return Contact.create(data)

    def find(self, contact_id: int) -> Contact | None:
        """Return one contact, or None."""
        return Contact.find(contact_id)

    def names(self, ids: list[int]) -> dict[int, str]:
        """Return the full name of each contact id that exists."""
        if not ids:
            return {}
        rows = Contact.query().where_in("id", ids).get()
        return {row.get_attribute("id"): _full_name(row) for row in rows}

    def options(self) -> list[dict]:
        """Return every contact as an option for a select field."""
        rows = Contact.query().order_by("first_name").get()
        return [{"id": row.get_attribute("id"), "name": _full_name(row)} for row in rows]

    def count(self) -> int:
        """Return how many contacts exist."""
        return Contact.query().count()


def _full_name(contact: Contact) -> str:
    """Return the contact's name as stored: data, not copy."""
    return " ".join(part for part in (contact.get_attribute("first_name"), contact.get_attribute("last_name")) if part)

"""Business rules of the contacts module; exposed on the proxy as `contacts`."""

from craft.container.internal_proxy import InternalProxyError
from craft.facades import Proxy

from ..repositories.contact_repository import ContactRepository


class ContactService:
    """Contacts as the rest of the CRM sees them."""

    def __init__(self, repository: ContactRepository) -> None:
        self.repository = repository

    def create(self, data: dict) -> int:
        """Create a contact and return its id."""
        return self.repository.create(data).get_attribute("id")

    def rows(self, contacts: list) -> list[dict]:
        """Return contacts with their company name, asked from the companies module."""
        company_names = _ask("companies", "names", [c.get_attribute("company_id") for c in contacts], default={})
        return [{"contact": c, "company": company_names.get(c.get_attribute("company_id"), "")} for c in contacts]

    def company_options(self) -> list[dict]:
        """Return the companies a contact may belong to."""
        return _ask("companies", "options", default=[])

    def names(self, ids: list[int]) -> dict[int, str]:
        """Return contact names by id, for other modules' screens."""
        return self.repository.names(sorted({int(i) for i in ids if i}))

    def options(self) -> list[dict]:
        """Return the contacts a form may link to."""
        return self.repository.options()

    def exists(self, contact_id: int) -> bool:
        """Return whether a contact exists, for other modules' validation."""
        return self.repository.find(int(contact_id)) is not None

    def count(self) -> int:
        """Return the number of contacts, for the dashboard."""
        return self.repository.count()


def _ask(alias: str, method: str, *args: object, default: object) -> object:
    """Call another module through the proxy, degrading when it cannot serve.

    A module that is deactivated or out of service must not take this screen
    down with it: the screen renders without that module's data instead.
    """
    try:
        return Proxy.call(alias, method, *args)
    except InternalProxyError:
        return default

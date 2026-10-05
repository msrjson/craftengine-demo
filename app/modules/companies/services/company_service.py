"""Business rules of the companies module; exposed on the proxy as `companies`."""

from ..models import INDUSTRIES
from ..repositories.company_repository import CompanyRepository


class CompanyService:
    """Companies as the rest of the CRM sees them."""

    def __init__(self, repository: CompanyRepository) -> None:
        self.repository = repository

    def create(self, data: dict) -> int:
        """Create a company and return its id."""
        return self.repository.create(data).get_attribute("id")

    def names(self, ids: list[int]) -> dict[int, str]:
        """Return company names by id, for other modules' screens."""
        return self.repository.names(sorted({int(i) for i in ids if i}))

    def options(self) -> list[dict]:
        """Return the companies a form may link to."""
        return self.repository.options()

    def count(self) -> int:
        """Return the number of companies, for the dashboard."""
        return self.repository.count()

    @staticmethod
    def industries() -> tuple[str, ...]:
        """Return the industry values a company may have."""
        return INDUSTRIES

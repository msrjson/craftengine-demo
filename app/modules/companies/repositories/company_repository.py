"""Every query of the companies module."""

from typing import Any

from ..models import Company


class CompanyRepository:
    """Read and write companies; nothing else touches `crm_companies`."""

    def paginate(self, page: int) -> Any:
        """Return one page of companies, newest first."""
        return Company.query().order_by_desc("id").paginate(per_page=20, page=page)

    def create(self, data: dict) -> Company:
        """Persist a new company from validated data."""
        return Company.create(data)

    def names(self, ids: list[int]) -> dict[int, str]:
        """Return the name of each company id that exists."""
        if not ids:
            return {}
        return {company.get_attribute("id"): company.get_attribute("name") for company in Company.query().where_in("id", ids).get()}

    def options(self) -> list[dict]:
        """Return every company as an option for a select field."""
        return [{"id": c.get_attribute("id"), "name": c.get_attribute("name")} for c in Company.query().order_by("name").get()]

    def count(self) -> int:
        """Return how many companies exist."""
        return Company.query().count()

"""Business rules of the pages module; exposed on the proxy as `pages`."""

from datetime import UTC, datetime

from ..repositories.page_repository import PageRepository

#: The status a published page carries.
PUBLISHED = "published"
DRAFT = "draft"


class PageService:
    """Pages as the rest of the CRM sees them."""

    def __init__(self, repository: PageRepository) -> None:
        self.repository = repository

    def save(self, data: dict, page_id: int | None = None) -> int:
        """Create or update a page and return its id."""
        status = data.get("status") or DRAFT
        data["status"] = status
        data["published_at"] = datetime.now(UTC).isoformat() if status == PUBLISHED else None
        if page_id is None:
            return self.repository.create(data).get_attribute("id")
        page = self.repository.find(page_id)
        if page is None:
            return page_id
        self.repository.update(page, data)
        return page_id

    def publish(self, page_id: int) -> bool:
        """Mark a page published; return False when it does not exist."""
        page = self.repository.find(page_id)
        if page is None:
            return False
        self.repository.update(page, {"status": PUBLISHED, "published_at": datetime.now(UTC).isoformat()})
        return True

    def unpublish(self, page_id: int) -> bool:
        """Return a page to draft; return False when it does not exist."""
        page = self.repository.find(page_id)
        if page is None:
            return False
        self.repository.update(page, {"status": DRAFT, "published_at": None})
        return True

    def count_published(self) -> int:
        """Return the number of published pages, for the dashboard."""
        return self.repository.count_published()

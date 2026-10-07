"""Every query of the pages module."""

from typing import Any, Optional

from ..models import Page


class PageRepository:
    """Read and write pages; nothing else touches `crm_pages`."""

    def paginate(self, page: int) -> Any:
        """Return one page of pages, newest first."""
        return Page.query().order_by_desc("id").paginate(per_page=20, page=page)

    def create(self, data: dict) -> Page:
        """Persist a new page from validated data."""
        return Page.create(data)

    def find(self, page_id: int) -> Optional[Page]:
        """Return a page by id, or None."""
        return Page.find(int(page_id))

    def update(self, page: Page, data: dict) -> Page:
        """Apply validated changes to a page."""
        page.update(data)
        return page

    def count_published(self) -> int:
        """Return how many pages are published, for the dashboard."""
        return Page.query().where("status", "published").count()

"""Thin HTTP layer of the pages module."""

from typing import Any

from craft.facades import Auth
from craft.http.controller import Controller
from craft.http.response import redirect
from craft.validation import Validator

from ..models import STATUSES
from ..repositories.page_repository import PageRepository
from ..services.page_service import PageService

RULES = {
    "title": ["required", "string", "min:2", "max:160"],
    "body": ["nullable", "string", "max:20000"],
    "status": ["nullable", "in:" + ",".join(STATUSES)],
}


class PageController(Controller):
    """List, write and publish pages."""

    def __init__(self, service: PageService, repository: PageRepository) -> None:
        self.service = service
        self.repository = repository

    def index(self, request: Any) -> Any:
        """Show one page of pages."""
        rows = self.repository.paginate(int(request.input("page", 1) or 1))
        return self.view("pages::index", {"pages": list(rows), "pagination": rows.pagination})

    def create(self, request: Any) -> Any:
        """Show the editor for a new page."""
        return self.view("pages::create", {"page": None, "statuses": STATUSES})

    def store(self, request: Any) -> Any:
        """Validate and save a new page, or return to the editor with errors."""
        validator = Validator(request.all(), RULES)
        if validator.fails():
            return redirect.back(request).with_errors(validator).with_input(request.all())
        data = dict(validator.validated())
        data["author_id"] = Auth.id()
        self.service.save(data)
        return redirect(route="pages.index")

    def edit(self, request: Any, page: int) -> Any:
        """Show the editor for an existing page."""
        found = self.repository.find(int(page))
        if found is None:
            return redirect(route="pages.index")
        return self.view("pages::edit", {"page": found, "statuses": STATUSES})

    def update(self, request: Any, page: int) -> Any:
        """Validate and save changes to a page."""
        validator = Validator(request.all(), RULES)
        if validator.fails():
            return redirect.back(request).with_errors(validator).with_input(request.all())
        self.service.save(validator.validated(), page_id=int(page))
        return redirect(route="pages.index")

    def publish(self, request: Any, page: int) -> Any:
        """Publish a page, or return it to draft when the form asks for that."""
        if str(request.input("action", "")) == "draft":
            self.service.unpublish(int(page))
        else:
            self.service.publish(int(page))
        return redirect(route="pages.index")

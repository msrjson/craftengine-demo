"""Thin HTTP layer of the contacts module."""

from typing import Any

from craft.http.controller import Controller
from craft.http.response import redirect
from craft.validation import Validator

from ..repositories.contact_repository import ContactRepository
from ..services.contact_service import ContactService

RULES = {
    "first_name": ["required", "string", "max:80"],
    "last_name": ["required", "string", "max:80"],
    "email": ["nullable", "email", "max:255"],
    "phone": ["nullable", "string", "max:40"],
    "company_id": ["nullable", "integer"],
}


class ContactController(Controller):
    """List and create contacts."""

    def __init__(self, service: ContactService, repository: ContactRepository) -> None:
        self.service = service
        self.repository = repository

    def index(self, request: Any) -> Any:
        """Show one page of contacts with their companies."""
        page = self.repository.paginate(int(request.input("page", 1) or 1))
        return self.view("contacts::index", {"rows": self.service.rows(list(page)), "pagination": page.pagination})

    def create(self, request: Any) -> Any:
        """Show the new-contact form."""
        return self.view("contacts::create", {"companies": self.service.company_options()})

    def store(self, request: Any) -> Any:
        """Validate and save a contact, or return to the form with errors."""
        validator = Validator(request.all(), RULES)
        if validator.fails():
            return redirect.back(request).with_errors(validator).with_input(request.all())
        data = {key: value for key, value in validator.validated().items() if value not in ("", None)}
        self.service.create(data)
        return redirect(route="contacts.index")

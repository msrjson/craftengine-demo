"""Thin HTTP layer of the companies module."""

from typing import Any

from craft.http.controller import Controller
from craft.http.response import redirect
from craft.validation import Validator

from ..models import INDUSTRIES
from ..repositories.company_repository import CompanyRepository
from ..services.company_service import CompanyService

RULES = {
    "name": ["required", "string", "max:120"],
    "website": ["nullable", "url", "max:255"],
    "industry": ["nullable", "in:" + ",".join(INDUSTRIES)],
}


class CompanyController(Controller):
    """List and create companies."""

    def __init__(self, service: CompanyService, repository: CompanyRepository) -> None:
        self.service = service
        self.repository = repository

    def index(self, request: Any) -> Any:
        """Show one page of companies."""
        page = self.repository.paginate(int(request.input("page", 1) or 1))
        return self.view("companies::index", {"companies": list(page), "pagination": page.pagination})

    def create(self, request: Any) -> Any:
        """Show the new-company form."""
        return self.view("companies::create", {"industries": INDUSTRIES})

    def store(self, request: Any) -> Any:
        """Validate and save a company, or return to the form with errors."""
        validator = Validator(request.all(), RULES)
        if validator.fails():
            return redirect.back(request).with_errors(validator).with_input(request.all())
        self.service.create(validator.validated())
        return redirect(route="companies.index")

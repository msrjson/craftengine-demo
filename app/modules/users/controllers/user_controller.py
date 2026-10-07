"""Thin HTTP layer of the users module."""

from typing import Any, Optional

from craft.http.controller import Controller
from craft.http.response import redirect
from craft.validation import Validator

from ..services.user_service import UserService

RULES = {
    "name": ["required", "string", "min:2", "max:100"],
    "email": ["required", "email", "unique:users,email"],
    "password": ["required", "string", "min:8", "confirmed"],
}


class UserController(Controller):
    """List, create and re-role the CRM's accounts."""

    def __init__(self, service: UserService) -> None:
        self.service = service

    def index(self, request: Any) -> Any:
        """Show every account with its roles."""
        rows = [{"user": user, "roles": self.service.role_names(user)} for user in self.service.users()]
        return self.view("users::index", {"rows": rows, "roles": self.service.roles()})

    def create(self, request: Any) -> Any:
        """Show the new-user form."""
        return self.view("users::create", {"roles": self.service.roles()})

    def store(self, request: Any) -> Any:
        """Validate and create an account, or return to the form with errors."""
        validator = Validator(request.all(), RULES)
        if validator.fails():
            return redirect.back(request).with_errors(validator).with_input(request.all())
        self.service.create(validator.validated(), self._role_id(request))
        return redirect(route="users.index")

    def assign_role(self, request: Any, user: int) -> Any:
        """Replace one account's role."""
        role_id = self._role_id(request)
        if role_id is not None:
            self.service.assign_role(int(user), role_id)
        return redirect(route="users.index")

    def _role_id(self, request: Any) -> Optional[int]:
        """The chosen role's id, or None when no role was selected."""
        from app.Models.Role import Role

        raw = request.input("role_id")
        if raw in (None, "", "0"):
            return None
        role = Role.find(int(raw))
        return None if role is None else role.get_attribute("id")

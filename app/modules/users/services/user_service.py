"""Administration of the CRM's accounts, on top of the RBAC models.

The module owns no table: it reads `app/Models/User.py` and `app/Models/Role.py`
and the `role_user` pivot, the same models the `role:` middleware checks.
"""

from typing import Any, Optional


class UserService:
    """List, create and re-role users; a password is never handled in clear text."""

    def create(self, data: dict, role_id: Optional[int] = None) -> int:
        """Create a user (the auth mixin hashes the password) and set one role."""
        user = self._user_model().create({
            "name": data["name"],
            "email": data["email"],
            "password": data["password"],
        })
        if role_id is not None:
            user.roles().sync([role_id])
        return user.get_attribute("id")

    def assign_role(self, user_id: int, role_id: int) -> bool:
        """Replace a user's roles with the one given; False when it does not exist."""
        user = self._user_model().find(int(user_id))
        if user is None:
            return False
        user.roles().sync([role_id])
        return True

    def users(self) -> list[Any]:
        """Return every account, by name."""
        return self._user_model().query().order_by("name").get()

    def roles(self) -> list[Any]:
        """Return every role a user may be given, by name."""
        return self._role_model().query().order_by("name").get()

    def role_names(self, user: Any) -> list[str]:
        """Return the names of the roles assigned to a user."""
        return [role.get_attribute("name") for role in user.roles().get()]

    def count(self) -> int:
        """Return the number of accounts, for the dashboard."""
        return self._user_model().query().count()

    @staticmethod
    def _user_model() -> Any:
        from app.Models.User import User

        return User

    @staticmethod
    def _role_model() -> Any:
        from app.Models.Role import Role

        return Role

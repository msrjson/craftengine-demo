from app.Http.Controllers.Auth.AuthController import AuthController
"""Web routes of the CRM shell.

Every screen of the CRM belongs to an extension under `app/modules`; this file
only sends the home page to the dashboard module. `craft route:list` shows
every route, the extensions' included.
"""

from typing import Any

from craft.facades import Route
from craft.http.response import redirect


def home(request: Any) -> Any:
    """Send the visitor to the CRM overview (which asks them to sign in first)."""
    return redirect("/overview")


Route.get("/", home).name("home")

# Authentication Routes (Scaffolded by make:auth)
Route.get("/login", [AuthController, "show_login"]).name("login")
Route.get("/signin", [AuthController, "show_signin"])
Route.post("/login", [AuthController, "login"]).middleware("throttle").name("login.attempt")
Route.get("/register", [AuthController, "show_register"]).name("register")
Route.post("/register", [AuthController, "register"]).middleware("throttle").name("register.store")
Route.post("/logout", [AuthController, "logout"]).name("logout")
Route.get("/dashboard", [AuthController, "dashboard"]).middleware("auth").name("dashboard")

# Admin Panel Routes (make:admin)
from app.Http.Controllers.Admin.CrudBuilderController import CrudBuilderController
from app.Http.Controllers.Admin.GroupController import GroupController
from app.Http.Controllers.Admin.HomeController import HomeController
from app.Http.Controllers.Admin.RoleController import PermissionController, RoleController

Route.get("/admin", [HomeController, "admin"]).middleware("auth", "role:admin").name("admin.dashboard")
Route.get("/admin/crud-builder", [CrudBuilderController, "index"]).middleware("auth", "role:admin").name(
    "admin.crud_builder.index"
)
Route.post("/admin/crud-builder", [CrudBuilderController, "store"]).middleware("auth", "role:admin").name(
    "admin.crud_builder.store"
)
Route.get("/admin/roles", [RoleController, "index"]).middleware("auth", "role:admin").name("admin.roles.index")
Route.post("/admin/roles/grant", [RoleController, "grant"]).middleware("auth", "role:admin").name("admin.roles.grant")
Route.get("/admin/permissions", [PermissionController, "index"]).middleware("auth", "role:admin").name(
    "admin.permissions.index"
)
Route.get("/admin/groups", [GroupController, "index"]).middleware("auth", "role:admin").name("admin.groups.index")
Route.post("/admin/groups", [GroupController, "store"]).middleware("auth", "role:admin").name("admin.groups.store")
Route.post("/admin/groups/members", [GroupController, "add_member"]).middleware("auth", "role:admin").name(
    "admin.groups.members"
)
Route.post("/admin/groups/roles", [GroupController, "grant_role"]).middleware("auth", "role:admin").name(
    "admin.groups.roles"
)
Route.post("/admin/groups/permissions", [GroupController, "grant_permission"]).middleware("auth", "role:admin").name(
    "admin.groups.permissions"
)

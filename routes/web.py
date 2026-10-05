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

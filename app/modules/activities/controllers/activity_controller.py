"""Thin HTTP layer of the activities module."""

from typing import Any

from craft.http.controller import Controller
from craft.http.response import redirect
from craft.validation import Validator

from ..models import KINDS
from ..services.activity_service import ActivityService

RULES = {
    "contact_id": ["required", "integer"],
    "kind": ["required", "in:" + ",".join(KINDS)],
    "subject": ["nullable", "string", "max:160"],
    "due_at": ["nullable", "date"],
}


class ActivityController(Controller):
    """Show the agenda, schedule and complete activities."""

    def __init__(self, service: ActivityService) -> None:
        self.service = service

    def index(self, request: Any) -> Any:
        """Show the agenda."""
        return self.view("activities::index", {"rows": self.service.agenda()})

    def create(self, request: Any) -> Any:
        """Show the new-activity form."""
        return self.view("activities::create", {"contacts": self.service.contact_options(), "kinds": KINDS})

    def store(self, request: Any) -> Any:
        """Validate and schedule an activity, or return to the form with errors."""
        validator = Validator(request.all(), RULES)
        if validator.fails():
            return redirect.back(request).with_errors(validator).with_input(request.all())
        self.service.schedule({k: v for k, v in validator.validated().items() if v not in ("", None)})
        return redirect(route="activities.index")

    def complete(self, request: Any, activity: int) -> Any:
        """Mark an activity done."""
        self.service.complete(int(activity))
        return redirect(route="activities.index")

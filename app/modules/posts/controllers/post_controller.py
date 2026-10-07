"""Thin HTTP layer of the posts module."""

from typing import Any

from craft.facades import Auth
from craft.http.controller import Controller
from craft.http.response import redirect
from craft.validation import Validator

from ..models import STATUSES
from ..repositories.post_repository import PostRepository
from ..services.post_service import PostService

RULES = {
    "title": ["required", "string", "min:2", "max:160"],
    "body": ["nullable", "string", "max:20000"],
    "status": ["nullable", "in:" + ",".join(STATUSES)],
}


class PostController(Controller):
    """List, write and publish posts."""

    def __init__(self, service: PostService, repository: PostRepository) -> None:
        self.service = service
        self.repository = repository

    def index(self, request: Any) -> Any:
        """Show one page of posts."""
        page = self.repository.paginate(int(request.input("page", 1) or 1))
        return self.view("posts::index", {"posts": list(page), "pagination": page.pagination})

    def create(self, request: Any) -> Any:
        """Show the editor for a new post."""
        return self.view("posts::create", {"post": None, "statuses": STATUSES})

    def store(self, request: Any) -> Any:
        """Validate and save a new post, or return to the editor with errors."""
        validator = Validator(request.all(), RULES)
        if validator.fails():
            return redirect.back(request).with_errors(validator).with_input(request.all())
        data = dict(validator.validated())
        data["author_id"] = Auth.id()
        self.service.save(data)
        return redirect(route="posts.index")

    def edit(self, request: Any, post: int) -> Any:
        """Show the editor for an existing post."""
        found = self.repository.find(int(post))
        if found is None:
            return redirect(route="posts.index")
        return self.view("posts::edit", {"post": found, "statuses": STATUSES})

    def update(self, request: Any, post: int) -> Any:
        """Validate and save changes to a post."""
        validator = Validator(request.all(), RULES)
        if validator.fails():
            return redirect.back(request).with_errors(validator).with_input(request.all())
        self.service.save(validator.validated(), post_id=int(post))
        return redirect(route="posts.index")

    def publish(self, request: Any, post: int) -> Any:
        """Publish a post, or return it to draft when the form asks for that."""
        if str(request.input("action", "")) == "draft":
            self.service.unpublish(int(post))
        else:
            self.service.publish(int(post))
        return redirect(route="posts.index")

"""Business rules of the posts module; exposed on the proxy as `posts`."""

from datetime import UTC, datetime

from ..repositories.post_repository import PostRepository

#: The status a published post carries.
PUBLISHED = "published"
DRAFT = "draft"


class PostService:
    """Posts as the rest of the CRM sees them."""

    def __init__(self, repository: PostRepository) -> None:
        self.repository = repository

    def save(self, data: dict, post_id: int | None = None) -> int:
        """Create or update a post and return its id."""
        status = data.get("status") or DRAFT
        data["status"] = status
        data["published_at"] = datetime.now(UTC).isoformat() if status == PUBLISHED else None
        if post_id is None:
            return self.repository.create(data).get_attribute("id")
        post = self.repository.find(post_id)
        if post is None:
            return post_id
        self.repository.update(post, data)
        return post_id

    def draft(self, title: str, body: str = "") -> int:
        """Create a draft post, for the dashboard's Quick Draft."""
        return self.repository.create({"title": title, "body": body, "status": DRAFT}).get_attribute("id")

    def publish(self, post_id: int) -> bool:
        """Mark a post published; return False when it does not exist."""
        post = self.repository.find(post_id)
        if post is None:
            return False
        self.repository.update(post, {"status": PUBLISHED, "published_at": datetime.now(UTC).isoformat()})
        return True

    def unpublish(self, post_id: int) -> bool:
        """Return a post to draft; return False when it does not exist."""
        post = self.repository.find(post_id)
        if post is None:
            return False
        self.repository.update(post, {"status": DRAFT, "published_at": None})
        return True

    def count_published(self) -> int:
        """Return the number of published posts, for the dashboard."""
        return self.repository.count_published()

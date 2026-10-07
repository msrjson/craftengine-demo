"""Every query of the posts module."""

from typing import Any, Optional

from ..models import Post


class PostRepository:
    """Read and write posts; nothing else touches `crm_posts`."""

    def paginate(self, page: int) -> Any:
        """Return one page of posts, newest first."""
        return Post.query().order_by_desc("id").paginate(per_page=20, page=page)

    def create(self, data: dict) -> Post:
        """Persist a new post from validated data."""
        return Post.create(data)

    def find(self, post_id: int) -> Optional[Post]:
        """Return a post by id, or None."""
        return Post.find(int(post_id))

    def update(self, post: Post, data: dict) -> Post:
        """Apply validated changes to a post."""
        post.update(data)
        return post

    def count_published(self) -> int:
        """Return how many posts are published, for the dashboard."""
        return Post.query().where("status", "published").count()

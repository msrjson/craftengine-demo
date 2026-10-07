"""The post record of the posts module."""

from craft.orm import Model, SoftDeletes

#: Post statuses; persisted values, labels are `posts.status.<value>`.
STATUSES = ("draft", "published")


class Post(SoftDeletes, Model):
    """A piece of content the CRM publishes. Deleting it only stamps `deleted_at`."""

    __table__ = "crm_posts"
    fillable = ["title", "body", "status", "author_id", "published_at"]

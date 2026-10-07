"""The page record of the pages module."""

from craft.orm import Model, SoftDeletes

#: Page statuses; persisted values, labels are `pages.status.<value>`.
STATUSES = ("draft", "published")


class Page(SoftDeletes, Model):
    """A static piece of content. Deleting it only stamps `deleted_at`."""

    __table__ = "crm_pages"
    fillable = ["title", "body", "status", "author_id", "published_at"]

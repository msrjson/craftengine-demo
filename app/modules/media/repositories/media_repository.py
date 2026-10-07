"""Every query of the media module."""

from typing import Any, Optional

from ..models import Media


class MediaRepository:
    """Read and write media rows; nothing else touches `crm_media`."""

    def all(self) -> list[Any]:
        """Return the library, newest first."""
        return Media.query().order_by_desc("id").get()

    def create(self, data: dict) -> Media:
        """Persist a new media row."""
        return Media.create(data)

    def find(self, media_id: int) -> Optional[Media]:
        """Return a media row by id, or None."""
        return Media.find(int(media_id))

    def count(self) -> int:
        """Return how many files the library holds, for the dashboard."""
        return Media.query().count()

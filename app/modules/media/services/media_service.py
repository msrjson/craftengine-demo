"""Media storage: the file goes to the storage layer, its metadata to the table."""

import re
import uuid
from typing import Any, Optional

from craft.facades import Storage

#: The extensions the library accepts.
ALLOWED_EXTENSIONS = ("jpg", "jpeg", "png", "gif", "webp", "svg", "pdf")
#: Largest file accepted, in bytes.
MAX_BYTES = 5 * 1024 * 1024
#: The disk and folder uploads land in.
DISK = "public"
FOLDER = "media"


class MediaService:
    """Store uploads and read the library; never handles a password or a secret."""

    def __init__(self, repository: Any) -> None:
        self.repository = repository

    def store(self, original_name: str, mime: str, data: bytes, uploaded_by: Optional[int] = None) -> int:
        """Write the bytes to the disk and record the row; return its id."""
        stored = f"{uuid.uuid4().hex}-{self._safe_name(original_name)}"
        path = f"{FOLDER}/{stored}"
        Storage.put(path, data, disk=DISK)
        return self.repository.create({
            "name": stored,
            "original_name": original_name,
            "mime": mime or "",
            "size": len(data),
            "disk": DISK,
            "path": path,
            "uploaded_by": uploaded_by,
        }).get_attribute("id")

    def library(self) -> list[Any]:
        """Return every stored file, newest first."""
        return self.repository.all()

    def find(self, media_id: int) -> Optional[Any]:
        """Return a stored file's row, or None."""
        return self.repository.find(media_id)

    def contents(self, media: Any) -> Optional[bytes]:
        """Return the file's bytes from the disk, or None."""
        return Storage.get(media.get_attribute("path"), disk=media.get_attribute("disk") or DISK)

    def count(self) -> int:
        """Return the number of files, for the dashboard."""
        return self.repository.count()

    @staticmethod
    def extension_of(name: str) -> str:
        """The lowercase extension of a filename, without the dot."""
        return name.rsplit(".", 1)[-1].lower() if "." in name else ""

    @staticmethod
    def _safe_name(name: str) -> str:
        """A filesystem-safe version of the client's filename."""
        base = name.rsplit("/", 1)[-1].rsplit("\\", 1)[-1]
        base = re.sub(r"[^A-Za-z0-9._-]+", "_", base).strip("._")
        return (base or "file")[:80]

"""Thin HTTP layer of the media module."""

from typing import Any

from craft.facades import Auth
from craft.http.controller import Controller
from craft.http.response import redirect

from ..services.media_service import ALLOWED_EXTENSIONS, MAX_BYTES, MediaService


class MediaController(Controller):
    """Upload to and browse the media library."""

    def __init__(self, service: MediaService) -> None:
        self.service = service

    def index(self, request: Any) -> Any:
        """Show the library and the upload form."""
        return self.view("media::index", {"items": self.service.library()})

    def store(self, request: Any) -> Any:
        """Store one upload, or return to the library with the reason."""
        upload = request.file("file")
        if upload is None or not upload.filename:
            return self._refuse(request, "media.error.file")
        if self.service.extension_of(upload.filename) not in ALLOWED_EXTENSIONS:
            return self._refuse(request, "media.error.mimes")
        upload.file.seek(0)
        data = upload.file.read()
        if not data:
            return self._refuse(request, "media.error.file")
        if len(data) > MAX_BYTES:
            return self._refuse(request, "media.error.size")
        self.service.store(upload.filename, upload.content_type or "", data, Auth.id())
        return redirect(route="media.index")

    def show(self, request: Any, media: int) -> Any:
        """Stream one stored file back with its content type."""
        from starlette.responses import Response as StarletteResponse

        row = self.service.find(int(media))
        if row is None:
            return redirect(route="media.index")
        data = self.service.contents(row)
        if data is None:
            return redirect(route="media.index")
        return StarletteResponse(content=data, media_type=row.get_attribute("mime") or "application/octet-stream")

    def _refuse(self, request: Any, error_key: str) -> Any:
        """Send the uploader back to the library with a translatable reason."""
        return redirect.back(request, fallback="/media").with_errors({"file": [error_key]})

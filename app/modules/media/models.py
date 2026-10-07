"""The media record of the media module: a file on disk and its metadata."""

from craft.orm import Model, SoftDeletes


class Media(SoftDeletes, Model):
    """An uploaded file. Deleting it only stamps `deleted_at`; the file stays."""

    __table__ = "crm_media"
    fillable = ["name", "original_name", "mime", "size", "disk", "path", "uploaded_by"]

"""The company record of the companies module."""

from craft.orm import Model, SoftDeletes

#: Industry values persisted in `crm_companies.industry`; labels are keys.
INDUSTRIES = ("technology", "retail", "services", "manufacturing", "health")


class Company(SoftDeletes, Model):
    """A customer organization. Deleting it only stamps `deleted_at`."""

    __table__ = "crm_companies"
    fillable = ["name", "website", "industry"]

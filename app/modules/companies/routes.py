"""Routes of the companies module; the engine tags each with the slug."""

from .controllers.company_controller import CompanyController


def register(router: object) -> None:
    """Register the module's screens, all behind sign-in."""
    router.get("/companies", [CompanyController, "index"]).name("companies.index").middleware("auth")
    router.get("/companies/create", [CompanyController, "create"]).name("companies.create").middleware("auth")
    router.post("/companies", [CompanyController, "store"]).name("companies.store").middleware("auth")

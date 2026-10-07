"""The CRM is made only of extensions; these tests prove they cooperate and stay isolated."""

from typing import Any

import pytest

from craft.container.internal_proxy import InternalProxyError
from craft.facades import DB, Proxy, View


def _service(app: Any, module: str, name: str) -> Any:
    """Resolve a module's service the way the module itself binds it."""
    import importlib

    package, cls = {
        "companies": ("companies.services.company_service", "CompanyService"),
        "contacts": ("contacts.services.contact_service", "ContactService"),
        "deals": ("deals.services.deal_service", "DealService"),
        "activities": ("activities.services.activity_service", "ActivityService"),
    }[module]
    return app.make(getattr(importlib.import_module(f"app.modules.{package}"), cls))


@pytest.fixture
def people(crm: Any) -> dict:
    """One company with one contact."""
    company = _service(crm, "companies", "service").create({"name": "Acme Ltda", "industry": "retail"})
    contact = _service(crm, "contacts", "service").create({"first_name": "Ana", "last_name": "Souza", "company_id": company})
    return {"company": company, "contact": contact}


class TestModulesCooperateThroughSeams:
    def test_every_extension_is_active_and_serving(self, crm: Any) -> None:
        status = {row["slug"]: row["availability"] for row in crm.make("extensions").status()}
        assert set(status.values()) == {"serving"}
        assert len(status) == 17

    def test_contacts_get_company_names_through_the_proxy(self, crm: Any, people: dict) -> None:
        assert Proxy.call("companies", "names", [people["company"]]) == {people["company"]: "Acme Ltda"}

    def test_a_won_deal_schedules_exactly_one_follow_up(self, crm: Any, people: dict) -> None:
        deals = _service(crm, "deals", "service")
        deal = deals.create({"title": "Annual plan", "contact_id": people["contact"], "amount": "1500,90", "currency": "BRL"})
        deals.move(deal, "won")
        deals.move(deal, "won")
        rows = DB.table("crm_activities").where("deal_id", deal).get()
        assert [(row["kind"], row["source"]) for row in rows] == [("call", "deal_won")]
        assert DB.table("crm_deals").where("id", deal).first()["amount_cents"] == 150090

    def test_the_menu_and_dashboard_are_built_from_the_active_modules(self, crm: Any) -> None:
        events = crm.make("events")
        routes = [item["route"] for item in events.apply_filters("crm.navigation", [])]
        assert routes[0] == "dashboard.index"
        assert {"companies.index", "contacts.index", "deals.index", "activities.index", "extension_manager.index"} <= set(routes)
        labels = {card["label_key"] for card in events.apply_filters("crm.dashboard.cards", [])}
        assert {"companies.card.label", "contacts.card.label", "deals.card.open", "activities.card.pending"} <= labels

    def test_writes_reach_the_audit_trail_without_personal_data(self, crm: Any, people: dict) -> None:
        entry = DB.table("crm_audit_entries").where("table_name", "crm_contacts").where("record_id", str(people["contact"])).first()
        assert entry["event"] == "model.created"
        assert set(entry.keys()) >= {"event", "table_name", "record_id", "actor_id"}
        assert "Ana" not in " ".join(str(value) for value in entry.values())

    def test_the_theme_overrides_the_layout(self, crm: Any) -> None:
        html = View.render("dashboard::index", {"cards": []})
        assert "harbor::" not in html and "/extensions/harbor/css/harbor.css" in html


class TestOneModuleFailingNeverTakesTheCrmDown:
    def test_contacts_still_render_when_companies_is_out_of_service(self, crm: Any, people: dict) -> None:
        manager = crm.make("extensions")
        for _ in range(manager.breaker.threshold):
            manager.breaker.record_failure("companies", "TEST")
        try:
            with pytest.raises(InternalProxyError):
                Proxy.call("companies", "names", [people["company"]])
            rows = _service(crm, "contacts", "service").rows([])
            assert rows == []
            from app.modules.contacts.models import Contact

            rows = _service(crm, "contacts", "service").rows([Contact.find(people["contact"])])
            assert rows[0]["company"] == ""
        finally:
            manager.breaker.reset("companies")

    def test_a_dependency_cannot_be_switched_off_under_its_dependents(self, crm: Any) -> None:
        from craft.extensions.errors import ExtensionError

        with pytest.raises(ExtensionError) as refused:
            crm.make("extensions").deactivate("contacts")
        assert refused.value.code == "EXTENSION_HAS_ACTIVE_DEPENDENTS"

    def test_a_plugin_can_be_switched_off_and_on_without_a_restart(self, crm: Any, people: dict) -> None:
        manager = crm.make("extensions")
        manager.deactivate("audit_log")
        try:
            company = _service(crm, "companies", "service").create({"name": "Quiet Co"})
            assert DB.table("crm_audit_entries").where("table_name", "crm_companies").where("record_id", str(company)).count() == 0
        finally:
            manager.activate("audit_log")
        company = _service(crm, "companies", "service").create({"name": "Loud Co"})
        assert DB.table("crm_audit_entries").where("table_name", "crm_companies").where("record_id", str(company)).count() == 1


class TestTranslations:
    @pytest.mark.parametrize("key", ["companies.nav.label", "deals.stage.won", "extension_manager.action.activate", "crm.app.name"])
    def test_every_key_exists_in_three_locales(self, crm: Any, key: str) -> None:
        assert {row["locale"] for row in DB.table("translations").where("key", key).get()} == {"en", "pt-BR", "es"}

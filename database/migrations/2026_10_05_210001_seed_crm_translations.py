"""Seed the CRM shell's own keys (layout, menu, pagination) in en, pt-BR and es.

Module copy ships with each module (`app/modules/<slug>/lang/catalog.json`) and
is seeded when the module is installed. Rows that already exist are left alone,
so an edited translation survives. Forward-only: translations are never deleted.
"""

import json
import os

from craft.facades import DB

CATALOG = os.path.join(os.path.dirname(__file__), "..", "..", "resources", "lang", "catalog.json")


def up():
    with open(CATALOG, encoding="utf-8") as handle:
        catalog = json.load(handle)
    for locale, entries in catalog.items():
        for key, value in entries.items():
            if DB.table("translations").where("key", key).where("locale", locale).first() is None:
                DB.table("translations").insert({"key": key, "locale": locale, "value": value})

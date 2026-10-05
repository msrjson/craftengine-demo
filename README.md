# Craft CRM - a demo built only from extensions

A complete CRM on [Craft Engine](https://github.com/msrjson/craftengine), made
entirely of extensions (modules, plugins and a theme). It exists to show - and
to test - what the engine's extension model promises:

- a business feature is a self-contained directory, added without touching the engine;
- modules never import each other: they talk through the internal proxy,
  events and filters;
- when one extension fails, the rest of the CRM keeps serving.

The engine is installed from its GitHub release (`Dockerfile`, `CRAFT_ENGINE_REF`),
never copied: the demo uses the framework exactly as any project would.

## Run it

```bash
cp .env.example .env            # then set APP_KEY: docker compose run --rm app python dev.py key:generate
docker compose up -d --build    # app on http://localhost:9002, PostgreSQL on 5500
docker compose exec app python dev.py extension list
```

Install and activate the extensions (the order follows their dependencies):

```bash
for slug in companies contacts deals activities dashboard audit_log harbor extension_manager; do
  docker compose exec app python dev.py extension install $slug
  docker compose exec app python dev.py extension activate $slug
done
```

## What is inside

| Extension | Kind | Does | Talks to others through |
|---|---|---|---|
| `companies` | module | customer organizations | exposes `names`, `options`, `count` on the proxy |
| `contacts` | module, requires `companies` | people | proxy (company names), degrades when companies is out |
| `deals` | module, requires `contacts` | pipeline; money as cents + ISO 4217 | emits `crm.deal.won` |
| `activities` | module, requires `contacts` | calls, emails, meetings | listens to `crm.deal.won` and schedules one follow-up |
| `dashboard` | module | overview cards | the `crm.dashboard.cards` filter each module feeds |
| `extension_manager` | module | install, activate, deactivate, uninstall, choose the theme | the engine's `ExtensionManager`, same as the CLI |
| `audit_log` | plugin | audit trail of identifiers only (no personal data) | listens to model and auth events |
| `harbor` | theme | the CRM's look, light and dark | overrides `layouts.crm` |

The menu is the `crm.navigation` filter: each module adds its entry, so a
deactivated module disappears from it with no edit anywhere.

## Tests

```bash
docker compose exec app python -m pytest tests -q
```

Each session runs on a disposable SQLite database and installs every extension
through the real lifecycle. The tests cover the cooperation between modules,
the follow-up on a won deal, the audit trail, the theme override, and the
isolation guarantees: a module out of service, a dependency that cannot be
switched off under its dependents, a plugin switched off and on without a restart.

All copy is translation keys in English, Brazilian Portuguese (default) and Spanish.

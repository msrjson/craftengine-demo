# Craft Engine demo - a WordPress-style admin built only from extensions

This is the public demo application of
[Craft Engine](https://github.com/msrjson/craftengine), a batteries-included
Python web framework built on Starlette.

The demo is a WordPress-style admin: an admin bar and a side menu, a login
screen, a dashboard of widgets with a quick draft, Posts, Pages, Users with
roles, a Media library, Settings, and an Extensions panel. "WordPress-style"
describes the shape of the admin only; the demo claims no compatibility with
any other product.

It exists to validate the engine's extension isolation architecture. Every
screen listed above is an extension, and the demo is there to show - and to
test - that:

- a feature is a self-contained directory, added without touching the engine;
- extensions never import each other: they talk through the internal proxy,
  events and filters;
- when one extension fails or is deactivated, the rest keeps serving;
- a dependency cannot be switched off under its dependents;
- plugins and connectors toggle in the running process, without a restart.

The demo started as a small CRM. Those modules (companies, contacts, deals,
activities, invoices, tickets) are still here as further extensions, and several
internal names still carry the `crm` prefix (see [Naming notes](#naming-notes)).

The engine is installed from its GitHub release, never copied: the demo uses
the framework exactly as any project would (see
[Engine pin and upgrade](#engine-pin-and-upgrade)).

## Run it

```bash
cp .env.example .env
docker compose run --rm app python dev.py key:generate   # generates APP_KEY; set it in .env
docker compose up -d --build
docker compose exec app python dev.py extension list
```

| Service | Container | Reachable at |
|---|---|---|
| `app` | `craftengine-demo` | http://localhost:9002 |
| `db` | `craftengine-demo-db` | PostgreSQL 18 on host port 5500 |

The `app` container runs `python dev.py migrate` and then serves on port 9002.
`docker-compose.yml` sets the database connection for the container, so the
commented PostgreSQL block in `.env.example` is not needed to run the demo
this way.

Install and activate every extension. The order follows the `[requires]` table
of each manifest (`contacts` needs `companies`; `deals` and `activities` need
`contacts`); it is the same order the test suite uses in `tests/conftest.py`:

```bash
for slug in companies contacts deals activities dashboard posts pages users media settings \
            audit_log harbor extension_manager tickets invoices activity_digest midnight \
            outbound_webhooks; do
  docker compose exec app python dev.py extension install $slug
  docker compose exec app python dev.py extension activate $slug
done
```

Then create an administrator: register at http://localhost:9002/register and
grant the role from the console.

```bash
docker compose exec app python dev.py user assign-role you@example.com admin
```

The home page redirects to `/overview`, which asks for sign-in first. Screens
under `/admin/...` (users, menus, settings, extensions, audit trail) require the
`admin` role.

The other extension commands are `status`, `update`, `deactivate` and
`uninstall`; `python dev.py extension --help` lists them.

## What is inside

Each extension is one directory with an `extension.toml` manifest (`slug`,
`kind`, `version`, the accepted `engine` range, and an optional `[requires]`
table). There are 18, in four kinds:

| Directory | Kind | Count |
|---|---|---|
| `app/modules/` | module | 13 |
| `app/plugins/` | plugin | 2 |
| `app/themes/` | theme | 2 |
| `app/connectors/` | connector | 1 |

### Admin modules

| Slug | Kind | What it does | How it talks to others |
|---|---|---|---|
| `dashboard` | module | The overview at `/overview`: module counts, the agenda and a quick draft | Puts itself first in the `crm.navigation` filter. Renders the cards other modules add to the `crm.dashboard.cards` filter. Calls `activities.agenda` and `posts.draft` on the proxy and degrades when either cannot serve |
| `posts` | module | Posts: list, editor, draft, publish and unpublish | Exposes `draft`, `publish`, `unpublish`, `count_published` on the proxy as `posts`. Adds a menu entry and a dashboard card |
| `pages` | module | Pages: list, editor, publish and unpublish | Exposes `publish`, `unpublish`, `count_published` on the proxy as `pages`. Adds a menu entry and a dashboard card |
| `users` | module | Admin-only user list, add user, assign a role | Adds a menu entry and a dashboard card. Exposes nothing on the proxy |
| `media` | module | Media library: upload, browse, and a route that serves the stored file | Adds a menu entry and a dashboard card. Exposes nothing on the proxy |
| `settings` | module | General settings (site name, tagline, posts per page) and menu visibility | Adds two menu entries. Reads the `crm.navigation` filter to list the entries that can be hidden; the application shell drops hidden entries from the menu |
| `extension_manager` | module | The Extensions panel at `/admin/extensions`: extensions grouped by kind, install, activate, deactivate, uninstall, choose the theme | Uses the engine's extension manager, the same one `dev.py extension` drives. Installs the theme resolver and removes it when unloaded. Adds a menu entry |

### Business modules (the original CRM)

| Slug | Kind | What it does | How it talks to others |
|---|---|---|---|
| `companies` | module | Customer organizations | Exposes `names`, `options`, `count` on the proxy as `companies`. Adds a menu entry and a dashboard card |
| `contacts` | module, requires `companies` | People | Exposes `names`, `options`, `exists`, `count` on the proxy as `contacts`. Calls `companies.names` and `companies.options` and degrades when companies cannot serve. Adds a menu entry and a dashboard card |
| `deals` | module, requires `contacts` | Sales pipeline; money as integer cents plus a currency code | Exposes `summary` on the proxy as `deals`. Calls `contacts.names` and `contacts.options`. Dispatches the `crm.deal.won` event. Adds a menu entry and two dashboard cards |
| `activities` | module, requires `contacts` | Calls, emails and meetings | Exposes `agenda`, `contact_options`, `schedule` on the proxy as `activities`. Listens to `crm.deal.won` and schedules one follow-up call. Calls `contacts.names` and `contacts.options`. Adds a menu entry and a dashboard card |
| `tickets` | module | Support tickets | Exposes `summary`, `open` on the proxy as `tickets`. No menu entry and no dashboard card |
| `invoices` | module | Invoices | Exposes `summary`, `issue` on the proxy as `invoices`. No menu entry and no dashboard card |

### Plugins, themes and the connector

| Slug | Kind | What it does | How it talks to others |
|---|---|---|---|
| `audit_log` | plugin | Audit trail at `/admin/audit`, storing identifiers only: event, table, record id, acting user id | Listens to `model.created`, `model.updated`, `model.deleted`, `auth.login`, `auth.logout`, `auth.failed`. Knows no module by name |
| `activity_digest` | plugin | Counts, per table, the records created since the process started | Listens to `model.created` for tables ending in `_records`. Exposes `snapshot` on the proxy as `activity_digest` |
| `harbor` | theme | The look of the admin: the chrome (admin bar, side menu, menu toggle), the auth shell for login and register, and the menu icon sprite | Provides the `layouts.crm` and `layouts.auth` views and its own stylesheet. No provider code |
| `midnight` | theme | A second theme that overrides one module view | Overrides the `tickets::index` view when it is the active theme. No provider code |
| `outbound_webhooks` | connector | Forwards created records to an outside service and keeps a delivery log; ships one inbound acknowledgement route | Listens to `model.created` for tables ending in `_records`. Exposes `deliver` on the proxy as `outbound_webhooks`. It has no network transport until the application injects one, so a fresh install never reaches out |

`tickets`, `invoices`, `activity_digest`, `midnight` and `outbound_webhooks`
were generated with `dev.py make <kind>`; only their business rules are
hand-written.

### The three seams

| Seam | Name | Who provides | Who consumes |
|---|---|---|---|
| Internal proxy | `companies`, `contacts`, `deals`, `activities`, `posts`, `pages`, `tickets`, `invoices`, `activity_digest`, `outbound_webhooks` | the extension of the same slug, with an explicit list of callable methods | `contacts`, `deals`, `activities`, `dashboard` |
| Event | `crm.deal.won` | `deals` | `activities` |
| Event | `model.created`, `model.updated`, `model.deleted`, `auth.login`, `auth.logout`, `auth.failed` | the engine | `audit_log`, `activity_digest`, `outbound_webhooks` |
| Filter | `crm.navigation` | every module with a screen in the menu | the application shell (`app/Providers/AppServiceProvider.py`) and `settings` |
| Filter | `crm.dashboard.cards` | `posts`, `pages`, `companies`, `contacts`, `deals`, `activities`, `media`, `users` | `dashboard` |

The menu is the `crm.navigation` filter: each module adds its own entry, with
its icon, so a deactivated module disappears from the menu with no edit
anywhere. A caller that reaches a module through the proxy catches
`InternalProxyError` and falls back to an empty value, which is what keeps a
screen rendering when the module it asks is out of service.

## What this demo validates

Each guarantee below is asserted by a test that runs against extensions
installed and activated through the real lifecycle.

| Guarantee | Proven by |
|---|---|
| Every one of the 18 extensions is active and serving after a real install | `tests/test_crm.py` (`test_every_extension_is_active_and_serving`) |
| The five generated extensions import no other extension | `tests/test_extension_matrix.py` (`test_no_generated_extension_imports_another_extension`) |
| A module reads another module's data through the proxy | `tests/test_crm.py` (`test_contacts_get_company_names_through_the_proxy`) |
| An event links two modules that never import each other: a won deal schedules exactly one follow-up, even when the deal is moved to won twice | `tests/test_crm.py` (`test_a_won_deal_schedules_exactly_one_follow_up`) |
| A plugin and a connector react to records of modules they do not know by name | `tests/test_extension_matrix.py` (`TestCooperationWithoutCoupling`) |
| The menu and the dashboard are built from whatever modules are active | `tests/test_crm.py` (`test_the_menu_and_dashboard_are_built_from_the_active_modules`), `tests/test_admin_chrome.py` (`test_the_left_menu_is_built_from_the_active_modules`) |
| A module out of service does not take its dependent down: with the `companies` circuit breaker open, the proxy refuses the call and contacts still render | `tests/test_crm.py` (`test_contacts_still_render_when_companies_is_out_of_service`) |
| A failing connector never breaks the business write or the plugin beside it | `tests/test_extension_matrix.py` (`TestFaultIsolation`) |
| A dependency cannot be switched off under its dependents: deactivating `contacts` is refused with `EXTENSION_HAS_ACTIVE_DEPENDENTS`, and the panel explains the refusal | `tests/test_crm.py` (`test_a_dependency_cannot_be_switched_off_under_its_dependents`), `tests/test_walkthrough.py` (`test_the_panel_explains_a_refusal`) |
| A plugin is switched off and on without a restart: it stops recording, then records again | `tests/test_crm.py` (`test_a_plugin_can_be_switched_off_and_on_without_a_restart`) |
| A deactivated plugin is refused on the proxy while the modules keep writing | `tests/test_extension_matrix.py` (`test_a_deactivated_plugin_stops_counting_and_is_refused_on_the_proxy`) |
| A deactivated connector stops forwarding and its route stops answering; both resume on reactivation | `tests/test_extension_matrix.py` (`test_a_deactivated_connector_stops_forwarding_and_resumes_when_reactivated`, `test_the_inbound_webhook_answers_without_csrf_and_stops_when_the_connector_is_off`) |
| A module is switched off and on from the panel: its route answers 404, its menu entry disappears, the other screens keep serving | `tests/test_walkthrough.py` (`test_the_panel_switches_a_module_off_and_on`) |
| Uninstalling an extension keeps its rows | `tests/test_extension_matrix.py` (`test_uninstalling_keeps_the_rows`) |
| A theme overrides a layout or a module view at runtime and can be dropped | `tests/test_crm.py` (`test_the_theme_overrides_the_layout`), `tests/test_extension_matrix.py` (`test_the_theme_overrides_the_module_view_at_runtime_and_can_be_dropped`) |
| The audit trail holds identifiers, never personal data | `tests/test_crm.py` (`test_writes_reach_the_audit_trail_without_personal_data`) |
| The Extensions panel groups by kind: module, plugin, theme, connector | `tests/test_walkthrough.py` (`test_the_extension_panel_groups_by_kind`) |

The admin screens themselves are covered one file per feature:

| Feature | Test file |
|---|---|
| Login, register and the admin chrome | `tests/test_admin_chrome.py` |
| Dashboard widgets and the quick draft | `tests/test_dashboard_widgets.py` |
| Posts | `tests/test_posts_module.py` |
| Pages | `tests/test_pages_module.py` |
| Users and roles | `tests/test_users_module.py` |
| Media library | `tests/test_media_module.py` |
| Settings and menu visibility | `tests/test_settings_module.py` |
| Every screen rendered with the theme, the sales flow, menu icons | `tests/test_walkthrough.py` |

## Tests

```bash
docker compose exec app python -m pytest tests -q
```

Each session boots the application on a fresh, disposable SQLite file, runs the
migrations, then installs and activates every extension through the engine's
extension manager, exactly as an operator would. The demo's own database is
never touched.

Setting `CRM_TEST_DB=pgsql` runs the same suite on the PostgreSQL server named
by the `DB_*` variables instead. Those variables must then point at a
disposable database, never at the demo's own.

## Translations

No screen carries hardcoded copy: templates and manifests reference
translation keys. Each extension ships its keys in `lang/catalog.json`, in
three locales - `en`, `pt-BR` and `es` - and the shell's own keys are in
`resources/lang/catalog.json`. The tests assert that keys exist in all three
locales in the `translations` table and that screens render translated copy,
including a plural form.

The locale a visitor gets with no preference is `APP_LOCALE`; `.env.example`
sets it to `en`.

## Engine pin and upgrade

The engine is a package installed from a release archive of the canonical
repository. The pinned release tag is the `CRAFT_ENGINE_REF` build argument in
the `Dockerfile`, and `craft-engine.lock` records the same pin (mode
`package`, with `Dockerfile` as the file that spells the ref). No engine source
is copied, linked or mounted into this repository: a framework change reaches
the demo only through a release.

```bash
docker compose exec app python dev.py engine status             # pin, running release, newer releases
docker compose exec app python dev.py engine update --dry-run   # newest release of the same major.minor line
docker compose exec app python dev.py engine upgrade --to <version> --dry-run
```

Without `--dry-run` the command applies the move. Afterwards rebuild the image
so the new release is installed; the container runs the migrations on start:

```bash
docker compose up -d --build
```

Each extension declares the engine range it accepts in the `engine` field of its
`extension.toml`. An administrator can review the same update from the panel at
`/admin/engine`.

## Naming notes

The demo was a CRM first, and some names in the code still say so. They are
documented here as they are:

- the filters `crm.navigation` and `crm.dashboard.cards`, and the event
  `crm.deal.won`;
- the admin layout view `layouts.crm`;
- tables such as `crm_companies`, `crm_contacts`, `crm_deals`, `crm_activities`
  and `crm_audit_entries`;
- the setting `crm.theme`, the test switch `CRM_TEST_DB`, and the default
  database name `crm_demo` in `docker-compose.yml`.

# AGENTS.md

## Cursor Cloud specific instructions

### Project overview
This is an Odoo 18 Community custom addon module (`operation_logistics`) for logistics/shipment management. It depends on standard Odoo modules: `base`, `mail`, `sale`, `account`.

### Runtime dependencies
- **Odoo 18 Community** is installed at `/opt/odoo` (cloned from `https://github.com/odoo/odoo.git` branch `18.0`).
- **PostgreSQL 16** is the required database backend.
- The Odoo config is at `/etc/odoo.conf` with `addons_path = /opt/odoo/addons,/workspace`.
- The development database is `odoo_dev`.

### Starting services

1. **PostgreSQL**: `pg_ctlcluster 16 main start`
2. **Odoo dev server**: `python3 /opt/odoo/odoo-bin -c /etc/odoo.conf -d odoo_dev --dev=all`
   - Serves at `http://localhost:8069`
   - Admin credentials: `admin` / `admin`
   - The `--dev=all` flag enables auto-reload on Python file changes (requires `inotify` for full support).

### Module installation / update
- **First-time install**: `python3 /opt/odoo/odoo-bin -c /etc/odoo.conf -d odoo_dev -i operation_logistics --stop-after-init`
- **Update after code changes**: `python3 /opt/odoo/odoo-bin -c /etc/odoo.conf -d odoo_dev -u operation_logistics --stop-after-init`
- When running test or update commands while the dev server is active, use `--http-port=8070` to avoid port conflicts.

### Linting
- `flake8 operation_logistics/ --max-line-length=120 --ignore=E501,W503`
- Note: `F401` warnings on `__init__.py` files are expected (Odoo re-export pattern).

### Testing
- Run Odoo tests: `python3 /opt/odoo/odoo-bin -c /etc/odoo.conf -d odoo_dev --test-enable -u operation_logistics --stop-after-init --http-port=8070`
- The module currently has no `tests/` directory. When adding tests, place them in `operation_logistics/tests/` and import them from `operation_logistics/tests/__init__.py`.

### Important Odoo 18 caveats
- Odoo 18 uses `<list>` instead of `<tree>` for list/tree views. Do not use `<tree>` tags.
- Odoo 18 uses `<chatter/>` instead of the old `<div class="oe_chatter"><field name="message_follower_ids" .../>` pattern. Using the old chatter markup causes the form `<sheet>` section to not render at all.
- The `states` attribute on buttons was removed in Odoo 17+. Use `invisible` with domain expressions instead (e.g., `invisible="state != 'draft'"`).
- Use `column_invisible` instead of `invisible` for hiding columns in list views.
- Use `@api.model_create_multi` with `vals_list` parameter (batch) instead of `@api.model` with single `vals` for the `create` method override.
- PostgreSQL users `root` and `odoo` are configured as superusers for development convenience.

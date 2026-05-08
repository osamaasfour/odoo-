# AGENTS.md

## Cursor Cloud specific instructions

### Project overview
This is an Odoo 16 custom addon module (`operation_logistics`) for logistics/shipment management. It depends on standard Odoo modules: `base`, `mail`, `sale`, `account`.

### Runtime dependencies
- **Odoo 16 Community** is installed at `/opt/odoo` (cloned from `https://github.com/odoo/odoo.git` branch `16.0`).
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

### Linting
- `flake8 operation_logistics/ --max-line-length=120 --ignore=E501,W503`
- Note: `F401` warnings on `__init__.py` files are expected (Odoo re-export pattern).

### Testing
- Run Odoo tests: `python3 /opt/odoo/odoo-bin -c /etc/odoo.conf -d odoo_dev --test-enable -i operation_logistics --stop-after-init`
- The module currently has no `tests/` directory. When adding tests, place them in `operation_logistics/tests/` and import them from `operation_logistics/tests/__init__.py`.

### Important caveats
- The module uses `states` attribute in XML views, which is **Odoo 16 only** (deprecated in Odoo 17+). Do not upgrade to Odoo 17 without migrating the views.
- The `create` method override in `shipment.py` triggers a warning about not using batch creation. This is harmless for the current use case.
- PostgreSQL users `root` and `odoo` are configured as superusers for development convenience.

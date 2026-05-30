# Logistics Operations (`operation_logistics`)

Odoo 16 addon for managing shipments, vendor costs, client invoices, and per-shipment revenue for logistics and freight forwarding operations.

## Overview

This module provides a dedicated **Operations** application in Odoo where teams can:

- Create and track shipments from draft through delivery
- Record origin/destination, cargo details, and client information
- Manage billing through service lines linked to vendor bills and client invoices
- Calculate shipment-level and line-level revenue automatically
- Collaborate via Odoo's chatter (messages, followers, activities)

## Features

### Shipment lifecycle

Shipments follow a simple workflow:

| Status      | Description                          |
|-------------|--------------------------------------|
| Draft       | Initial record, editable             |
| Confirmed   | Shipment confirmed for execution     |
| In Transit  | Cargo is en route                    |
| Delivered   | Shipment completed                   |
| Cancelled   | Shipment cancelled                   |

State transitions are available from the shipment form header buttons.

### Automatic reference numbering

New shipments receive a unique reference from the sequence `logistics.shipment.sequence`, formatted as `SHIP/<year>/<00001>` (e.g. `SHIP/2026/00001`).

### Billing and profitability

Each shipment has a **Billing** tab with editable service lines. For every line you can record:

- Service name and vendor
- Vendor bill link and cost
- Client invoice link and amount
- Per-line revenue (invoice amount minus vendor cost)

Shipment totals are computed automatically:

- **Total Vendor Cost** — sum of all service line vendor costs
- **Total Invoice Amount** — sum of all client invoice amounts
- **Revenue** — total invoice amount minus total vendor cost

### Integrations

- **Contacts** — clients and vendors from `res.partner`
- **Accounting** — optional links to vendor bills and client invoices (`account.move`)
- **Sales** — optional link to a related sales order
- **Mail** — full chatter support on shipments

## Dependencies

| Module    | Purpose                                      |
|-----------|----------------------------------------------|
| `base`    | Core Odoo framework                          |
| `mail`    | Chatter, followers, and activities           |
| `sale`    | Related sales order linking                  |
| `account` | Vendor bill and client invoice linking       |

**Target Odoo version:** 16.0 Community

## Installation

1. Add this repository (or the `operation_logistics` folder) to your Odoo `addons_path`.
2. Update the app list in Odoo (**Apps → Update Apps List**).
3. Search for **Logistics Operations** and install it.

From the command line:

```bash
python3 odoo-bin -c /etc/odoo.conf -d YOUR_DATABASE -i operation_logistics --stop-after-init
```

After code changes, upgrade the module:

```bash
python3 odoo-bin -c /etc/odoo.conf -d YOUR_DATABASE -u operation_logistics --stop-after-init
```

## Usage

1. Open **Operations → Shipments**.
2. Create a new shipment and fill in client, date, origin, destination, and optional cargo details.
3. Add service lines on the **Billing** tab with vendor costs and client invoice amounts.
4. Use the header buttons to move the shipment through its lifecycle.
5. Review computed revenue on the billing tab and in the shipment list view.

## Data model

### `logistics.shipment`

Main shipment record with fields for routing, client, cargo (weight/volume), workflow state, billing totals, and optional sales order link.

### `logistics.shipment.service.line`

Child lines on a shipment for individual services, each with vendor/invoice links and computed line revenue.

## Security

All authenticated internal users (`base.group_user`) have full read, write, create, and delete access to shipments and service lines. Adjust `security/ir.model.access.csv` and add record rules if you need stricter access control.

## Development

### Module structure

```
operation_logistics/
├── __init__.py
├── __manifest__.py
├── models/
│   ├── __init__.py
│   └── shipment.py
├── security/
│   └── ir.model.access.csv
├── tests/
│   ├── __init__.py
│   └── test_shipment_defaults.py
└── views/
    ├── __init__.py
    └── shipment_views.xml
```

### Linting

```bash
flake8 operation_logistics/ --max-line-length=120 --ignore=E501,W503
```

### Tests

```bash
python3 odoo-bin -c /etc/odoo.conf -d YOUR_DATABASE --test-enable -i operation_logistics --stop-after-init
```

Current tests cover sequence assignment on create and default field behavior.

## Notes

- XML views use the `states` attribute on buttons, which is supported in Odoo 16 but deprecated in Odoo 17+. Plan a view migration before upgrading.
- The shipment `create` override assigns sequences per record; Odoo may log a batch-creation warning, which is harmless for typical usage.

## License

LGPL-3

from datetime import date

from odoo import fields
from odoo.tests.common import TransactionCase


class TestShipmentDefaults(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.company_partner = cls.env['res.partner'].create({
            'name': 'Default Test Client',
            'is_company': True,
        })

    def _shipment_vals(self, origin, destination):
        return {
            'origin_location': origin,
            'destination_location': destination,
            'client_id': self.company_partner.id,
        }

    def test_default_get_does_not_consume_shipment_sequence(self):
        Shipment = self.env['logistics.shipment']
        count_before = Shipment.search_count([])

        first_defaults = Shipment.default_get(['name'])
        second_defaults = Shipment.default_get(['name'])

        self.assertEqual(first_defaults.get('name'), 'New')
        self.assertEqual(second_defaults.get('name'), 'New')
        self.assertEqual(Shipment.search_count([]), count_before)

    def test_batch_create_assigns_unique_shipment_references(self):
        Shipment = self.env['logistics.shipment']

        shipments = Shipment.create([
            self._shipment_vals('Aqaba Port', 'Jebel Ali Port'),
            self._shipment_vals('Amman Warehouse', 'Riyadh Distribution Center'),
        ])

        self.assertEqual(len(shipments), 2)
        self.assertNotIn('New', shipments.mapped('name'))
        self.assertEqual(len(set(shipments.mapped('name'))), 2)

    def test_shipment_date_default_is_dynamic(self):
        Shipment = self.env['logistics.shipment']
        default = Shipment._fields['shipment_date'].default
        closure_values = [cell.cell_contents for cell in (default.__closure__ or [])]

        self.assertTrue(callable(default))
        self.assertFalse(any(isinstance(value, date) for value in closure_values))
        self.assertEqual(
            Shipment.default_get(['shipment_date']).get('shipment_date'),
            fields.Date.context_today(Shipment),
        )

from odoo.tests.common import TransactionCase


class TestAccountingReporting(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = cls.env['res.partner'].create({
            'name': 'Accounting Report Client',
            'is_company': True,
        })
        cls.vendor = cls.env['res.partner'].create({
            'name': 'Accounting Report Vendor',
            'is_company': True,
        })

    def test_accounting_report_action_is_configured(self):
        action = self.env.ref('operation_logistics.logistics_shipment_accounting_report_action')
        menu = self.env.ref('operation_logistics.logistics_shipment_accounting_report_menu')
        search_view = self.env.ref('operation_logistics.logistics_shipment_service_line_accounting_search')

        self.assertEqual(action.res_model, 'logistics.shipment.service.line')
        self.assertEqual(action.search_view_id, search_view)
        self.assertIn('pivot', action.view_mode.split(','))
        self.assertIn('graph', action.view_mode.split(','))
        self.assertEqual(menu.parent_id, self.env.ref('account.menu_finance_reports'))
        self.assertEqual(menu.action, action)

    def test_service_lines_expose_shipment_accounting_dimensions(self):
        shipment = self.env['logistics.shipment'].create({
            'client_id': self.client.id,
            'origin_location': 'Aqaba Port',
            'destination_location': 'Jebel Ali Port',
        })
        line = self.env['logistics.shipment.service.line'].create({
            'shipment_id': shipment.id,
            'name': 'Ocean Freight',
            'vendor_id': self.vendor.id,
            'vendor_bill_amount': 100.0,
            'client_invoice_amount': 175.0,
        })

        self.assertEqual(line.client_id, self.client)
        self.assertEqual(line.shipment_date, shipment.shipment_date)
        self.assertEqual(line.shipment_state, 'draft')
        self.assertEqual(line.service_revenue, 75.0)

        grouped_totals = self.env['logistics.shipment.service.line'].read_group(
            [('client_id', '=', self.client.id)],
            ['vendor_bill_amount:sum', 'client_invoice_amount:sum', 'service_revenue:sum'],
            ['client_id'],
        )

        self.assertEqual(grouped_totals[0]['vendor_bill_amount'], 100.0)
        self.assertEqual(grouped_totals[0]['client_invoice_amount'], 175.0)
        self.assertEqual(grouped_totals[0]['service_revenue'], 75.0)

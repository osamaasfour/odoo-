# operation_logistics/models/shipment.py
from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
import logging

_logger = logging.getLogger(__name__)

# This message will appear in your Odoo server log if this file is loaded successfully.
_logger.info("LOGISTICS SHIPMENT MODULE: shipment.py is being loaded!")

# Define the main Shipment model
class LogisticsShipment(models.Model):
    _name = 'logistics.shipment'
    _description = 'Logistics Shipment'
    _inherit = ['mail.thread', 'mail.activity.mixin'] # Inherit for communication features (chatter, activities)

    name = fields.Char(string='Shipment Reference', required=True, copy=False, readonly=True,
                       default=lambda self: self.env['ir.sequence'].next_by_code('logistics.shipment.sequence') or 'New')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('in_transit', 'In Transit'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='draft', tracking=True)

    # Basic Shipment Details
    shipment_date = fields.Date(string='Shipment Date', default=fields.Date.today(), required=True)
    origin_location = fields.Char(string='Origin Location', required=True)
    destination_location = fields.Char(string='Destination Location', required=True)
    client_id = fields.Many2one('res.partner', string='Client', required=True, domain=[('is_company', '=', True)])
    shipper_name = fields.Char(string='Shipper Name')
    consignee_name = fields.Char(string='Consignee Name')
    description = fields.Text(string='Description')
    weight = fields.Float(string='Weight (KG)')
    volume = fields.Float(string='Volume (CBM)')
    # You can add more fields here like shipment type, transport mode (sea/air/land), bill of lading number, etc.

    # Link to Sales Module
    sale_order_id = fields.Many2one('sale.order', string='Related Sales Order', copy=False)

    # "Billing" Tab Fields
    # One2many field linking to the service lines for this shipment
    service_line_ids = fields.One2many('logistics.shipment.service.line', 'shipment_id', string='Service Lines')

    # Computed fields for billing totals
    total_vendor_cost = fields.Monetary(string='Total Vendor Cost', compute='_compute_billing_totals', store=True, currency_field='currency_id')
    total_invoice_amount = fields.Monetary(string='Total Invoice Amount', compute='_compute_billing_totals', store=True, currency_field='currency_id')
    revenue = fields.Monetary(string='Revenue', compute='_compute_billing_totals', store=True, currency_field='currency_id')
    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env.company.currency_id.id)

    @api.depends('service_line_ids.vendor_bill_amount', 'service_line_ids.client_invoice_amount')
    def _compute_billing_totals(self):
        """
        Computes the total vendor cost, total invoice amount, and revenue for the shipment
        based on its service lines.
        """
        for shipment in self:
            shipment.total_vendor_cost = sum(line.vendor_bill_amount for line in shipment.service_line_ids)
            shipment.total_invoice_amount = sum(line.client_invoice_amount for line in shipment.service_line_ids)
            shipment.revenue = shipment.total_invoice_amount - shipment.total_vendor_cost

    @api.model
    def create(self, vals):
        """
        Overrides the create method to generate a unique shipment reference using a sequence.
        """
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('logistics.shipment.sequence') or 'New'
        return super(LogisticsShipment, self).create(vals)

    # Workflow/State Transition Buttons (methods called from XML buttons)
    def action_confirm_shipment(self):
        for rec in self:
            rec.state = 'confirmed'

    def action_set_in_transit(self):
        for rec in self:
            rec.state = 'in_transit'

    def action_set_delivered(self):
        for rec in self:
            rec.state = 'delivered'

    def action_cancel_shipment(self):
        for rec in self:
            rec.state = 'cancelled'

    # SQL Constraints for uniqueness
    _sql_constraints = [
        ('name_unique', 'UNIQUE(name)', 'Shipment Reference must be unique!'),
    ]

# Define the Service Line model (This is the child model for service_line_ids)
class LogisticsShipmentServiceLine(models.Model):
    _name = 'logistics.shipment.service.line'
    _description = 'Shipment Service Line'

    shipment_id = fields.Many2one('logistics.shipment', string='Shipment', required=True, ondelete='cascade')
    
    # This is the 'name' field that holds the service description/name.
    # The XML view refers to this field as 'name'.
    name = fields.Char(string='Service Name', required=True) 
    
    vendor_id = fields.Many2one('res.partner', string='Vendor', domain=[('is_company', '=', True)])
    # Link to Account Move (Vendor Bill)
    vendor_bill_id = fields.Many2one('account.move', string='Vendor Bill', domain=[('move_type', '=', 'in_invoice')])
    vendor_bill_amount = fields.Monetary(string='Vendor Cost', currency_field='currency_id')
    
    # Link to Account Move (Client Invoice)
    client_invoice_id = fields.Many2one('account.move', string='Client Invoice', domain=[('move_type', '=', 'out_invoice')])
    client_invoice_amount = fields.Monetary(string='Invoice Amount', currency_field='currency_id')
    
    notes = fields.Text(string='Notes')
    # Currency is related to the parent shipment's currency
    currency_id = fields.Many2one('res.currency', string='Currency', related='shipment_id.currency_id')

    # Computed field for individual service line revenue
    service_revenue = fields.Monetary(string='Service Revenue', compute='_compute_service_revenue', store=True, currency_field='currency_id')

    @api.depends('vendor_bill_amount', 'client_invoice_amount')
    def _compute_service_revenue(self):
        """
        Computes the revenue for an individual service line.
        """
        for line in self:
            line.service_revenue = line.client_invoice_amount - line.vendor_bill_amount

    # Optional: You can uncomment these methods if you want to automatically
    # populate amounts when linking existing bills/invoices.
    # @api.onchange('vendor_bill_id')
    # def _onchange_vendor_bill_id(self):
    #     if self.vendor_bill_id:
    #         self.vendor_bill_amount = self.vendor_bill_id.amount_total

    # @api.onchange('client_invoice_id')
    # def _onchange_client_invoice_id(self):
    #     if self.client_invoice_id:
    #         self.client_invoice_amount = self.client_invoice_id.amount_total

from odoo import models, fields, api


class CiconMaintenanceRequestLine(models.Model):
    _name = 'cicon.maintenance.request.line'

    request_id = fields.Many2one('maintenance.request', "Maintenance Request")
    purchase_order_id = fields.Many2one('purchase.order', "Purchase Order")
    purchase_order_line_id = fields.Many2one('purchase.order.line', "Item",
                                             domain="[('order_id', '=', purchase_order_id)]")
    line_date = fields.Date('Date', default=fields.date.today())
    description = fields.Text(related='purchase_order_line_id.name', string='Description')
    product_qty = fields.Float(related='purchase_order_line_id.product_qty', string="Quantity")
    price_unit = fields.Float(related='purchase_order_line_id.price_unit', string="Unit Price")
    price_tax = fields.Float(related='purchase_order_line_id.price_tax', string="Tax Amount")
    taxes_id = fields.Many2many(related='purchase_order_line_id.taxes_id', string="Tax")
    currency_id = fields.Many2one(related='purchase_order_line_id.currency_id', string='Currency')
    price_subtotal = fields.Monetary(related='purchase_order_line_id.price_subtotal', string="Sub Total")
    product_uom = fields.Many2one(related='purchase_order_line_id.product_uom', string="Unit")


class CiconMaintenanceRequest(models.Model):
    _inherit = 'maintenance.request'

    line_ids = fields.One2many('cicon.maintenance.request.line', 'request_id', string="Expenses")

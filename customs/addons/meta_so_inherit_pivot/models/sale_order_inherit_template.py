from  odoo import fields, models

class SaleOrder(models.Model):
    # _name = 'sale.order.line.custom'
    _inherit = 'sale.order.line'

    quality = fields.Selection([
        ("high", "High Quality"),
        ("medium", "Medium Quality"),
        ("low", "Low Quality"),
    ], string="Quality")

    # quality = fields.Float(string="Quality")

    a_b_c = fields.Integer(string="Unique")

    # tax_id = fields.Many2many(
    #     'account.tax',
    #     'sale_order_line_account_tax_rel',  # This should match the naming convention
    #     'sale_order_line_id',
    #     'tax_id',
    #     string="Taxes"
    # )


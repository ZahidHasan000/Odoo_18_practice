from odoo import models, fields


class ProductInheritTemplate(models.Model):
    _inherit = "product.template"
    _description = "Some new fields in product template model"

    # dest_from = fields.Char(string="Name of production organization")
    dest_from = fields.Char(string="From")
    # dest_to = fields.Char(string="Name of dealer house")
    dest_to = fields.Char(string="To")
    quality = fields.Selection([
        ("high", "High Quality"),
        ("medium", "Medium Quality"),
        ("low", "Low Quality")
    ], string="Quality")
    quantity = fields.Char(string="quantity")

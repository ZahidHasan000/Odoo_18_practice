from odoo import models, fields


class SaleReportCustom(models.Model):
    _inherit = 'sale.report'

    quality = fields.Selection([
        ("high", "High Quality"),
        ("medium", "Medium Quality"),
        ("low", "Low Quality"),
    ], string="Quality")

    a_b_c = fields.Integer(string="Unique")

    tax_id = fields.Many2many(
        'account.tax',
        'sale_order_line_account_tax_rel',
        'sale_order_line_id',
        'tax_id',
        string="Taxes"
    )

    def _from_sale(self):
        from_clause = super()._from_sale()
        # Adding a join to the Many2many relationship table
        from_clause += """
               LEFT JOIN sale_order_line_account_tax_rel so_tax ON so_tax.sale_order_line_id = l.id
               LEFT JOIN account_tax at ON at.id = so_tax.tax_id
           """
        return from_clause

    def _select_additional_fields(self):
        res = super()._select_additional_fields()
        res['quality'] = "l.quality"

        res['a_b_c'] = "l.a_b_c"

        # res['tax_count'] = "COUNT(DISTINCT l.id) FILTER (WHERE at.id IS NOT NULL)"

        res['tax_id'] = "at.id"
        # Aggregate the taxes as an array
        # res['tax_id'] = "array_agg(at.id)"
        # res['tax_id'] = "COALESCE(string_agg(CAST(at.name AS TEXT), ', '), 'No Tax')"

        return res

    # Override _group_by_sale to group by the quality field
    def _group_by_sale(self):
        res = super()._group_by_sale()
        res += """,
            l.quality,
            l.a_b_c,
            at.id
            """
        return res

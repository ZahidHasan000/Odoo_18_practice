from odoo import fields, models


class SaleOrderWizardReport(models.TransientModel):
    _name = 'wizard.xlsx'

    start_date = fields.Datetime(string="Start Date", required=True)
    end_date = fields.Datetime(string="End Date", required=True)

    def sale_order_print_report(self):
        sale_data = self.env['sale.order'].sudo().search_read([
            ('create_date', '>=', self.start_date),
            ('create_date', '<=', self.end_date),
            ('state', '=', 'sale')
        ])

        data = {
            # 'form_data': self.read()[0]
            'sale_data': sale_data,
            'form_data': self.read()[0]
        }

        return self.env.ref('meta_sale_order_xlsx.sale_order_wizard_report_xlsx').report_action([], data=data)


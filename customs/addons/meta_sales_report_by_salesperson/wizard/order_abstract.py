from odoo import api, models


class ReportOrdersSalespersonWise(models.AbstractModel):
    _name = 'report.meta_sales_report_by_salesperson.report_wizard_order'

    @api.model
    def _get_report_values(self, docids, data=None):
        return {
            'doc_ids': data.get('ids'),
            'doc_model': data.get('model'),
            'data': data['form'],
            'start_date': data['start_date'],
            'end_date': data['end_date'],
        }

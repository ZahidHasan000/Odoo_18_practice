from odoo import models


# import json


class SaleOrderXlsx(models.AbstractModel):
    _name = 'report.meta_sale_order_xlsx.report_sale_order_xlsx'
    _inherit = 'report.report_xlsx.abstract'
    _description = "Sale Order Xlsx Report"

    def generate_xlsx_report(self, workbook, data, sale):
        for obj in sale:
            # Calculate the width of the column based on the object name length
            name_length = len(obj.name)
            column_width = max(15, name_length)  # Set a minimum width of 10

            sheet = workbook.add_worksheet(obj.name)
            bold = workbook.add_format({'bold': True})
            wrap = workbook.add_format({'text_wrap': True})
            date_format = workbook.add_format({'num_format': 'dd/mm/yy', 'align': 'center'})
            gray_format = workbook.add_format({'bg_color': '#aba8a7'})
            sale_order_text_format = workbook.add_format({
                'bg_color': '#d2491b',
                'font_color': '#FFFFFF',
                'font_size': '15px',
                'bold': True,
                'align': 'center'
            })
            green_white_text_format = workbook.add_format({
                'font_color': '#00B050',
                'bold': True
            })
            header_text_format = workbook.add_format({
                'bg_color': '#00B050',
                'font_color': '#FFFFFF',
                'bold': True,
                'border': 1,
            })

            # Set the column width dynamically based on the name length
            sheet.set_column(8, 8, column_width)

            column_width2 = max(12, name_length)
            sheet.set_column(1, 1, column_width2)
            sheet.set_column(2, 2, column_width2)
            sheet.set_column(4, 4, column_width2)
            sheet.set_column(7, 7, column_width2)

            row = 5
            col = 7
            sheet.write(row, col, 'Order Date:', bold)
            col += 1
            sheet.merge_range(row, 8, row, 9, '', None)
            sheet.write(row, col, obj.date_order, date_format)
            row += 1
            col -= 1
            sheet.write(row, col, 'Payment Terms:', bold)
            col += 1
            sheet.merge_range(row, 8, row, 9, '', None)
            sheet.write(row, col, obj.payment_term_id.name)
            row += 1
            col -= 1
            sheet.write(row, col, 'Invoice Status:', bold)
            col += 1
            sheet.merge_range(row, 8, row, 9, '', None)
            sheet.write(row, col, obj.invoice_status)
            row = 1
            col = 1
            sheet.merge_range(row, col, row, col + 8, 'Sale Order', sale_order_text_format)

            row += 1
            col = 1
            sheet.merge_range(row, col, row, col + 8, '', gray_format)

            row += 1
            col = 1
            sheet.merge_range(row, col, row, col + 8, '')
            sheet.write(row, col, obj.name, green_white_text_format)

            row += 1
            col = 1
            sheet.merge_range(row, col, row, col + 8, '', gray_format)

            row += 1
            sheet.write(row, col, 'Customer:', bold)
            col += 1
            sheet.merge_range(row, 2, row, 5, '', None)
            sheet.write(row, col, obj.partner_id.name)
            row += 1
            col -= 1
            sheet.write(row, col, 'Salesperson:', bold)
            col += 1
            sheet.merge_range(row, 2, row, 5, '', None)
            sheet.write(row, col, obj.user_id.name)
            row += 1
            col -= 1
            sheet.write(row, col, 'State:', bold)
            col += 1
            sheet.merge_range(row, 2, row, 3, '', None)
            sheet.write(row, col, obj.state)
            if obj.origin:
                row += 1
                col -= 1
                sheet.write(row, col, 'Source Document:', bold)
                col += 1
                sheet.merge_range(row, 2, row, 5, '', None)
                sheet.write(row, col, obj.origin)

            row += 1
            col = 1
            sheet.merge_range(row, col, row, col + 8, '', gray_format)

            row += 1
            col = 1
            sheet.write(row, col, 'Product', header_text_format)
            col += 1
            sheet.write(row, col, 'Description', header_text_format)
            col += 1
            sheet.write(row, col, 'Quantity', header_text_format)
            col += 1
            sheet.write(row, col, 'Delivered', header_text_format)
            col += 1
            sheet.write(row, col, 'Invoiced', header_text_format)
            col += 1
            sheet.write(row, col, 'UoM', header_text_format)
            col += 1
            sheet.write(row, col, 'Unit Price', header_text_format)
            col += 1
            sheet.write(row, col, 'Taxes', header_text_format)
            col += 1
            sheet.write(row, col, 'Subtotal', header_text_format)
            row += 1
            col = 1
            tx_list = []
            for record in obj.order_line:
                for tx in record.tax_id:
                    tx_list.append(tx.name)
                sheet.write(row, col, record.product_id.name)
                col += 1
                sheet.write(row, col, record.name, wrap)
                col += 1
                sheet.write(row, col, record.product_uom_qty)
                col += 1
                sheet.write(row, col, record.qty_delivered)
                col += 1
                sheet.write(row, col, record.qty_invoiced)
                col += 1
                sheet.write(row, col, record.product_uom.name)
                col += 1
                sheet.write(row, col, record.price_unit)
                col += 1
                sheet.write(row, col, ', '.join(tx_list))
                col += 1
                sheet.write(row, col, record.price_subtotal)
                col = 1
                row += 1
                tx_list.clear()
            row += 1
            col = 8
            sheet.write(row, col, 'Untaxed Amount:', bold)
            col += 1

            # Writing the untaxed amount
            sheet.write(row, col, obj.tax_totals.get('base_amount', 0))
            row += 1
            col = 8

            # Iterate over the subtotals to find 'Untaxed Amount'
            subtotals = obj.tax_totals.get('subtotals', [])
            for subtotal in subtotals:
                if subtotal.get('name') == 'Untaxed Amount':  # Check if the subtotal is for 'Untaxed Amount'
                    for rec in subtotal.get('tax_groups', []):
                        sheet.write(row, col, rec.get('group_name'))
                        col += 1
                        sheet.write(row, col, rec.get('tax_amount'))
                        row += 1
                        col -= 1

            # Reset the column and write the total
            col = 8
            sheet.write(row, col, 'Total:', bold)
            col += 1
            sheet.write(row, col, obj.tax_totals.get('total_amount'))

            # sheet.write(row, col, obj.tax_totals.get('amount_untaxed', 0))
            # # sheet.write(row, col, json.loads(obj.tax_totals_json).get('amount_untaxed'))
            # row += 1
            # col = 8
            #
            # # if obj.tax_totals.get('groups_by_subtotal').get('Untaxed Amount'):
            # if obj.tax_totals.get('subtotals').get('Untaxed Amount'):
            #     for rec in obj.tax_totals.get('subtotals').get('Untaxed Amount'):
            #         sheet.write(row, col, rec.get('group_name'))
            #         col += 1
            #         sheet.write(row, col, rec.get('tax_amount'))
            #         row += 1
            #         col -= 1
            # col = 8
            # sheet.write(row, col, 'Total:', bold)
            # col += 1
            # sheet.write(row, col, obj.tax_totals.get('amount_total'))
    #
    # def get_report_action(self, docids, data=None):
    #     context = dict(self.env.context)
    #     return {
    #         'type': 'ir.actions.report',
    #         'report_type': 'xlsx',
    #         'context': context,  # Ensure the context is passed here
    #         'data': data or {},
    #     }

# from odoo import models
#
#
# class SaleOrderXlsx(models.AbstractModel):
#     _name = 'report.meta_sale_order_xlsx.report_sale_order_xlsx'
#     _inherit = 'report.report_xlsx.abstract'
#     _description = "Sale Order Xlsx Report"
#
#     def generate_xlsx_report(self, workbook, data, sale):
#         for obj in sale:
#             # Calculate the width of the column based on the object name length
#             name_length = len(obj.name)
#             column_width = max(15, name_length)  # Set a minimum width of 10
#
#             sheet = workbook.add_worksheet(obj.name)
#             bold = workbook.add_format({'bold': True})
#             wrap = workbook.add_format({'text_wrap': True})
#             date_format = workbook.add_format({'num_format': 'dd/mm/yy', 'align': 'center'})
#             gray_format = workbook.add_format({'bg_color': '#aba8a7'})
#             sale_order_text_format = workbook.add_format({
#                 'bg_color': '#d2491b',
#                 'font_color': '#FFFFFF',
#                 'font_size': '15px',
#                 'bold': True,
#                 'align': 'center'
#             })
#             green_white_text_format = workbook.add_format({
#                 'font_color': '#00B050',
#                 'bold': True
#             })
#             header_text_format = workbook.add_format({
#                 'bg_color': '#00B050',
#                 'font_color': '#FFFFFF',
#                 'bold': True,
#                 'border': 1,
#             })
#
#             # Set the column width dynamically based on the name length
#             sheet.set_column(8, 8, column_width)
#             sheet.set_column(1, 1, max(12, name_length))
#             sheet.set_column(2, 2, max(12, name_length))
#             sheet.set_column(4, 4, max(12, name_length))
#             sheet.set_column(7, 7, max(12, name_length))
#
#             # Write Sale Order details
#             row, col = 5, 7
#             sheet.write(row, col, 'Order Date:', bold)
#             sheet.write(row, col + 1, obj.date_order, date_format)
#
#             row += 1
#             sheet.write(row, col, 'Payment Terms:', bold)
#             sheet.write(row, col + 1, obj.payment_term_id.name or '')
#
#             row += 1
#             sheet.write(row, col, 'Invoice Status:', bold)
#             sheet.write(row, col + 1, obj.invoice_status)
#
#             # Sale order title
#             row, col = 1, 1
#             sheet.merge_range(row, col, row, col + 8, 'Sale Order', sale_order_text_format)
#             row += 1
#             sheet.merge_range(row, col, row, col + 8, '', gray_format)
#
#             # Order details
#             row += 2
#             sheet.write(row, col, 'Customer:', bold)
#             sheet.write(row, col + 1, obj.partner_id.name or '')
#
#             row += 1
#             sheet.write(row, col, 'Salesperson:', bold)
#             sheet.write(row, col + 1, obj.user_id.name or '')
#
#             row += 1
#             sheet.write(row, col, 'State:', bold)
#             sheet.write(row, col + 1, obj.state or '')
#
#             if obj.origin:
#                 row += 1
#                 sheet.write(row, col, 'Source Document:', bold)
#                 sheet.write(row, col + 1, obj.origin)
#
#             row += 1
#             sheet.merge_range(row, col, row, col + 8, '', gray_format)
#
#             # Table headers for products
#             row += 1
#             headers = ['Product', 'Description', 'Quantity', 'Delivered', 'Invoiced', 'UoM', 'Unit Price', 'Taxes',
#                        'Subtotal']
#             for i, header in enumerate(headers):
#                 sheet.write(row, col + i, header, header_text_format)
#
#             # Product lines
#             row += 1
#             tx_list = []
#             for line in obj.order_line:
#                 tx_list = [tax.name for tax in line.tax_id]
#                 sheet.write(row, col, line.product_id.name or '')
#                 sheet.write(row, col + 1, line.name, wrap)
#                 sheet.write(row, col + 2, line.product_uom_qty)
#                 sheet.write(row, col + 3, line.qty_delivered)
#                 sheet.write(row, col + 4, line.qty_invoiced)
#                 sheet.write(row, col + 5, line.product_uom.name or '')
#                 sheet.write(row, col + 6, line.price_unit)
#                 sheet.write(row, col + 7, ', '.join(tx_list))
#                 sheet.write(row, col + 8, line.price_subtotal)
#                 row += 1
#
#             # Totals
#             row += 1
#             sheet.write(row, col + 7, 'Untaxed Amount:', bold)
#             sheet.write(row, col + 8, obj.tax_totals.get('amount_untaxed', 0))
#
#             row += 1
#             sheet.write(row, col + 7, 'Total:', bold)
#             sheet.write(row, col + 8, obj.tax_totals.get('amount_total', 0))

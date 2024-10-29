from odoo import models


class SaleOrderXlsx(models.AbstractModel):
    _name = 'report.meta_sale_order_xlsx.report_sale_order_wizard_xlsx'
    _inherit = 'report.report_xlsx.abstract'
    _description = "Sale Order Wizard XLSX Report"

    def generate_xlsx_report(self, workbook, data, sale):
        sale_orders = data['sale_data']  # Data passed from the wizard

        # Loop through each sale order to create a sheet per sale order
        for obj in sale_orders:
            sheet = workbook.add_worksheet(obj['name'])  # Create a sheet named after the sale order

            # Create formats
            bold = workbook.add_format({'bold': True})
            wrap = workbook.add_format({'text_wrap': True})
            date_format = workbook.add_format({'num_format': 'dd/mm/yy'})
            # align_center = workbook.add_format({'align': 'center'})
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

            # Set the column width dynamically based on the order name length
            name_length = len(obj['name'])
            column_width = max(15, name_length)
            sheet.set_column(8, 8, column_width)

            column_width2 = max(12, name_length)
            sheet.set_column(1, 1, column_width2)
            sheet.set_column(2, 2, column_width2)
            sheet.set_column(4, 4, column_width2)
            sheet.set_column(7, 7, column_width2)

            # Write headers
            row = 5
            col = 7
            sheet.write(row, col, 'Order Date:', bold)
            col += 1
            sheet.merge_range(row, 8, row, 9, '', None)
            sheet.write(row, col, obj['date_order'], date_format)

            row += 1
            col -= 1
            sheet.write(row, col, 'Payment Terms:', bold)
            col += 1
            sheet.merge_range(row, 8, row, 9, '', None)
            sheet.write(row, col, obj['payment_term_id'][1] if obj['payment_term_id'] else '')

            row += 1
            col -= 1
            sheet.write(row, col, 'Invoice Status:', bold)
            col += 1
            sheet.merge_range(row, 8, row, 9, '', None)
            sheet.write(row, col, obj['invoice_status'])

            # Merged header for the sale order name
            row = 1
            col = 1
            sheet.merge_range(row, col, row, col + 8, 'Sale Order', sale_order_text_format)

            row += 1
            col = 1
            sheet.merge_range(row, col, row, col + 8, '', gray_format)

            # Write the sale order name
            row += 1
            col = 1
            sheet.merge_range(row, col, row, col + 8, '')
            sheet.write(row, col, obj['name'], green_white_text_format)

            row += 1
            col = 1
            sheet.merge_range(row, col, row, col + 8, '', gray_format)

            # Write additional information: Customer, Salesperson, State, Source Document
            row += 1
            sheet.write(row, col, 'Customer:', bold)
            col += 1
            sheet.merge_range(row, 2, row, 5, '', None)
            sheet.write(row, col, obj['partner_id'][1])

            row += 1
            col -= 1
            sheet.write(row, col, 'Salesperson:', bold)
            col += 1
            sheet.merge_range(row, 2, row, 5, '', None)
            sheet.write(row, col, obj['user_id'][1])

            row += 1
            col -= 1
            sheet.write(row, col, 'State:', bold)
            col += 1
            sheet.merge_range(row, 2, row, 3, '', None)
            sheet.write(row, col, obj['state'])

            if obj['origin']:
                row += 1
                col -= 1
                sheet.write(row, col, 'Source Document:', bold)
                col += 1
                sheet.merge_range(row, 2, row, 5, '', None)
                sheet.write(row, col, obj['origin'])

            # Write Product details
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

            print("XLSXXXXXXXXXXXXXX", obj)

            row += 1
            col = 1
            tx_list = []
            # order_line = self.env['sale.order.line'].sudo().search([('id', '=', obj['id'])])

            # Fetching the order lines using the order_line IDs from the sale order
            order_lines_ids = obj['order_line']  # This should be a list of order line IDs
            order_line = self.env['sale.order.line'].sudo().browse(order_lines_ids)  # Use browse to get records

            for record in order_line:
                # Reset tx_list for each record
                tx_list.clear()

                # Write product details
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

                # Append tax names to the list
                for tx in record.tax_id:
                    tx_list.append(tx.name)

                # Write the taxes and subtotal
                sheet.write(row, col, ', '.join(tx_list))
                col += 1
                sheet.write(row, col, record.price_subtotal)

                row += 1  # Move to the next row for the next product
                col = 1  # Reset column to 1 for the next product row

            row += 1
            col = 8
            sheet.write(row, col, 'Untaxed Amount:', bold)
            col += 1
            sheet.write(row, col, obj['tax_totals'].get('base_amount', 0))

            # Write VAT details only once
            row += 1
            col = 8
            subtotals = obj['tax_totals'].get('subtotals', [])
            for subtotal in subtotals:
                if subtotal.get('name') == 'Untaxed Amount':  # Check if the subtotal is for 'Untaxed Amount'
                    for rec in subtotal.get('tax_groups', []):
                        sheet.write(row, col, rec.get('group_name'))
                        col += 1
                        sheet.write(row, col, rec.get('tax_amount'))
                        row += 1
                        col -= 1  # Reset column for next tax group


            col = 8
            sheet.write(row, col, 'Total:', bold)
            col += 1
            sheet.write(row, col, obj['tax_totals'].get('total_amount', 0))

            # for record in order_line:
            #     for tx in record.tax_id:
            #         tx_list.append(tx.name)
            #
            #         sheet.write(row, col, record.product_id.name)
            #         col += 1
            #         sheet.write(row, col, record.name, wrap)
            #         col += 1
            #         sheet.write(row, col, record.product_uom_qty)
            #         col += 1
            #         sheet.write(row, col, record.qty_delivered)
            #         col += 1
            #         sheet.write(row, col, record.qty_invoiced)
            #         col += 1
            #         sheet.write(row, col, record.product_uom.name)
            #         col += 1
            #         sheet.write(row, col, record.price_unit)
            #         col += 1
            #         sheet.write(row, col, ', '.join(tx_list))
            #         col += 1
            #         sheet.write(row, col, record.price_subtotal)
            #         col = 1
            #         row += 1
            #         tx_list.clear()
            #     row += 1
            #     col = 8
            #     sheet.write(row, col, 'Untaxed Amount:', bold)
            #     col += 1
            #
            #     # Writing the base amount
            #     sheet.write(row, col, obj['tax_totals'].get('base_amount', 0))
            #     row += 1
            #     col = 8
            #
            #     # Iterate over the subtotals to find 'Untaxed Amount'
            #     subtotals = obj['tax_totals'].get('subtotals', [])
            #     for subtotal in subtotals:
            #         if subtotal.get('name') == 'Untaxed Amount':  # Check if the subtotal is for 'Untaxed Amount'
            #             for rec in subtotal.get('tax_groups', []):
            #                 sheet.write(row, col, rec.get('group_name'))
            #                 col += 1
            #                 sheet.write(row, col, rec.get('tax_amount'))
            #                 row += 1
            #                 col -= 1
            #
            #     # Reset the column and write the total
            #     col = 8
            #     sheet.write(row, col, 'Total:', bold)
            #     col += 1
            #     sheet.write(row, col, obj['tax_totals'].get('total_amount'))

            # sheet.write(row, col, obj['tax_totals'].get('base_amount', 0))
            # row += 1
            # col = 8
            #
            # if obj['tax_totals'].get('subtotals').get('Untaxed Amount'):
            #     for rec in obj['tax_totals'].get('subtotals').get('Untaxed Amount'):
            #         sheet.write(row, col, rec.get('group_name'))
            #         col += 1
            #         sheet.write(row, col, rec.get('tax_amount'))
            #         row += 1
            #         col -= 1
            # col = 8
            # sheet.write(row, col, 'Total:', bold)
            # col += 1
            # sheet.write(row, col, obj['tax_totals'].get('total_amount'))

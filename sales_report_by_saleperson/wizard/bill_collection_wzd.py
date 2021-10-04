# -*- coding: utf-8 -*-

from odoo import api, fields, models


class BillCollection(models.TransientModel):
    _name = 'bill.collection'

    start_date = fields.Date('Start Date', default=fields.Date.today(), required=True)
    end_date = fields.Date(string="End Date", default=fields.Date.today(), required=True)
    user_ids = fields.Many2many('res.users', string="Bill User")

    @api.multi
    def print_test(self):
        collection = "out_invoice"
        refund = "out_refund"
        null = ''
        sale_collection = self.env['account.invoice'].search([('state', '=', 'paid')])

        groupby_dict = {}
        for user in self.user_ids:
            filtered_user = list(filter(lambda x: x.create_uid == user, sale_collection))
            # filtered_type = list(filter(lambda x: x.type == collection, filtered_user))
            filtered_by_date = list(
                filter(lambda x: x.date_invoice >= self.start_date and x.date_invoice <= self.end_date, filtered_user))
            groupby_dict[user.name] = filtered_by_date
        # print groupby_dict

        final_dict = {}
        for user in groupby_dict.keys():
            temp = []
            for order in groupby_dict[user]:
                # if order.type == collection:
                temp_2 = []
                temp_2.append(order.date_invoice)  # invoice date
                temp_2.append(order.number)  # invoice number
                temp_2.append(order.origin)  # Sale order / source document number

                for i in sale_collection:
                    # product names according to invoices
                    if i.origin == order.origin:
                        servicesName = []
                        finalServicesName = []
                        servicesQuant = []
                        finalServiceQuant = []
                        prod = self.env['account.invoice.line'].search([('invoice_id', '=', i.id)])
                        for j in prod:
                            serviceName = j.name
                            servicesName.append(serviceName)
                            finalServicesName = servicesName

                            serviceQuant = j.quantity
                            servicesQuant.append(serviceQuant)
                            finalServiceQuant = servicesQuant
                        temp_2.append(finalServicesName)  # product names
                        temp_2.append(finalServiceQuant)
                        temp_2.append(order.partner_id.name)  # patient names
                        temp_2.append(order.amount_total_signed)
                        temp.append(temp_2)

                final_dict[user] = temp


        datas = {
            'ids': self.ids,
            'model': 'bill.collection',
            'form': final_dict,
            'start_date': self.start_date,
            'end_date': self.end_date,

        }
        return self.env['report'].get_action(self, 'sales_report_by_saleperson.bill_collection_report', data=datas)

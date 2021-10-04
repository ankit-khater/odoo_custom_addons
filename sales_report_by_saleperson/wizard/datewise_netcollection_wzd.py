# -*- coding: utf-8 -*-
##############################################################################

##############################################################################

from odoo import api, fields, models


class DatewiseCollection(models.TransientModel):
    _name = 'datewise.collection'

    start_date = fields.Date('Start Date', default=fields.Date.today(), required=True)
    end_date = fields.Date(string="End Date", default=fields.Date.today(), required=True)
    user_ids = fields.Many2many('res.users', string="Bill User")

    @api.multi
    def print_netcollection(self):
        global temp, temp_2, totalInvoice, totalPatient, totalAmount
        net_collection = self.env['account.invoice'].search([('state', '=', 'paid')])

        groupby_dict = {}
        for user in self.user_ids:
            filtered_user = list(filter(lambda x: x.create_uid == user, net_collection))
            # filtered_type = list(filter(lambda x: x.type == collection, filtered_user))
            filtered_by_date = list(
                filter(lambda x: x.date_invoice >= self.start_date and x.date_invoice <= self.end_date, filtered_user))
            groupby_dict[user.name] = filtered_by_date
        # print groupby_dict
        # user_pool = self.env['res.users'].search([])
        # list = []
        # list1 = []
        # for i in user_pool:
        #     uname = i.login
        #     list1.append(uname)
        #     sales = self.env['account.invoice'].search([('state', '=', 'paid')])
        #     for j in sales:
        #         inv = j.number
        #         list1.append(inv)
        #         amount = j.amount_total
        #         list1.append(amount)
        #     list.append(list1)
        # print list
        final_dict = {}
        for user in groupby_dict.keys():
            temp = []
            totalInvoice = []
            totalPatient = []
            totalAmount = []
            for order in groupby_dict[user]:
                temp_2 = []
                totalInvoice.append(order.number)
                totalPatient.append(order.partner_id.name)
                totalAmount.append(order.amount_total_signed)

                invoiceCount = (len(totalInvoice))
                t3 = str(invoiceCount)
                temp_2.append(t3)

                patientCount = len(totalPatient)
                t2 = str(patientCount)
                temp_2.append(t2)

                amountCount = sum(totalAmount)
                t1 = str(amountCount)
                temp_2.append(t1)
            temp.append(temp_2)
        final_dict[user] = temp
        print temp
        print('=============================================')
        print ('user name:', user)
        print ('Total invoice count:', len(totalInvoice))
        print ('Total patient count:', len(totalPatient))
        print ('Total amount collected:', sum(totalAmount))
        print('=============================================')

        datas = {
            'ids': self.ids,
            'model': 'datewise.collection',
            'form': final_dict,
            'start_date': self.start_date,
            'end_date': self.end_date,
        }

        return self.env['report'].get_action(self, 'sales_report_by_saleperson.datewise_netcollection_report',
                                             data=datas)

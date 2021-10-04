# -*- coding: utf-8 -*-
##############################################################################

##############################################################################
from odoo import api, models


class ReportSalesSalespersonWise(models.AbstractModel):
    _name = 'report.sales_report_by_saleperson.sale_productcate'

    def get_default_user(self):
        user_pool = self.env['res.users']
        user = user_pool.browse(self.env.user.id)
        if user:
            return user.id
            print "user--------------"
            print "user.id"
        else:
            return False

    def prepare_productcate_refund_line_by_date(self, start_date, end_date, categ_id):
        print "function call"
        print start_date
        print end_date
        print categ_id
        id = self.get_default_user()
        print "User_ID:",id
        # function use for recursion
        list = []

        def recursive(categ_id):
            data = self.env['product.category'].search([('id', '=', categ_id)])
            print "User Id:",id
            for i in data:
                print "category name:", i.name
                data1 = self.env['product.template'].search([('categ_id', '=', categ_id)])
                c = self.env['product.template'].search_count([('categ_id', '=', categ_id)])
                print c
                for j in data1:
                    count = self.env['account.invoice.line'].search_count(
                        ['&', ('product_id', '=', j.id), ('create_date', '>=', start_date),
                         ('create_date', '<=', end_date)])
                    dict = {'name': '', 'quantity': '', 'total': '', 'category': ''}
                    print j.name
                    data3 = self.env['account.invoice.line'].search(
                        ['&', ('product_id', '=', j.id), ('create_date', '>=', start_date),
                         ('create_date', '<=', end_date)])
                    qty = 0
                    sum = 0
                    flag = False
                    flag2 = False
                    user_flag=False
                    for k in data3:
                        print "Invoice_Id:",k.invoice_id.id
                        user=self.env['account.invoice'].search([('id','=',k.invoice_id.id),('user_id','=',id)])
                        print user
                        for u in user:
                            user_flag=True
                            print user_flag
                        if user_flag:
                            if k.price_subtotal_signed < 0:
                                flag = True
                                qty = qty + k.quantity
                                sum = (sum + k.price_subtotal_signed)
                            # if sum==-0.0:
                            #     sum=0.0

                    print "Sale Quantity:", qty
                    print "Total:", sum
                    if flag :
                        if count != 0:
                            dict['name'] = j.name
                            dict['quantity'] = int(qty)
                            dict['total'] = sum * -1
                            dict['category'] = i.name
                            list.append(dict)
                            print dict
                            print list
                data2 = self.env['product.category'].search([('parent_id', '=', i.id)])
                for l in data2:
                    recursive(l.id)  # function call itself
                return list

        lst = recursive(categ_id)
        print "List of Dictonary", lst
        params = (categ_id, start_date, end_date)
        print params
        self.env.cr.execute('select * from product_category where parent_id = 1', params)
        res = self.env.cr.dictfetchall()
        print res
        return lst

    def prepare_productcate_line_by_date(self, start_date, end_date, categ_id):
        print "function call"
        print start_date
        print end_date
        print categ_id
        id = self.get_default_user()
        print "User_ID:", id
        # function use for recursion
        list = []

        def recursive(categ_id):
            data = self.env['product.category'].search([('id', '=', categ_id)])
            for i in data:
                print "category name:", i.name
                data1 = self.env['product.template'].search([('categ_id', '=', categ_id)])
                c = self.env['product.template'].search_count([('categ_id', '=', categ_id)])
                print c
                for j in data1:
                    count = self.env['account.invoice.line'].search_count(
                        ['&', ('product_id', '=', j.id), ('create_date', '>=', start_date),
                         ('create_date', '<=', end_date)])
                    dict = {'name': '', 'quantity': '', 'total': '', 'category': ''}
                    print j.name
                    data3 = self.env['account.invoice.line'].search(
                        ['&', ('product_id', '=', j.id), ('create_date', '>=', start_date),
                         ('create_date', '<=', end_date)])
                    qty = 0
                    sum = 0
                    flag = False
                    user_flag=False
                    for k in data3:
                        print "Invoice_Id:", k.invoice_id.id
                        user = self.env['account.invoice'].search([('id', '=', k.invoice_id.id), ('user_id', '=', id)])
                        print user
                        for u in user:
                            user_flag=True
                            print user_flag
                        if user_flag:
                            if k.price_subtotal_signed > 0:
                                flag = True
                                qty = qty + k.quantity
                                sum = (sum + k.price_subtotal_signed)
                    print "Sale Quantity:", qty
                    print "Total:", sum
                    if flag:
                        if count != 0:
                            dict['name'] = j.name
                            dict['quantity'] = int(qty)
                            dict['total'] = sum
                            dict['category'] = i.name
                            list.append(dict)
                            print dict
                            print list
                data2 = self.env['product.category'].search([('parent_id', '=', i.id)])
                for l in data2:
                    recursive(l.id)  # function call itself
                return list

        lst = recursive(categ_id)
        print "List of Dictonary", lst
        params = (categ_id, start_date, end_date)
        print params
        self.env.cr.execute('select * from product_category where parent_id = 1', params)
        res = self.env.cr.dictfetchall()
        print res
        return lst

    @api.model
    def render_html(self, docids, data=None):
        self.model = self.env.context.get('active_model')
        docs = self.env[self.model].browse(self.env.context.get('active_id'))
        report_obj = self.env['report']
        report = report_obj._get_report_from_name('sales_report_by_saleperson.sale_productcate')
        print report
        lines = self.prepare_productcate_line_by_date(docs.start_date, docs.end_date, docs.categ_id.id)
        print lines
        refund_lines = self.prepare_productcate_refund_line_by_date(docs.start_date, docs.end_date, docs.categ_id.id)

        docargs = {
            'doc_model': data.get('model'),
            'docs': self,
            'from_date': docs.start_date,
            'to_date': docs.end_date,
            'category': docs.categ_id.name,
            'lines': lines,
            'refund_lines': refund_lines
        }
        # print docargs['docs']

        return self.env['report'].render('sales_report_by_saleperson.sale_productcate', docargs)

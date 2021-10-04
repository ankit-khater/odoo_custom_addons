from odoo import api, models
from datetime import datetime, timedelta


class ReportSalesSalespersonWise(models.AbstractModel):
    _name = 'report.sales_report_by_saleperson.sale_productcate_doctor'

    def prepare_productcate_refund_line_by_date(self, start_date, end_date, categ_id,id):
        print "function call"
        print start_date
        print end_date
        print categ_id


        print "Doctor_ID:",id

        list = []

        def recursive(categ_id):
            data = self.env['product.category'].search([('id', '=', categ_id)])
            print data
            for i in data:
                print "category name:", i.name
                data1 = self.env['product.template'].search([('categ_id', '=', i.id)])
                c = self.env['product.template'].search_count([('categ_id', '=', i.id)])

                print c
                print data1
                for j in data1:
                 data2 = self.env['product.product'].search([('product_tmpl_id','=',j.id)])
                 for p in data2:
                    count = self.env['account.invoice.line'].search_count(
                        ['&', ('product_id', '=', p.id), ('write_date', '>=', start_date),
                         ('write_date', '<=', end_date)])
                    dict = {'name': '', 'quantity': '', 'total': '', 'category': '','type': ''}
                    print j.name
                    data3 = self.env['account.invoice.line'].search(
                        ['&','&', ('product_id', '=', p.id), ('write_date', '>=', start_date),
                         ('write_date', '<=', end_date),])
                    qty = 0
                    sum = 0
                    flag = False

                    paid_flag=False
                    typ=''
                    for k in data3:
                        print "Invoice_Id:", k.invoice_id.id
                        user = self.env['account.invoice'].search(
                            [('id', '=', k.invoice_id.id), ('doctor_refer', '=', id), ('origin', '=', k.origin),
                             ('create_date', '>=', start_date),
                             ('create_date', '<=', end_date), ('state', '=', 'paid')])

                        print "Product:",k.name
                        user_flag = False
                        for u in user:
                            if u.doctor_refer.id==id:
                                user_flag=True
                                print user_flag
                                print "userrrr:",u.user_id.id

                        if user_flag and k.price_subtotal_signed < 0:
                                flag = True
                                # if k.price_subtotal_signed  > 0:
                                qty = qty + k.quantity
                                # elif k.price_subtotal_signed  < 0 :

                                sum = (sum + k.price_subtotal_signed) *-1

                    print "Sale Quantity:", qty
                    print "Total:", sum
                    if flag:
                        if count != 0:
                            dict['name'] = j.name
                            dict['quantity'] = int(qty)
                            dict['total'] = sum
                            dict['category'] = i.name
                            # dict['type']=typ
                            list.append(dict)
                            print dict
                            print list
                # data2 = self.env['product.category'].search([('parent_id', '=', i.id)])
                # for l in data2:
                #     recursive(l.id)  # function call itself
                return list

        lst = recursive(categ_id)
        print "List of Dictonary", lst
        params = (categ_id, start_date, end_date)
        print params
        self.env.cr.execute('select * from product_category where parent_id = 1', params)
        res = self.env.cr.dictfetchall()
        print res
        return lst

    def prepare_productcate_line_by_date(self, start_date, end_date, categ_id,id):
        print "function call"
        print start_date
        print end_date
        print categ_id
        # id = self.get_default_user()
        print "User_ID:", id
        # function use for recursion
        list = []

        def recursive(categ_id):
            data = self.env['product.category'].search([('id', '=', categ_id)])
            print data
            for i in data:
                print "category name:", i.name
                data1 = self.env['product.template'].search([('categ_id', '=', i.id)])
                c = self.env['product.template'].search_count([('categ_id', '=', i.id)])

                print c
                print data1
                for j in data1:
                 data2 = self.env['product.product'].search([('product_tmpl_id','=',j.id)])
                 for p in data2:
                    count = self.env['account.invoice.line'].search_count(
                        ['&', ('product_id', '=', p.id), ('write_date', '>=', start_date),
                         ('write_date', '<=', end_date)])
                    dict = {'name': '', 'quantity': '', 'total': '', 'category': '','type': ''}
                    print j.name
                    data3 = self.env['account.invoice.line'].search(
                        ['&','&', ('product_id', '=', p.id), ('write_date', '>=', start_date),
                         ('write_date', '<=', end_date),])
                    qty = 0
                    sum = 0
                    flag = False

                    paid_flag=False
                    typ=''
                    for k in data3:
                        print "Invoice_Id:", k.invoice_id.id
                        user = self.env['account.invoice'].search([('id', '=', k.invoice_id.id), ('doctor_refer', '=', id),('origin','=',k.origin),('create_date', '>=', start_date),
                         ('create_date', '<=', end_date),('state','=','paid')])

                        print "Product:",k.name
                        user_flag = False
                        for u in user:
                            if u.doctor_refer.id==id:
                                user_flag=True
                                print user_flag
                                print "userrrr:",u.user_id.id

                        if user_flag and k.price_subtotal_signed>0:
                                flag = True
                                # if k.price_subtotal_signed  > 0:
                                qty = qty + k.quantity
                                # elif k.price_subtotal_signed  < 0 :

                                sum = (sum + k.price_subtotal_signed)

                    print "Sale Quantity:", qty
                    print "Total:", sum
                    if flag:
                        if count != 0:
                            dict['name'] = j.name
                            dict['quantity'] = int(qty)
                            dict['total'] = sum
                            dict['category'] = i.name
                            # dict['type']=typ
                            list.append(dict)
                            print dict
                            print list
                # data2 = self.env['product.category'].search([('parent_id', '=', i.id)])
                # for l in data2:
                #     recursive(l.id)  # function call itself
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
        report = report_obj._get_report_from_name('sales_report_by_saleperson.sale_productcate_doctor')
        print report
        lines = self.prepare_productcate_line_by_date(docs.start_date, docs.end_date, docs.categ_id.id,docs.doctor.id)
        print lines
        refund_lines = self.prepare_productcate_refund_line_by_date(docs.start_date, docs.end_date, docs.categ_id.id,docs.doctor.id)
        DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
        sd = datetime.strptime(docs.start_date, DATETIME_FORMAT)
        ed = datetime.strptime(docs.end_date, DATETIME_FORMAT)
        sd_convert = sd + timedelta(hours=6, minutes=00)
        ed_convert = ed + timedelta(hours=6, minutes=00)
        print sd_convert
        print ed_convert
        docargs = {
            'doc_model': data.get('model'),
            'docs': self,
            'from_date': docs.start_date,
            'to_date': docs.end_date,
            'category': docs.categ_id.name,
            'lines': lines,
            'refund_lines': refund_lines,
            # 'us':docs.user.name,
            'doctor':docs.doctor.name_provider,
            'convert_sd':sd_convert,
            'convert_ed':ed_convert

        }
        # print docargs['docs']

        return self.env['report'].render('sales_report_by_saleperson.sale_productcate_doctor', docargs)

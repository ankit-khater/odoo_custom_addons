import json
import socket
import urllib3
import numpy
from odoo import http, fields
from odoo.http import Controller, request, route
from datetime import datetime, timedelta


class ApiController(Controller):
    # User Wise Bill Report(Single)
    @route('/billReportSingle/<string:startDate>/<string:endDate>/<int:uid>', type='http', auth="public", website=True,
           content_type='application/json; charset = utf-8')
    def api_user_report_single(self, startDate, endDate, uid, **post):
        DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
        sd = datetime.strptime(startDate, DATETIME_FORMAT)
        ed = datetime.strptime(endDate, DATETIME_FORMAT)
        sd_convert = sd + timedelta(hours=6, minutes=00)
        ed_convert = ed + timedelta(hours=6, minutes=00)
        fmt = "%Y-%m-%d %H:%M:%S"
        free = 'fixed'
        paid = 'none'

        #GETTING THE CURRENT USER
        user = request.env['res.users'].search([('id', '=', uid)])

        # RETRIVE PAID INVOICE DATA USER WISE
        account_invoice_datas=request.env['account.invoice'].search([('write_uid','=',uid),('create_date','>=',startDate),('create_date','<=',endDate),('state','=','paid'),('type','=','out_invoice'),('discount_type','!=','fixed')])
        print account_invoice_datas

        #COUNT PAID PATIENT USER WISE
        paidPatient = request.env['account.invoice'].search_count(
            [('write_uid', '=', uid), ('create_date', '>=', startDate), ('create_date', '<=', endDate),
             ('state', '=', 'paid'), ('type', '=', 'out_invoice'),('discount_type','!=','fixed')])

        print "Invoice Count",paidPatient

        #COUNT FREE PATIENT USER WISE
        freePatient=request.env['account.invoice'].search_count(
            [('write_uid', '=', uid), ('create_date', '>=', startDate), ('create_date', '<=', endDate),
             ('state', '=', 'paid'), ('type', '=', 'out_invoice'),('discount_type','=','fixed')])

        print "free patient count",freePatient

        #CALCULLATE THE TOTAL PAID AMOUNT
        totalAmount=0
        for inv in account_invoice_datas:
            totalAmount += inv.amount_total_signed

        account_invoice_refund = request.env['account.invoice'].search(
            [('write_uid', '=', uid), ('create_date', '>=', startDate), ('create_date', '<=', endDate),
             ('state', '=', 'paid'), ('type', '=', 'out_refund')])

        print account_invoice_refund

        #CALCULATE THE TOTAL REFUND AMOUNT
        totalRefund=0
        for refInv in account_invoice_refund:
            totalRefund += refInv.amount_total_signed

        #CALCULATE THE NET AMOUNT
        netCollection=totalAmount+totalRefund

        list=[]
        dict={
            'userName':user.partner_id.name,
            'freePatient':freePatient,
            'paidPatient':paidPatient,
            'totalCallection':netCollection
        }
        list.append(dict)

        print "User Wise Collection",list

        context = {
            'start_date': sd_convert,
            'end_date': ed_convert,
            'data':list
        }
        return request.render('custom_report.single_user_bill_report', context)


    # User wise Test bill report
    @route('/billReportDet/<string:startDate>/<string:endDate>/<int:uid>', type='http', auth="public", website=True,
           content_type='application/json; charset = utf-8')
    # @route('/hello/<model("patient.patient"):patient>', type='http', auth="public", website=True)
    def api_user_report_det(self, startDate, endDate, uid, **post):
        DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
        sd = datetime.strptime(startDate, DATETIME_FORMAT)
        ed = datetime.strptime(endDate, DATETIME_FORMAT)
        sd_convert = sd + timedelta(hours=6, minutes=00)
        ed_convert = ed + timedelta(hours=6, minutes=00)

        collection = "out_invoice"
        refund = "out_refund"
        free = 'fixed'
        paid = 'none'

        user = request.env['res.users'].search([('id', '=', uid)])
        sale_collection = request.env['account.invoice'].search(
            [('state', '=', 'paid'), ('create_date', '>=', startDate), ('create_date', '<=', endDate)])

        result_dict = []

        filter_by_user = list(filter(lambda x: x.write_uid == user, sale_collection))
        filter_by_type = list(filter(lambda x: x.type == collection, filter_by_user))
        filtered_by_date = list(
            filter(lambda x: x.create_date >= startDate and x.create_date <= endDate, filter_by_type))

        filter_by_without_refund = []
        filter_by_with_refund = []
        for fd in filtered_by_date:
            refund_invoice = request.env['account.invoice'].search([('origin', '=', fd.move_name)])
            if len(refund_invoice) == 0:
                filter_by_without_refund.append(fd)
            else:
                for ref in refund_invoice:
                    if fd.amount_total != ref.amount_total:
                        filter_by_with_refund.append(ref)

        # for fd in filtered_by_date:
        for fd in filter_by_without_refund:
            main_invoice = request.env['account.invoice'].search([('move_name', '=', fd.move_name)])
            main_line = request.env['account.invoice.line'].search([('invoice_id', '=', main_invoice.id)])
            refund_invoice = request.env['account.invoice'].search([('origin', '=', main_invoice.move_name)])
            ref_line = request.env['account.invoice.line'].search([('invoice_id', '=', refund_invoice.id)])
            serviceList = []

            len(refund_invoice)

            if len(refund_invoice) > 0:
                for m in main_line:
                    serviceListAdd = []
                    serviceListAdd.append(main_invoice.partner_id.name)
                    serviceListAdd.append(main_invoice.date_invoice)
                    serviceListAdd.append(main_invoice.number)
                    serviceListAdd.append(main_invoice.origin)
                    serviceListAdd.append(main_invoice.amount_total)  # ????????????????????????/
                    sn = []
                    for r in ref_line:
                        if m.product_id != r.product_id:
                            sn.append(m.name)
                            serviceListAdd.append(sn)
                        serviceList.append(serviceListAdd)
                result_dict.append(serviceList)

            else:
                serviceListAdd = []
                serviceListAdd.append(main_invoice.partner_id.name)
                serviceListAdd.append(main_invoice.date_invoice)
                serviceListAdd.append(main_invoice.number)
                serviceListAdd.append(main_invoice.origin)
                if main_invoice.discount_type == free:
                    serviceListAdd.append(0.0)
                else:
                    serviceListAdd.append(main_invoice.amount_total)
                sn = []
                for m in main_line:
                    sn.append(m.name)
                    serviceListAdd.append(sn)
                serviceListAdd.append(main_invoice.discount_type)
                serviceList.append(serviceListAdd)
            result_dict.append(serviceList)

        print "sssssss ",filter_by_with_refund
        for fd in filter_by_with_refund:
            main_invoice = request.env['account.invoice'].search([('move_name', '=', fd.origin)])
            main_line = request.env['account.invoice.line'].search([('invoice_id', '=', main_invoice.id)])
            # refund_invoice = request.env['account.invoice'].search([('origin', '=', fd.move_name)])
            ref_line = request.env['account.invoice.line'].search([('invoice_id', '=', fd.id)])
            after_refund_total = 0.0
            after_refund_sn = []
            serviceList = []

            for r in ref_line:
                sn = []
                net_total = 0.0
                print "refund line :", r.name, ';', r.product_id, '22 /n', r.origin, ' ', r.price_subtotal
                for m in main_line:
                    if m.product_id != r.product_id:
                        print "main line :", m.name, ';', m.product_id, '33 /n', m.origin, ' ', m.price_subtotal
                        sn.append(m.name)
                        net_total += m.price_subtotal
                if len(sn) > 0:
                    # print sn
                    # print net_total
                    after_refund_total = net_total
                    after_refund_sn = sn

            serviceListAdd = []
            serviceListAdd.append(main_invoice.partner_id.name)
            serviceListAdd.append(main_invoice.date_invoice)
            serviceListAdd.append(main_invoice.number)
            serviceListAdd.append(main_invoice.origin)
            serviceListAdd.append(after_refund_total)
            serviceListAdd.append(after_refund_sn)
            serviceListAdd.append(main_invoice.discount_type)
            serviceList.append(serviceListAdd)
            result_dict.append(serviceList)

        context = {
            'start_date': sd_convert,
            'end_date': ed_convert,
            'data': result_dict,
            'user': user,
        }
        return request.render('custom_report.bill_user_report_det', context)

    # User Wise Daily Bill Collection Report
    @route('/billReportUserWiseAll/<string:startDate>/<string:endDate>', type='http', auth="public",
           website=True)
    def api_user_report(self, startDate, endDate, **post):
        DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
        sd = datetime.strptime(startDate, DATETIME_FORMAT)
        ed = datetime.strptime(endDate, DATETIME_FORMAT)
        sd_convert = sd + timedelta(hours=6, minutes=00)
        ed_convert = ed + timedelta(hours=6, minutes=00)
        # fmt = "%Y-%m-%d %H:%M:%S"
        # free = 'fixed'
        # paid = 'none'

        users = request.env['res.users'].search([('active', '=', 'true')])
        final_data = []

        for user in users:
            # RETRIVE PAID INVOICE DATA USER WISE
            account_invoice_datas = request.env['account.invoice'].search([('write_uid', '=', user.id), ('create_date', '>=', startDate), ('create_date', '<=', endDate),('state', '=', 'paid'), ('type', '=', 'out_invoice')])

            #CALCULATE TOTAL PAID AMOUNT USER WISE
            totalAmount = 0
            for inv in account_invoice_datas:
                totalAmount += inv.amount_total_signed

            #COUNT THE PAID PATIENT
            paidPatient = request.env['account.invoice'].search_count(
                [('write_uid', '=', user.id), ('create_date', '>=', startDate), ('create_date', '<=', endDate),
                 ('state', '=', 'paid'), ('type', '=', 'out_invoice'), ('discount_type', '!=', 'fixed')])

            #COUNT THE FREE PATIENT
            freePatient = request.env['account.invoice'].search_count(
                [('write_uid', '=', user.id), ('create_date', '>=', startDate), ('create_date', '<=', endDate),
                 ('state', '=', 'paid'), ('type', '=', 'out_invoice'), ('discount_type', '=', 'fixed')])
            #RETRIVE THE REFUND DATA USER WISE
            account_invoice_refund = request.env['account.invoice'].search(
                [('write_uid', '=', user.id), ('create_date', '>=', startDate), ('create_date', '<=', endDate),
                 ('state', '=', 'paid'), ('type', '=', 'out_refund')])

            print account_invoice_refund
            #CALCULATE TOTAL REFUND USER WISE
            totalRefund = 0
            for refInv in account_invoice_refund:
                totalRefund += refInv.amount_total_signed

            #CALCULATE THE NET AMONT USER WISE
            netCollection = totalAmount + totalRefund

            dict = {
                'userName': user.partner_id.name,
                'freePatient':freePatient,
                'paidPatient':paidPatient,
                'totalCallection': netCollection
            }

            #CONDITION FOR CHECKS WHEATHER USER HAS ANY COLLECTION OR NOT
            if netCollection != 0:
                final_data.append(dict)
        print "final data",final_data

        context = {
            'start_date': sd_convert,
            'end_date': ed_convert,
            'data': final_data,
        }
        return request.render('custom_report.bill_user_wise_report', context)

    # Department Wise Report
    @route(
        '/departmentWiseReport/<string:start_date>/<string:end_date>/<int:user_id>/<int:categ_id>/<string:categ_name>/<string:user_name>',
        type='http', auth="public", website=True,
        content_type='application/json; charset = utf-8')
    def departmentWiseReport(self, start_date, end_date, user_id, categ_id, categ_name, user_name, **post):
        DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
        sd = datetime.strptime(start_date, DATETIME_FORMAT)
        ed = datetime.strptime(end_date, DATETIME_FORMAT)
        sd_convert = sd + timedelta(hours=6, minutes=00)
        ed_convert = ed + timedelta(hours=6, minutes=00)


        print "category_name",categ_name
        print "category_id",categ_id
        print "User_id",user_id
        print "User_id",user_name

        def prepare_productcate_line_by_date(start_date, end_date, categ_id, id):
            print "function call"
            print start_date
            print end_date
            print categ_id
            # id = self.get_default_user()
            print "User_ID:", id
            # function use for recursion
            list = []

            def recursive(categ_id):
                data = request.env['product.category'].search([('id', '=', categ_id)])
                print data
                for i in data:
                    print "category name:", i.name
                    data1 = request.env['product.template'].search([('categ_id', '=', i.id)])
                    c = request.env['product.template'].search_count([('categ_id', '=', i.id)])
                    print c
                    print data1
                    for j in data1:
                        data2 = request.env['product.product'].search([('product_tmpl_id', '=', j.id)])
                        for p in data2:
                            count = request.env['account.invoice.line'].search_count(
                                ['&', ('product_id', '=', p.id), ('write_date', '>=', start_date),
                                 ('write_date', '<=', end_date)])
                            dict = {'name': '', 'quantity': '', 'total': '', 'category': '', 'type': ''}
                            print j.name
                            data3 = request.env['account.invoice.line'].search(
                                ['&', '&', ('product_id', '=', p.id), ('write_date', '>=', start_date),
                                 ('write_date', '<=', end_date), ('write_uid', '=', id), ])
                            qty = 0
                            sum = 0
                            flag = False

                            paid_flag = False
                            typ = ''
                            for k in data3:
                                print "Invoice_Id:", k.invoice_id.id
                                user = request.env['account.invoice'].search(
                                    [('id', '=', k.invoice_id.id), ('user_id', '=', id),
                                     ('discount_type', '!=', 'fixed'), ('origin', '=', k.origin),
                                     ('create_date', '>=', start_date),
                                     ('create_date', '<=', end_date), ('state', '=', 'paid')])

                                print "Product:", k.name
                                user_flag = False
                                for u in user:
                                    if u.user_id.id == id and u.discount_type == 'none':
                                        user_flag = True
                                        print user_flag
                                        print "userrrr:", u.user_id.id
                                if user_flag and k.price_subtotal_signed > 0:
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
                    return list

            lst = recursive(categ_id)
            print "List of Dictonary", lst
            return lst
        data=prepare_productcate_line_by_date(start_date,end_date,categ_id ,user_id)
        resultFinal=data
        print "Datasssssss list",data

        def prepare_productcate_refund_line_by_date(start_date, end_date, categ_id, id):
            print "function call"
            print start_date
            print end_date
            print categ_id

            # id = self.get_default_user()
            print "User_ID:", id
            # function use for recursion
            list = []

            def recursive(categ_id):
                data = request.env['product.category'].search([('id', '=', categ_id)])
                print data
                for i in data:
                    print "category name:", i.name
                    data1 = request.env['product.template'].search([('categ_id', '=', i.id)])
                    c = request.env['product.template'].search_count([('categ_id', '=', i.id)])

                    print c
                    print data1
                    for j in data1:
                        data2 = request.env['product.product'].search([('product_tmpl_id', '=', j.id)])
                        for p in data2:
                            count = request.env['account.invoice.line'].search_count(
                                ['&', ('product_id', '=', p.id), ('write_date', '>=', start_date),
                                 ('write_date', '<=', end_date)])
                            dict = {'name': '', 'quantity': '', 'total': '', 'category': '', 'type': ''}
                            print j.name
                            data3 = request.env['account.invoice.line'].search(
                                ['&', '&', ('product_id', '=', p.id), ('write_date', '>=', start_date),
                                 ('write_date', '<=', end_date), ('write_uid', '=', id), ])
                            qty = 0
                            sum = 0
                            flag = False

                            paid_flag = False
                            typ = ''
                            for k in data3:
                                print "Invoice_Id:", k.invoice_id.id
                                user = request.env['account.invoice'].search(
                                    [('id', '=', k.invoice_id.id), ('user_id', '=', id),
                                     ('discount_type', '!=', 'fixed'), ])

                                print "Product:", k.name
                                user_flag = False
                                for u in user:
                                    if u.user_id.id == id and u.discount_type == 'none':
                                        user_flag = True
                                        print user_flag
                                        print "userrrr:", u.user_id.id

                                if user_flag and k.price_subtotal_signed < 0:
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
                                    dict['total'] = abs(sum)
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
            print "List of Dictonary refund-------------", lst
            return lst
        data=prepare_productcate_refund_line_by_date(start_date,end_date,categ_id ,user_id)
        refundLine=data
        print "Datas for refund",data
        context = {
            'start_date': sd_convert,
            'end_date': ed_convert,
            'line': resultFinal,
            'refundLine':refundLine,
            'us': user_name,
            'categ_name': categ_name
        }
        return request.render('custom_report.department_wise_report', context)

from odoo.addons.report_xlsx.report.report_xlsx import ReportXlsx
import xlsxwriter
from odoo import models, fields, api
import time
from odoo import api, models
from odoo.exceptions import UserError


class ReportTrailXlsx(ReportXlsx):

    def generate_xlsx_report(self, workbook, data, lines):
        print "Xlsx Generated"
        vals=data['data_values']

        print vals
        # workbook = xlsxwriter.Workbook('Expenses01.xlsx')
        # sheet = workbook.add_worksheet()
        bold = workbook.add_format({'bold': 1})

        list=[]
        for j in vals:
            list.append(j['code'])
        print list

        list2=[]
        for i in vals:
            list2.append(i['name'])

        list3=[]
        for i in vals:
            list3.append(i['debit'])

        list4=[]
        for i in vals:
            list4.append(i['credit'])

        list5 = []
        for i in vals:
            list5.append(i['balance'])


        # workbook = xlsxwriter.Workbook('Expenses01.xlsx')
        worksheet = workbook.add_worksheet()
        worksheet.write('A1', 'Code',bold)
        worksheet.write('B1', 'Account',bold)
        worksheet.write('C1', 'Debit',bold)
        worksheet.write('D1', 'Credit',bold)
        worksheet.write('E1', 'Balance',bold)

        row = 1
        col = 0

        # Iterate over the data and write it out row by row.
        for item in (list):
            worksheet.write(row, 0, item)
            # worksheet.write(row, col + 1, cost)
            row += 1
        row2=1
        for item in (list2):
            worksheet.write(row2, 1, item)
            # worksheet.write(row, col + 1, cost)
            row2 += 1
        row3=1
        for item in (list3):
            worksheet.write(row3, 2, item)
            # worksheet.write(row, col + 1, cost)
            row3 += 1
        row4=1
        for item in (list4):
            worksheet.write(row4, 3, item)
            # worksheet.write(row, col + 1, cost)
            row4 += 1
        row5=1
        for item in (list5):
            worksheet.write(row5, 4, item)
            # worksheet.write(row, col + 1, cost)
            row5 += 1

        workbook.close()

ReportTrailXlsx('report.account_balance_report.report_account_balance_report.xlsx','account.balance.report')
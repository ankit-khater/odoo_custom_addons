from odoo.addons.report_xlsx.report.report_xlsx import ReportXlsx

class ReportBalanceSheetXlsx(ReportXlsx):

    def generate_xlsx_report(self, workbook, data, lines):

        print "ExcelGenerated",data['line']

        vals=data['line']

        flag=data['debitCredit']

        if flag != True:
            list=[]
            for i in vals[1:]:
                list.append(i['name'])

            print"Name",list

            list1=[]
            for i in vals[1:]:
                list1.append(i['balance'])

            print "Balance",list1

            bold = workbook.add_format({'bold': 1})

            worksheet = workbook.add_worksheet()
            worksheet.write('A1', 'Name', bold)
            worksheet.write('B1', 'Balance', bold)

            row = 1
            col = 0

            # Iterate over the data and write it out row by row.
            for item in (list):
                worksheet.write(row, 0, item)
            # worksheet.write(row, col + 1, cost)
                row += 1

            row2 = 1
            col = 0

            # Iterate over the data and write it out row by row.
            for item in (list1):
                worksheet.write(row2, 1, item)
            # worksheet.write(row, col + 1, cost)
                row2 += 1

        if flag:

            list = []
            for i in vals[1:]:
                list.append(i['name'])

            print"Name", list

            list1 = []
            for i in vals[1:]:
                list1.append(i['debit'])

            print "Debit", list1

            list2=[]
            for i in vals[1:]:
                list2.append(i['credit'])

            print "Credit",list2

            list3=[]
            for i in vals[1:]:
                list3.append(i['balance'])

            print "Balance", list3
            bold = workbook.add_format({'bold': 1})

            worksheet = workbook.add_worksheet()
            worksheet.write('A1', 'Name', bold)
            worksheet.write('B1', 'Debit', bold)
            worksheet.write('C1', 'Credit', bold)
            worksheet.write('D1', 'Balance', bold)

            row = 1
            col = 0

            # Iterate over the data and write it out row by row.
            for item in (list):
                worksheet.write(row, 0, item)
                # worksheet.write(row, col + 1, cost)
                row += 1

            row2 = 1
            col = 0

            # Iterate over the data and write it out row by row.
            for item in (list1):
                worksheet.write(row2, 1, item)
                # worksheet.write(row, col + 1, cost)
                row2 += 1

            row3 = 1
            col = 0

            # Iterate over the data and write it out row by row.
            for item in (list2):
                worksheet.write(row3, 2, item)
                # worksheet.write(row, col + 1, cost)
                row3 += 1

            row4 = 1
            col = 0

            # Iterate over the data and write it out row by row.
            for item in (list3):
                worksheet.write(row4, 3, item)
                # worksheet.write(row, col + 1, cost)
                row4 += 1


ReportBalanceSheetXlsx('report.accounting_report.report_accounting_report.xlsx','accounting.report')
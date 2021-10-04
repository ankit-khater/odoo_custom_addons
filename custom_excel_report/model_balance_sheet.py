
from odoo import api, fields, models

class AccountingReportInherited(models.TransientModel):
    _inherit='accounting.report'

    def print_excel(self):
        print "call from button"

        data=self.check_report()
        data['data']['form']['date_to']=self.date_to
        print "Datasss", data['data']['form']
        line=self.env['report.account.report_financial'].get_account_lines(data['data']['form'])
        print"----------------------", line
        print self.debit_credit
        data={
            'debitCredit':self.debit_credit,
            'line':line
        }

        return {'type': 'ir.actions.report.xml',
                'report_name': 'accounting_report.report_accounting_report.xlsx',
                'datas':data

                }




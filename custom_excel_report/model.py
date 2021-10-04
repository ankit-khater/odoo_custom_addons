
from odoo import api, fields, models


class ReportTrialBalance(models.AbstractModel):
    _inherit = ['report.account.report_trialbalance']

    @api.model
    def _get_accounts(self, accounts, display_account):
        res = super(ReportTrialBalance, self)._get_accounts(accounts, display_account)
        return res




class InheritAccountJournal(models.TransientModel):
    _inherit = 'account.balance.report'

    @api.multi
    def _get_accounts_data(self, accounts, display_account,tables,where_clause,where_params):
        """ compute the balance, debit and credit for the provided accounts
            :Arguments:
                `accounts`: list of accounts record,
                `display_account`: it's used to display either all accounts or those accounts which balance is > 0
            :Returns a list of dictionary of Accounts with following key and value
                `name`: Account name,
                `code`: Account code,
                `credit`: total amount of credit,
                `debit`: total amount of debit,
                `balance`: total amount of balance,
        """

        account_result = {}
        # Prepare sql query base on selected parameters from wizard
        tables, where_clause, where_params = tables,where_clause,where_params

        # print tables, where_clause, where_params
        # print "tables data",tables
        # print "Table Type",type(tables)
        # print "where clause data",where_clause
        # print "where clause",type(where_clause)
        # print "where params data",where_params
        # print "where params",type(where_params)

        tables = tables.replace('"','')
        if not tables:
            tables = 'account_move_line'
        wheres = [""]
        if where_clause.strip():
            wheres.append(where_clause.strip())
        filters = " AND ".join(wheres)
        # compute the balance, debit and credit for the provided accounts
        request = ("SELECT account_id AS id, SUM(debit) AS debit, SUM(credit) AS credit, (SUM(debit) - SUM(credit)) AS balance" +\
                   " FROM " + tables + " WHERE account_id IN %s " + filters + " GROUP BY account_id")
        params = (tuple(accounts.ids),) + tuple(where_params)
        self.env.cr.execute(request, params)
        for row in self.env.cr.dictfetchall():
            account_result[row.pop('id')] = row
        account_res = []
        for account in accounts:
            res = dict((fn, 0.0) for fn in ['credit', 'debit', 'balance'])
            currency = account.currency_id and account.currency_id or account.company_id.currency_id
            res['code'] = account.code
            res['name'] = account.name
            if account.id in account_result.keys():
                res['debit'] = account_result[account.id].get('debit')
                res['credit'] = account_result[account.id].get('credit')
                res['balance'] = account_result[account.id].get('balance')
            if display_account == 'all':
                account_res.append(res)
            if display_account == 'not_zero' and not currency.is_zero(res['balance']):
                account_res.append(res)
            if display_account == 'movement' and (not currency.is_zero(res['debit']) or not currency.is_zero(res['credit'])):
                account_res.append(res)
        print "data from core report model",account_res
        return account_res

    @api.multi
    def print_excel_1(self,data):
        print "call from button function"
        print self.date_from
        print self.date_to
        print self.target_move
        print self.display_account
        account_data = self.env['account.account'].search([])


        if self.target_move=="all" and self.date_to != False and self.date_from != False:
            tables='"account_move_line"'
            where_clause='(("account_move_line"."date" <= %s)  AND  ("account_move_line"."date" >= %s))'
            where_params=[self.date_to,self.date_from]
            print where_params
            print where_clause

        if self.target_move=="all" and self.date_to == False:
            tables='"account_move_line"'
            where_clause ='("account_move_line"."date" >= %s)'
            where_params=[self.date_from]
            print where_params
            print where_clause

        if self.target_move=="all" and self.date_from == False:
            tables='"account_move_line"'
            where_clause ='("account_move_line"."date" <= %s)'
            where_params=[self.date_to]
            print where_params
            print where_clause

        if self.target_move == "all" and self.date_to == False and self.date_from == False:
            tables = ''
            where_clause = ''
            where_params = []
            print where_params
            print where_clause


        if self.target_move=="posted" and self.date_to != False and self.date_from != False:
            tables = '"account_move" as "account_move_line__move_id","account_move_line"'
            where_clause = '("account_move_line"."move_id"="account_move_line__move_id"."id") AND ((("account_move_line"."date" <= %s)  AND  ("account_move_line"."date" >= %s))  AND  ("account_move_line__move_id"."state" = %s))'
            where_params = [self.date_to, self.date_from,'posted']
            print where_params
            print where_clause

        if self.target_move=="posted" and self.date_to == False:
            tables = '"account_move" as "account_move_line__move_id","account_move_line"'
            where_clause = '("account_move_line"."move_id"="account_move_line__move_id"."id") AND (("account_move_line"."date" >= %s)  AND  ("account_move_line__move_id"."state" = %s))'
            where_params = [self.date_from, 'posted']
            print where_params
            print where_clause

        if self.target_move == "posted" and self.date_from == False:
            tables = '"account_move" as "account_move_line__move_id","account_move_line"'
            where_clause = '("account_move_line"."move_id"="account_move_line__move_id"."id") AND (("account_move_line"."date" <= %s)  AND  ("account_move_line__move_id"."state" = %s))'
            where_params = [self.date_to, 'posted']
            print where_params
            print where_clause

        if self.target_move=="posted" and self.date_to == False and self.date_from == False:
            tables = '"account_move" as "account_move_line__move_id","account_move_line"'
            where_clause = '("account_move_line"."move_id"="account_move_line__move_id"."id") AND ("account_move_line__move_id"."state" = %s)'
            where_params = ['posted']
            print where_params
            print where_clause


        data_value = self._get_accounts_data(account_data, self.display_account, tables, where_clause, where_params)

        print "hhhhhhhhhhhhhhh",data_value

        data={
            'date_from':self.date_from,
            'date_to':self.date_to,
            'target_move':self.target_move,
            'display_account':self.display_account,
            'data_values':data_value,
        }
        return {'type': 'ir.actions.report.xml',
                'report_name': 'account_balance_report.report_account_balance_report.xlsx',
                'datas': data,

                }

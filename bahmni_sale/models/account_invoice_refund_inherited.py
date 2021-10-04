
from odoo import models,fields,api,_

class AccountInvoiceRefundInherited(models.TransientModel):
    _inherit = 'account.invoice.refund'


    @api.multi
    def _get_inv(self):
        self.inv=self.env['account.invoice'].browse(self._context.get('inv'))
        return self.inv

    inv = fields.Char('Invoice Number', compute=_get_inv,readonly=False)

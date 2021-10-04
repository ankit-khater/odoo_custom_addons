from odoo import fields, models, api

class AccountInvoice(models.Model):
    _inherit='account.invoice'

    doctor_refer = fields.Many2one('res.doctor', string='Referal Doctor', store=True, readonly=False)
    consultant_refer = fields.Many2one('res.consultant', string='Referal Consultant', store=True, readonly=False)
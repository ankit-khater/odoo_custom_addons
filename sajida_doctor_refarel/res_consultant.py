from odoo import models,fields,api

class Consultant(models.Model):
    _name = 'res.consultant'

    _rec_name = 'name_provider'


    # recipient = fields.Many2one(comodel_name='sale.order', store=True)
    name_provider= fields.Char(string='Consultant',store=True)

    department = fields.Many2one('res.doctor.department', string='Department',store=True)

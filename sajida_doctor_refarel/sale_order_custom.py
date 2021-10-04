
from lxml import etree
from odoo import fields, models,api
import logging
_logger = logging.getLogger(__name__)

class SaleOrder(models.Model):

    _inherit = 'sale.order'
    _rec_name = "doctor_refer"

    @api.multi
    @api.onchange('provider_name')
    def set_field2(self,**kw):

        doctor_count = self.env['res.doctor'].search_count([('name_provider','=',self.provider_name)])
        print doctor_count
        # for record in doctor:
        #     print record.name_provider
        doctor = self.env['res.doctor'].search([('name_provider', '=', self.provider_name)]).id
        print doctor
        if (self.provider_name != False) and (doctor_count == 0) and (self.doctor_refer != False) and (self.consultant_refer != False):
            vals = {
                'name_provider': self.provider_name
            }
            self.env['res.doctor'].create(vals)

        else:
            print 'Execute Else block'

    # @api.onchange('provider_name')
    # def set_field(self):
    #     self.name_provider = self.provider_name
    #

    # name_provider = fields.Char('Doctor', required=True, readonly=False,compute='set_field')


    doctor_refer=fields.Many2one('res.doctor', string='Referal Doctor',store=True,readonly=False)
    consultant_refer=fields.Many2one('res.consultant',string='Referal Consultant',store=True,readonly=False)




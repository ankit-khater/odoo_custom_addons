# -*- coding: utf-8 -*-
##############################################################################

##############################################################################

from odoo import api, fields, models
from datetime import datetime, timedelta
from pytz import timezone


class CustomReportInfo(models.TransientModel):
    _name = 'custom.report.info'

    start_date = fields.Datetime('Start Date', default=fields.Datetime.now(), required=True)
    end_date = fields.Datetime(string="End Date", default=fields.Datetime.now(), required=True)
    user_ids = fields.Many2many('res.users', string="Billing User")
    categ_id = fields.Many2one('product.category', 'Product category', required=False)

    # user wise single report
    @api.multi
    def bill_report_short(self):
        return {
            'type': 'ir.actions.act_url',
            'url': '/billReportSingle/%s' % self.start_date + '/%s' % self.end_date + '/%s' % self.user_ids.id,
            'target': 'current',
            'view_type': 'form',
            'view_mode': 'form'
        }

    # Test Wise Bill Report wizard
    @api.multi
    def bill_report_det(self):
        return {
            'type': 'ir.actions.act_url',
            'url': '/billReportDet/%s' % self.start_date + '/%s' % self.end_date + '/%s' % self.user_ids.id,
            'target': 'current',
            'view_type': 'form',
            'view_mode': 'form'
        }

    # User Wise Daily Bill Collection Report wizard
    @api.multi
    def bill_user_wise_report(self):
        return {
            'type': 'ir.actions.act_url',
            'url': '/billReportUserWiseAll/%s' % self.start_date + '/%s' % self.end_date,
            'target': 'current',
            'view_type': 'form',
            'view_mode': 'form'
        }

    @api.multi
    def department_wise_report(self):

        print "Patient Id------------",self.user_ids.id

        return {
            'type': 'ir.actions.act_url',
            'url': '/departmentWiseReport/%s' % self.start_date + '/%s' % self.end_date + '/%s' % self.user_ids.id + '/%s' % self.categ_id.id + '/%s' % self.categ_id.name + '/%s' % self.user_ids.name,
            'target': 'current',
            'view_type': 'form',
            'view_mode': 'form'
        }

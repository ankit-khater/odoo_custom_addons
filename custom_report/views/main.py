from odoo import models, fields, api, tools
import json
import werkzeug
import json
from odoo.http import request, route
from pytz import timezone
from datetime import timedelta
from datetime import datetime


class PatientRecord(models.Model):
    _name = 'custom.report'

    name = fields.Char(string='Name', required=True)
    action_name = fields.Char(string='Action Name', required=True)
    group = fields.Char(string='Group Name', required=False)

    # start_date = fields.Datetime('Start Date', default=fields.Datetime.now(), required=True)
    # end_date = fields.Datetime(string="End Date", default=fields.Datetime.now(), required=True)
    # user_ids = fields.Many2many('res.users', string="Billing User")

    @api.multi
    def edit_form(self):
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'custom.report',
            'res_id': self.id,
            'target': 'current',
            'flags': {'initial_mode': 'edit'}
            # 'context': {'form_view_initial_mode': 'edit', 'force_detailed_view': 'true'},
        }

    def open_wizard(self, context=None):
        view_id = self.env.ref('custom_report.' + self.action_name).id
        # // custom_report.custom_bill_report_by_user_form_view
        if view_id:
            return {
                'name': str(self.action_name).upper(),
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'custom.report.info',
                'view_id': view_id,
                'target': 'new',
            }
        else:
            return {'warning': {
                'title': ('Warning'),
                'message': ('My warning message.'),
            }
            }

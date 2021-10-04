# -*- coding: utf-8 -*-
##############################################################################

##############################################################################
from odoo import api, models
import json
from pytz import timezone
from datetime import datetime, timedelta


class CustomReportByUserWise(models.AbstractModel):
    _name = 'report.custom_report.bill_user_report_short'

    @api.model
    def render_html(self, docids, data=None):
        DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
        sd = datetime.strptime(data['start_date'], DATETIME_FORMAT)
        ed = datetime.strptime(data['end_date'], DATETIME_FORMAT)
        sd_convert = sd + timedelta(hours=6, minutes=00)
        ed_convert = ed + timedelta(hours=6, minutes=00)
        d = json.dumps(data['form']),
        docargs = {
            'doc_ids': data.get('ids'),
            'doc_model': data.get('model'),
            'data': data['form'],
            'd': d,
            'start_date': sd_convert,
            'end_date': ed_convert,
        }
        docargs
        return self.env['report'].render('custom_report.bill_user_report_short', docargs)


class CustomReportByUserDetils(models.AbstractModel):
    _name = 'report.custom_report.bill_user_report_det'

    @api.model
    def render_html(self, docids, data=None):
        DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
        sd = datetime.strptime(data['start_date'], DATETIME_FORMAT)
        ed = datetime.strptime(data['end_date'], DATETIME_FORMAT)
        sd_convert = sd + timedelta(hours=6, minutes=00)
        ed_convert = ed + timedelta(hours=6, minutes=00)
        d = json.dumps(data['form']),
        print data['form']
        print d
        docargs = {
            'doc_ids': data.get('ids'),
            'doc_model': data.get('model'),
            'data': data['form'],
            'd': d,
            'start_date': sd_convert,
            'end_date': ed_convert,
        }
        docargs
        return self.env['report'].render('custom_report.bill_user_report_det', docargs)

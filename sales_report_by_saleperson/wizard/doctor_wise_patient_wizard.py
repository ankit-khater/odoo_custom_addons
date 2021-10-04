from odoo import api, fields, models

class DoctorWisePatient(models.TransientModel):
    _name = 'doctor.wise.patient'

    start_date = fields.Date('Start Date', default=fields.Date.today(), required=True)
    end_date = fields.Date(string="End Date", default=fields.Date.today(), required=True)

    @api.multi
    def doctor_wise_patient(self,data):
        print 'wizard is working'
        return self.env['report'].get_action(self, 'sales_report_by_saleperson.doctor_wise_patient', data=data)
from odoo import api, models

class DoctorWisePatient(models.AbstractModel):
    _name = 'report.sales_report_by_saleperson.doctor_wise_patient'

    def prepare_doctor_wise_patient(self,startDate,endDate):
        print "Function Calling"

        lst=[]
        def patient_count(self):
            doctor = self.env['res.doctor'].search([])
            print doctor

            for id in doctor:
                dict = {'name': '', 'patient': ''}
                patient_count=self.env['account.invoice'].search_count([('state','=','paid'),('write_date', '>=',startDate),('write_date', '<=',endDate),('doctor_refer','=',id.id)])
                data=self.env['account.invoice'].search([('state','=','paid'),('write_date', '>=',startDate),('write_date', '<=',endDate),('doctor_refer','=',id.id)])
                if patient_count != 0:
                    dict['name']=id.name_provider
                    dict['patient']=int(patient_count)
                    lst.append(dict)
            print "List Of Dictonary",lst
            return lst

        func=patient_count(self)
        print "from inner function",func
        return func




    @api.model
    def render_html(self, docids, data=None):
        self.model = self.env.context.get('active_model')
        docs = self.env[self.model].browse(self.env.context.get('active_id'))
        report_obj = self.env['report']
        report = report_obj._get_report_from_name('sales_report_by_saleperson.doctor_wise_patient')
        func=self.prepare_doctor_wise_patient(docs.start_date, docs.end_date)
        print "from render function", func
        docargs = {
            'doc_model': data.get('model'),
            'docs': self,
            'from_date': docs.start_date,
            'to_date': docs.end_date,
            'data':func

        }

        return self.env['report'].render('sales_report_by_saleperson.doctor_wise_patient',docargs)

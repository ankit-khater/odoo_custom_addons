from odoo import models,fields,api

class Departments(models.Model):
    _name = 'res.doctor.department'
    _rec_name ='name_department'

    name_department=fields.Char(string="Department")

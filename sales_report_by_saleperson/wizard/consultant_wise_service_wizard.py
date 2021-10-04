from odoo import api, fields, models

class ProductcategoryWizard(models.TransientModel):
    _name = 'category.wizard.consultant'

    start_date=fields.Datetime('Start Date', default=fields.Datetime.now(), required=True)
    end_date=fields.Datetime(string="End Date", default=fields.Datetime.now(), required=True)
    categ_id = fields.Many2one('product.category', 'Product category', required=False)
    doctor=fields.Many2one('res.consultant',string="Consultant",required=False)
    @api.multi
    def sale_productcategory_report(self,data):

        return self.env['report'].get_action(self,'sales_report_by_saleperson.sale_productcate_consultant',data=data)
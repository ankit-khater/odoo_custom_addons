from odoo import api, fields, models


class ProductcategoryWizard(models.TransientModel):
    _name = 'category.wizard'

    start_date = fields.Date('Start Date', default=fields.Date.today(), required=True)
    end_date = fields.Date(string="End Date", default=fields.Date.today(), required=True)
    categ_id = fields.Many2one('product.category', 'Product category', required=False)

    @api.multi
    def sale_productcategory_report(self,data):

        return self.env['report'].get_action(self,'sales_report_by_saleperson.sale_productcate',data=data)
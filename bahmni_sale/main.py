import odoo.http as http
from odoo.http import Controller, request, route
from odoo import models


class Invoice(Controller):
    @route('/custom/url/<string:origin>', type='http', auth="public", website='True')
    def show_webpage(self, origin, **post):
        finalInvoiceLines = []
        data = request.env['account.invoice'].sudo().search([('origin', '=', origin)])
        refund_inv = request.env['account.invoice'].sudo().search([('origin', '=', data.move_name)])

        mainInvoicesProductIds = []
        refundInvoicesProductIds = []

        for m in data.invoice_line_ids:
            mainInvoicesProductIds.append(m.product_id)

        if len(refund_inv) > 0:
            for ref in refund_inv:
                for ref1 in ref.invoice_line_ids:
                    refundInvoicesProductIds.append(ref1.product_id)
        else:
            for mainInvoice in data.invoice_line_ids:
                finalInvoiceLines.append(mainInvoice)

        filterList = []
        for mainInv in mainInvoicesProductIds:
            if mainInv not in refundInvoicesProductIds:
                filterList.append(mainInv)

        if len(refundInvoicesProductIds) > 0:
            for m in data.invoice_line_ids:
                for ref in filterList:
                    if m.product_id.id == ref.id:
                        finalInvoiceLines.append(m)

        return request.render("bahmni_sale.custom_page", {
            'data': data,
            'invoiceLines': finalInvoiceLines
        })

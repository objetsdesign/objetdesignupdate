from odoo import fields, models
import base64


class SaleOrder(models.Model):
    _inherit = "sale.order"


class SaleOrderTemplateInherit(models.Model):
    _inherit = "sale.order.template"

    pied_page = fields.Html(string="Pied de page", translate=True)



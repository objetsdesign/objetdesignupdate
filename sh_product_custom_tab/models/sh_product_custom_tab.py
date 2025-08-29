# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import _, fields, models
from odoo.exceptions import UserError


class ProductTab(models.Model):
    _name = 'sh.product.custom.tab'
    _description = 'Custom Tab'
    _order = "sequence, id desc"

    name = fields.Char(string="Tab Name", required=True, translate=True)
    description = fields.Html(string="Tab Description", translate=True)
    active = fields.Boolean("Active")
    sequence = fields.Integer("Sequence")
    code = fields.Char(string='Code')
    is_global = fields.Boolean(string='Global')
    icon = fields.Char(string='Icon',default="fa-exclamation")

    def unlink(self):
        if any(rec.code for rec in self):
            raise UserError(_('You are not able to delete standard records.'))
        return super(ProductTab, self).unlink()

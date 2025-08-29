# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    sh_tab_ids = fields.Many2many(
        comodel_name='sh.product.custom.tab', string='Custom Tab')

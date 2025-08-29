# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields


class Website(models.Model):
    _inherit = 'website'

    sh_tab_style = fields.Selection([('one', 'Style 1'), ('two', 'Style 2'), ('three', 'Style 3'), ('four', 'Style 4'), ('five', 'Style 5'), ('six', 'Style 6')], string='Select Tab Style', default='one')
    sh_product_custom_tab_heading = fields.Char(string='Tab Main Heading')

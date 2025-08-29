# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    sh_tab_style = fields.Selection(
        related='website_id.sh_tab_style', string='Select Tab Style', readonly=False)
    sh_product_custom_tab_heading = fields.Char(
        related='website_id.sh_product_custom_tab_heading', string='Tab Main Heading', readonly=False)

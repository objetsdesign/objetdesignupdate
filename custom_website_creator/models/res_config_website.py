from odoo import api, fields, models


class ResConfigWebsite(models.TransientModel):
    _inherit = 'res.config.settings'

    website_quote = fields.Many2one(
        'website',
        string="Choisir le site",
        index=True,
        store=True,
        config_parameter='website.website_quote'
    )

    page_access = fields.Many2one(
        'website.page',
        string="Choisir la page Devenir client",
        index=True,
        store=True,
        config_parameter='website.page_access'
    )

    crm_team_access = fields.Many2one(
        'crm.team',
        string="Choisir l'équipe de validation d'accès",
        config_parameter='website.crm_team_access'
    )

    crm_team_demande = fields.Many2one(
        'crm.team',
        string="Choisir l'équipe de demande de devis",
        config_parameter='website.crm_team_demande'
    )



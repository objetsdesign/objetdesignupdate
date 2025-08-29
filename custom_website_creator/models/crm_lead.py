from odoo import models, fields, api

class CrmLeads(models.Model):
    _inherit = 'crm.lead'

    lead_line_ids = fields.One2many('crm.lead.line', 'lead_id', string="Produits associés")


class CrmLeadLine(models.Model):
    _name = 'crm.lead.line'
    _description = 'Ligne de produits pour les opportunités CRM'

    lead_id = fields.Many2one('crm.lead', string="Opportunité", ondelete='cascade')
    product_id = fields.Many2one('product.product', string="Produit", required=True)
    product_uom_qty = fields.Float(string="Quantité", required=True)
    price_unit = fields.Float(string="Prix Unitaire", required=True)
    price_subtotal = fields.Float(string="Sous-total", compute="_compute_price_subtotal", store=True)

    @api.depends('product_uom_qty', 'price_unit')
    def _compute_price_subtotal(self):
        for line in self:
            line.price_subtotal = line.product_uom_qty * line.price_unit



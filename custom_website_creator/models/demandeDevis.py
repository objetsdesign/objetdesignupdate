from odoo import api, fields, models, _
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)

class DemandeDevis(models.Model):
    _name = 'demande.devis'
    _inherit = ['mail.thread.cc',
                'mail.thread.blacklist',
                'mail.thread.phone',
                'mail.activity.mixin',
                'utm.mixin',
                'format.address.mixin',
                'mail.tracking.duration.mixin',
                ]
    _description = "Demande de Devis"
    _order = 'sequence desc'

    sequence = fields.Char(string="Référence", required=True, copy=False, readonly=True, default=lambda self: _('New'))
    name = fields.Char(string='Nom', required=True, tracking=True)
    partner_id = fields.Many2one('res.partner', string="Client", required=True, tracking=True)
    phone = fields.Char(related='partner_id.phone', string="Téléphone", readonly=True)
    email = fields.Char(related='partner_id.email', string="Email", readonly=True)
    street = fields.Char(related='partner_id.street', string="Adresse", readonly=True)

    order_line_ids = fields.One2many('demande.devis.line', 'demande_id', string="Lignes de commande")
    state = fields.Selection([
        ('draft', 'Brouillon'),
        ('confirmed', 'Confirmé'),
        ('cancelled', 'Annulé')
    ], string="État", default='draft', tracking=True)

    extra_info = fields.Html(string="Informations supplémentaires")
    devis_creation_date = fields.Datetime(string="Date de création du devis", tracking=True)

    @api.model_create_multi
    def create(self, vals_list):
        _logger.info(f"Valeurs reçues pour la création : {vals_list} ({type(vals_list)})")

        # Vérification que `vals_list` est bien une liste
        if not isinstance(vals_list, list):
            vals_list = [vals_list]  # Convertir un dictionnaire unique en liste

        for vals in vals_list:
            # Gestion de la séquence automatique
            if vals.get('sequence', _('New')) == _('New'):
                vals['sequence'] = self.env['ir.sequence'].next_by_code('demande.devis') or _('New')

        return super(DemandeDevis, self).create(vals_list)

    # @api.model
    # def create(self, vals):
    #     """Génère un numéro de séquence unique lors de la création"""
    #     if vals.get('sequence', _('New')) == _('New'):
    #         vals['sequence'] = self.env['ir.sequence'].next_by_code('demande.devis') or _('New')
    #     return super(DemandeDevis, self).create(vals)

    def action_confirmer_devis(self):
        """Créer un devis (sale.order) à partir de la demande et changer l'état à 'confirmé'."""
        for demande in self:
            if not demande.order_line_ids:
                raise UserError("La demande de devis n'a pas de lignes de commande.")

            # Créer le devis dans le modèle sale.order
            order = self.env['sale.order'].create({
                'partner_id': demande.partner_id.id,
                'origin': demande.name,
                'order_line': [(0, 0, {
                    'product_id': line.product_id.id,
                    'product_uom_qty': line.product_uom_qty,
                    'price_unit': line.price_unit,
                    # 'image_128': line.product_id.image_1920,
                }) for line in demande.order_line_ids],
            })

            # Mettre à jour l'état et enregistrer la date de création du devis
            demande.write({
                'state': 'confirmed',
                # 'devis_creation_date': fields.Datetime.now(),
            })

            # Ouvrir le devis créé
            return {
                'type': 'ir.actions.act_window',
                'res_model': 'sale.order',
                'res_id': order.id,
                'view_mode': 'form',
                'target': 'current',
            }

    def action_annuler_devis(self):
        """Annuler la demande sans créer de devis."""
        self.write({'state': 'cancelled'})
        return True



class DemandeDevisLine(models.Model):
    _name = 'demande.devis.line'
    _description = "Ligne de Demande de Devis"

    demande_id = fields.Many2one('demande.devis', string="Demande de devis", required=True, ondelete="cascade")
    product_id = fields.Many2one('product.product', string="Produit", required=True)
    product_uom_qty = fields.Float(string="Quantité", required=True)
    price_unit = fields.Float(string="Prix Unitaire", required=True)
    price_subtotal = fields.Float(string="Total", compute="_compute_price_subtotal", store=True)
    image_1920 = fields.Binary(string="Image", related="product_id.image_1920", store=True, readonly=True)

    @api.depends('product_uom_qty', 'price_unit')
    def _compute_price_subtotal(self):
        for line in self:
            line.price_subtotal = line.product_uom_qty * line.price_unit



class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    image_1920 = fields.Binary(string="Image", related="product_id.image_1920", store=True, readonly=True)

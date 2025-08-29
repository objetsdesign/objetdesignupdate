from odoo import http, fields
from odoo.http import request
import logging

_logger = logging.getLogger(__name__)

class WebsiteSaleDevis(http.Controller):

    @http.route('/shop/remove_order', type='http', auth='public', methods=['POST'], csrf=False, website=True)
    def remove_order(self, **post):
        order = request.website.sale_get_order()
        if order:
            order.sudo().unlink()
            request.session.update({'sale_order_id': None})
            request.website.sale_reset()
            _logger.info("✅ Panier supprimé via popup JS")
            return http.Response(status=200)
        _logger.warning("❌ Aucun panier à supprimer")
        return http.Response(status=204)



    @http.route('/shop/confirm_devis', type='http', auth="public", website=True, methods=['POST'])
    def confirm_devis(self, **post):

        if request.httprequest.method != 'POST':
            return request.redirect('/shop/cart')

        """Enregistrer la demande de devis avec les informations supplémentaires"""
        _logger.info("Début du processus de confirmation de devis")

        # Récupérer les informations supplémentaires envoyées par le formulaire
        extra_info = post.get('extra_info', '').replace('\n', '<br/>')
        _logger.info(f"Valeur reçue pour extra_info: {extra_info}")

        # Récupérer la commande du panier
        order = request.website.sale_get_order()
        if not order or not order.order_line:
            _logger.warning("Aucune commande trouvée ou panier vide")
            return request.redirect('/shop/cart')

        _logger.info(f"Commande trouvée : ID {order.id}, Partner ID : {order.partner_id.id}")

        # Récupérer le client (partner_id) lié à la commande
        partner = order.partner_id

        #🔹 Récupérer l'équipe CRM définie dans la configuration pour la demande de devis
        crm_team_demande_id = request.env['ir.config_parameter'].sudo().get_param('website.crm_team_demande')
        crm_team_demande = request.env['crm.team'].sudo().browse(
            int(crm_team_demande_id)) if crm_team_demande_id else None

        # Vérifier si l'équipe CRM existe bien
        if not crm_team_demande or not crm_team_demande.exists():
            crm_team_demande = None

        # Créer la demande de devis avec `extra_info`
        demande = request.env['demande.devis'].sudo().create({
            'name': f"Demande de devis - {partner.name}",
            'partner_id': partner.id,
            'extra_info': extra_info,
            'devis_creation_date': fields.Datetime.now(),
        })
        _logger.info(f"Demande de devis créée : ID {demande.id}, Extra Info : {extra_info}")

        # Création de l'opportunité CRM
        opportunity = request.env['crm.lead'].sudo().create({
            'name': f"Opportunité - {partner.name}",
            'partner_id': partner.id,
            'email_from': partner.email,
            'phone': partner.phone,
            'description': f"{extra_info}",
            'type': 'opportunity',
            'user_id': crm_team_demande.user_id.id if crm_team_demande and crm_team_demande.user_id else request.env.ref('base.user_admin').id,
            'team_id': crm_team_demande.id if crm_team_demande else False,
        })
        _logger.info(
            f"Opportunité CRM créée : ID {opportunity.id}, Associée au partenaire {partner.name}, Équipe CRM : {crm_team_demande.name if crm_team_demande else 'Aucune'}")

        # Ajouter les lignes de produits à l'opportunité
        for line in order.order_line:
            request.env['crm.lead.line'].sudo().create({
                'lead_id': opportunity.id,
                'product_id': line.product_id.id,
                'product_uom_qty': line.product_uom_qty,
                'price_unit': line.price_unit,
            })

        _logger.info("Lignes de produits ajoutées à l'opportunité CRM")

        # Ajouter les lignes de commande dans la demande de devis
        for line in order.order_line:
            request.env['demande.devis.line'].sudo().create({
                'demande_id': demande.id,
                'product_id': line.product_id.id,
                'product_uom_qty': line.product_uom_qty,
                'price_unit': line.price_unit,
            })

        # Supprimer la commande et réinitialiser la session du panier
        order.sudo().unlink()
        request.session.update({'sale_order_id': None})  # Réinitialisation du panier
        request.website.sale_reset()  # Mise à jour du nombre d'articles dans l'icône du panier
        _logger.info("Le panier a été réinitialisé")

        # Redirection vers la page de confirmation
        return request.redirect('/shop/confirmationpage')

    @http.route('/shop/confirmationpage', type='http', auth="public", website=True)
    def confirmation_page(self, **kwargs):
        """Affiche la page de confirmation après enregistrement du devis"""
        _logger.info("Affichage de la page de confirmation")
        return request.render("custom_website_creator.confirmation_page", {})

    @http.route('/shop/add_to_devis', type='http', auth="public", website=True, methods=['POST'])
    def add_to_devis(self, **post):
        # Récupérer la commande en cours (panier)
        order = request.website.sale_get_order()

        # Vérifier si la commande existe
        if order:
            _logger.info(f"Panier existant trouvé: ID {order.id}")

            # Supprimer la commande existante
            order.sudo().unlink()
            _logger.info(f"Commande {order.id} supprimée automatiquement")

        # Ajouter le produit au panier (logique par défaut d'Odoo)
        # Vous pouvez implémenter ici la logique d'ajout au panier ou utiliser le mécanisme de base d'Odoo

        # Renvoyer une réponse ou rediriger vers la page de confirmation
        return request.redirect('/shop/cart')

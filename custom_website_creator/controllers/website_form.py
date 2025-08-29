from odoo import http
from odoo.http import request


class WebsiteCustomForm(http.Controller):

    @http.route('/custom-form', type='http', auth='public', website=True)
    def custom_form(self, **kwargs):
        # Récupérer l'ID de la page configurée
        page_id = request.env['ir.config_parameter'].sudo().get_param('website.page_access')

        if page_id:
            # Rechercher la page dans le modèle `website.page`
            page = request.env['website.page'].sudo().search([('id', '=', int(page_id))], limit=1)

            if page:
                # Rediriger vers l'URL réelle de la page
                return request.redirect(page.url)

        # Si aucune page configurée ou introuvable, rediriger vers la page de login
        return request.redirect('/web/login')

    @http.route('/custom-form/submit', type='http', auth='public', methods=['POST'], website=True, csrf=False)
    def custom_form_submit(self, **post):
        """Créer une opportunité CRM et l'assigner à l'équipe définie dans la configuration."""

        # Récupération des données du formulaire
        name = post.get('name')
        email = post.get('email')
        phone = post.get('phone')
        street = post.get('street')
        street2 = post.get('street2', '')
        city = post.get('city')
        zip_code = post.get('zip', '')
        country_id = post.get('country_id')
        state_id = post.get('state_id')
        message = post.get('message', '').replace('\n', '<br/>')

        # 🔹 Récupérer l'équipe CRM définie dans la configuration avec sudo()
        crm_team_access_id = request.env['ir.config_parameter'].sudo().get_param('website.crm_team_access')
        crm_team_access = request.env['crm.team'].sudo().browse(int(crm_team_access_id)) if crm_team_access_id else None

        # Vérifier si l'équipe CRM existe bien
        if not crm_team_access or not crm_team_access.exists():
            crm_team_access = None


        # 🔹 Création de l'opportunité CRM avec sudo()
        crm_lead = request.env['crm.lead'].sudo().create({
            'name': f'Demande accès de {name}',
            'contact_name': name,
            'email_from': email,
            'phone': phone,
            'street': street,
            'street2': street2,
            'city': city,
            'zip': zip_code,
            'country_id': int(country_id) if country_id else False,
            'team_id': crm_team_access.id if crm_team_access else False,  # Assignation à l'équipe
            'description': message,
        })

        # 🔹 Envoi de l'e-mail de confirmation
        template = request.env.ref('custom_website_creator.email_template_custom_form')
        if template:
            template.send_mail(crm_lead.id, force_send=True)

        # Redirection vers la page de confirmation
        return request.redirect('/custom-form/success')

    @http.route('/custom-form/success', type='http', auth='public', website=True)
    def custom_form_success(self, **kwargs):
        return request.render('custom_website_creator.template_custom_form_success')

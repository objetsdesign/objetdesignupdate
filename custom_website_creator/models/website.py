from odoo import models, _, _lt


class Website(models.Model):
    _inherit = 'website'

    def _get_checkout_step_list(self):
        """Override to customize checkout button for specific website."""
        self.ensure_one()
        is_extra_step_active = self.viewref('website_sale.extra_info').active
        redirect_to_sign_in = self.account_on_checkout == 'mandatory' and self.is_public_user()

        # Récupérer le site configuré dans les paramètres
        website_quote_id = self.env['ir.config_parameter'].sudo().get_param('website.website_quote')
        website_quote = self.env['website'].browse(int(website_quote_id)) if website_quote_id else None

        # Appel de la méthode originale
        steps = super(Website, self)._get_checkout_step_list()

        # if self == website_quote:
        #     steps = [(['website_sale.cart'], {
        #         'name': _lt("My personalised quotation"),
        #         'current_href': '/shop/cart',
        #         'main_button': _lt("Sign In") if redirect_to_sign_in else _lt("Validate the quote request"),
        #         # valider au dessous
        #         'main_button_href': "/web/login?redirect=/shop/cart" if redirect_to_sign_in else "javascript:(function(){ var form=document.getElementById('o_wsale_checkout_form'); if(form){form.submit();} else {alert('Votre compte n est pas encore validé.'); } })();",
        #         # 'main_button_href': "/web/login?redirect=/shop/cart" if redirect_to_sign_in else "javascript:(function(){ var form=document.getElementById('o_wsale_checkout_form'); if(form){form.submit();} else {window.location='/shop/confirm_devis';} })();",
        #         'back_button': _lt("Continue shopping"),
        #         'back_button_href': '/shop',
        #     }),
        #              ]
        #     return steps

        if self == website_quote:
            user = self.env.user

            # Vérifie si c’est un utilisateur "admin" ou "utilisateur interne" (non portail)
            is_internal_user = not user.has_group('base.group_portal')

            main_button_href = (
                "/web/login?redirect=/shop/cart" if redirect_to_sign_in else (
                        "javascript:(function(){" +
                        (
                            # Utilisateur interne
                            (
                                "let popup=document.createElement('div');"
                                "popup.id='validationPopup';"
                                "popup.style.cssText='display:flex;align-items:center;justify-content:center;position:fixed;top:0;left:0;width:100vw;height:100vh;background:rgba(0,0,0,0.6);z-index:1000;';"
                                "let content=document.createElement('div');"
                                "content.style.cssText='background:#fff;padding:30px;border-radius:8px;max-width:400px;text-align:center;';"
                                "let title=document.createElement('h5');"
                                "title.textContent='⚠️ Attention';"
                                "let msg=document.createElement('p');"
                                "msg.textContent='Votre compte n\\'est pas validé.';"
                                "let btn=document.createElement('button');"
                                "btn.textContent='Annuler';"
                                "btn.className='btn btn-secondary mt-3';"
                                "btn.onclick=function(){"
                                "document.body.removeChild(popup);"
                                "fetch('/shop/remove_order', {method: 'POST'}).then(r=>console.log('🗑️ Panier supprimé'));"
                                "};"
                                "content.appendChild(title);"
                                "content.appendChild(msg);"
                                "content.appendChild(btn);"
                                "popup.appendChild(content);"
                                "document.body.appendChild(popup);"
                                "console.log('✅ Popup created dynamically');"
                            )
                            if is_internal_user else
                            # Utilisateur portail
                            (
                                "var form=document.getElementById('o_wsale_checkout_form');"
                                "if(form){form.submit();"
                                "var link=document.getElementsByName('website_sale_main_button')[0];"
                                "link.style.pointerEvents = 'none';"
                                "link.style.color = 'gray';"
                                "link.style.cursor = 'default';"
                                "}"

                                # "if(window._quoteSubmitted){alert('Déjà envoyé. Veuillez patienter...');return;}"
                                # "window._quoteSubmitted = true;"
                                # "var form=document.getElementById('o_wsale_checkout_form');"
                                # "if(form){form.submit();}"

                            )
                        ) +
                        "})();"
                )
            )

            steps = [(['website_sale.cart'], {
                'name': _lt("My personalised quotation"),
                'current_href': '/shop/cart',
                'main_button': _lt("Sign In") if redirect_to_sign_in else _lt("Validate the quote request"),
                'main_button_href': main_button_href,
                'back_button': _lt("Continue shopping"),
                'back_button_href': '/shop',
            })]
            return steps

        else:
            steps = [(['website_sale.cart'], {
                'name': _lt("Review Order"),
                'current_href': '/shop/cart',
                'main_button': _lt("Sign In") if redirect_to_sign_in else _lt("Checkout"),
                'main_button_href': f'{"/web/login?redirect=" if redirect_to_sign_in else ""}/shop/checkout?try_skip_step=true',
                'back_button': _lt("Continue shopping"),
                'back_button_href': '/shop',
            }), (['website_sale.checkout', 'website_sale.address'], {
                'name': _lt("Delivery"),
                'current_href': '/shop/checkout',
                'main_button': _lt("Confirm"),
                'main_button_href': f'{"/shop/extra_info" if is_extra_step_active else "/shop/confirm_order"}',
                'back_button': _lt("Back to cart"),
                'back_button_href': '/shop/cart',
            })]
            if is_extra_step_active:
                steps.append((['website_sale.extra_info'], {
                    'name': _lt("Extra Info"),
                    'current_href': '/shop/extra_info',
                    'main_button': _lt("Continue checkout"),
                    'main_button_href': '/shop/confirm_order',
                    'back_button': _lt("Back to delivery"),
                    'back_button_href': '/shop/checkout',
                }))
            steps.append((['website_sale.payment'], {
                'name': _lt("Payment"),
                'current_href': '/shop/payment',
                'back_button': _lt("Back to delivery"),
                'back_button_href': '/shop/checkout',
                'main_button_href': '/shop/confirmation',

            }))
            return steps

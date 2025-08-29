from odoo import models, fields, api

# ----------------------------------------------------------------------
# Modèles pour budget
# ----------------------------------------------------------------------
class PartnerBudgetFournisseur(models.Model):
    _name = "partner.budget.fournisseur"
    _description = "Budget Partner Fournisseur"

    name = fields.Char(string="Nom", required=True)  # Haute, Moyenne, Faible
    color_class = fields.Selection([
        ("haute", "Haute"),
        ("moyenne", "Moyenne"),
        ("faible", "Faible"),
    ], string="Classe", required=True)
    color = fields.Integer(string="Couleur", compute="_compute_color", store=True)

    @api.depends("color_class")
    def _compute_color(self):
        mapping = {"haute": 0, "moyenne": 1, "faible": 2}
        for rec in self:
            rec.color = mapping.get(rec.color_class, 0)


class PartnerBudget(models.Model):
    _name = "partner.budget"
    _description = "Budget Partner"

    name = fields.Char(string="Nom", required=True)  # Bronze, Silver, Gold
    color_class = fields.Selection([
        ("bronze", "Bronze"),
        ("silver", "Silver"),
        ("gold", "Gold"),
    ], string="Classe", required=True)
    color = fields.Integer(string="Couleur", compute="_compute_color", store=True)

    @api.depends("color_class")
    def _compute_color(self):
        mapping = {"bronze": 0, "silver": 1, "gold": 2}
        for rec in self:
            rec.color = mapping.get(rec.color_class, 0)


# ----------------------------------------------------------------------
# Certifications et incidents qualité
# ----------------------------------------------------------------------
class PartnerCertification(models.Model):
    _name = 'partner.certification'
    _description = 'Certification Partner'

    name = fields.Char(string='Nom', required=True)  # ISO, CE, autre
    description = fields.Text(string='Description')


class PartnerQualityIncident(models.Model):
    _name = 'partner.quality.incident'
    _description = 'Quality Incident'

    partner_id = fields.Many2one('res.partner', string='Fournisseur', required=True)
    date_incident = fields.Date(string='Date de l’incident', required=True)
    description = fields.Text(string='Description')


# ----------------------------------------------------------------------
# Extension res.partner
# ----------------------------------------------------------------------
class ResPartner(models.Model):
    _inherit = "res.partner"

    # Champs internes
    secteur_activite = fields.Char(string="Secteur d’activité")
    nbr_site = fields.Char(string="Nombre de sites / sièges")
    company_currency_id = fields.Many2one(
        'res.currency', related='company_id.currency_id', store=True
    )

    # --- Équipe interne ---
    commercial_id = fields.Many2one('res.users', string="Commercial assigné")
    autres_commerciaux_ids = fields.Many2many(
        'res.users', 'res_partner_commerciaux_rel', 'partner_id', 'user_id',
        string="Autres commerciaux liés"
    )
    responsable_projet_id = fields.Many2one('res.users', string="Responsable projet / ADV")
    referent_logistique_id = fields.Many2one('res.users', string="Référent logistique")
    referent_facturation_id = fields.Many2one('res.users', string="Référent facturation")

    # Budgets
    budget_ids = fields.Many2many("partner.budget", string="Importance")

    # Zone et Produits
    zone = fields.Selection([
        ('dp_france', 'DP-France'),
        ('dp_allemagne', 'DP-Allemagne'),
        ('dp_tunisie', 'DP-Tunisie'),
        ('dp_autre', 'Autre'),
    ], string="Zone")
    produits = fields.Selection([
        ('textile', 'Textile'),
        ('maroquinerie', 'Maroquinerie'),
        ('electronique', 'Électronique'),
        ('ceramique', 'Céramique'),
    ], string="Produits")

    # Badge VIP
    gold_vip = fields.Boolean(string="Gold VIP")
    gold_vip_text = fields.Char(string="VIP Badge", compute="_compute_gold_vip_text", store=True)

    @api.depends('gold_vip')
    def _compute_gold_vip_text(self):
        for partner in self:
            partner.gold_vip_text = "Gold VIP" if partner.gold_vip else ""

    # Classification client
    statut_relationnel = fields.Selection([
        ("prospect_froid", "Prospect froid"),
        ("prospect_chaud", "Prospect chaud"),
        ("actif", "Client actif"),
        ("inactif", "Client inactif"),
    ], string="Statut relationnel")

    potentiel_strategique = fields.Selection([
        ("vip", "VIP"),
        ("strategique", "Stratégique"),
        ("one_shot", "One shot"),
    ], string="Potentiel stratégique")

    type_client = fields.Selection([
        ("agence", "Agence"),
        ("b2b", "B2B direct"),
        ("marketplace", "Marketplace"),
        ("particulier", "Particulier"),
    ], string="Type client")

    # Localisation
    pays_zone = fields.Many2one("res.country", string="Pays")
    region_zone = fields.Char(string="Région")
    site_location = fields.Char(string="Localisation / Site")

    # Influence & Observations
    influence = fields.Selection([
        ('d', 'Décideur'),
        ('a', 'Approuveur'),
        ('c', 'Consulté'),
        ('i', 'Informé'),
    ], string="Influence (D/A/C/I)")
    observation = fields.Text(string="Observations")

    # Suivi clients
    is_client = fields.Boolean(string="Client", compute='_compute_is_client', store=True)

    @api.depends('customer_rank')
    def _compute_is_client(self):
        for partner in self:
            partner.is_client = partner.customer_rank > 0

    # Stats clients
    ca_cumule = fields.Monetary(string="CA cumulé", compute="_compute_stats")
    commandes_nb = fields.Integer(string="Nombre de commandes", compute="_compute_stats")
    commandes_montant = fields.Monetary(
        string="Montant des commandes", compute="_compute_stats",
        currency_field='company_currency_id'
    )

    @api.depends('sale_order_ids.amount_total', 'sale_order_ids.state')
    def _compute_stats(self):
        for partner in self:
            orders = partner.sale_order_ids.filtered(lambda o: o.state in ['sale', 'done'])
            partner.ca_cumule = sum(orders.mapped('amount_total'))
            partner.commandes_nb = len(orders)
            partner.commandes_montant = partner.ca_cumule

    produits_achetes = fields.Char(
        string="Produits achetés / demandés", compute="_compute_produits_achetes"
    )

    @api.depends('sale_order_ids.order_line.product_id')
    def _compute_produits_achetes(self):
        for partner in self:
            products = partner.sale_order_ids.order_line.mapped('product_id.name')
            partner.produits_achetes = ", ".join(set(products)) if products else False

    # Incidents & certifications
    certification_ids = fields.Many2many('partner.certification', string="Certifications")
    quality_incident_ids = fields.One2many(
        'partner.quality.incident', 'partner_id', string="Historique incidents qualité"
    )

    # Fournisseur
    purchase_responsible_id = fields.Many2one("res.users", string="Responsable Achat")
    other_buyers_ids = fields.Many2many("res.users", string="Autres Acheteurs")
    quality_ref_id = fields.Many2one("res.users", string="Référent Qualité")
    logistic_ref_id = fields.Many2one("res.users", string="Référent Logistique")
    billing_ref_id = fields.Many2one("res.users", string="Référent Facturation")

    supplier_fiability = fields.Many2many("partner.budget.fournisseur", string="Fiabilité")
    supplier_dependence = fields.Selection([
        ('strategic', 'Stratégique'),
        ('secondary', 'Secondaire'),
        ('alternative', 'Alternatif'),
    ], string="Niveau de dépendance")
    supplier_type = fields.Selection([
        ('subcontractor', 'Sous-traitant'),
        ('raw_material', 'Matière première'),
        ('key_partner', 'Partenaire clé'),
    ], string="Type de fournisseur")
    supplier_zone = fields.Char(string="Zone géographique")

    # Suivi commandes fournisseurs
    purchase_order_ids = fields.One2many("purchase.order", "partner_id", string="Commandes fournisseur")

    commandes_passees_count = fields.Integer(
        string="Nombre de commandes passées", compute="_compute_historique_suivi"
    )
    commandes_passees_montant = fields.Monetary(
        string="Montant commandes passées", currency_field="currency_id",
        compute="_compute_historique_suivi"
    )
    volume_achats_cumule = fields.Monetary(
        string="Volume d’achats cumulé", currency_field="currency_id",
        compute="_compute_historique_suivi"
    )
    produits_fournis_ids = fields.Many2many(
        "product.product", string="Produits / matières fournis", compute="_compute_historique_suivi"
    )

    @api.depends("purchase_order_ids", "purchase_order_ids.order_line")
    def _compute_historique_suivi(self):
        for partner in self:
            orders = partner.purchase_order_ids.filtered(lambda o: o.state in ["purchase", "done"])
            partner.commandes_passees_count = len(orders)
            partner.commandes_passees_montant = sum(orders.mapped("amount_total"))
            partner.volume_achats_cumule = partner.commandes_passees_montant
            partner.produits_fournis_ids = orders.mapped("order_line.product_id")


    class PartnerCertification(models.Model):
        _name = 'partner.certification'
        _description = 'Certification Partner'

        name = fields.Char(string='Nom', required=True)  # ISO, CE, autre
        description = fields.Text(string='Description')

    class PartnerQualityIncident(models.Model):
        _name = 'partner.quality.incident'
        _description = 'Quality Incident'

        partner_id = fields.Many2one('res.partner', string='Fournisseur', required=True)
        date_incident = fields.Date(string='Date de l’incident', required=True)
        description = fields.Text(string='Description')








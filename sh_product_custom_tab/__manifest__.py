# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    "name": "Website Product Custom Tab",
    "author": "Softhealer Technologies",
    "website": "https://www.softhealer.com",
    "support": "support@softhealer.com",
    "category": "Website",
    "summary": """New Tab In Product Module, Create Dynamic Tabs App, Add Multiple Tabs In Product, Make Product Dynamic Tab, Update Global Custom Tabs, Ecommerece Product Custom Tabs,Custom Product Tabs,woocommerce Custom Tabs,ecommerce Custom Tabs Website Product Custom Tab Custom Product Tabs for Website E-commerce Product Tab Customization Website Product Tabs Management Customizable Product Tabs Module Product Page Custom Tabs Tool Website Product Information Tabs Custom Tabs for Online Store Products Product Detail Tabs Odoo""",
    "description": """
    Do you want to create dynamic product tabs? Currently, in odoo, you can't create dynamic custom tabs in the product. This module is useful to create and add a dynamic tab in any product without any technical knowledge. You have 5+ attractive styles to present tabs. You can create many tabs in each product. You can modify the created product tabs. Admin can active/deactivate product tabs easily. cheers!
Website Product Custom Tab Odoo
 Add New Tab In Product Module, Create Dynamic Tabs, Add Multiple Tabs In Product, Make Product Dynamic Tab, Update Global Custom Tabs, Create Product Custom Tabs Odoo
New Tab In Product Module, Create Dynamic Tabs App, Add Multiple Tabs In Product, Make Product Dynamic Tab, Update Global Custom Tabs, Create Product Custom Tabs Odoo.
                    """,
    "version": "0.0.1",
    "depends": [
        'sh_font_awesome_icon_picker_widget',"website_sale_comparison"
    ],
    "application": True,
    "data": [
        "security/ir.model.access.csv",
        "data/sh_product_custom_tab_data.xml",
        "views/res_config_setting_views.xml",
        "views/sh_product_custom_tab_views.xml",
        "views/product_template_views.xml",
        "views/website_sale_templates.xml",
    ],
    'assets': {
        'web.assets_frontend': [
            'sh_product_custom_tab/static/src/scss/sh_product_custom_tab.scss',
            'sh_product_custom_tab/static/src/js/sh_product_custom_tab.js',
        ],
    },
    "images": ["static/description/background.png", ],
    "license": "OPL-1",
    "auto_install": False,
    "installable": True,
    "price": 0,
    "currency": "EUR"
}

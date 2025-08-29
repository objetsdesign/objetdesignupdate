# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies

{
    "name": "Font Awesome Icon Picker Widget",
    "author": "Softhealer Technologies",
    "website": "https://www.softhealer.com",
    "support": "support@softhealer.com",
    "version": "0.0.1",
    "category": "Extra Tools",
    "summary": "Font Awesome Widget Font Awesome Icon Widget Font Awesome Icons Widget FontAwesome Widget FontAwesome Icon Widget FontAwesome Icons Widget Fontawesome Resources Font Awesome Resources Add Font Awesome In Odoo Add Font Awesome Icons In Odoo Add Font Awesome Icon In Odoo Font Awesome 4.3.0 Fontawesome 4.3.0 Font Awesome 5.3 FontAwesome 5.3 Font Awesome v 4.3.0 Fontawesome v 4.3.0 Font Awesome v 5.3 FontAwesome v 5.3 Font Awesome 4.4.0 FontAwesome 4.4.0 Font Awesome v 4.4.0 FontAwesome v 4.4.0 Fonts Awesome Font Awesome File In Odoo Font Awesome Icon In Field Font Awesome Icons In Field Font Awesome Widget Icon In Character Field Custom Fontawesome Icons Custom Icon In Character Field Icon Picker Odoo Fontawesome Icon Picker Custom Widget Backend Widget Font Awesome Widget Icons In Character Fields Custom Icons In Character Fields",
    "description": """Using this module, you can add a font awesome icon picker widget to any character field in any Odoo model. With the icon picker, the character field becomes more visually interesting.""",
    "depends": ['web'],
    "installable": True,
    "auto_install": False,
    "assets": {
        'sh_font_awesome_icon_picker_widget.assets_icon': [
            #NOTE: See web_editor.IconSelector
            'sh_font_awesome_icon_picker_widget/static/src/components/icon_picker_popover/icon_picker_popover_data.js',
        ],
        'web.assets_backend':[
            'sh_font_awesome_icon_picker_widget/static/src/components/icon_picker_popover/icon_picker_popover.scss',
            'sh_font_awesome_icon_picker_widget/static/src/components/icon_picker_popover/icon_picker_popover.xml',
            'sh_font_awesome_icon_picker_widget/static/src/components/icon_picker_popover/icon_picker_popover.js',
            'sh_font_awesome_icon_picker_widget/static/src/components/icon_picker_char_field/icon_picker_char_field.xml',
            'sh_font_awesome_icon_picker_widget/static/src/components/icon_picker_char_field/icon_picker_char_field.js',
        ],
    },
    "price": 50,
    "currency": "EUR",
    "images": ["static/description/background.png", ],
    "license": "OPL-1"
}

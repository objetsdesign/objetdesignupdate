/* @odoo-module */

import publicWidget from '@web/legacy/js/public/public_widget';

publicWidget.registry.ShProductCustomTab = publicWidget.Widget.extend({
	selector: '.js_cls_sh_product_custom_tab_ul',

	start() {
		this.$el.find("li:first a").addClass('active');
		var Href = this.$el.find("li:first a").attr('href');
		$(document).find(Href).addClass('active show');
		
		
		this.$el.find("a:first").addClass('active');
		var Href = this.$el.find("a:first").attr('href');
		$(document).find(Href).addClass('active show');
		return this._super.apply(this, arguments);
	},
});

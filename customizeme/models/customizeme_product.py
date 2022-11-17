# -*- coding: utf-8 -*-

from odoo import fields, models


class CustomizeMeProduct(models.Model):
    _name = 'product.template'
    _inherit = 'product.template'

    customizeme_product_url = fields.Char(string='Product link')
    customizeme_product_custom_inject_to = fields.Char(
        string='Custom inject to', help='You can override here option "Inject to" from CustomizeMe settings for this product.')
    customizeme_attribute_line_ids = fields.One2many(
        'product.template.attribute.line', 'product_tmpl_id', 'Customizeme Product Attributes', copy=True)

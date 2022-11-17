# -*- coding: utf-8 -*-

from odoo import fields, models


class CustomizeMeAttribute(models.Model):
    _name = 'product.template.attribute.line'
    _inherit = 'product.template.attribute.line'

    customizeme_attribute_type = fields.Selection([
        ('suggestion', 'Set suggestion'),
        ('material', 'Set material to part'),
        ('optionalPart', 'Set optional part to part')],
        default='material',
        string='Reaction type',
        help='What should happen on attribute change'
    )
    customizeme_attribute_part_name = fields.Char(
        string='Part name', help='Responding 3D model part name (you can ignore it for type: suggestion)')

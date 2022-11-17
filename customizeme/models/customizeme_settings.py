# -*- coding: utf-8 -*-

from odoo import fields, models


class CustomizeMeSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    customizeme_access_key = fields.Char(string='Access key')
    customizeme_inject_to = fields.Char(
        string='Inject to', help='Pseudo selector of element to which CustomizeMe should be added. Let it empty to add CustomizeMe before product details.')

    def set_values(self):
        res = super(CustomizeMeSettings, self).set_values()
        self.env['ir.config_parameter'].set_param(
            'customizeme.customizeme_access_key', self.customizeme_access_key)
        self.env['ir.config_parameter'].set_param(
            'customizeme.customizeme_inject_to', self.customizeme_inject_to)
        return res

    def get_values(self):
        res = super(CustomizeMeSettings, self).get_values()
        res.update(customizeme_access_key=self.env['ir.config_parameter'].sudo(
        ).get_param('customizeme.customizeme_access_key'))
        res.update(customizeme_inject_to=self.env['ir.config_parameter'].sudo(
        ).get_param('customizeme.customizeme_inject_to'))
        return res

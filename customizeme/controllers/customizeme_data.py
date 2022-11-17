# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request, Controller
import json


class CustomizemeDataController(Controller):
    @http.route('/customizeme/data', type='http', auth="public", website=True, csrf=False)
    def get_settings(self, product_id):

        product = request.env['product.template'].browse(int(product_id))
        product_attributes = product['customizeme_attribute_line_ids']
        attributes = []

        for attribute in product_attributes:
            attributes.append({
                'id': attribute['id'],
                'type': attribute['customizeme_attribute_type'],
                'partName': attribute['customizeme_attribute_part_name']
            })

        settings = request.env['ir.config_parameter']
        access_key = settings.get_param('customizeme.customizeme_access_key')
        inject_to = settings.get_param('customizeme.customizeme_inject_to')
        data = {
            'accessKey': access_key,
            'injectTo': inject_to,
            'attributes': attributes,
            'productUrl': product['customizeme_product_url'],
            'customInjectTo': product['customizeme_product_custom_inject_to']
        }

        return request.make_response(json.dumps(data), [('Content-Type', 'application/json')])

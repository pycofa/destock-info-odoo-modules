# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import api, fields, models, _
import requests
import base64

from odoo.exceptions import UserError


class IcecatForm(models.TransientModel):
    _name = 'icecat.form'
    _description = 'Icecat Form'

    ean_upc = fields.Char(
        'EAN/UPC',
        required=True,
    )
    
    image_url = fields.Char()

    @api.model
    def _default_lang_ids(self):
        active_langs = self.env['res.lang'].search([('active', '=', True)])

        return active_langs

    language_ids = fields.Many2many(
        'res.lang',
        'icecat_form_res_lang_rel',
        string='Language',
        required=True,
        default=lambda self: self._default_lang_ids()
    )

    detailed_type = fields.Selection(
        [
            ('consu', 'Consumable'),
            ('service', 'Service'),
            ('product', 'Product'),
        ],
        default='product',
        string='Type',
        required=True
    )

    categ_id = fields.Many2one(
        'product.category',
        'Category',
    )

    def upsert_product(self, ean_upc, language_ids, detailed_type, categ_id):
        existing_product = self.env['product.template'].search(
            [('ean_upc', '=', ean_upc)],
            limit=1,
        )

        if len(existing_product) > 0:
            self.env['bus.bus']._sendone(self.env.user.partner_id, 'simple_notification', {
                'type': 'warning',
                'title': _("Warning"),
                'message': _('Product is already registered in your database.')
            })

            return existing_product[0]
        else:

            try:
                return self.create_product_with_icecat(language_ids, ean_upc, detailed_type, categ_id)

            except requests.exceptions.HTTPError as http_err:
                # See 404, 500, etc. errors
                # print(f"HTTP error occurred: {http_err}")

                error_info = http_err.response.json()

                if error_info['Message']:
                    return self.env['bus.bus']._sendone(self.env.user.partner_id, 'simple_notification', {
                        'type': 'danger',
                        'title': _("Error"),
                        'message': _(error_info['Message'])
                    })

                pass
            except requests.exceptions.RequestException as req_err:
                print(f"Request error occurred: {req_err}")

    def create_product_with_icecat(self, language_ids, ean_upc, detailed_type, categ_id):
        response = False

        for lang in language_ids:
            url = "https://live.icecat.biz/api?shopname=openIcecat-live&lang=%s&content=&ean_upc=%s" % (lang.iso_code, ean_upc)
            response = requests.get(url)

            if response.status_code == 200:
                break

        if not response:
            raise UserError(_("The product with the EAN code {ean_upc} was not found").format(ean_upc=ean_upc))

        response.raise_for_status()
        product_info = response.json()

        product_sheet = product_info['data']['GeneralInfo']
        product_image = product_info['data']['Image']
        product_features = product_info['data']['FeaturesGroups']

        product = self.env['product.template'].create({
            'name': product_sheet['TitleInfo']['GeneratedIntTitle'],
            'ean_upc': ean_upc,
            'detailed_type': detailed_type,
        })

        if product_sheet['BrandPartCode']:
            product.part_number_code = product_sheet['BrandPartCode']

        if categ_id:
            product.categ_id = categ_id

        if product_sheet['BrandInfo']:
            existing_manufacturer = self.env['product.manufacturer'].search(
                [('name', '=', product_sheet['BrandInfo']['BrandName'])],
                limit=1,
            )

            if len(existing_manufacturer) > 0:
                if not product.product_manufacturer_id.image_1920:
                    product.product_manufacturer_id.image_1920 = base64.b64encode(
                        requests.get(product_sheet['BrandInfo']['BrandLogo']).content)

                product.product_manufacturer_id = existing_manufacturer[0].id
            else:
                manufacturer = self.env['product.manufacturer'].create({
                    'name': product_sheet['BrandInfo']['BrandName'],
                    'image_1920': base64.b64encode(requests.get(product_sheet['BrandInfo']['BrandLogo']).content)
                })

                product.product_manufacturer_id = manufacturer

        self.image_url = False
        if product_image['HighPic']:
            self.image_url = product_image['HighPic']
            product.image_1920 = base64.b64encode(requests.get(product_image['HighPic']).content)

        # Datas that need to be filled by lang
        for lang in language_ids:
            url = "https://live.icecat.biz/api?shopname=openIcecat-live&lang=%s&content=&ean_upc=%s" % (lang.iso_code, ean_upc)
            response_lang = requests.get(url)

            if response_lang.status_code != 404:
                product_lang_info = response_lang.json()
                product_lang_sheet = product_lang_info['data']['GeneralInfo']

                if product_lang_sheet['SummaryDescription']['LongSummaryDescription']:
                    product.with_context(lang=lang.code).description_sale = product_lang_sheet['SummaryDescription']['LongSummaryDescription']

        # Weight field dedicated only for Smartphones
        for feature_group in product_features:
            if feature_group['ID'] == 6881:
                for feature in feature_group['Features']:
                    if feature['Feature']['ID'] == "94":
                        product.weight = float(feature['RawValue']) / 1000

        return product

    def action_icecat_api_call(self):
        self.ensure_one()

        product_id = self.upsert_product(self.ean_upc, self.language_ids, self.detailed_type, self.categ_id)

        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'res_model': 'product.template',
            'view_mode': 'form',
            'res_id': product_id.id,
			'image_url': self.image_url,
			'target': 'current',
        }

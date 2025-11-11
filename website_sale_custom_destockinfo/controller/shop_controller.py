# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).
from odoo.addons.website_sale.controllers.variant import WebsiteSaleVariantController
from odoo import http
from odoo.addons.website_sale.controllers.main import WebsiteSale, TableCompute
from odoo.http import request
from datetime import datetime


class WebsiteSaleCustom(WebsiteSale):
    
    @http.route([
        '/shop',
        '/shop/page/<int:page>',
        '/shop/category/<model("product.public.category"):category>',
        '/shop/category/<model("product.public.category"):category>/page/<int:page>',
    ], type='http', auth="public", website=True)
    def shop(self, page=0, category=None, search='', min_price=0.0, max_price=0.0, ppg=False, **post):
        if not request.env.user.id != request.env.ref('base.public_user').id:
            return request.redirect(f'/web/login?redirect={request.httprequest.path}')
        
        min_price_tmp = False
        max_price_tmp = False
        if min_price:
            min_price_tmp = min_price
            min_price = False
        if max_price:
            max_price_tmp = max_price
            max_price = False
            
        if search != "":
            if request.session.get('old_search'):
                if request.session.get('old_search') == search:
                    request.session.update({
                        'old_search': '',
                        'has_search': False,
                    })
                else:
                    request.session.update({
                        'old_search': search,
                        'has_search': True,
                    })
            else:
                request.session.update({
                    'old_search': search,
                    'has_search': True,
                })

        if not request.session.get('has_search'):
            search = False

        res = super().shop(page=page, category=category, search=search, min_price=min_price, max_price=max_price,
                           ppg=ppg, **post)

        user = request.env.user.partner_id
        # if not user.company_name or not user.street or not user.city or not user.country_id or not user.phone or not user.zip:
        #     return request.redirect(f'/my/account?infos_missing=1')

        categories = request.env['product.category'].search([('parent_id.name', '=', 'All')]).mapped('name')
        public_categories = request.env['product.public.category'].search(
            [('name', 'in', categories), ('parent_id', '=', False), ('categ_filter_visible_in_shop', '=', True)])
        res.qcontext.update({
            'categories': public_categories,
        })

        if not category:
            res.qcontext.update({
                'home': True,
            })
            return res

        if isinstance(category, str):
            category = request.env['product.public.category'].search([('id', '=', category)])

        domain = []
        request_args = request.httprequest.args
        
        filters = False
        # ========== Manufacturers filtered ==========
        m_ids = request_args.getlist('ma')
        if m_ids:
            filters = True
            m_ids = [int(m_id.split('_')[1]) for m_id in m_ids]
            domain.append(('product_manufacturer_id.id', 'in', m_ids))
        # ========== Screen size filtered ==========
        ss_ints = request_args.getlist('ss')
        if ss_ints:
            filters = True
            ss_ints = [int(ss_id.split('_')[1]) for ss_id in ss_ints]
            domain.append(('screen_size_id.id', 'in', ss_ints))
        # ========== Screen quality filtered ==========
        sq_ints = request_args.getlist('sq')
        if sq_ints:
            filters = True
            sq_ints = [int(sq_int.split('_')[1]) for sq_int in sq_ints]
            domain.append(('screen_quality_id.id', 'in', sq_ints))
        # ========== OS filtered ==========
        os_ids = request_args.getlist('os')
        if os_ids:
            filters = True
            os_ids = [int(os_id.split('_')[1]) for os_id in os_ids]
            domain.append(('operating_system_id.id', 'in', os_ids))
        # ========== Network filtered ==========
        network_ids = request_args.getlist('nw')
        if network_ids:
            filters = True
            network_ids = [int(network_id.split('_')[1]) for network_id in network_ids]
            domain.append(('network_ids.id', 'in', network_ids))
        # ========== Video input filtered ==========
        video_input_ids = request_args.getlist('vi')
        if video_input_ids:
            filters = True
            video_input_ids = [int(video_input_id.split('_')[1]) for video_input_id in video_input_ids]
            domain.append(('video_input_ids.id', 'in', video_input_ids))
        # ========== Video input filtered ==========
        video_output_ids = request_args.getlist('vo')
        if video_output_ids:
            filters = True
            video_output_ids = [int(video_output_id.split('_')[1]) for video_output_id in video_output_ids]
            domain.append(('video_output_ids.id', 'in', video_output_ids))
        # ========== Number of ports filtered ==========
        number_of_ports_ids = request_args.getlist('np')
        if number_of_ports_ids:
            filters = True
            number_of_ports_ids = [int(number_of_ports_id.split('_')[1]) for number_of_ports_id in number_of_ports_ids]
            domain.append(('number_of_ports', 'in', number_of_ports_ids))
        # ========== Number of displays filtered ==========
        number_of_displays_ids = request_args.getlist('nd')
        if number_of_displays_ids:
            filters = True
            number_of_displays_ids = [int(number_of_display.split('_')[1]) for number_of_display in number_of_displays_ids]
            domain.append(('number_of_displays', 'in', number_of_displays_ids))
        # # ========== HD type filtered ==========
        hdt_ids = request_args.getlist('hdt')
        if hdt_ids:
            filters = True
            hdt_ids = [int(hdt_id.split('_')[1]) for hdt_id in hdt_ids]
            domain.append(('hard_drive_type_id.id', 'in', hdt_ids))
        # ========== HD capacity filtered ==========
        hdc_ints = request_args.getlist('hdc')
        if hdc_ints:
            filters = True
            hdc_ints = [int(hdc_int.split('_')[1]) for hdc_int in hdc_ints]
            domain.append(('hard_drive_capacity_id.id', 'in', hdc_ints))
        # ========== RAM capacity filtered ==========
        ram_ints = request_args.getlist('ram')
        if ram_ints:
            filters = True
            ram_ints = [int(ram_int.split('_')[1]) for ram_int in ram_ints]
            domain.append(('ram_capacity_id.id', 'in', ram_ints))
        # ========== Processor capacity filtered ==========
        pr_ids = request_args.getlist('pr')
        if pr_ids:
            filters = True
            pr_ids = [int(pr_id.split('_')[1]) for pr_id in pr_ids]
            domain.append(('processor_id.generation_id.model_id.id', 'in', pr_ids))
        # ========== Graphic processor filtered ==========
        gpr_ids = request_args.getlist('gpr')
        if gpr_ids:
            filters = True
            gpr_ids = [int(gpr_id.split('_')[1]) for gpr_id in gpr_ids]
            domain.append(('graphic_card_id.id', 'in', gpr_ids))
        # ========== Bluetooth filtered ==========
        bluetooth_selected = False
        has_bluetooth = request_args.getlist('blt')
        if has_bluetooth:
            filters = True
            bluetooth_selected = True
            domain.append(('has_bluetooth', '=', True))
        # ========== Optical drive filtered ==========
        optical_drive_selected = False
        has_optical_drive = request_args.getlist('od')
        if has_optical_drive:
            filters = True
            optical_drive_selected = True
            domain.append(('has_optical_drive', '=', True))
        # ========== Adjustable stand filtered ==========
        adjustable_stand_selected = False
        has_adjustable_stand = request_args.getlist('as')
        if has_adjustable_stand:
            filters = True
            adjustable_stand_selected = True
            domain.append(('has_adjustable_stand', '=', True))
        # ========== Adjustable stand filtered ==========
        is_poe_selected = False
        is_poe = request_args.getlist('poe')
        if is_poe:
            filters = True
            is_poe_selected = True
            domain.append(('is_poe', '=', True))
        # ========== Adjustable stand filtered ==========
        is_dual_sim_selected = False
        is_dual_sim = request_args.getlist('dual')
        if is_dual_sim:
            filters = True
            is_dual_sim_selected = True
            domain.append(('is_dual_sim', '=', True))
        # ========== Adjustable stand filtered ==========
        is_usb_c_selected = False
        is_usb_c = request_args.getlist('usbc')
        if is_usb_c:
            filters = True
            is_usb_c_selected = True
            domain.append(('is_usb_c', '=', True))
        # ========== Adjustable stand filtered ==========
        is_videopro_interactive_selected = False
        is_videopro_interactive = request_args.getlist('inter')
        if is_videopro_interactive:
            filters = True
            is_videopro_interactive_selected = True
            domain.append(('is_videopro_interactive', '=', True))
        # ========== Adjustable stand filtered ==========
        is_printer_multifunction_selected = False
        is_printer_multifunction = request_args.getlist('multi')
        if is_printer_multifunction:
            filters = True
            is_printer_multifunction_selected = True
            domain.append(('is_printer_multifunction', '=', True))
        # ========== Adjustable stand filtered ==========
        is_printer_color_selected = False
        is_printer_color = request_args.getlist('color')
        if is_printer_color:
            filters = True
            is_printer_color_selected = True
            domain.append(('is_printer_color', '=', True))
        # ========== Adjustable stand filtered ==========
        is_tactile_selected = False
        is_tactile = request_args.getlist('tact')
        if is_tactile:
            filters = True
            is_tactile_selected = True
            domain.append(('is_tactile', '=', True))

        # products = res.qcontext.get('products', False)

        all_categ = request.env['product.public.category'].search([('id', 'child_of', category.id)])
        if not category.shared_category_in_shop:
            all_categ = all_categ.filtered(lambda p: not p.shared_category_in_shop)

        all_categ = all_categ.ids
        available_products = request.env['product.product'].search([
            ('public_categ_ids', 'in', all_categ),
            ('qty_available', '>', 0),
            ('is_published', '=', True)
        ])

        products = request.env['product.template'].search([
            ('qty_available', '>', 0),
            ('is_published', '=', True),
        ])

        products = products.filtered(lambda p: any(cat.id in all_categ for cat in p.public_categ_ids))

        domain.append(('id', 'in', products.ids))

        # attributes (conditions)
        product_variant_ids = False
        conditions_selected = False
        attrib_values = res.qcontext['attrib_values']
        len_attrib = len(attrib_values)
        if attrib_values:
            conditions_selected = True
            lt = []
            for attrib in attrib_values:
                lt.append(attrib[1])
            filters = True
            product_variant_ids = request.env['product.product'].search([
                ('qty_available', '>', 0),
                ('product_template_attribute_value_ids.product_attribute_value_id.id', 'in', lt)
            ])
            product_templates = request.env['product.template'].search([
                ('product_variant_ids', 'in', product_variant_ids.ids)
            ])
            
            domain.append(('id', 'in', product_templates.ids))
        
        order = res.qcontext['order']
        if not order:
            order = 'list_price asc'

        products = request.env['product.template'].search(domain, order=order)
        products = products.filtered(lambda m: m.qty_available > 0)
        
        # Product price
        products_prices = {}
        if not product_variant_ids:
            product_variant_ids = available_products

        x = product_variant_ids & available_products
        available_products = request.env['product.product'].search([('id', 'in', list(set(x.ids)))])

        if available_products:
            available_max_price = max(available_products, key=lambda p: p.sale_price).sale_price
        else:
            available_max_price = 0

        if min_price_tmp or max_price_tmp:
            filters = True

        product_tmpl_to_rmv_ids = []
        price_dict = {}
        for product in products:
            lowest_price = None
            if product.pricelist_item_count > 0:
                price_list_items = request.env['product.pricelist.item'].search([('product_tmpl_id', '=', product.id)])
                price_dict = {
                    item.product_id.id: item.fixed_price
                    for item in price_list_items
                    if item.date_start is not False and item.date_start <= datetime.today()
                       and item.date_end is not False and item.date_end > datetime.today()
                }
            nb = 0
            for attr in product.product_variant_ids:
                if attr.qty_available > 0 and attr in product_variant_ids:

                    if price_dict and attr.id in price_dict.keys():
                        sale_price = price_dict[attr.id]
                    else:
                        sale_price = attr.sale_price

                    if min_price_tmp and float(min_price_tmp) > sale_price or max_price_tmp and float(max_price_tmp) < sale_price:
                        nb += 1

                    if lowest_price is None or sale_price < lowest_price:
                        lowest_price = sale_price

            if lowest_price is not None:
                products_prices[product.id] = {'price_reduce': lowest_price}

            var = product.product_variant_ids.filtered(lambda p: p.qty_available > 0)
            if len(var) == nb:
                product_tmpl_to_rmv_ids.append(product.id)

        products = products.filtered(lambda p: p.id not in product_tmpl_to_rmv_ids)
        
        available_min_price = res.qcontext.get('available_min_price')

        for key, value in products_prices.items():
            if value['price_reduce'] < available_min_price:
                available_min_price = value['price_reduce']
            if value['price_reduce'] > available_max_price:
                available_max_price = value['price_reduce']

        min_price = min_price_tmp or available_min_price
        max_price = max_price_tmp or available_max_price


        ram_filter_visible = True if products.mapped('ram_capacity_id') else False
        screen_size_filter_visible = True if products.mapped('screen_size_id') else False
        screen_quality_filter_visible = True if products.mapped('screen_quality_id') else False
        operating_system_filter_visible = True if products.mapped('operating_system_id') else False
        networks_filter_visible = True if products.mapped('network_ids') else False
        video_input_filter_visible = True if products.mapped('video_input_ids') else False
        video_output_filter_visible = True if products.mapped('video_output_ids') else False
        number_of_ports_filter_visible = True if products.mapped('number_of_ports') else False
        number_of_displays_filter_visible = True if products.mapped('number_of_displays') else False
        hard_drive_type_filter_visible = True if products.mapped('hard_drive_type_id') else False
        hard_drive_capacity_filter_visible = True if products.mapped('hard_drive_capacity_id') else False
        processor_filter_visible = True if products.mapped('processor_id') else False
        graphic_card_filter_visible = True if products.mapped('graphic_card_id') else False
        
        # Manufacturers available
        available_manu_ids = available_products.mapped('product_manufacturer_id.id')
        manufacturers = request.env['product.manufacturer'].search([('id', 'in', available_manu_ids)])
        # Screen size available
        available_ss_ids = available_products.mapped('screen_size_id.id')
        sss = request.env['product.screen.size'].search([('id', 'in', available_ss_ids)])
        # Screen quality available
        available_sq_ids = available_products.mapped('screen_quality_id.id')
        sqs = request.env['product.screen.quality'].search([('id', 'in', available_sq_ids)])
        # OS available
        available_os_ids = available_products.mapped('operating_system_id.id')
        oss = request.env['product.operating.system'].search([('id', 'in', available_os_ids)])
        # Network available
        available_network_ids = available_products.mapped('network_ids.id')
        nws = request.env['product.network'].search([('id', 'in', available_network_ids)])
        # Video input available
        available_video_input_ids = available_products.mapped('video_input_ids.id')
        vis = request.env['product.video.input'].search([('id', 'in', available_video_input_ids)])
        # Video output available
        available_video_output_ids = available_products.mapped('video_output_ids.id')
        vos = request.env['product.video.output'].search([('id', 'in', available_video_output_ids)])
        # Hard drive type available
        available_hdt_ids = available_products.mapped('hard_drive_type_id.id')
        hdts = request.env['product.storage.type'].search([('id', 'in', available_hdt_ids)])
        # Hard drive capacity available
        available_hdc_ids = available_products.mapped('hard_drive_capacity_id.id')
        hdcs = request.env['product.storage.capacity'].search([('id', 'in', available_hdc_ids)])
        # RAM available
        available_ram_ids = available_products.mapped('ram_capacity_id.id')
        rams = request.env['product.storage.capacity'].search([('id', 'in', available_ram_ids)])
        # Processor available
        available_pr_ids = available_products.mapped('processor_id.generation_id.model_id.id')
        prs = request.env['product.processor.model'].search([('id', 'in', available_pr_ids)])
        # Graphic processor available
        available_gpr_ids = available_products.mapped('graphic_card_id.id')
        gprs = request.env['product.graphic.card'].search([('id', 'in', available_gpr_ids)])
        # Features available
        available_bluetooth = available_products.filtered(lambda p: p.has_bluetooth)
        available_optical_drive = available_products.filtered(lambda p: p.has_optical_drive)
        available_adjustable_stand = available_products.filtered(lambda p: p.has_adjustable_stand)
        available_is_poe = available_products.filtered(lambda p: p.is_poe)
        available_is_dual_sim = available_products.filtered(lambda p: p.is_dual_sim)
        available_is_usb_c = available_products.filtered(lambda p: p.is_usb_c)
        available_is_videopro_interactive = available_products.filtered(lambda p: p.is_videopro_interactive)
        available_is_printer_multifunction = available_products.filtered(lambda p: p.is_printer_multifunction)
        available_is_printer_color = available_products.filtered(lambda p: p.is_printer_color)
        available_is_tactile = available_products.filtered(lambda p: p.is_tactile)
        
        # Number of ports available
        available_number_of_ports = available_products.filtered(lambda p: p.number_of_ports)
        nps = set(request.env['product.product'].search([('number_of_ports', 'in', available_number_of_ports.mapped('number_of_ports'))]).mapped('number_of_ports'))
        nps = list(nps)
        # Number of displays available
        available_number_of_displays = available_products.filtered(lambda p: p.number_of_displays)
        nds = set(request.env['product.product'].search([('number_of_displays', 'in', available_number_of_displays.mapped('number_of_displays'))]).mapped('number_of_displays'))
        nds = list(nds)
        
        
        table_compute = TableCompute()
        bins = table_compute.process(products, ppg=res.qcontext.get('ppg', 20), ppr=res.qcontext.get('ppr', 3))
        search_count = len(products)
        available_attributes = [attr.name for attr_line in available_products.attribute_line_ids for attr in attr_line.value_ids]
        
        res.qcontext.update({
            'min_price': float(min_price),
            'max_price': float(max_price),
            'available_max_price': available_max_price,
            'available_min_price': available_min_price,
            'home': False,
            'products': products,
            'search_count': search_count,
            'products_prices': products_prices,
            'bins': bins,
            'conditions_selected': conditions_selected,
            'manufacturers': manufacturers,
            'manufacturers_selected': m_ids,
            'sss': sss,
            'sss_selected': ss_ints,
            'screen_size_filter_visible': screen_size_filter_visible,
            'sqs': sqs,
            'sqs_selected': sq_ints,
            'screen_quality_filter_visible': screen_quality_filter_visible,
            'oss': oss,
            'oss_selected': os_ids,
            'operating_system_filter_visible': operating_system_filter_visible,
            'nws': nws,
            'nws_selected': network_ids,
            'networks_filter_visible': networks_filter_visible,
            'vis': vis,
            'vis_selected': video_input_ids,
            'video_input_filter_visible': video_input_filter_visible,
            'vos': vos,
            'vos_selected': video_output_ids,
            'video_output_filter_visible': video_output_filter_visible,
            'hdcs': hdcs,
            'hdcs_selected': hdc_ints,
            'hard_drive_capacity_filter_visible': hard_drive_capacity_filter_visible,
            'hdts': hdts,
            'hdts_selected': hdt_ids,
            'hard_drive_type_filter_visible': hard_drive_type_filter_visible,
            'rams': rams,
            'rams_selected': ram_ints,
            'ram_filter_visible': ram_filter_visible,
            'prs': prs,
            'prs_selected': pr_ids,
            'processor_filter_visible': processor_filter_visible,
            'gprs': gprs,
            'gprs_selected': gpr_ids,
            'graphic_card_filter_visible': graphic_card_filter_visible,
            'available_bluetooth': available_bluetooth,
            'bluetooth_selected': bluetooth_selected,
            'available_optical_drive': available_optical_drive,
            'optical_drive_selected': optical_drive_selected,
            'available_adjustable_stand': available_adjustable_stand,
            'adjustable_stand_selected': adjustable_stand_selected,
            'available_is_poe': available_is_poe,
            'is_poe_selected': is_poe_selected,
            'available_is_dual_sim': available_is_dual_sim,
            'is_dual_sim_selected': is_dual_sim_selected,
            'available_is_videopro_interactive': available_is_videopro_interactive,
            'is_videopro_interactive_selected': is_videopro_interactive_selected,
            'available_is_printer_multifunction': available_is_printer_multifunction,
            'is_printer_multifunction_selected': is_printer_multifunction_selected,
            'available_is_printer_color': available_is_printer_color,
            'is_printer_color_selected': is_printer_color_selected,
            'available_is_tactile': available_is_tactile,
            'is_tactile_selected': is_tactile_selected,
            'available_is_usb_c': available_is_usb_c,
            'is_usb_c_selected': is_usb_c_selected,
            'available_number_of_ports': available_number_of_ports,
            'nps': nps,
            'nps_selected': number_of_ports_ids,
            'number_of_ports_filter_visible': number_of_ports_filter_visible,
            'available_number_of_displays': available_number_of_displays,
            'nds': nds,
            'nds_selected': number_of_displays_ids,
            'number_of_displays_filter_visible': number_of_displays_filter_visible,
            'get_product_prices': lambda product: products_prices.get(product.id, {'price_reduce': 0}),
            'filters': filters,
            'len_attrib': len_attrib,
            'available_attributes': available_attributes,
        })
        
        return res


    @http.route(['/shop/<model("product.template"):product>'], type='http', auth="public", website=True, sitemap=True)
    def product(self, product, category='', search='', **kwargs):
        if not request.env.user.id != request.env.ref('base.public_user').id:
            return request.redirect(f'/web/login?redirect={request.httprequest.path}')

        if product:
            product.sudo().write({
                'list_price': product.product_variant_id.sale_price
            })
            return request.render("website_sale.product", self._prepare_product_values(product, category, search, **kwargs))
        else:
            return request.redirect('/shop')


class WebsiteSaleVariantControllerCustom(WebsiteSaleVariantController):

    @http.route('/website_sale/get_combination_info', type='json', auth='public', methods=['POST'], website=True)
    def get_combination_info_website(
        self, product_template_id, product_id, combination, add_qty, parent_combination=None,
        **kwargs
    ):
        res = super().get_combination_info_website(product_template_id, product_id, combination, add_qty, parent_combination=None,**kwargs)

        attr_value = request.env['product.template.attribute.value'].browse(combination)
        product = attr_value.ptav_product_variant_ids[0]
        sale_price = product.sale_price
        res.update({
            'list_price': sale_price,
            'price': sale_price,
        })

        return res

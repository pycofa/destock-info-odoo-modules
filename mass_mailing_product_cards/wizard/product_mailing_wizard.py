from odoo import _, models, fields
from markupsafe import Markup
from odoo.exceptions import UserError
from lxml import html


class ProductMailingWizard(models.TransientModel):
    _name = 'product.mailing.wizard'
    _description = 'Allow to add product card into mail template'
    
    product_tmpl_id = fields.Many2one('product.template', required=True, string="Product")
    column_size = fields.Selection([
        ('small', 'Small'),
        ('large', 'Large'),
    ], default='small')
    mailing_id = fields.Many2one('mailing.mailing')

    def action_add_product(self):
        product_tmpl_id = self.env['product.template'].browse([self.product_tmpl_id.id])
        mailing_id = self.env.context.get('active_id')
        
        mailing_record = self.env['mailing.mailing'].browse(mailing_id)
        mailing_content_arch = mailing_record.body_arch
        if not mailing_content_arch:
            raise UserError(_('Please, add a template first.'))
        mailing_root = html.fromstring(mailing_content_arch)
        if not product_tmpl_id:
            raise UserError(_('This product must have been deleted.'))
        
        product_name = product_tmpl_id.name
        product_conditions = product_tmpl_id.product_variant_ids

        product_conditions_block = []

        product_conditions_dict = {}

        if product_conditions:
            for p in product_conditions:
                if p.qty_available > 0:
                    product_conditions_dict[p.product_condition_id.name] = p.sale_price
                    product_conditions_block.append(Markup('''
                        <div class="pe-0 text-center"  style="display: flex;">
                            <span style="background-color: {color}; min-width: 50px;"
                                    class="px-2 mb-1 mx-1 rounded-1 d-flex badge-colored"
                                    >{key}</span>
                            <dd class="m-0">{value} € HT</dd>
                        </div>
                    ''').format(key=p.product_condition_id.name, value=p.sale_price, color=p.product_condition_id.color))

        ram_capacity = product_tmpl_id.ram_capacity_id.name or None
        ram_block = ""
        if ram_capacity:
            if self.column_size == 'small':
                ram_block = Markup('''
                    <div class="feature_block ram_block pe-0 text-center">
                        <dt class="dt_card">RAM</dt>
                        <dd class="dd_card" style="border-radius: 0 0 10px 0;">{ram_capacity}</dd>
                    </div>
                ''').format(ram_capacity=ram_capacity)
            elif self.column_size == 'large':
                ram_block = Markup('''
                   <div class="feature_block ram_block pe-0 text-center">
                    <dt class="dt_card" style="width: 70px;">RAM</dt>
                    <dd class="dd_card" style="width: 70px; border-radius: 0 0 10px 0;">{ram_capacity}</dd>
                </div>''').format(ram_capacity=ram_capacity)

        hard_drive_capacity = product_tmpl_id.hard_drive_capacity_id.name or None
        hard_drive_block = ""
        if hard_drive_capacity:
            if self.column_size == 'small':
                hard_drive_block = Markup('''
                    <div class="feature_block hard_drive_type_block pe-0 text-center">
                        <dt class="dt_card">SSD</dt>
                        <dd class="dd_card"  style="border-radius: 0 0 10px 0;">{hard_drive_capacity}</dd>
                    </div>
                ''').format(hard_drive_capacity=hard_drive_capacity)
            elif self.column_size == 'large':
                hard_drive_block = Markup('''
                    <div class="feature_block hard_drive_type_block pe-0 text-center">
                        <dt class="dt_card" style="width: 70px;">SSD</dt>
                        <dd class="dd_card" style="width: 70px; border-radius: 0 0 10px 0;">{hard_drive_capacity}</dd>
                    </div>
                ''').format(hard_drive_capacity=hard_drive_capacity)

        cpu_block = ""
        processor_name = product_tmpl_id.processor_id.name or None
        if processor_name:
            if self.column_size == 'small':
                cpu_block = Markup('''
                    <div class="feature_block cpu_block pe-0 text-center">
                        <dt class="dt_card">CPU</dt>
                        <dd class="dd_card" style="border-radius: 0 0 10px 0;">{processor_name}</dd>
                    </div>
                ''').format(processor_name=processor_name)
            elif self.column_size == 'large':
                cpu_block = Markup('''
                    <div class="feature_block cpu_block pe-0 text-center">
                        <dt class="dt_card" style="width: 70px;">CPU</dt>
                        <dd class="dd_card" style="width: 70px; border-radius: 0 0 10px 0;">{processor_name}</dd>
                    </div>
                ''').format(processor_name=processor_name)

        os = product_tmpl_id.operating_system_id.name or None
        os_block = ""
        if os:
            if self.column_size == 'small':
                os_block = Markup('''
                    <div class="feature_block os_block pe-0 text-center">
                        <dt class="dt_card">OS</dt>
                        <dd class="dd_card" style="border-radius: 0 0 10px 0;">{os}</dd>
                    </div>
                ''').format(os=os)
            elif self.column_size == 'large':
                os_block = Markup('''
                    <div class="feature_block os_block pe-0 text-center">
                        <dt class="dt_card" style="min-width: 70px;">OS</dt>
                        <dd class="dd_card" style="min-width: 70px; border-radius: 0 0 10px 0;">{os}</dd>
                    </div>
                ''').format(os=os)

        screen_size = product_tmpl_id.screen_size_id.name or None
        pattern = product_tmpl_id.product_pattern in ['screen', 'laptop_computer', 'all_in_one']
        screen_size_block = ""
        if screen_size:
            if pattern:
                if self.column_size == 'small':
                    screen_size_block = Markup('''
                        <div class="feature_block screen_block pe-0 text-center">
                            <dt class="dt_card">Size</dt>
                            <dd class="dd_card" style="border-radius: 0 0 10px 0;">{screen_size}</dd>
                        </div>
                    ''').format(screen_size=screen_size)
                elif self.column_size == 'large':
                    screen_size_block = Markup('''
                        <div class="feature_block screen_block pe-0 text-center">
                            <dt class="dt_card" style="width: 70px;">Size</dt>
                            <dd class="dd_card" style="width: 70px; border-radius: 0 0 10px 0;">{screen_size}</dd>
                        </div>
                    ''').format(screen_size=screen_size)
        
        screen_quality = product_tmpl_id.screen_quality_id.name or None
        pattern = product_tmpl_id.product_pattern == 'screen'
        screen_quality_block = ""
        if screen_quality:
            if pattern:
                if self.column_size == 'small':
                    screen_quality_block = Markup('''
                        <div class="feature_block qual_block pe-0 text-center">
                            <dt class="dt_card">Quality</dt>
                            <dd class="dd_card" style="border-radius: 0 0 10px 0;">{screen_quality}</dd>
                        </div>
                    ''').format(screen_quality=screen_quality)
                elif self.column_size == 'large':
                    screen_quality_block = Markup('''
                        <div class="feature_block qual_block pe-0 text-center">
                            <dt class="dt_card" style="width: 70px;">Quality</dt>
                            <dd class="dd_card" style="width: 70px; border-radius: 0 0 10px 0;">{screen_quality}</dd>
                        </div>
                    ''').format(screen_quality=screen_quality)
                    
        video_inputs = product_tmpl_id.video_input_ids or None
        pattern = product_tmpl_id.product_pattern == 'screen'
        video_inputs_block = []
        if video_inputs:
            if pattern:
                if self.column_size == 'small':
                    for video_input in video_inputs:
                        video_inputs_block.append(Markup('''
                            <div class="feature_block os_block pe-0 text-center">
                                <dt class="dt_card">Input</dt>
                                <dd class="dd_card" style="border-radius: 0 0 10px 0;">{}</dd>
                            </div>
                        ''').format(video_input.name))
                elif self.column_size == 'large':
                    for video_input in video_inputs:
                        video_inputs_block.append(Markup('''
                            <div class="feature_block os_block pe-0 text-center">
                                <dt class="dt_card" style="width: 70px;">Input</dt>
                                <dd class="dd_card" style="width: 70px; border-radius: 0 0 10px 0;">{}</dd>
                            </div>
                        ''').format(video_input.name))

        image_1920_uri = ""
        if product_tmpl_id.image_1920:
            image_1920 = product_tmpl_id.image_1920.decode('utf-8')
            image_1920_uri = f"data:image/png;base64,{image_1920}"
        
        link = product_tmpl_id.website_url
        link = self.env['ir.config_parameter'].get_param('web.base.url') + link

        processor_logo_uri = ""
        if product_tmpl_id.processor_id and product_tmpl_id.processor_id.generation_id and product_tmpl_id.processor_id.generation_id.logo:
            processor_logo = product_tmpl_id.processor_id.generation_id.logo.decode('utf-8') or None
            processor_logo_uri = f"data:image/png;base64,{processor_logo}"

        if self.column_size == 'small':
            snippet = Markup(
                '''
                <div class="col-lg-6 my-1" >
                    <div class="shadow-sm p-2 pt-3" style="border-radius: 8px; height: 100%; width: 100%;">
                        <a href="{link}" style="text-decoration: none;">
                            <div class="o_draggable o_wsale_product_grid_wrapper position-relative h-100
                                 o_wsale_product_grid_wrapper_1_1 px-1 card_product">
        
                                <form action="/shop/cart/update" method="post" class="oe_product_cart h-100 d-flex overflow-hidden flex-column">
        
                                    <div style="width: 100%; height: 250px; display: flex; flex-wrap: wrap; flex-direction: row;">
                                        
                                        <div class="col-12 col-md-3" style="width: 25%;">
                                        
                                            <table style="width: 100%; border-collapse: collapse;">
                                            
                                                <tr>
                                                    <td>
                                                        <!-- if Size -->
                                                        {screen_size_block}
                                                    </td>
                                                </tr>
                                                <tr>
                                                    <td>
                                                        <!-- if Quality -->
                                                        {screen_quality_block}
                                                    </td>
                                                </tr>
                                                <tr>
                                                    <td>
                                                        <!-- if Inputs -->
                                                        {video_inputs_block}
                                                    </td>
                                                </tr>
                                                <tr>
                                                    <td>
                                                        <!-- if CPU -->
                                                        {cpu_block}
                                                    </td>
                                                </tr>
                                                <tr>
                                                    <td>
                                                        <!-- if RAM -->
                                                        {ram_block}
                                                    </td>
                                                </tr>
                                                <tr>
                                                    <td>
                                                        <!-- if Hard Drive -->
                                                        {hard_drive_block}
                                                    </td>
                                                </tr>
                                                <tr>
                                                    <td>
                                                        <!-- if OS -->
                                                        {os_block}
                                                    </td>
                                                </tr>
                                            </table>
                                        
                                        </div>

                                        <div class="col-12 col-md-9"
                                             style="padding-inline-start: 1em; width: 75%; height: 80%; display: flex; flex-direction: column; justify-content: center;">
                                            <img src="{image_1920_uri}" itemprop="image" alt="{product_name}" loading="lazy"
                                                 style="max-width: 100%; max-height: 100%; object-fit: contain;"
                                                 mimetype="image/png">
                                            <div class="o_wsale_product_information_text flex-grow-1">
                                                <h3 style="text-align: center;" class="o_wsale_products_item_title">
                                                    {product_name}
                                                </h3>
                                            </div>
                                        </div>

                                    </div>

                                    <div class="o_wsale_product_information d-flex flex-column flex-grow-1 flex-shrink-1"
                                         style="position: relative; border-top: 1px solid; padding: 0; padding-top: 10px">
                                        <div class="o_wsale_product_sub d-flex justify-content-between align-items-end gap-2 flex-wrap">
                                            <div style="display: flex; align-items: center; " itemprop="offers"
                                                 itemscope="itemscope"
                                                 itemtype="http://schema.org/Offer">
                                                <h6 class="mb-0 me-2 second-text d-flex align-items-center">
                                                    <div class="d-flex"  style="display: flex; flex-wrap: wrap;">
                                                        {product_conditions_block}
                                                    </div>
                                                </h6>
                                            </div>
                                        </div>
                                    </div>
                                </form>
                            </div>
                        </a>
                    </div>
                </div>
                '''
            ).format(product_name=product_name, product_conditions_block=Markup("".join(product_conditions_block)),
                     product_conditions=product_conditions_dict, product_conditions_keys=product_conditions_dict.keys(),
                     product_conditions_values=product_conditions_dict.values(), ram_block=ram_block,
                     hard_drive_block=hard_drive_block, cpu_block=cpu_block, screen_quality_block=screen_quality_block,
                     screen_size_block=screen_size_block, os_block=os_block, video_inputs_block=Markup("".join(video_inputs_block)),
                     image_1920_uri=image_1920_uri, processor_logo_uri=processor_logo_uri, link=link)

        elif self.column_size == 'large':
            snippet = Markup(
                '''
                <div class="col-lg-12 my-1" style="margin-bottom: 5px;">
                    <div class="shadow-sm p-2 pt-3" style="border-radius: 8px; height: 100%; width: 100%;">
                        <a href="{link}" style="text-decoration: none;">
                            <div class="o_draggable o_wsale_product_grid_wrapper position-relative h-100
                                                 o_wsale_product_grid_wrapper_1_1 px-1 card_product">
                
                                <form action="/shop/cart/update" method="post" class="h-100" style="display: flex; flex-direction: column;
                                                align-items: center;">
                
                                    <div style="width: 100%; height: 200px; display: flex;">
                
                                        <img src="{image_1920_uri}" itemprop="image" alt="{product_name}" loading="lazy"
                                             style="max-width: 100%; max-height: 100%; object-fit: contain;" mimetype="image/png">
                
                                        <div class="o_wsale_product_information"
                                             style="position: relative; display: flex; flex-direction: column;
                                             justify-content: center; margin-left: 25px">
                                            <div class="o_wsale_product_information_text">
                                                <h2 style="text-align: start;" class="o_wsale_products_item_title">
                                                    {product_name}
                                                </h2>
                                            </div>
                
                                            <div class="o_wsale_product_sub d-flex justify-content-between align-items-end gap-2 flex-wrap pb-1 mt-2">
                                                <div style="display: flex; align-items: center; " itemprop="offers"
                                                     itemscope="itemscope"
                                                     itemtype="http://schema.org/Offer">
                                                    <h6 class="mb-0 me-2 second-text d-flex align-items-center">
                                                        <div style="display: flex; flex-wrap: wrap;">
                                                            {product_conditions_block}
                                                        </div>
                                                    </h6>
                                                </div>
                                            </div>
                                        </div>
                
                                    </div>
                
                
                                    <div class="col-12 col-md-3 mt-2" style="width: 100%;">
                
                                        <table style="border-spacing: 1em; vertical-align: middle;">
                                            <tr>
                                                <td>
                                                    <!-- if Size -->
                                                    {screen_size_block}
                                                </td>
                                                <td>
                                                    <!-- if Quality -->
                                                    {screen_quality_block}
                                                </td>
                                                <td style="display: flex; flex-direction: row;">
                                                    <!-- if Inputs -->
                                                    {video_inputs_block}
                                                </td>
                                                <td>
                                                    <!-- if CPU -->
                                                    {cpu_block}
                                                </td>
                                                <td>
                                                    <!-- if RAM -->
                                                    {ram_block}
                                                </td>
                
                                                <td>
                                                    <!-- if Hard Drive -->
                                                    {hard_drive_block}
                                                </td>
                
                                                <td>
                                                    <!-- if OS -->
                                                    {os_block}
                                                </td>
                                            </tr>
                                        </table>
                
                                    </div>
                
                                </form>
                            </div>
                        </a>
                    </div>
                </div>
                '''
            ).format(product_name=product_name, product_conditions_block=Markup("".join(product_conditions_block)), ram_block=ram_block,
                     hard_drive_block=hard_drive_block, cpu_block=cpu_block, screen_size_block=screen_size_block, os_block=os_block,
                     video_inputs_block=Markup("".join(video_inputs_block)),
                     image_1920_uri=image_1920_uri, processor_logo_uri=processor_logo_uri, screen_quality_block=screen_quality_block,
                     link=link)
        
        mailing_product_container_inner = mailing_root.xpath(
            '//div[hasclass("s_product_container")]/div[hasclass("row")]')
        if not mailing_product_container_inner:
            raise UserError(_('Please, add the snippet called "Product Container" in your E-mail template.'))
        col_placeholder = mailing_product_container_inner[0].xpath('.//div[hasclass("col_placeholder")]')
        if col_placeholder:
            mailing_product_container_inner[0].remove(col_placeholder[0])
        mailing_product_container_inner[0].append(html.fromstring(str(snippet)))
        arch = html.tostring(mailing_root, pretty_print=True, encoding='unicode')
        mailing_record.write({'body_arch': arch})
        
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'message': _('%s has been imported.' % product_name),
                'type': 'success',
                'sticky': False,
                'next': {
                    'name': _('Product imported'),
                    'type': 'ir.actions.act_window_close',
                },
            }
        }

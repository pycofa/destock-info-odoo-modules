# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

import json

from odoo import api, fields, models

from lxml import etree


class IrViews(models.Model):
    _name = 'ir.views'
    _description = 'Saved views'
    _order = 'category asc, sequence asc'

    name = fields.Char(
        string='Name',
        required=True,
        translate=True,
    )

    active = fields.Boolean(
        'Active',
        default=True,
    )

    system = fields.Boolean(
        'Is system?',
        default=False,
    )

    shared = fields.Boolean(
        'View shared',
        compute='_compute_shared',
        inverse='_inverse_shared',
    )

    category = fields.Selection(
        [
            ('system', 'System'),
            ('personal', 'Personal'),
            ('shared', 'Shared'),
        ],
        store=True,
        compute='_compute_category',
    )

    sequence = fields.Integer(
        'Sequence',
        default=lambda self: (self.search([], order='sequence desc', limit=1).sequence or 0) + 1,
    )

    view_mode = fields.Selection(
        [
            ('tree', 'List'),
            ('kanban', 'Kanban'),
        ],
        string='View Mode',
        default='tree',
        required=True,
    )

    user_id = fields.Many2one(
        'res.users',
        string='User',
        ondelete='cascade',
        default=lambda self: self.env.user.id,
    )

    group_ids = fields.Many2many(
        'res.groups',
        'ir_views_group_rel',
        'ir_view_id',
        'group_id',
        string='Groups',
        help="If this field is empty, the view applies to all users. Otherwise, the view applies to the users of those groups only.",
    )

    res_model_id = fields.Many2one(
        'ir.model',
        string='Model',
        required=True,
        ondelete='cascade',
        domain=[('transient', '=', False)],
    )

    res_model_name = fields.Char(
        string='Model name',
        compute='_compute_res_model_name',
        inverse='_inverse_res_model_name',
    )

    res_field_ids = fields.One2many(
        'ir.views.field',
        'view_id',
        string='Fields',
    )

    res_group_by_ids = fields.One2many(
        'ir.views.group_by',
        'view_id',
        string='Groups by',
    )

    res_order_by_ids = fields.One2many(
        'ir.views.order_by',
        'view_id',
        string='Orders by',
    )

    expert_mode = fields.Boolean(
        'Expert mode',
        store=False,
        help='Display more options to configure the view',
    )

    limit = fields.Integer(
        default=80,
        help='Default limit for the list view',
    )

    domain = fields.Char(
        string='Domain',
        help='Optional domain filtering of the destination data, as a Python expression',
    )

    context = fields.Char(
        string='Context Value',
        help='Context dictionary as Python expression'
    )

    arch = fields.Text(
        string='Architecture',
        compute='_compute_arch',
    )

    main_ir_action_id = fields.Many2one(
        'ir.actions.act_window',
        string='Main Action',
        ondelete='cascade',
    )

    ir_action_id = fields.Many2one(
        'ir.actions.act_window',
        string='Action',
        ondelete='cascade',
    )

    ir_view_id = fields.Many2one(
        'ir.ui.view',
        string='View',
        ondelete='cascade',
    )

    display_page_fields = fields.Boolean(
        'Display fields?',
        compute='_compute_display_page_fields',
    )

    # Common settings
    # ---------------

    no_create = fields.Boolean(
        'No create',
        help='Disable creation of records',
    )

    no_edit = fields.Boolean(
        'No edit',
        help='Disable edition of records',
    )

    no_delete = fields.Boolean(
        'No delete',
        help='Disable deletion of records',
    )

    no_import = fields.Boolean(
        'No import',
        help='Disable importation of records',
    )

    classes = fields.Char(
        'CSS Class',
        help='Define custom CSS classes',
    )

    js_class = fields.Char(
        'JS Class',
        help='Define the CSS class to extend the Form Controller',
    )

    sample = fields.Boolean(
        'Sample',
        help='Display sample data when view is empty',
    )

    # List settings
    #--------------

    editable = fields.Selection(
        [
            ('top', 'Top'),
            ('bottom', 'Bottom'),
        ],
        string='Position of edition',
        help='Placing of the new record creation',
    )

    no_duplicate = fields.Boolean(
        'No duplicate',
        help='Disable duplication of records',
    )

    no_export = fields.Boolean(
        'No export',
        help='Disable exportation of records',
    )

    no_open_form_view = fields.Boolean(
        'No open form view',
        help='Disable open form view',
    )

    multi_edit = fields.Boolean(
        'Multi edition',
        help='Allow inline editing when selecting one or more records',
    )

    expand = fields.Boolean(
        'Expand groups',
        help='Allow to expand all groups by when list is grouped by fields',
    )

    # Kanban settings
    # ---------------

    no_group_create = fields.Boolean(
        'No group creation',
        help='Disable creation of groups',
    )

    no_quick_create = fields.Boolean(
        'No quick creation',
        help='Disable quick creation in card',
    )

    no_records_draggable = fields.Boolean(
        'No records draggable',
        help='Disable dragging of cards',
    )

    def write(self, vals):
        res = super().write(vals)
        self._sync_ir_action_view()

        return res

    def _sync_ir_action_view(self):
        for rec in self:
            if rec.view_mode in rec._available_view_mode_custom_view():
                view_vals = {
                    'name': rec.name,
                    'type': rec.view_mode,
                    'mode': 'primary',
                    'model': rec.res_model_id.model,
                    'arch': rec.arch,
                    'priority': 1000000,
                    'active': False,
                    'ir_views_id': rec.id,
                }

                if not rec.ir_view_id:
                    view = self.env['ir.ui.view'].sudo().create(view_vals)
                    rec.ir_view_id = view.id
                else:
                    rec.ir_view_id.sudo().write(view_vals)

            def build_action_context(views):
                ctx = json.loads(views.context or '{}')

                if views.res_group_by_ids:
                    ctx.update({
                        'group_by': [gb.field_name + (f":{gb.grouping_type}" if gb.grouping_type else '') for gb in views.res_group_by_ids],
                    })

                if views.res_order_by_ids:
                    ctx.update({
                        'default_order': ', '.join([f"{ob.field_name} {ob.sort}" for ob in views.res_order_by_ids]),
                    })

                return json.dumps(ctx)

            action_vals = {
                'name': rec.name,
                'res_model': rec.res_model_id.model,
                'target': 'main',
                'view_mode': ','.join([rec.view_mode, 'form']),
                'mobile_view_mode': rec.view_mode,
                'view_id': rec.ir_view_id.id,
                'search_view_id': False,
                'help': False,
                'domain': rec.domain,
                'context': build_action_context(rec),
                'limit': rec.limit,
                'ir_views_id': rec.id,
            }

            if not rec.ir_action_id:
                action = self.env['ir.actions.act_window'].sudo().create(action_vals)
                rec.ir_action_id = action.id

                self.env['ir.actions.act_window.view'].sudo().create({
                    'view_mode': rec.view_mode,
                    'view_id': rec.ir_view_id.id,
                    'act_window_id': action.id,
                })
            else:
                rec.ir_action_id.sudo().write(action_vals)

    @api.model
    def _available_view_mode_custom_view(self):
        return ['tree']

    @api.model
    def _available_view_mode_fields(self):
        return ['tree']

    @api.depends('view_mode')
    def _compute_display_page_fields(self):
        for rec in self:
            rec.display_page_fields = rec.view_mode in self._available_view_mode_fields()

    @api.depends('user_id')
    def _compute_shared(self):
        for rec in self:
            rec.shared = not rec.user_id

    @api.onchange('shared')
    def _inverse_shared(self):
        for rec in self:
            rec.user_id = self.env.user if not rec.shared else False

    @api.depends('system', 'shared')
    def _compute_category(self):
        for rec in self:
            if rec.system:
                rec.category = 'system'
            elif rec.shared:
                rec.category = 'shared'
            else:
                rec.category = 'personal'

    @api.depends('res_model_id')
    def _compute_res_model_name(self):
        for rec in self:
            rec.res_model_name = rec.res_model_id.model

    @api.onchange('res_model_name')
    def _inverse_res_model_name(self):
        for rec in self:
            if rec.res_model_name and not rec.res_model_id:
                rec.res_model_id = rec.res_model_id.search([('model', '=', self.res_model_name)], limit=1)
                rec.res_model_name = rec.res_model_id.model

    @api.onchange('res_field_ids')
    def _onchange_res_field_ids(self):
        for rec in self:
            for f in rec.res_field_ids:
                if f.field_name and not f.field_id:
                    f.field_id = f.field_id.search([('model', '=', self.res_model_name), ('name', '=', f.field_name)], limit=1)
                    f.field_name = rec.res_model_id.model

    @api.onchange('res_group_by_ids')
    def _onchange_res_group_by_ids(self):
        for rec in self:
            for gb in rec.res_group_by_ids:
                if gb.field_name and not gb.field_id:
                    parts = gb.field_name.split(':', 1)
                    field_name = parts[0]
                    grouping_type = parts[1] if len(parts) > 1 else None

                    gb.field_id = gb.field_id.search([('model', '=', self.res_model_name), ('name', '=', field_name)], limit=1)
                    gb.field_name = rec.res_model_id.model

                    if gb.field_id:
                        gb.grouping_type = grouping_type

    @api.onchange('res_order_by_ids')
    def _onchange_res_order_by_ids(self):
        for rec in self:
            for ob in rec.res_order_by_ids:
                if ob.field_name and not ob.field_id:
                    ob.field_id = ob.field_id.search(
                        [('model', '=', self.res_model_name), ('name', '=', ob.field_name)], limit=1)
                    ob.field_name = rec.res_model_id.model

    @api.depends(
        'view_mode',
        'res_model_id',
        'res_field_ids',
        'res_order_by_ids',
        'domain',
        'context',
        'name',
    )
    def _compute_arch(self):
        for rec in self:
            if not rec.view_mode:
                rec.arch = False
                continue

            root = etree.Element(rec.view_mode)
            method_name = '_build_arch_' + rec.view_mode

            if hasattr(rec, method_name):
                method = getattr(rec, method_name)
                method(root)

            rec.arch = etree.tostring(root, pretty_print=True, encoding='unicode')

    def _build_arch_common(self, root):
        self.ensure_one()

        if self.no_create:
            root.attrib['create'] = '0'

        if self.no_edit:
            root.attrib['edit'] = '0'

        if self.no_delete:
            root.attrib['delete'] = '0'

        if self.no_import:
            root.attrib['import'] = '0'

        if self.classes:
            root.attrib['class'] = self.classes

        if self.js_class:
            root.attrib['js_class'] = self.js_class

        if self.sample:
            root.attrib['sample'] = '1'

        if self.res_order_by_ids:
            root.attrib['default_order'] = ', '.join([f"{ob.field_name} {ob.sort}" for ob in self.res_order_by_ids])

    def _build_arch_tree(self, root):
        self._build_arch_common(root)

        if self.editable:
            root.attrib['editable'] = self.editable

        if self.no_duplicate:
            root.attrib['duplicate'] = '0'

        if self.no_export:
            root.attrib['export_xlsx'] = '0'

        if self.no_open_form_view:
            root.attrib['open_form_view'] = '0'

        if self.multi_edit:
            root.attrib['multi_edit'] = '1'

        if self.expand:
            root.attrib['expand'] = '1'

        for field in self.res_field_ids:
            tree_field = etree.SubElement(root, 'field')

            if field.field_id.name:
                tree_field.attrib['name'] = field.field_id.name

            if field.label:
                tree_field.attrib['string'] = field.label

            if field.widget:
                tree_field.attrib['widget'] = field.widget

            if field.optional == 'invisible':
                tree_field.attrib['column_invisible'] = 'True'
            elif field.optional:
                tree_field.attrib['optional'] = field.optional

            if field.options:
                tree_field.attrib['options'] = field.options

            if field.width:
                tree_field.attrib['width'] = field.width.rstrip('px') + 'px'

    def _build_arch_kanban(self, root):
        self._build_arch_common(root)

        if self.no_group_create:
            root.attrib['group_create'] = 'false'

        if self.no_quick_create:
            root.attrib['quick_create'] = 'false'

        if self.no_records_draggable:
            root.attrib['records_draggable'] = 'false'

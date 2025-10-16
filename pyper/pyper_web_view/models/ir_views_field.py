# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import api, fields, models


class IrViewsField(models.Model):
    _name = 'ir.views.field'
    _description = 'Fields of views'
    _order = 'view_id ASC, sequence ASC, id ASC'

    name = fields.Char(
        related='field_id.name',
        store=True,
    )

    sequence = fields.Integer(
        'Sequence',
        default=10,
        index=True,
    )

    view_id = fields.Many2one(
        'ir.views',
        required=True,
        ondelete='cascade',
    )

    user_id = fields.Many2one(
        related='view_id.user_id',
        store=True,
    )

    model_id = fields.Many2one(
        related='view_id.res_model_id',
        store=True,
    )

    field_id = fields.Many2one(
        'ir.model.fields',
        string='Field',
        required=True,
        ondelete='cascade',
    )

    field_name = fields.Char(
        string='Field name',
        compute='_compute_field_name',
        inverse='_inverse_field_name',
        store=True,
    )

    field_id_domain = fields.Binary(
        'Field domain',
        compute='_compute_field_id_domain',
    )

    label = fields.Char(
        string='Custom label',
        translate=True,
    )

    widget = fields.Selection(
        [
            ('char', 'Text'),
            ('char_image', 'Text Image'),
            ('text', 'Textarea'),
            ('url', 'URL'),
            ('phone', 'Phone'),
            ('email', 'Email'),
            ('html', 'HTML'),
            ('boolean', 'Boolean'),
            ('boolean_favorite', 'Boolean Favorite'),
            ('boolean_icon', 'Boolean Icon'),
            ('boolean_toggle', 'Boolean Toggle'),
            ('integer', 'Integer'),
            ('float', 'Float'),
            ('float_time', 'Float Time'),
            ('monetary', 'Monetary'),
            ('percentage', 'Percentage'),
            ('priority', 'Priority'),
            ('date', 'Date'),
            ('datetime', 'Datetime'),
            ('selection', 'Selection'),
            ('selection_badge', 'Selection Badge'),
            ('state_selection', 'State Selection'),
            ('color', 'Color'),
            ('color_picker', 'Color Picker'),
            ('badge', 'Badge'),
            ('progress_circular', 'Progress Circular'),
            ('progressbar', 'Progressbar'),
            ('image', 'Image'),
            ('image_url', 'Image URL'),
            ('attachment_image', 'Attachment Image'),
            ('binary', 'Binary'),
            ('jsonb', 'JSON'),
            ('many2one', 'Relation'),
            ('many2one_badge', 'Relation Badge'),
            ('many2one_avatar', 'Relation Avatar'),
            ('many2one_image', 'Relation Image'),
            ('many2one_reference', 'Relation Reference'),
            ('one2many', 'Relation List'),
            ('many2many', 'Many Relations'),
            ('many2many_tags', 'Many Relations Tags'),
            ('many2many_tags_avatar', 'Many Relations Avatar'),
            ('many2many_tags_avatar_popover', 'Many Relations Avatar Popover'),
            ('many2many_binary', 'Many Relations Binary'),
            ('many2many_checkboxes', 'Many Relations Checkboxes'),
            ('relative_days', 'Relative Days'),
            ('slider', 'Slider'),
            ('handle', 'Handle'),
        ],
    )

    optional = fields.Selection(
        [
            ('show', 'Show'),
            ('hide', 'Hide'),
            ('invisible', 'Invisible'),
        ],
        string='Optional',
    )

    options = fields.Char(
        string='Options',
    )

    width = fields.Char(
        string='Width',
    )

    @api.depends('field_id')
    def _compute_field_name(self):
        for rec in self:
            rec.field_name = rec.field_id.name

    @api.onchange('field_name')
    def _inverse_field_name(self):
        for rec in self:
            if self.field_name:
                rec.field_id = rec.field_id.search([('name', '=', self.field_name)], limit=1)
                rec.field_name = rec.field_id.name

    @api.depends('field_id')
    def _compute_field_id_domain(self):
        for rec in self:
            rec.field_id_domain = [('model_id', '=', rec.model_id.id)]

    @api.model_create_multi
    def create(self, vals_list):
        fields_info = self.fields_get(['widget'])
        widget_values = [value[0] for value in fields_info['widget']['selection']]

        for vals in vals_list:
            if 'widget' in vals and vals['widget'] not in widget_values:
                del vals['widget']

        return super().create(vals_list)

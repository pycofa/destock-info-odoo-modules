# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import api, fields, models


class IrViewsOrderBy(models.Model):
    _name = 'ir.views.order_by'
    _description = 'Orders by of views'
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

    sort = fields.Selection(
        [
            ('asc', 'Ascending'),
            ('desc', 'Descending'),
        ],
        string='Sort',
        required=True,
        default='asc',
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
            rec.field_id_domain = [('model_id', '=', rec.model_id.id), ('store', '=', True)]

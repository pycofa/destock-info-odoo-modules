# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import api, fields, models


class IrUiView(models.Model):
    _inherit = 'ir.actions.act_window'

    ir_views_id = fields.Many2one(
        'ir.views',
        string='Saved views',
        ondelete='cascade',
    )

    @api.depends('ir_views_id.main_ir_action_id.name')
    def _compute_display_name(self):
        for rec in self:
            if rec.ir_views_id.main_ir_action_id:
                rec.display_name = rec.ir_views_id.main_ir_action_id.name
            else:
                super(IrUiView, rec)._compute_display_name()

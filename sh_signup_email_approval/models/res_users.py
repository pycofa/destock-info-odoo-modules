# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
from odoo import models, fields, api, _
import uuid


class ShUsers(models.Model):
    _inherit = 'res.users'

    sh_user_from_signup = fields.Boolean('User From Signup ?', default=False)
    verification_code = fields.Char('Code')
    sh_password = fields.Char("Password ")
    sh_access_token = fields.Char('Access Token')

    # @api.model_create_multi
    # def create(self, vals_list):

    #     for vals in vals_list:
    #         vals.update({'sh_access_token': uuid.uuid4().hex})
    #     res = super(ShUsers, self).create(vals_list)
    #     if res.share == True:
    #         res.sh_user_from_signup = False
    #     return res

    # def action_ras_users_update_all_allowed_signup(self):
    #     return {
    #         'name': 'Mass Update Approve/Reject',
    #         'res_model': 'sh.mass.approve.reject.wizard',
    #         'view_mode': 'form',
    #         'context': {'default_active_ids': [(6, 0, self.env.context.get('active_ids'))]},
    #         'view_id': self.env.ref('sh_signup_email_approval.sh_mass_approve_reject_wizard_view_form').id,
    #         'target': 'new',
    #         'type': 'ir.actions.act_window'
    #     }


# class SHportalwizarduser(models.TransientModel):
#     _inherit = "portal.wizard.user"

#     def action_grant_access(self):
#         rec = super().action_grant_access()
#         self.user_id.sh_user_from_signup = True
#         return rec

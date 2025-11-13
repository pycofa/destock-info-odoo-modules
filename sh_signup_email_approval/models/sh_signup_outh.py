# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields


class ShSignupOuth(models.Model):
    _name="sh.signup.outh"
    _descripiton = 'Signup OTP Verification'

    name = fields.Char(string="OTP")
    email = fields.Char(string="email")
    company_id = fields.Many2one('res.company', string='Company')
    partner_id = fields.Many2one('res.partner', string='Partner') 

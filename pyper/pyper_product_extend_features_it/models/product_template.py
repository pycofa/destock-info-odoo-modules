# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    product_pattern = fields.Selection(
        related='categ_id.product_pattern',
    )

    operating_system_id = fields.Many2one(
        'product.operating.system',
        'Operating system',
    )

    hard_drive_capacity_id = fields.Many2one(
        'product.storage.capacity',
        'Hard drive capacity',
    )

    hard_drive_type_id = fields.Many2one(
        'product.storage.type',
        'Hard drive type',
    )

    ram_capacity_id = fields.Many2one(
        'product.storage.capacity',
        'RAM capacity',
    )

    processor_id = fields.Many2one(
        'product.processor',
        'Processor',
    )

    screen_size_id = fields.Many2one(
        'product.screen.size',
        'Screen size',
    )

    screen_quality_id = fields.Many2one(
        'product.screen.quality',
        'Screen quality',
    )

    graphic_card_id = fields.Many2one(
        'product.graphic.card',
        'Graphic card',
    )

    has_webcam = fields.Boolean(
        'Has webcam',
    )

    has_bluetooth = fields.Boolean(
        'Has bluetooth',
    )

    has_optical_drive = fields.Boolean(
        'Has optical drive',
    )

    has_adjustable_stand = fields.Boolean(
        'Has adjustable stand',
    )

    format = fields.Char(
        'Format'
    )

    screen_format = fields.Char(
        'Screen format'
    )
    
    flow = fields.Char(
        'Flow'
    )
    
    number_of_displays = fields.Integer(
        'Number of displays',
    )
    
    focal = fields.Char(
        'Focal',
    )
    
    specific_informations = fields.Char(
        'Specific informations'
    )
    
    is_tactile = fields.Boolean(
        'Tactile',
    )
    
    is_usb_c = fields.Boolean(
        'USB-C',
    )
    
    is_printer_color = fields.Boolean(
        'Printer color',
    )
    
    is_printer_multifunction = fields.Boolean(
        'Printer multifunction',
    )
    
    is_videopro_interactive = fields.Boolean(
        'Interactive',
    )
    
    is_dual_sim = fields.Boolean(
        'Dual sim',
    )
    
    is_poe = fields.Boolean(
        'POE'
    )
    
    number_of_ports = fields.Integer(
        'Number of ports',
    )
    
    video_output_ids = fields.Many2many(
        'product.video.output',
        string='Video output'
    )

    video_input_ids = fields.Many2many(
        'product.video.input',
        string='Video input'
    )

    network_ids = fields.Many2many(
        'product.network',
        string='Network'
    )

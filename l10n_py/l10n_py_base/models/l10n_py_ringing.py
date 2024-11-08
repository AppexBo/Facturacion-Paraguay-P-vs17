# -*- coding:utf-8 -*-

from odoo import api, models, fields

class L10nPyRinging(models.Model):
    _name = 'l10n.py.ringing'
    _description = 'Numero timbrado'

    
    name = fields.Char(
        string='Numero',
    )
    
    
    company_id = fields.Many2one(
        string='Compañia', 
        comodel_name='res.company', 
        required=True, 
    )
    
    active = fields.Boolean(
        string='Activo',
        default=True
    )
    
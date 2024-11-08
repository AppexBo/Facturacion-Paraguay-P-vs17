# -*- coding:utf-8 -*-

from odoo import api, models, fields

class ResPartner(models.Model):
    _inherit = ['res.partner']
    
    
    operation_type_id = fields.Many2one(
        string='Tipo operacion',
        comodel_name='l10n.py.operation.type',
        company_dependent=True
    )
    
    
    receiver_nature = fields.Selection(
        string='Naturaleza del receptor',
        selection=[
            ('1', '(1) Contribuyente'), 
            ('2', '(2) No contribuyente')
        ]
    )
    